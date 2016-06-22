#!/usr/local/bin/python3

import socket
import json
import sys
from dns_operate import *

if __name__ == '__main__':
    bd = bind()
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8880))
    sock.listen(5)
    while True:
        connection,address = sock.accept()
        try:
            connection.settimeout(5)
            buf = connection.recv(1024)

            if len(buf) != 0:
                #js = json.loads(buf)
                #print('recv js', js)
                bd.operate_zone(buf.decode())
                
        except socket.timeout:
            print('time out')
        connection.close()
    
    
