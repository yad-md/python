import argparse
import jinja2

parser = argparse.ArgumentParser()

parser.add_argument ('--hostname', help="Switch hostname", required=True)

parser.add_argument ('--loopback', help="'loopback port number' 'ip address mask' 'ipv6 address' {'enable'|'disable'} 'description'", action="append", nargs=6)

parser.add_argument ('--portchannel', help="'port-channel port number' 'description' 'switchport trunk encapsulation' 'switchport trunk allowed vlan' 'switchport mode' 'switchport mode {nonegotiate|""}' 'load-interval' 'mtu' {'shutdown'|'no shutdown'} ", action="append", nargs=9)

parser.add_argument ('--fastethernet', help="'fast ethernet port number' 'ip vrf forwarding' 'ip address mask | "" ' '{'shutdown'|'no shutdown'} ", action="append", nargs=5)

parser.add_argument ('--gigabit', help="'GigabitEthernet port number' 'description' 'switchport trunk encapsulation' 'switchport trunk allowed vlan' 'switchport mode' 'switchport mode {nonegotiate|""}' 'load-interval' 'channel-group {number active|passive}' 'media-type' 'spanning-tree' {'shutdown'|'no shutdown'} ", action="append", nargs=12)

parser.add_argument ('--vlan', help="'vlan port number' 'description' 'ip address mask' 'ipv6 address' {'enable'|'disable'} {'shutdown'|'no shutdown'}", action="append", nargs=7)

args = parser.parse_args()

#Create new list of dictionaries instead of list of lists for LOOPBACK
list_of_dict = []
for unnamed_list in args.loopback:
  num = 0
  named_list = {}
  for names in 'id','ipaddress','mask','ipv6','ipv6_enable','description':
    named_list[names] = unnamed_list[num]
    num += 1
  list_of_dict.append(named_list)
args.loopback = list_of_dict

# Create new list of dictionaries instead of list of lists for PORT-CHANNEL
list_of_dict = []
for unnamed_list in args.portchannel:
  num = 0
  named_list = {}
  for names in 'id','description','trunk_encapsulation','trunk_allowed_vlan','switchport_mode','switchport_nonegotiate','load_interval','mtu','shutdown':
    named_list[names] = unnamed_list[num]
    num += 1
  list_of_dict.append(named_list)
args.portchannel = list_of_dict

#Create new list of dictionaries instead of list of lists for FASTETHERNET
list_of_dict = []
for unnamed_list in args.fastethernet:
  num = 0
  named_list = {}
  for names in 'id','vrf_forwarding','ipaddress','mask','shutdown':
    named_list[names] = unnamed_list[num]
    num += 1
  list_of_dict.append(named_list)
args.fastethernet = list_of_dict

# Create new list of dictionaries instead of list of lists for GIGABITETHERNET
list_of_dict = []
for unnamed_list in args.gigabit:
  num = 0
  named_list = {}
  for names in 'id','description','trunk_encapsulation','trunk_allowed_vlan','switchport_mode','switchport_nonegotiate','load_interval','media_type','channel_group','channel_group_mode','spanning_tree','shutdown':
    named_list[names] = unnamed_list[num]
    num += 1
  list_of_dict.append(named_list)
args.gigabit = list_of_dict

# Create new list of dictionaries instead of list of lists for VLAN
list_of_dict = []
for unnamed_list in args.vlan:
  num = 0
  named_list = {}
  for names in 'vlanid','description','ipaddress','mask','ipv6','ipv6_enable','shutdown':
    named_list[names] = unnamed_list[num]
    num += 1
  list_of_dict.append(named_list)
args.vlan = list_of_dict


#Here jinja2 starts
templateLoader = jinja2.FileSystemLoader(searchpath="templates/")
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "cisco.jinja"
template = templateEnv.get_template( TEMPLATE_FILE )
templateVars = { 
		'hostname'    : args.hostname,
                'loopback'    : args.loopback,
		'portchannel' : args.portchannel,
		'fastethernet': args.fastethernet,
		'gigabit'     : args.gigabit,
 		'vlan'        : args.vlan
	       }
outputText = template.render( templateVars )

#print outputText

f = open('output/cisco', 'w')
f.write(outputText)
f.close()
