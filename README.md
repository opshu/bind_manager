# bind_manager
designed by python to manage bind DNS server

管理BIND，通过json数据进行传递，具体见下：
'{"operate":"ZONE_ADD", "named":{"zone":"bazh.org."}, "zone":[{'type': 'SOA', 'addr': 'bazh.org.', 'zone': '@', 'expire': '604800', 'email': 'root.bazh.org.', 'minimum': '86400', 'refresh': '3600', 'retry': '900', 'serial': '2006021402', 'proto': 'IN'}, {"type": "A", "addr": "192.168.1.150", "zone": "ns1"}]}'
'{"operate":"ZONE_ADD", "named":{"zone":"bazh.org."}}'
'{"operate":"ZONE_ADD", "named":{"zone":"bazh.org."}, "zone":[{}, {"type": "A", "addr": "192.168.1.150", "zone": "ns1"}]}'
'{"operate":"ZONE_DEL", "named":{"zone":"bazh.org."}}'
'{"operate":"ZONE_ENTRY_ADD", "named":{"zone":"bazh.org."}, "zone":[{}, {"type": "A", "addr": "192.168.1.150", "zone": "ns1"}]}'
'{"operate":"ZONE_ENTRY_DEL", "named":{"zone":"bazh.org."}, "zone":[{}, {"type": "A", "addr": "192.168.1.150", "zone": "ns1"}]}'

第一个operate表示操作的具体动作，操作类型ZONE_ADD表示添加一个zone，ZONE_ENTRY_ADD表示添加一个zone的条目。
named表示添加的zone名称，zone列表则表示域文件内的具体条目，最复杂的一条即如上面第一条命令所示，添加了一个bazh.org的域，并添加了其SOA记录，和一条A记录，zone中的红色字体字段名称都和bind中的zone记录相一致，具体可以参看bind的zone配置。
形如第一条的zone控制粒度很细，但是过于繁琐，也可以使用形如第二条的命令，添加默认的一个zone。或者第三条命令，添加一个默认的SOA记录，和一个A记录。
ZONE_ENTRY_ADD是向现有的一个ZONE记录添加一个三级域名的记录，如上地五条，添加一个A记录:ns1.bazh.org。
相应的DEL则是删除zone或者zone的一个记录。
