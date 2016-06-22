from pathlib import Path

from zone_parser import *


class zone:
    zone = []
    zone_tmp = []
    serial = None
    operate = None
    
    def __init__(self, file_path=None, list=None, operate=None, serial=None):
        self.serial = serial
        self.operate = operate

        if file_path == None or len(file_path.strip()) == 0:
            self.file_path = None
            return
        else:
            self.file_path = Path(file_path)
            self.init_from_file()
            
        if list != None and len(list) != 0:
            self.init_from_list(list)
        
    @property
    def file_path_str(self):
        return str(self.file_path)

    @property
    def file_name(self):
        return str(self.file_path.name)

    @property
    def entries(self):
        return self.zone

    @property
    def list(self):
        return [self.file_path, self.zone]

    def __add_zone_file(self):
        if self.file_path == None:
            print("del zone file err, obj has no file_path")
            return

        if not self.file_path.parent.exists():
            self.file_path.parent.mkdir(mode=0o666)

        if not self.file_path.exists():
            self.file_path.touch(mode=0o666, exist_ok=True)
            

    def __del_zone_file(self):
        if self.file_path == None:
            print("del zone file err, obj has no file_path")
            return
        
        if self.file_path.exists():
            self.file_path.unlink()

    # 1th paramater is a zone dict
    def __write_SOA_to_file(self, dict):

        self.__del_zone_file()
        self.__add_zone_file()

        zone_entry = '%s\t%s\t%s %s %s (\n\t\t\t%s\n\t\t\t%s\n\t\t\t%s\n\t\t\t%s\n\t\t\t%s\n\t\t\t)\n\n' % \
            (dict['zone'], dict['proto'], dict['type'], dict['addr'], dict['email'],
             dict['serial'], dict['refresh'], dict['retry'], dict['expire'], dict['minimum'])
        print("write SOA:\n", zone_entry)

        with self.file_path.open('wb') as f:
            f.seek(0)
            f.write(zone_entry.encode())
            f.close()

    # 1th paramater is a zone dict
    def __write_ANY_to_file(self, dict):

        zone_entry = '%s\t%s\t%s\t%s\n' % (dict['zone'], dict['proto'], dict['type'], dict['addr'])
        print("write ANY:\n", zone_entry)

        with self.file_path.open(mode='ab') as f:
            f.write(zone_entry.encode())
            f.close()

    # ? Need re match for strict check, and need logging
    def check_SOA_entry(self, dc):
        if 'addr' not in dc or 'type' not in dc or 'zone' not in dc:
            return False
        if len(dc['addr']) == 0 or len(dc['zone']) == 0 or len(dc['type']) == 0:
            return False

        # already has this entry
        sz = self.get_zone_SOA_dict(self.zone)
        if sz != None:
            if sz['type'] == dc['type'] and \
                sz['addr'] == dc['addr'] and \
                sz['zone'] == dc['zone'] and \
                sz['expire'] == dc['expire'] and \
                sz['email'] == dc['email'] and \
                sz['minimum'] == dc['minimum'] and \
                sz['refresh'] == dc['refresh'] and \
                sz['retry'] == dc['retry'] :
                return False

        return True
    
    def get_zone_SOA_dict(self, list):
        sz = None
        if len(list) >= 1:
            for i in range(len(list)):
                if 'type' in list[i] and list[i]['type'] == 'SOA':
                    sz = list[i]
                    break
        return sz

    #{'type': 'SOA', 'addr': 'bazh.org.', 'zone': '@', 'expire': '604800', 'email': 'root.bazh.org.',
    #'minimum': '86400', 'refresh': '3600', 'retry': '900', 'serial': '2006021402', 'proto': 'IN'}
    def add_zone_SOA_entry(self, zone_entry):
        self.__write_SOA_to_file(zone_entry)

    # ? Need re match for strict check, and need logging
    def check_ANY_entry(self, dc):
        if 'addr' not in dc or 'type' not in dc or 'zone' not in dc:
            return False
        if len(dc['addr']) == 0 or len(dc['zone']) == 0 or len(dc['type']) == 0:
            return False
        
        # already has this entry
        if dc in self.zone:
            print("already has zone entry:", dc)
            return False

        return True

    def add_zone_ANY_entry(self, zone_entry):
        self.__write_ANY_to_file(zone_entry)

    def add_zone(self):
        print("add_zone zone_tmp:\n", self.zone_tmp)

        if len(self.zone_tmp) <= 0:
            return
        
        if len(self.zone) == 0:
            self.zone.append({})
            sz = self.zone[0]
        else:
            sz = self.get_zone_SOA_dict(self.zone)
        
        sz_tmp = self.get_zone_SOA_dict(self.zone_tmp)
        if sz_tmp == None:
            print("sz_tmp err")
            return
        
        if sz == None or len(sz) == 0:
            self.zone[len(self.zone)-1].update(sz_tmp)
        
        if self.check_SOA_entry(sz_tmp):
            sz.update(sz_tmp)
        
        self.add_zone_SOA_entry(sz)

        for i in range(1, len(self.zone_tmp)):
            if self.check_ANY_entry(self.zone_tmp[i]) and self.zone_tmp[i] not in self.zone:
                self.zone.append(self.zone_tmp[i])
        
        print("add_zone self.zone", self.zone)
        for i in range(1, len(self.zone)):
            self.add_zone_ANY_entry(self.zone[i])
                    
                
    def add_zone_entry(self):
        #print("add_zone_entry zone_tmp:\n", self.zone_tmp)

        if len(self.zone_tmp) > 1:
            for i in range(1, len(self.zone_tmp)):
                if self.check_ANY_entry(self.zone_tmp[i]):
                    self.add_zone_ANY_entry(self.zone_tmp[i])

    # zone_entry is a dict of SOA zone entry
    def init_default_SOA_entry(self, zone_entry):
        if 'zone' not in zone_entry:
            zone_entry.setdefault('zone', '@')
        if 'addr' not in zone_entry:
            zone_entry.setdefault('addr', self.file_name[3:]+'.')
        if 'serial' not in zone_entry:
            zone_entry.setdefault('serial', self.serial)
        if 'type' not in zone_entry:
            zone_entry.setdefault('type', 'SOA')
        if 'proto' not in zone_entry:
            zone_entry.setdefault('proto', 'IN')
        if 'email' not in zone_entry:
            zone_entry.setdefault('email', 'root.' + zone_entry['addr'])
        if 'expire' not in zone_entry:
            zone_entry.setdefault('expire', '604800')
        if 'refresh' not in zone_entry:
            zone_entry.setdefault('refresh', '3600')
        if 'retry' not in zone_entry:
            zone_entry.setdefault('retry', '900')
        if 'minimum' not in zone_entry:
            zone_entry.setdefault('minimum', '900')

    # zone_entry is a dict of any zone entry
    def init_default_ANY_entry(self, zone_entry):
        if 'proto' not in zone_entry:
            zone_entry.setdefault('proto', 'IN')

    # [{}, {"type": "A", "addr": "192.168.1.150", "zone": "ns1"}]
    def init_from_list(self, list):
        #print("init list:\n", list)
        self.zone_tmp.append({})
        
        if len(list) <= 0:
            print("init from emptry list")
            return
        
        self.merge_zone_entries(list)
        
        if 'ZONE_ADD' == self.operate or 'ZONE_ENTRY_ADD' == self.operate:
            self.zone_tmp[0].update(list[0])
            self.init_default_SOA_entry(self.zone_tmp[0])
        if 'ZONE_DEL' == self.operate:
            pass
        #print("self.zone_tmp[0]:\n", self.zone_tmp[0])
        
        for i in range(1, len(list)):
            entry = {}
            entry.update(list[i])
            self.init_default_ANY_entry(entry)
            self.zone_tmp.append({})
            self.zone_tmp[i].update(entry)

    def merge_zone_entries(self, list):
        lst = list.copy()
        list.clear()
        for i in lst:
            if i not in list:
                list.append(i)
        
    def init_from_file(self):
        if self.file_path.exists() and self.file_path.stat().st_size > 20:
            self.zone = parser_zone_lists(parser_conf_to_list(self.file_path_str))
            self.merge_zone_entries(self.zone)
            print("init_from_file:\n", self.zone)
            
    def set_operate(self, operate):
        self.operate = operate
        
    def store(self):
        if 'ZONE_ADD' == self.operate:
            self.add_zone()
        elif 'ZONE_ENTRY_ADD' == self.operate:
            self.add_zone_entry()
        elif 'ZONE_DEL' == self.operate:
            pass
        elif 'ZONE_ENTRY_DEL' == self.operate:
            pass

#TEST
#file_path = '/var/bind/db.bazh.org'
#ls = [{}, {"type": "A", "addr": "192.168.1.150", "zone": "ns1"}]
#z = zone(list=ls, serial=2016010101, file_path=file_path, operate='ZONE_ENTRY_ADD')
#z.store()
