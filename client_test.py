#!/usr/local/bin/python3
import socket
import time
import json




if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8880))
    time.sleep(1)
    #sock.send(b'1')
    #print("recv", sock.recv(1024))
    json_str = b'{"operate":"ZONE_ADD", "named":{"zone":"bazh.org"}, "zone":[{}, {"type": "A", "addr": "192.168.1.150", "zone": "ns1"}]}'
    #json_str_len = str(len(json_str))
    #sock.send(json_str_len.encode())
    sock.send(json_str)
    sock.close()
