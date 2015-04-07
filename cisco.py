import argparse #paramiko
import jinja2

parser = argparse.ArgumentParser()
parser.add_argument ('--hostname', help="Switch hostname", required=True)
parser.add_argument ('--loopback', help="'loopback port number' 'ip address' 'mask' 'ipv6 address' 'enable/disable' 'description'", action="append", nargs=6)
parser.add_argument ('--vlan', help="'vlan port number' 'ip address' 'mask' 'shutdown'/'no shutdown' 'ipv6 address' 'enable'/'disable' 'description'", action="append", nargs=7)
#parser.add_argument ('--vlan', help="vlanid:ipaddress:mask:shutdown_str:description", action="append",nargs=5)
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

# Create new list of dictionaries instead of list of lists for VLAN
list_of_dict = []
for unnamed_list in args.vlan:
  num = 0
  named_list = {}
  for names in 'vlanid','ipaddress','mask','shutdown','ipv6','ipv6_enable','description':
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
		'hostname' : args.hostname,
                'loopback' : args.loopback,
 		'vlan'     : args.vlan
	       }
outputText = template.render( templateVars )

#print outputText

f = open('output/cisco', 'w')
f.write(outputText)
f.close()
