#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import *
import json

server_port = 53533

serverSock = socket(AF_INET, SOCK_DGRAM)
serverSock.bind(('', server_port))
ip_map = {}


def get_request(query_message):
    message = json.loads(query_message.decode())
    ip = 'VALUE' in message

    if not ip:
        hostname = message['NAME']
        request_type = message['TYPE']
        return dns_request(hostname, request_type)
    else:
        hostname = message['NAME']
        ip = message['VALUE']
        request_type = message['TYPE']
        ttl = message['TTL']
        return register(hostname, ip, request_type, ttl)


def dns_request(hostname, request_type):
    content = ip_map[request_type + ' ' + hostname]
    fs_ip = content['VALUE']
    return str(fs_ip).encode()


def register(hostname, ip, request_type, ttl):
    content = {'TYPE': request_type, 'NAME': hostname, 'VALUE': ip, 'TTL': ttl}
    key = request_type + ' ' + hostname
    ip_map[key] = content
    return json.dumps('').encode()

        
while True:
    query_message, addr = serverSock.recvfrom(2048)
    response_message = get_request(query_message)
    serverSock.sendto(response_message, addr)