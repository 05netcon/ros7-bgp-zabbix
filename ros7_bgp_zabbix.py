#!/usr/bin/env python3

import argparse
import json

import librouteros

from librouteros.query import Key


parser = argparse.ArgumentParser(
    description='Monitoring MikroTik RouterOS 7 BGP in Zabbix'
)
parser.add_argument(
    'command', 
    type = str, 
    choices=['discover', 'status'],
    help = 'script operating mode'
)
parser.add_argument('host', type = str, help = 'device hostname or ip address')
parser.add_argument('username', type = str, help = 'device username')
parser.add_argument('password', type = str, help = 'device password')
parser.add_argument(
    '-p', '--peer', 
    metavar = '', 
    type = str, 
    help = 'peer name (only if in status mode)'
)
args = parser.parse_args()

if __name__ == '__main__':
    api = librouteros.connect(
        host = args.host,
        username = args.username,
        password = args.password
    )
    bgp_sessions = api.path('/routing/bgp/session').select(
        Key('name'), 
        Key('established')
    )
    peers = {
        bgp_session['name']: bgp_session['established'] 
        for bgp_session in bgp_sessions
    }
    command = args.command
    if command == 'discover':
        result = {
            'data': [
                {'{#BGPPEER}': peer_name} for peer_name in peers
            ]
        }
        print(json.dumps(result, indent = 4, sort_keys = True))
    elif command == 'status':
        peer_name = args.peer
        if peer_name in peers:
            if peers[peer_name]:
                print(1)
            else:
                print(0)
        else:
            print(0)
