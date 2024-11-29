"""Physical topology with correct routing configurations for leader election."""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal object.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Node node-0
node_0 = request.RawPC('node-0')
iface0 = node_0.addInterface('interface-13', pg.IPv4Address('10.0.5.1','255.255.255.0'))
iface1 = node_0.addInterface('interface-15', pg.IPv4Address('10.0.4.2','255.255.255.0'))

# Add routing configuration to node-0
node_0.addService(pg.Execute(shell="bash", command="""
sudo sysctl -w net.ipv4.ip_forward=1
sudo ip route add 10.0.2.0/24 via 10.0.4.1
sudo ip route add 10.0.3.0/24 via 10.0.4.3
"""))

# Node node-2
node_2 = request.RawPC('node-2')
iface2 = node_2.addInterface('interface-19', pg.IPv4Address('10.0.2.2','255.255.255.0'))
iface3 = node_2.addInterface('interface-20', pg.IPv4Address('10.0.3.1','255.255.255.0'))

# Add routing configuration to node-2
node_2.addService(pg.Execute(shell="bash", command="""
sudo ip route add 10.0.4.0/24 via 10.0.2.1
sudo ip route add 10.0.5.0/24 via 10.0.2.1
"""))

# Node node-1
node_1 = request.RawPC('node-1')
iface4 = node_1.addInterface('interface-16', pg.IPv4Address('10.0.4.1','255.255.255.0'))
iface5 = node_1.addInterface('interface-18', pg.IPv4Address('10.0.2.1','255.255.255.0'))

# Add routing configuration to node-1
node_1.addService(pg.Execute(shell="bash", command="""
sudo sysctl -w net.ipv4.ip_forward=1
sudo ip route add 10.0.3.0/24 via 10.0.2.2
sudo ip route add 10.0.5.0/24 via 10.0.4.2
"""))

# Node node-3
node_3 = request.RawPC('node-3')
iface6 = node_3.addInterface('interface-17', pg.IPv4Address('10.0.4.3','255.255.255.0'))
iface7 = node_3.addInterface('interface-21', pg.IPv4Address('10.0.3.2','255.255.255.0'))

# Add routing configuration to node-3
node_3.addService(pg.Execute(shell="bash", command="""
sudo sysctl -w net.ipv4.ip_forward=1
sudo ip route add 10.0.2.0/24 via 10.0.3.1
sudo ip route add 10.0.5.0/24 via 10.0.4.2
"""))

# Node node-4
node_4 = request.RawPC('node-4')
iface8 = node_4.addInterface('interface-14', pg.IPv4Address('10.0.5.2','255.255.255.0'))

# Add routing configuration to node-4
node_4.addService(pg.Execute(shell="bash", command="""
sudo ip route add 10.0.2.0/24 via 10.0.5.1
sudo ip route add 10.0.3.0/24 via 10.0.5.1
sudo ip route add 10.0.4.0/24 via 10.0.5.1
"""))

# Link link-5
link_5 = request.Link('link-5')
iface0.bandwidth = 1000000
link_5.addInterface(iface0)
iface8.bandwidth = 1000000
link_5.addInterface(iface8)

# Link link-6
link_6 = request.Link('link-6')
iface1.bandwidth = 1000000
link_6.addInterface(iface1)
iface4.bandwidth = 1000000
link_6.addInterface(iface4)
iface6.bandwidth = 1000000
link_6.addInterface(iface6)

# Link link-7
link_7 = request.Link('link-7')
iface5.bandwidth = 1000000
link_7.addInterface(iface5)
iface2.bandwidth = 1000000
link_7.addInterface(iface2)

# Link link-8
link_8 = request.Link('link-8')
iface3.bandwidth = 1000000
link_8.addInterface(iface3)
iface7.bandwidth = 1000000
link_8.addInterface(iface7)

# Print the generated RSpec
pc.printRequestRSpec(request)
