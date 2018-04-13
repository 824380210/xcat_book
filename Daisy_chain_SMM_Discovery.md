## Daisy chain SMM configure Example


```
[root@base e1350]# tabedit site
[root@base e1350]# tabedit networks
[root@base e1350]# makenetworks
[root@base e1350]# tabedit networks
[root@base e1350]# chtab net=172.20.0.0 networks.dynamicrange=172.20.255.1-172.20.255.254
[root@base e1350]# chtab node=compute nodehm.serialport=0 nodehm.serialspeed=115200 nodehm.serialflow=hard
[root@base e1350]# chtab node=compute nodetype.os=rhels7.4 nodetype.arch=x86_64 nodetype.Profile=compute
[root@base e1350]# chtab node=compute noderes.netboot=xnba noderes.nfsserver=172.20.0.1 noderes.installnic=mac noderes.primarynic=mac
[root@base e1350]# nodeadd switch01 groups=switch
[root@base e1350]# nodeadd n01-n03  groups=ipmi,42perswitch,84nodeperrack,compute,all,CPOMxxxx,RACKA1,MFG1A
[root@base e1350]# nodeadd n[01-03]-xcc groups=bmc,84bmcperrack
[root@base e1350]#  nodeadd smm[01-03] groups=smm

```
## Lab topology 

```
1: 3 node with 3 chassis ,3 SMM
n01 in chassis 1 ,bay 1 ,and managed by smm01
n02 is chassis 2 ,bay 1 ,and managed by smm02
n03 in chassis 3 ,bay 1 ,and managed by smm03

smm01 connect to switch01 port 14
smm02 connect to smm02
smm03 connect to smm03

n01 data NIC connect to switch01 port 1
n01 data NIC connect to switch01 port 2
n01 data NIC connect to switch01 port 3

```

##  define the SMM as below ,make sure bmcusername and bmcpassword is set 。 the bmc should be set to the SMM's IP
```
[root@base ~]# lsdef smm
Object name: smm01
    bmc=172.30.101.131
    bmcpassword=PASSW0RD
    bmcusername=USERID
    groups=smm
    ip=172.30.101.131
    mgt=ipmi
    postbootscripts=otherpkgs
    postscripts=syslog,remoteshell,syncfiles
Object name: smm02
    bmc=172.30.101.132
    bmcpassword=PASSW0RD
    bmcusername=USERID
    groups=smm
    ip=172.30.101.132
    mgt=ipmi
    postbootscripts=otherpkgs
    postscripts=syslog,remoteshell,syncfiles
Object name: smm03
    bmc=172.30.101.133
    bmcpassword=PASSW0RD
    bmcusername=USERID
    groups=smm
    ip=172.30.101.133
    mgt=ipmi
    postbootscripts=otherpkgs
    postscripts=syslog,remoteshell,syncfiles

```

## define the node as below ,make sure mpa amd slot id is correctly configured 

```
[root@base ~]# lsdef n03
Object name: n03
    arch=x86_64
    bmc=n03-xcc
    chain=runcmd=bmcsetup,shell
    groups=ipmi,42perswitch,84nodeperrack,compute,all,CPOMxxxx,RACKA1,MFG1A
    installnic=mac
    ip=172.20.101.3
    mgt=ipmi
    mpa=smm03
    netboot=xnba
    nfsserver=172.20.0.1
    ondiscover=nodediscover
    os=rhels7.4
    postbootscripts=otherpkgs
    postscripts=syslog,remoteshell,syncfiles
    primarynic=mac
    profile=compute
    rack=1
    serialflow=hard
    serialport=0
    serialspeed=115200
    slotid=1
    switch=switch1
    switchport=3
    unit=3

[root@mgt18a ~]# lsdef n01-xcc
Object name: n01-xcc
    groups=bmc,84bmcperrack
    ip=172.29.102.1
    postbootscripts=otherpkgs
    postscripts=syslog,remoteshell,syncfiles


```

## install confluent service 

```
yum install lenovo-confluent.noarch -y
systemctl enable confluent.service
source /etc/profile.d/confluent_env.sh


```

