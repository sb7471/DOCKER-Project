#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_api import status
import json
from socket import *
app = Flask(__name__)


@app.route('/fibonacci', methods = ['GET'])
def fibonacci():
    number = request.args['number']
    result = calculate_fibonacci_number(number)
    return str(result)

def calculate_fibonacci_number(number):
    number = int(number)
    if number <= 2:
        return 1
    return calculate_fibonacci_number(number-1) + calculate_fibonacci_number(number-2)


@app.route('/register', methods = ['PUT'])
def register():
    content = request.get_json()
    hostname = content.get('hostname')
    ip = content.get('ip')
    as_ip = content.get('as_ip')
    as_port = int(content.get('as_port'))

    register_json = {'TYPE': 'A', 'NAME': hostname, 'VALUE': ip, 'TTL': 10}

    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.sendto(json.dumps(register_json).encode(), (as_ip, as_port))
    response_message, server_address = client_socket.recvfrom(2048)
    return 'Registered Ok', status.HTTP_201_CREATED


app.run(host='0.0.0.0',
        port=9090,
        debug=True)