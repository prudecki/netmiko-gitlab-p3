from jinja2 import Environment, FileSystemLoader
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


int_dict = [
    { 'name': 'Gi0/1',
      'vlan': 100},
    {
        'name': 'Gi0/2',
        'vlan': 200
    }
]

j2_env = Environment(loader=FileSystemLoader('./templates'),
                     trim_blocks=True)

for interface in int_dict:
    print(j2_env.get_template('interface.txt').render(
        interface_name=interface['name'], vlan_id=interface['vlan']
    ))

print('-----------------------------------------------')
# commit
print(j2_env.get_template('interfaces.txt').render(
    interfaces=int_dict))

j2_env.list_templates()