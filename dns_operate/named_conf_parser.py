import os
from pathlib import Path
import re

#__all__ = ['named']

class named:
    def __init__(self, named_path='/etc/bind/named.conf'):
        self.zone = [] # zone dict list [{},{}]
        self.options = []
        self.keys = []
        self.controls = []
        self.named_path = Path(named_path)

    def has_zone(self, zone_name):
        for i in range(len(self.zone)):
            dict = self.zone[i]
            if zone_name in dict.values():
                return True
        return False
    
    def named_conf_list(self):
        conf_list = []
        p = self.named_path
        if not p.exists():
            return None
        f = p.open()
        for l in f:
            tmp = l.strip()
            if len(tmp) == 0 or tmp.split('#')[0] == '':
                continue
            conf_list.append(tmp)
        return conf_list
    
    def check_zone(self, zone):
        if 'zone' not in zone or 'type' not in zone and 'file' not in zone:
            return False
        if len(zone['zone']) == 0 or len(zone['type']) == 0 or len(zone['file']) == 0:
            return False
        return True
    
    def add_zone(self, zone):
        if self.check_zone(zone):
            self.zone.append(zone)
            return True
        else:
            return False
    
    def check_key(self, key):
        if 'key' not in key or 'algorithm' not in key or 'secret' not in key:
            return False
        if len(key['key']) == 0 or len(key['algorithm']) == 0 or len(key['secret']) == 0:
            return False
        return True
    
    def add_key(self, key):
        if self.check_key(key):
            self.keys.append(key)
            return True
        else:
            return False
    
    def add_control(self, control):
        pass
    def add_option(self, option):
        pass


    def add_named_conf_file(self):
        self.name_path.touch(mode=0o666, exist_ok=True)
    def del_named_conf_file(self):
        self.name_path.unlink()

    def add_named_conf_key():
        pass
    def del_named_conf_key():
        pass

    # {"zone":"bazh.org"}
    def add_named_conf_zone(self, dict):
        nz = {}
        nz['zone'] = dict['zone']
        if 'type' not in dict:
            nz['type'] = 'master'
        else:
            nz['type'] = dict['type']

        if 'file' not in dict:
            nz['file'] = 'db.' + dict['zone']
        else:
            nz['file'] = dict['file']

        if 'allow-update' in dict:
            named_zone = 'zone "%s" {\n\ttype %s;\n\tfile "%s";\n\tallow-update {%s;};\n};\n' % \
                (nz['zone'], nz['type'], nz['file'], nz['allow-update'])
        else:
            named_zone = 'zone "%s" {\n\ttype %s;\n\tfile "%s";\n};\n' % (nz['zone'], nz['type'], nz['file'])

        print("add named zone:\n", named_zone)
        with self.named_path.open(mode='ab') as f:
            f.write(named_zone.encode())
            f.close()
        self.add_zone(nz)

    # {"zone":"bazh.org"}
    def del_named_conf_zone(self, dict):
        pass

    def _parser_key(self, conf_str):
        pass
    def _parser_keys(self, conf_str):
        pass
    
    def _parser_control(self, conf_str):
        pass
    def _parser_controls(self, conf_str):
        pass

    # Like this:
    # directory "/var/bind";
    def _parser_option(self, conf_str):
        pattern = conf_str.split()
        #print(len(pattern), pattern)
        if len(pattern) < 1:
            return None
        self.options.append({})
        option = self.options[len(self.options) - 1]
        option[pattern[0]] = pattern[1].rstrip(';')
        #print(option)

    #
    def _parser_options(self, conf_str):
        find = re.findall(r'options\s*\{([\w\s"/;\-_]+)\}\s*;', conf_str)
        for i in range(len(find)):
            self._parser_option(find[i])
        print("options:\n", self.options)
    
    # zone "bazh.org" {allow-update { any; };type master;file "db.bazh.org";};
    # zone "bazh.org" {type master;file "db.bazh.org";allow-update { any; };};
    def _parser_zone(self, conf_str):
        self.zone.append({})
        z = self.zone[len(self.zone) - 1]
        find = re.search(r'allow-update\s*\{\s*(\w+)\s*;\s*\}', conf_str)
        z['allow-update'] = find.group(1)
        find = re.search(r'zone\s*(["\.\-_\w]+)\s*', conf_str)
        z['zone_name'] = find.group(1)
        find = re.search(r'type\s*(\w+);', conf_str)
        z['type'] = find.group(1)
        find = re.search(r'file\s*([\w\s\.\-_"]+);', conf_str)
        z['file'] = find.group(1)

    # zone "0.0.127.in-addr.arpa" {type master;file "127.0.0.zone";};
    def _parser_common_zone(self, conf_str):
        #('"localhost"', 'type', 'master', 'file', '"db.local"')
        find = re.search(r'zone\s*(["\.\-_\w]+)\s*\{\s*type\s+(\w+)\s*;\s*file\s+([\w\s"\.\-_]+)\s*;\s*\}\s*;', conf_str)
        #print("*****zone:", find.groups())
        self.zone.append({})
        z = self.zone[len(self.zone) - 1]
        z['zone_name'] = find.group(1)
        z['type'] = find.group(2)
        z['file'] = find.group(3)

    def _parser_zones(self, conf_str):
        find = re.findall(r'zone\s*"[^"]+"\s*\{\s*[\w\s"\.\-_;]*}\s*;', conf_str)
        #print(find)
        for i in range(len(find)):
            self._parser_common_zone(find[i])
        find = re.findall(r'zone\s*"[^"]+"\s*\{[\w\s"\.\-_;]*allow-update[\{\}\w\s"\.\-_;]*[\w\s"\.\-_;]*}\s*;', conf_str)
        #print(find)
        for i in range(len(find)):
            self._parser_zone(find[i])
        print("zone:\n", self.zone)

    def _parser_named_conf_str(self, conf_str):
        if len(conf_str) == 0:
            return None

    #
    def parser_named_conf(self):
        conf_list = self.named_conf_list()
        conf_str = ''.join(conf_list)
        print("conf_str:\n", conf_str)
        if len(conf_str) != 0:
            self._parser_keys(conf_str)
            self._parser_options(conf_str)
            self._parser_zones(conf_str)
            self._parser_controls(conf_str)
            
# Test:
#file_path = '/etc/bind/named.conf'
#name = named(file_path)
#name.parser_named_conf()
