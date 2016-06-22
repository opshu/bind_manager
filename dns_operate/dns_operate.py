import io
from pathlib import Path
import json
import re
import datetime

from zone import *
from named_conf_parser import *

OPERATION = ['ZONE_ADD', 'ZONE_DEL', 'ZONE_ENTRY_ADD', 'ZONE_ENTRY_DEL']

class bind:
    def __init__(self, named_path='/etc/bind/named.conf', zone_dir='/var/bind/'):
        self.named_path = Path(named_path)
        self.zone_dir = Path(zone_dir)
        self.zone = []
        self.named = named(named_path)
        self.date = ''
        self.index = 0

    @property
    def next_serial(self):
        date = ''.join(str(datetime.date.today()).split('-'))
        if date == self.date:
            self.index += 1
        else:
            self.date = date
            self.index = 0
        count = '%s%02d' % (self.date, self.index)
        return count
    
    @property
    def serial(self):
        return '%s%02d' % (self.date, self.index)
    
    def mk_zone_dir():
        pass

    # Return True if zone_json if right for a whole zone, else return False
    # {"operate":"ZONE_ADD", "named":{"zone":"bazh.org."}, "zone":[{'type': 'SOA', 'addr': 'bazh.org.', 'zone': '@', 'expire': '604800', 'email': 'root.bazh.org.', 'minimum': '86400', 'refresh': '3600', 'retry': '900', 'serial': '2006021402', 'proto': 'IN'}, {"type": "A", "addr": "192.168.1.150", "zone": "ns1"}]}
    # {"operate":"ZONE_ADD", "named":{"zone":"bazh.org."}, "zone":[{}, {"type": "A", "addr": "192.168.1.150", "zone": "ns1"}]}
    # {"operate":"ZONE_ADD", "named":{"zone":"bazh.org."}}
    # {"operate":"ZONE_ENTRY_ADD", "named":{"zone":"bazh.org."}, "zone":[{}, {"type": "A", "addr": "192.168.1.150", "zone": "ns1"}]}
    # {"operate":"ZONE_ENTRY_ADD", "named":{"zone":"bazh.org."}, "zone":[{}, {"type": "A", "addr": "192.168.1.150", "zone": "ns1"}]}
    def __check_zone_js(self, zone_json):
        zone_obj = json.loads(zone_json)
        if 'zone' not in zone_obj or 'named' not in zone_obj or 'operate' not in zone_obj:
            return False
        
        if zone_obj['operate'] not in OPERATION or 'zone' not in zone_obj['named']:
            return False
        
        if len(zone_obj['zone']) == 0 or len(zone_obj['named']['zone']) == 0:
            return False
        
        return True
    
    # {"operate":"ADD_ZONE", "named":{"zone":"bazh.org"}, "zone":[{}, {"type": "A", "addr": "192.168.1.150", "zone": "ns1"}]}
    def operate_zone(self, zone_json):
        zone_js = json.loads(zone_json)
        print("operate_zone zone_js:", zone_js)
        
        if self.__check_zone_js(zone_json) == False:
            return False

        if 'ZONE_ADD' == zone_js['operate']:
            if not self.named.has_zone(zone_js['named']['zone']):
                self.named.add_named_conf_zone(zone_js['named'])
            else:
                print("Already has zone:", zone_js['named']['zone'])

            zone_file_name = 'db.' + zone_js['named']['zone']
            z = zone(serial=self.next_serial, list=zone_js['zone'], file_path=str(self.zone_dir / zone_file_name), operate=zone_js['operate'])
            z.store()
            
        elif 'ZONE_DEL' == zone_js['operate']:
            if self.named.has_zone(zone_js['named']['zone']):
                self.named.del_named_conf_zone(zone_js['named'])
            else:
                print("No this deleting zone:", zone_js['named']['zone'])
                
        elif 'ZONE_ENTRY_ADD' == zone_js['oprate']:
            pass
        elif 'ZONE_ENTRY_DEL' == zone_js['oprate']:
            pass

    def del_zone_entry():
        pass
    def del_named():
        pass
    def del_zone_file():
        pass
    def del_zone(named, zone):
        pass
        #for  in :
        #if named['zone_name'] in self.named:
    
    def store_to_zone_file():
        pass
    def store_to_zone_files():
        pass
    
    def store_to_named_file():
        pass
    
    def store():
        pass
    
    def dump():
        print("named_path:", self.named_path)
        print("zone_dir:", self.zone_dir)
        print("named:\n", self.named)
        print("zones:\n", self.zone)
    
    def reload():
        subprocess.call(["rndc", "reload"])
    def start():
        subprocess.call(["named"])
    def stop():
        subprocess.call(["killall", "named"])
    def reinit():
        pass
            
        
        
if __name__ == "__main__":
    #file_path = '/root/test/db.bazh.org'
    #print(parser_conf_to_list(file_path))
    #z = zone(file_path)
    #print(z.list)
 
     
    zone1 = '"zone":[{}, {"type": "A", "addr": "192.168.1.150", "zone": "ns1"}]'
    named1 = '"named":{"zone":"bazh.org"}'
    zone_json = '{"operate":"ZONE_ADD", %s, %s}' % (named1, zone1)
    
    #print("zone_json:\n", zone_json)

    #{"operate":"ZONE_ADD", "named":{"zone":"bazh.org"}, "zone":[{}, {"type": "A", "addr": "192.168.1.150", "zone": "ns1"}]}
    #print(json.loads(zone_json))
    #
    bd = bind()
    bd.operate_zone(zone_json)
    
