import os
from pathlib import Path

#import json

__all__ = ['parser_conf_to_list',
           'parser_zone_lists',
           'parser_zone_list']

# return a list of the zone file
def parser_conf_to_list(file_path):
    tmp = []
    f = open(file_path)
    n = 0
    for line in f:
        # del comment
        if ';' in line:
            #line = line.split(';')[0].split()
            line = str(line.split(';')[0])

        if len(line.split()) == 0:
            continue

        if line[0] != ' ' and line[0] != '\t':
            n += 1
            m = n - 1
            tmp.append([])
            #print()
            #print(m, "---------------")

        dst_str = line.split()
        for item in dst_str:
            tmp[m].append(item)
            #print(item)

    return tmp

# parser the list os a zone file and return the zone list dict -> [{},{}]   
def parser_zone_lists(zone_lists):
    zone = []
    j = 0
    var = None
    for lst in zone_lists:
        
        zone.append({})
        entry = zone[j]
        j += 1
        
        soa = None
        i = 0
        for item in lst:
            if i == 0:
                if item[0] == '$':
                    var = item[1:]
                    i += 1
                    continue

                elif item == '@':
                    entry['zone'] = item
                else:
                    entry['zone'] = item
            elif i == 1:
                if var != None:
                    entry[var] = item
                    var = None
                    break
                entry['proto'] = item
            elif i == 2:
                if item == 'SOA':
                    soa = True
                entry['type'] = item
            elif i == 3:
                entry['addr'] = item
            elif i == 4:
                entry['email'] = item

            i += 1

        if soa:
            idx_bgn = lst.index('(') + 1
            idx_end = lst.index(')')
            n = 0
            for i in lst[idx_bgn:idx_end]:
                if n == 0:
                    entry['serial'] = i
                if n == 1:
                    entry['refresh'] = i
                if n == 2:
                    entry['retry'] = i
                if n == 3:
                    entry['expire'] = i
                if n == 4:
                    entry['minimum'] = i
                n += 1
            
            n = lst.count('IN')-1
            for i in range(n):
                idx_bgn = lst.index('IN', idx_bgn) + 1
                zone.append({})
                entry = zone[j]
                j += 1
                entry['zone'] = '@'
                entry['proto'] = 'IN'
                entry['type'] = lst[idx_bgn]
                if entry['type'] == 'MX':
                    entry['prefer'] = lst[idx_bgn+1]
                    entry[lst[idx_bgn]] = lst[idx_bgn+2]
                
    return zone

#
def parser_zone_list(lst):
    zone = []
    j = 0
    var = None
    zone.append({})
    entry = zone[j]
    j += 1

    soa = None
    i = 0
    for item in lst:
        if i == 0:
            if item[0] == '$':
                var = item[1:]
                i += 1
                continue

            elif item == '@':
                entry['zone'] = item
            else:
                entry['zone'] = item
        elif i == 1:
            if var != None:
                entry[var] = item
                var = None
                break
            entry['proto'] = item
        elif i == 2:
            if item == 'SOA':
                soa = True
            entry['type'] = item
        elif i == 3:
            entry['addr'] = item
        elif i == 4:
            entry['email'] = item

        i += 1

    if soa:
        idx_bgn = lst.index('(') + 1
        idx_end = lst.index(')')
        n = 0
        for i in lst[idx_bgn:idx_end]:
            if n == 0:
                entry['serial'] = i
            if n == 1:
                entry['refresh'] = i
            if n == 2:
                entry['retry'] = i
            if n == 3:
                entry['expire'] = i
            if n == 4:
                entry['minimum'] = i
            n += 1

        n = lst.count('IN') - 1
        for i in range(n):
            idx_bgn = lst.index('IN', idx_bgn) + 1
            zone.append({})
            entry = zone[j]
            j += 1
            entry['zone'] = '@'
            entry['proto'] = 'IN'
            entry['type'] = lst[idx_bgn]
            if entry['type'] == 'MX':
                entry['prefer'] = lst[idx_bgn + 1]
                entry[lst[idx_bgn]] = lst[idx_bgn + 2]

    return zone

#TEST:
#file_path = '/root/test/db.bazh.org'
#
#
#print(parser_conf_to_list(file_path))
#print(json.dumps(parser_zone_lists(parser_conf_to_list(file_path)), indent=4))
#
#
#ls = ['blog', 'IN', 'NS', 'ns1']
#print(parser_zone_list(ls))
#

#z = zone(file_path)
#print(z.list)

