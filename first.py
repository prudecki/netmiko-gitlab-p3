from netmiko import NetMikoTimeoutException, NetMikoAuthenticationException, ConnectHandler
from jinja2 import Template
import requests
import re
import logging
import logzero
from logzero import logger
import sys
import os
import getpass

logzero.loglevel(logging.DEBUG)

devices_ip = '''
172.17.0.100
172.17.0.101
'''
devices_ip_strip = devices_ip.strip().splitlines()

username = input('Username: ')
password = getpass.getpass('Password: ')


def devices_connect(devices):
    connect = False
    n = int(0)
    for device in devices:
        try:
            print('~'*100 + f'\nConnecting to device: {device}')
            connect[n] = ConnectHandler(ip=device, device_type='cisco_ios', username=username, password=password)
            n = n+1
        except (NetMikoAuthenticationException, NetMikoTimeoutException) as conn_error:
            logger.warning(f'Unable to connect to device:\n{conn_error}')
    if not connect:
        logger.critical('No devices to connect to')
        sys.exit()


class ConfigInputException(Exception):
    pass


def push_standard_config():
    logger.debug('trying to connect to GITLAB')
    try:
        git_req = requests.get('http://172.17.0.3/api/v4/projects/1/repository/files/start/raw?ref=master', headers={'PRIVATE-TOKEN': 'x6sP6xf57gb5sxxiXutq'})
    except requests.exceptions.RequestException as req_error:
        logger.critical(f'unable to connect to GITLAB:\n{req_error}')
        return False
    logger.debug('checking if connection was successful')
    if git_req.status_code == 200:
        logger.debug('connection to GITLAB successful')
        out = git_req.text.splitlines()
        if isinstance(out, list):
            logger.debug(f'about to send this configuration to device:\n{out}')
            logger.debug(f'connecting to devices:\n{devices_ip}')
            devices_connect(devices=devices_ip_strip)
            try:
                abc = devices_connect.
                sendconf = connect.send_config_set(out)
            except Exception as sendconf_error:
                logger.critical(sendconf_error)
                return False
            if (re.search('\^', sendconf)) is not None:
                conf_apply_error = ConfigInputException('Error in some command! Check log')
                logger.critical(f'{conf_apply_error} output from device:\n{sendconf}')
                raise conf_apply_error
            else:
                conf_success = 'Configuration applied successfully'
                logger.info(conf_success + f'output from device:\n{sendconf}')
                return True
        else:
            list_error = AttributeError('Problem with converting template to list')
            logger.critical(list_error)
            raise list_error
    else:
        logger.info('Problem with downloading the template')
        return False


result = False

try:
    result = push_standard_config()
except ConfigInputException:
    print('ZLAPALEM DZIADA')

if not result:
    sys.exit()

# check_interface_status = connect.send_command('show interface status')
# print(check_interface_status)
#
# access = []
# trunk = []
#
# for line in check_interface_status.split('\n'):
#     interfaces = re.match('^(?P<int_name>\w+\d+\/\d+).*\w+\s+(?P<int_vlan>trunk|\d+).*$', line)
#     if interfaces is not None:
#         interface = {}
#         if interfaces.group('int_vlan') != 'trunk':
#             interface['name'] = interfaces.group('int_name')
#             interface['vlan'] = interfaces.group('int_vlan')
#             access.append(interface)
#         elif interfaces.group('int_vlan') == 'trunk':
#             interface['name'] = interfaces.group('int_name')
#             interface['vlan'] = interfaces.group('int_vlan')
#             trunk.append(interface)
#
# int_access_template = ''
# int_trunk_template = ''
#
# # configure access interfaces
# if access is not None:
#     get_int_access_template = requests.get('http://172.17.0.3/api/v4/projects/1/repository/files/access/raw?ref=master',
#                                            headers={'PRIVATE-TOKEN': 'x6sP6xf57gb5sxxiXutq'})
#     if get_int_access_template.status_code == 200:
#         int_access_template = Template(get_int_access_template.text)
#     else:
#         requests.exceptions.RequestException()
#     conf_access_interfaces = int_access_template.render(interfaces=access)
#     apply_access_interface_conf = connect.send_config_set(conf_access_interfaces)
#     print(apply_access_interface_conf)
#
# # configure trunk interfaces
# if trunk is not None:
#     get_int_trunk_template = requests.get('http://172.17.0.3/api/v4/projects/1/repository/files/trunk/raw?ref=master',
#                                           headers={'PRIVATE-TOKEN': 'x6sP6xf57gb5sxxiXutq'})
#     if get_int_trunk_template.status_code == 200:
#         int_trunk_template = Template(get_int_trunk_template.text)
#     else:
#         requests.exceptions.RequestException()
#     conf_trunk_interfaces = int_trunk_template.render(interfaces=trunk)
#     apply_trunk_interface_conf = connect.send_config_set(conf_trunk_interfaces)
#     print(apply_trunk_interface_conf)
#
#