## setup the confluent service 

```
confetty create /nodegroups/switch
confetty create /nodes/switch01 groups=switch
confetty set /nodegroups/switch/attributes/current secret.hardwaremanagementpassword="RO"
confetty set /nodegroups/everything/attributes/current discovery.policy=open

```

## configure the DNS /DHCP/confluent service to make it work


```
[root@base ~]# makehosts ipmi,smm,bmc,switch01
[root@base ~]# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
172.20.0.1      mgt     mgt.cluster
172.20.101.1 n01 n01.cluster
172.29.101.1 n01-xcc n01-xcc.cluster
172.20.101.2 n02 n02.cluster
172.29.101.2 n02-xcc n02-xcc.cluster
172.20.101.3 n03 n03.cluster
172.29.101.3 n03-xcc n03-xcc.cluster
172.30.101.131 smm01 smm01.cluster
172.30.101.132 smm02 smm02.cluster
172.30.101.133 smm03 smm03.cluster
172.30.50.1 switch01 switch01.cluster


[root@base ~]# makedhcp -n
Renamed existing dhcp configuration file to  /etc/dhcp/dhcpd.conf.xcatbak

The dhcp server must be restarted for OMAPI function to work
Warning: No dynamic range specified for 172.29.0.0. If hardware discovery is being used, a dynamic range is required.
Warning: No dynamic range specified for 172.30.0.0. If hardware discovery is being used, a dynamic range is required.
[root@base ~]# makedns -n
Handling smm02 in /etc/hosts.
Handling n01-xcc in /etc/hosts.
Handling mgt in /etc/hosts.
Handling localhost in /etc/hosts.
Handling n03-xcc in /etc/hosts.
Handling n02-xcc in /etc/hosts.
Handling n02 in /etc/hosts.
Handling n03 in /etc/hosts.
Handling switch01 in /etc/hosts.
Handling localhost in /etc/hosts.
Handling smm03 in /etc/hosts.
Handling smm01 in /etc/hosts.
Handling n01 in /etc/hosts.
Getting reverse zones, this may take several minutes for a large cluster.
Completed getting reverse zones.
Updating zones.
Completed updating zones.
Restarting named
Restarting named complete
Updating DNS records, this may take several minutes for a large cluster.
Completed updating DNS records.
DNS setup is completed
[root@base ~]# service  dhcpd restart
Redirecting to /bin/systemctl restart dhcpd.service



```


##  confluent server settings ,only the smm01 have switch connected ,and smm02 /smm03 have teh encolsure.extends attribute to set to upper layer SMM( the direction to the switch )

```
[root@base ~]# makeconfluentcfg ipmi
[root@base ~]# makeconfluentcfg smm

[root@base ~]# nodeattrib smm01 net.switch=switch01 net.switchport=14
smm01: switch01
smm01: 14

[root@base ~]# nodeattrib smm02 enclosure.extends=smm01
smm02: smm01
[root@base ~]# nodeattrib smm03 enclosure.extends=smm02
smm03: smm02


[root@base ~]# nodeattrib smm net
smm01: net.bootable:
smm01: net.hwaddr:
smm01: net.ipv4_gateway:
smm01: net.switch: switch01
smm01: net.switchport: 14
smm02: net.bootable:
smm02: net.hwaddr:
smm02: net.ipv4_gateway:
smm02: net.switch:
smm02: net.switchport:
smm03: net.bootable:
smm03: net.hwaddr:
smm03: net.ipv4_gateway:
smm03: net.switch:
smm03: net.switchport:
[root@base ~]# nodeattrib smm enclosure
smm01: enclosure.bay:
smm01: enclosure.extends:
smm01: enclosure.manager:
smm02: enclosure.bay:
smm02: enclosure.extends: smm01
smm02: enclosure.manager:
smm03: enclosure.bay:
smm03: enclosure.extends: smm02
smm03: enclosure.manager:

```

