from jinja2 import Environment, FileSystemLoader, Template
import os
import requests


int_dict = [
    { 'name': 'Gi0/1',
      'vlan': 100},
    {
        'name': 'Gi0/2',
        'vlan': 200
    }
]

int_template = requests.get('http://172.17.0.3/api/v4/projects/1/repository/files/access/raw?ref=master', headers={'PRIVATE-TOKEN': 'x6sP6xf57gb5sxxiXutq'})
if int_template.status_code == 200:
    int_access = Template(int_template.text)
else:
    requests.exceptions.RequestException()


print(int_access)

#j2_env = Environment(loader=FileSystemLoader('./templates'),
#                     trim_blocks=True)

#for interface in int_dict:
#    print(j2_env.get_template('interface.txt').render(
#        interface_name=interface['name'], vlan_id=interface['vlan']
#    ))

print('-----------------------------------------------')

print(int_access.render(interfaces=int_dict))


