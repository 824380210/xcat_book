#!/usr/bin/env python
#
import os
import json
import subprocess
#import re 
# nodediscover list | grep smm |awk '{print $5}'
import pyghmi.util.webclient as wc
#
print " Start to read the IPv4 and IPv6 Address From nodediscover Commnad"
#
smm_data = []
first_mac = []
chain_mac = []
verify_smm = []
last_mac = []
smm_mac_set = set()
smm_mac = set()
my_first_smm = set()
myinterface = ""
mylist = []
"""
[root@mgt ~]# nodediscover list | grep smm |awk '{print $5}'
172.30.101.131,fe80::a94:efff:fe51:3fe%ens8
172.30.101.133,fe80::a94:efff:fe53:afd4%ens8
172.30.101.132,fe80::a94:efff:fe57:419a%ens8
"""
###   nodediscover list | grep smm |awk '{print $5}'|cut -d, -f2| grep fe80
cmd = " nodediscover list | grep smm |awk '{print $5}'|cut -d, -f2| grep fe80"
check_ipv6 = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE
)
(myipv6data, err) = check_ipv6.communicate()
for entry in myipv6data.split('\n'):
    if 'fe80' in entry:
#       print "IPv6 Address: " + entry
        smm_data.append(entry)
# detect the interface that communicate with the SMM 
myinterface = smm_data[0].split('%')[1]
#print myinterface
smm_number = str(len(smm_data))
print "\n Now we found SMM device number is " + smm_number
#
print "\n Now start to fetch the SMM neighbor Data"
#
def mac2ipv6(mac):
    # only accept MACs separated by a colon
    parts = mac.split(":")

    # modify parts to match IPv6 value
    parts.insert(3, "ff")
    parts.insert(4, "fe")
    parts[0] = "%x" % (int(parts[0], 16) ^ 2)

    # format output
    ipv6Parts = []
    for i in range(0, len(parts), 2):
        ipv6Parts.append("".join(parts[i:i+2]))
    ipv6 = "fe80::%s" % (":".join(ipv6Parts))
    return ipv6
"""

>>> neigh[4]
{u'peerport': u'B', u'peername': u'', u'peerdesc': u'Lenovo SMM', u'mac': u'08:94:ef:51:03:fe', u'initted': True, u'peermac': u'08:94:ef:57:41:9a', u'sha256': u'k3zR32qwajCCJt7ru7rGvmZ1YK/u0g4ylu7Y//w5L8Q=', u'port': 4}
>>> neigh[5]
{u'peerport': u'Ethernet1/14', u'peername': u'', u'peerdesc': u'Other Device', u'mac': u'08:94:ef:51:03:fe', u'initted': True, u'peermac': u'a4:8c:db:96:b8:0f', u'port': 5}
>>>

pv6_addr = '[fe80::a94:efff:fe57:419a%ens8]'
>>> a = wc.SecureHTTPConnection(ipv6_addr, verifycallback=lambda x: True)
>>> neigh = a.grab_json_response('/scripts/neighdata.json')
>>> neigh[5]
{u'peerport': u'B', u'peername': u'', u'peerdesc': u'Lenovo SMM', u'mac': u'08:94:ef:57:41:9a', u'initted': True, u'peermac': u'08:94:ef:53:af:d4', u'sha256': u'VsH2pb+a1lLctnRPZRwdoAxfairS5Z5qJGwoGbHaY5Y=', u'port': 5}
>>> neigh[4]
{u'peerport': u'B', u'peername': u'', u'peerdesc': u'Lenovo SMM', u'mac': u'08:94:ef:57:41:9a', u'initted': True, u'peermac': u'08:94:ef:51:03:fe', u'sha256': u'bXSIzSV9++xh1c/6B5R8HqmrWDoky+2G+ffokXLcI6M=', u'port': 4}
>>>


"""
for smm_addr in smm_data:
    ipv6_addr = '[' + smm_addr + ']'
    a = wc.SecureHTTPConnection(ipv6_addr, verifycallback=lambda x: True)
    neighs = a.grab_json_response('/scripts/neighdata.json')
    for idx in (4,5):
        if 'peerport'  not in neighs[idx]:
            # no peerport means the port is empty ,so it did not have cable connected
            # 
            continue
        else:
            if neighs[idx]['peerport'] not in "TB":
                #print neighs[idx]['mac']
                print "we are expect first  SMM MAC : "+ neighs[idx]['mac'] + " IPv6 is "+  smm_addr
                first_mac.append(neighs[idx]['mac']) 
                first_mac.append(neighs[idx]['peermac']) 
                print "Switch MAC is " + neighs[idx]['peermac'] + " first SMM is"+ neighs[idx]['mac']
                my_first_smm.add(neighs[idx]['mac'])
            else:
                #record the mac of the SMM , PORT ID and peer MAC
                # 
                smm_mac.add(neighs[idx]['mac'])
                chain_mac.append({neighs[idx]['mac']:{idx:neighs[idx]['peermac']}})
                print "\n\033[31m"+neighs[idx]['peermac'] +" ===>"+ neighs[idx]['mac']+"\033[0m"
#chain_mac = smm_mac - my_first_smm
print my_first_smm
print "the all MAC in SMM is "
print smm_mac
"""
for mysmm in my_first_smm:
    ipv6 = mac2ipv6(mysmm)
    ipv6_addr = ipv6 +'%' + myinterface
    a = wc.SecureHTTPConnection(ipv6_addr, verifycallback=lambda x: True)
    neighs = a.grab_json_response('/scripts/neighdata.json')
    
smm_chain = []
"""
#def get_smm_chain(mac,):
#    global smm_chain[mac]
def get_smm_chain(mac1,mac2):
    """
    mac1 is the upstream SMM MAC
    mac2 is the downstream SMM MAC
    """
    upmac   = mac1
    downmac = mac2
    #global myinterface
    global mylist
    if upmac == downmac:
        mylist.append(upmac)
        ipv6 = mac2ipv6(upmac)
    else:
        mylist.append(downmac)
        ipv6 = mac2ipv6(downmac)
    ipv6_addr = '['+ipv6 +'%' + myinterface+']'
    #print "now the ipv6 is " + ipv6_addr
    a = wc.SecureHTTPConnection(ipv6_addr, verifycallback=lambda x: True)
    neighs = a.grab_json_response('/scripts/neighdata.json')
    if 'peerport' not in neighs[4] or 'peerport' not in  neighs[5]:
        print downmac + " is the last SMM in this Chain"
        pass
    elif  neighs[4]['peerport'] not in "TB" or neighs[5]['peerport'] not in "TB":
        print upmac + " is the first SMM MAC in this chain"
        if neighs[4]['peerport']  in "TB":
            next_mac = neighs[4]['peermac']
        else:
            next_mac = neighs[5]['peermac']
        get_smm_chain(downmac,next_mac)
    else:
        if neighs[4]['peermac'] not in mylist:
            next_mac = neighs[4]['peermac']
            get_smm_chain(downmac,next_mac)
        else:
            next_mac = neighs[5]['peermac']
            get_smm_chain(downmac,next_mac)
    #    mylist.append(next_mac)
    return mylist
#
for mysmm in  my_first_smm:
    print "\n\n\033[31mthis  is the chain SMM list ===>"
    print get_smm_chain(mysmm,mysmm)
    print "============END============\033[0m\n\n"

            
          
    
    