## SMM is discovery by the confluent service 
```
discovery of SMM, nodename would have been smm01"}
Apr 11 21:58:02 {"info": "Discovered smm02 (SMM)"}
Apr 11 21:58:15 {"info": "Discovered smm03 (SMM)"}
Apr 11 21:58:55 {"error": "Unexpected condition trying to reach switch \"switch1\" check trace log for more"}
Apr 11 21:59:00 {"error": "Attempt to discover SMM by switch, but chained topology or incorrect net attributes detected, which is not compatible with switch discovery of SMM, nodename would have been smm01"}
Apr 11 21:59:00 {"info": "Detected unknown SMM with hwaddr 08:94:ef:53:af:d4 at address fe80::a94:efff:fe53:afd4%ens8"}
Apr 11 21:59:05 {"info": "Discovered smm01 (SMM)"}
Apr 11 21:59:07 {"error": "Attempt to discover SMM by switch, but chained topology or incorrect net attributes detected, which is not compatible with switch discovery of SMM, nodename would have been smm01"}
Apr 11 22:00:23 {"info": "Discovered smm02 (SMM)"}
Apr 11 22:00:36 {"info": "Discovered smm03 (SMM)"}
```

## FAQ

###   if you take too much long time for the SMM discovery ,try to check with nodediscover list 

```
[root@mgt ~]# nodediscover list
           Node|          Model|         Serial|                                UUID|      Mac Address|        Type|                            Current IP Addresses
---------------|---------------|---------------|------------------------------------|-----------------|------------|------------------------------------------------
          smm01|               |               |3124fce3-e99d-e711-b274-a9e75359fdbb|08:94:ef:51:03:fe|  lenovo-smm|     172.30.101.131,fe80::a94:efff:fe51:3fe%ens8
          smm03|               |               |23e5da2c-04b1-e711-a5ea-e55989756955|08:94:ef:53:af:d4|  lenovo-smm|    172.30.101.133,fe80::a94:efff:fe53:afd4%ens8
            n02|     7X21CTO1WW|       J3005Y2X|ed19e1e6-2277-11e8-92f5-0a94ef572301|08:94:ef:57:22:ff|  lenovo-xcc|      172.29.101.2,fe80::a94:efff:fe57:22ff%ens8
            n03|     7X21CTO1WW|       J3005Y2V|7507848c-2277-11e8-8c6f-0a94ef5723dd|08:94:ef:57:23:db|  lenovo-xcc|      172.29.101.3,fe80::a94:efff:fe57:23db%ens8
            n01|     7X21CTO1WW|       J3005Y2W|8a53b15a-22a9-11e8-920e-0a94ef572419|08:94:ef:57:24:17|  lenovo-xcc|      172.29.101.1,fe80::a94:efff:fe57:2417%ens8
          smm02|               |               |2eb08e0a-9fca-e711-acb7-d6143f6377db|08:94:ef:57:41:9a|  lenovo-smm|    172.30.101.132,fe80::a94:efff:fe57:419a%ens8
               |               |               |                                    |a4:8c:db:96:b8:01|lenovo-switch|                                     172.30.50.1
[root@mgt ~]#


```

### want to make a fresh discovery  ,try with followign command 
```
[root@mgt confluent]# nodeattrib smm01-smm03 -c id.uuid pubkeys.tls_hardwaremanager; service confluent restart 


```

## trigger the nodediscovery again


```
nodediscover rescan
confetty set /networking/macs/rescan=start

```

## other reference is [here](http://taurus.labs.lenovo.com/users/documentation/chainedsmmdiscovery.html)

```
There are two strategies. The first is more resilient and easier, but requires confluent 1.8.0 together with SMM firmware 1.04.

Fully out of band discovery
The Ethernet switch must have LLDP enabled.
Confirm that you have confluent version 1.8.0, and that all SMMs will at least have firmware 1.04.
Set the net.switch and net.switchport attributes only on the SMM directly connected to a switch.
For other SMMs, set enclosure.extends attribute to a directly connected adjacent SMM. For example, with three SMMs, smm1 would have net attributes to describe connecting to switch, smm2 would have enclosure.extends==smm1, and smm3 would have enclosure.extends==smm2
It is not required to have net attributes defined for any of the nodes.
Discovery proceeds normally in accordance with the general documentation of discovery here.
```









