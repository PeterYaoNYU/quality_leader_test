import geni.portal as portal
import geni.rspec.pg as RSpec

# Create a request object to define the experiment
request = RSpec.Request()

# Parameters
node_count = 5  # Total nodes (4 in a ring + 1 additional)
node_image = "urn:publicid:IDN+emulab.net+image+UBUNTU22-64-STD"  # Ubuntu 22 image
link_bandwidth = 1000  # Mbps (1 Gbps)

# Create nodes and links
nodes = []
for i in range(node_count):
    node = request.XenVM("node" + str(i))
    # node.disk_image = node_image
    nodes.append(node)

# Connect nodes in a ring
for i in range(4):
    link = request.Link("link_" + str(i) + "_" + str((i + 1) % 4))
    link.bandwidth = link_bandwidth
    link.addNode(nodes[i])
    link.addNode(nodes[(i + 1) % 4])

# Add the additional node to the ring node 0
extra_link = request.Link("link_extra")
extra_link.bandwidth = link_bandwidth
extra_link.addNode(nodes[0])  # Connect to node 0 in the ring
extra_link.addNode(nodes[4])  # Additional node

# IP and routing setup script
routing_script = """
#!/bin/bash

# IP and routing configuration for the nodes
case $(hostname) in
    node0)
        ip addr add 10.0.1.1/24 dev ens1
        ip addr add 10.0.2.1/24 dev ens2
        ip addr add 10.0.5.1/24 dev ens3
        ip link set ens1 up
        ip link set ens2 up
        ip link set ens3 up
        ip route add 10.0.3.0/24 via 10.0.2.2
        ip route add 10.0.4.0/24 via 10.0.1.2
        ip route add 10.0.6.0/24 via 10.0.5.2
        ;;
    node1)
        ip addr add 10.0.1.2/24 dev ens1
        ip addr add 10.0.3.1/24 dev ens2
        ip link set ens1 up
        ip link set ens2 up
        ip route add 10.0.4.0/24 via 10.0.3.2
        ip route add 10.0.2.0/24 via 10.0.1.1
        ip route add 10.0.5.0/24 via 10.0.1.1
        ip route add 10.0.6.0/24 via 10.0.1.1
        ;;
    node2)
        ip addr add 10.0.3.2/24 dev ens1
        ip addr add 10.0.4.1/24 dev ens2
        ip link set ens1 up
        ip link set ens2 up
        ip route add 10.0.1.0/24 via 10.0.3.1
        ip route add 10.0.2.0/24 via 10.0.3.1
        ip route add 10.0.5.0/24 via 10.0.3.1
        ip route add 10.0.6.0/24 via 10.0.3.1
        ;;
    node3)
        ip addr add 10.0.4.2/24 dev ens1
        ip addr add 10.0.2.2/24 dev ens2
        ip link set ens1 up
        ip link set ens2 up
        ip route add 10.0.1.0/24 via 10.0.4.1
        ip route add 10.0.3.0/24 via 10.0.4.1
        ip route add 10.0.5.0/24 via 10.0.4.1
        ip route add 10.0.6.0/24 via 10.0.4.1
        ;;
    node4)
        ip addr add 10.0.5.2/24 dev ens1
        ip link set ens1 up
        ip route add 10.0.1.0/24 via 10.0.5.1
        ip route add 10.0.2.0/24 via 10.0.5.1
        ip route add 10.0.3.0/24 via 10.0.5.1
        ip route add 10.0.4.0/24 via 10.0.5.1
        ;;
esac
"""

# Add the routing script to each node
for node in nodes:
    node.addService(RSpec.Execute(shell="bash", command=routing_script))

# Generate the RSpec
portal.context.printRequestRSpec(request)
