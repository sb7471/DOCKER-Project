#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request
import requests
from flask_api import status
from socket import *
import json
app = Flask(__name__)


@app.route('/fibonacci', methods = ['GET'])
def accept_request():
    hostname = request.args['hostname'] 
    fs_port = request.args['fs_port']
    as_ip = request.args['as_ip']
    as_port = int(request.args['as_port'])
    number = request.args['number']

    if hostname == '' or fs_port == '' or as_ip == '' or as_port == '' or number == '' or not number.isdigit():
        return 'bad format', status.HTTP_400_BAD_REQUEST
        
    fs_ip = query_authoritative_server(as_ip, as_port, hostname)
    real_add = 'http://' + fs_ip + ':' + fs_port
    dict_to_send_1 = {'number': number}
    result = requests.get(real_add + '/fibonacci', params=dict_to_send_1)
    return result.text, status.HTTP_200_OK

def query_authoritative_server(as_ip, as_port, hostname):
    client_socket = socket(AF_INET, SOCK_DGRAM)
    query_json = {'TYPE': 'A', 'NAME': hostname}
    client_socket.sendto(json.dumps(query_json).encode(), (as_ip, as_port))
    ip_address, server_address = client_socket.recvfrom(2048)
    return ip_address.decode()


app.run(host='0.0.0.0',
        port=8080,
        debug=True)
