#  2018-01-16 Oceancat Management server  create with KVM 
---
### 1 : install the VM with minimal installation options 
### 2 : configure the yum repocitory , then yum groupinstall "Server with GUI" -y
```
mkdir /tmp/install
mount -o loop ./rhel-server-7.4-x86_64-dvd.iso  /tmp/install/
vi /etc/yum.repos.d/local.repo
yum groupinstall "Server with GUI" -y

```
example of yum repocitory configure
```
[root@base ~]# cat /etc/yum.repos.d/local.repo
[base]
name=rhels74
baseurl=file:///tmp/install/
enabled=1
gpgcheck=0

```
### 3 : boot the system,set hostname ,console settings as following
```
hostnamectl set-hostname oc1.cluster
getenforce  ===set to disable
systemctl status firewall
```
### 4 : disable the virbr0 
```
yum install *bin/virsh -y
virsh net-destroy default
virsh net-undefine default
```
### 5 : enable the "virsh console oc1 " function to the virtual machine 
```
[root@base ~]# cat /etc/sysconfig/grub
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
GRUB_DEFAULT=saved
GRUB_DISABLE_SUBMENU=true
GRUB_TERMINAL_OUTPUT="console"
GRUB_CMDLINE_LINUX="rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet console=ttyS0,115200n8r"
GRUB_DISABLE_RECOVERY="true"

vi /etc/sysconfig/grub
grub2-mkconfig -o /boot/grub2/grub.cfg
```
### 6 : enable the Gnome auto Login 
```
[root@base ~]# cat /etc/gdm/custom.conf
# GDM configuration storage

[daemon]
AutomaticLogin=root
AutomaticLoginEnable=True


[security]

[xdmcp]

[chooser]

[debug]
# Uncomment the line below to turn on debugging
#Enable=true


```
### 7: configure the network settings

```
nmcli connection add con-name eth0 ifname eth0 type ethernet autoconnect yes ip4 192.168.122.20/24
nmcli connection add con-name ens8 ifname ens8 type ethernet autoconnect yes ip4 172.20.0.1/16 ip4 172.29.0.1/16 ip4 172.30.0.1/16

```
 example of the output should look likes
```
[root@oc1 ~]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 52:00:00:74:11:11 brd ff:ff:ff:ff:ff:ff
    inet 192.168.122.20/24 brd 192.168.122.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::aff:6bee:7ce3:d24b/64 scope link
       valid_lft forever preferred_lft forever
3: ens8: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN qlen 1000
    link/ether 90:e2:ba:78:f5:55 brd ff:ff:ff:ff:ff:ff
    inet 172.20.0.1/16 brd 172.20.255.255 scope global ens8
       valid_lft forever preferred_lft forever
    inet 172.29.0.1/16 brd 172.29.255.255 scope global ens8
       valid_lft forever preferred_lft forever
    inet 172.30.0.1/16 brd 172.30.255.255 scope global ens8
       valid_lft forever preferred_lft forever
    inet6 fe80::ad3f:8620:5ed9:ac25/64 scope link tentative
       valid_lft forever preferred_lft forever

```
### 8 xCAT installations
[Lenovo xCAT 17E link is ](https://hpc.lenovo.com/downloads/latest/xcat-2.13.7.lenovo2_confluent-1.7.2_lenovo-confluent-0.7.1-el7.tar.bz2https://hpc.lenovo.com/downloads/latest/xcat-2.13.7.lenovo2_confluent-1.7.2_lenovo-confluent-0.7.1-el7.tar.bz2)
```
[root@oc1 ~]# tar  jxvf xcat-2.13.7.lenovo2_confluent-1.7.2_lenovo-confluent-0.7.1-el7.tar.bz2
[root@oc1 lenovo-hpc-el7]# bash mklocalrepo.sh
[root@oc1 lenovo-hpc-el7]# cat /etc/yum.repos.d/
lenovo-hpc.repo  local.repo       redhat.repo
[root@oc1 lenovo-hpc-el7]# cat /etc/yum.repos.d/lenovo-hpc.repo
[lenovo-hpc]
name=Lenovo recommended packages for HPC
baseurl=file:///root/lenovo-hpc-el7
enabled=1
gpgcheck=1
gpgkey=file:///root/lenovo-hpc-el7/lenovohpckey.pub
[root@oc1 lenovo-hpc-el7]#



```
start to install the xCAT and confluent packages

```
yum install xCAT.x86_64 lenovo-confluent confluent_* -y
[root@oc1 ~]# source /etc/profile.d/xcat.sh
[root@oc1 ~]# source /etc/profile.d/confluent_env.sh

```
verify the installations is ok or not 
```
[root@oc1 ~]# tabdump site
#key,value,comments,disable
"blademaxp","64",,
"domain","cluster",,
"fsptimeout","0",,
"installdir","/install",,
"ipmimaxp","64",,
"ipmiretries","3",,
"ipmitimeout","2",,
"consoleondemand","no",,
"master","192.168.122.20",,
"nameservers","192.168.122.20",,
"maxssh","8",,
"ppcmaxp","64",,
"ppcretry","3",,
"ppctimeout","0",,
"powerinterval","0",,
"syspowerinterval","0",,
"sharedtftp","1",,
"SNsyncfiledir","/var/xcat/syncfiles",,
"nodesyncfiledir","/var/xcat/node/syncfiles",,
"tftpdir","/tftpboot",,
"xcatdport","3001",,
"xcatiport","3002",,
"xcatconfdir","/etc/xcat",,
"timezone","US/Eastern",,
"useNmapfromMN","no",,
"enableASMI","no",,
"db2installloc","/mntdb2",,
"databaseloc","/var/lib",,
"sshbetweennodes","ALLGROUPS",,
"dnshandler","ddns",,
"vsftp","n",,
"cleanupxcatpost","no",,
"dhcplease","43200",,
"auditnosyslog","0",,
"xcatsslversion","TLSv1",,
"auditskipcmds","ALL",,

```

### 9 : restore the default tables settings (very important to all of us)
```
[root@oc1 ~]# cd /opt/xcat/share/xcat/templates/e1350/
[root@oc1 e1350]# for a in *csv; do tabrestore $a; echo $a; done
chain.csv
hosts.csv
ipmi.csv
mp.csv
nodehm.csv
nodepos.csv
noderes.csv
nodetype.csv
passwd.csv
servicenode.csv
switch.csv
[root@oc1 e1350]#cd

```
### 10 : build the osimage for future use
```
[root@oc1 ~]# copycds rhel-server-7.4-x86_64-dvd.iso
Copying media to /install/rhels7.4/x86_64
Media copy operation successful
[root@oc1 ~]# lsdef -t osimage
rhels7.4-x86_64-install-compute  (osimage)
rhels7.4-x86_64-install-service  (osimage)
rhels7.4-x86_64-netboot-compute  (osimage)
rhels7.4-x86_64-stateful-mgmtnode  (osimage)
rhels7.4-x86_64-statelite-compute  (osimage)
```

### 11 : xCAT site Table configure example
```
[root@oc1 ~]# chtab key=domain site.value=cluster
[root@oc1 ~]# chtab key=dhcpinterfaces site.value=ens8
[root@oc1 ~]# chtab key=nameservers site.value=172.20.0.1
[root@oc1 ~]# chtab key=master site.value=oc1

```
site table output should look like as

```
[root@oc1 ~]# tabdump site
#key,value,comments,disable
"blademaxp","64",,
"domain","cluster",,
"fsptimeout","0",,
"installdir","/install",,
"ipmimaxp","64",,
"ipmiretries","3",,
"ipmitimeout","2",,
"consoleondemand","no",,
"master","oc1",,
"nameservers","172.20.0.1",,
"maxssh","8",,
"ppcmaxp","64",,
"ppcretry","3",,
"ppctimeout","0",,
"powerinterval","0",,
"syspowerinterval","0",,
"sharedtftp","1",,
"SNsyncfiledir","/var/xcat/syncfiles",,
"nodesyncfiledir","/var/xcat/node/syncfiles",,
"tftpdir","/tftpboot",,
"xcatdport","3001",,
"xcatiport","3002",,
"xcatconfdir","/etc/xcat",,
"timezone","US/Eastern",,
"useNmapfromMN","no",,
"enableASMI","no",,
"db2installloc","/mntdb2",,
"databaseloc","/var/lib",,
"sshbetweennodes","ALLGROUPS",,
"dnshandler","ddns",,
"vsftp","n",,
"cleanupxcatpost","no",,
"dhcplease","43200",,
"auditnosyslog","0",,
"xcatsslversion","TLSv1",,
"auditskipcmds","ALL",,
"dhcpinterfaces","ens8",,


```
#####  check the different output of the site table in preview installation check  and after configure 

### 12 : xCAT networks Table configure example
```
[root@oc1 ~]# chtab net=172.20.0.0 networks.dynamicrange=172.20.255.1-172.20.255.254 networks.netname="data"
[root@oc1 ~]# chtab -d net=192.168.122.0  networks

[root@oc1 ~]# chtab net=172.29.0.0 networks.netname="bmc-network"
[root@oc1 ~]# chtab net=172.30.0.0 networks.netname="out-band"



```
 example of the default output should look like as :
```
[root@oc1 ~]# tabdump networks
#netname,net,mask,mgtifname,gateway,dhcpserver,tftpserver,nameservers,ntpservers,logservers,dynamicrange,staticrange,staticrangeincrement,nodehostname,ddnsdomain,vlanid,domain,mtu,comments,disable
"data","172.20.0.0","255.255.0.0","ens8","<xcatmaster>",,"<xcatmaster>",,,,"172.20.255.1-172.20.255.254",,,,,,,"1500",,
"bmc-network","172.29.0.0","255.255.0.0","ens8","<xcatmaster>",,"<xcatmaster>",,,,,,,,,,,"1500",,
"out-band","172.30.0.0","255.255.0.0","ens8","<xcatmaster>",,"<xcatmaster>",,,,,,,,,,,"1500",,

```



### 13 : xCAT nodehm  Table configure example
```
[root@oc1 ~]# chtab node=compute nodehm.serialport=0 nodehm.serialspeed=115200 nodehm.serialflow=hard
[root@oc1 ~]# tabdump nodehm
#node,power,mgt,cons,termserver,termport,conserver,serialport,serialspeed,serialflow,getmac,cmdmapping,consoleondemand,comments,disable
"ipmi",,"ipmi",,,,,,,,,,,,
"blade",,"blade",,,,,,,,,,,,
"cyclades",,,"cyclades",,,,,,,,,,,
"mrv",,,"mrv",,,,,,,,,,,
"x3250",,"ipmi","ipmi",,,,"0","115200",,,,,,
"x3550",,"ipmi","ipmi",,,,"0","115200",,,,,,
"x3650",,"ipmi","ipmi",,,,"0","115200",,,,,,
"dx360",,"ipmi","ipmi",,,,"0","115200",,,,,,
"x220",,"ipmi","ipmi",,,,"0","115200",,,,,,
"x240",,"ipmi","ipmi",,,,"0","115200",,,,,,
"x440",,"ipmi","ipmi",,,,"0","115200",,,,,,
"compute",,,,,,,"0","115200","hard",,,,,
[root@oc1 ~]#


```

### 14 : xCAT nodetype Table configure example



```
[root@oc1 ~]# chtab node=compute nodetype.os=rhels7.4 nodetype.arch=x86_64 nodetype.Profile=compute
[root@oc1 ~]# tabdump nodetype
#node,os,arch,profile,provmethod,supportedarchs,nodetype,comments,disable
"compute","rhels7.4","x86_64","compute",,,,,
"x3250",,,,,,"osi",,
"x3550",,,,,,"osi",,
"x3650",,,,,,"osi",,
"dx360",,,,,,"osi",,
"x220",,,,,,"mp",,
"x240",,,,,,"mp",,
"x440",,,,,,"mp",,
[root@oc1 ~]#




```
### 15 : xCAT noderes Table configure example

```
[root@oc1 ~]# chtab node=compute noderes.netboot=xnba noderes.nfsserver=172.20.0.1 noderes.installnic=mac noderes.primarynic=mac
[root@oc1 ~]# tabdump noderes
#node,servicenode,netboot,tftpserver,tftpdir,nfsserver,monserver,nfsdir,installnic,primarynic,discoverynics,cmdinterface,xcatmaster,current_osimage,next_osimage,nimserver,routenames,nameservers,proxydhcp,syslog,comments,disable
"compute",,"xnba",,,"172.20.0.1",,,"mac","mac",,,,,,,,,,,,
```
### 16 update the  hosts / ipmi / switch  / switches  Tables to fit the OceanCat Full rack build 
#### check the node defined groups  with the hosts related inforomation 
```

[root@oc1 ~]# tabdump hosts | grep -E 'bmcsw|switch|72node|72bmc'
"72bmcperrack","|\D+(\d+).*$|172.29.(101+(($1-1)/72)).(($1-1)%72+1)|",,,,
"72nodeperrack","|\D+(\d+).*$|172.20.(101+(($1-1)/72)).(($1-1)%72+1)|",,,,
"switch","|\D+(\d+).*$|172.30.50.($1+0)|",,,,
"bmcsw","|\D+(\d+).*$|172.30.50.($1+50)|",,,,
"bigswitch","|\D+(\d+).*$|172.30.80.($1+0)|",,,,

```

#### set the ipmi tables to chand the suffix from bmc to xcc 

```
[root@oc1 ~]# chtab node=ipmi ipmi.bmc='|(.*)|($1)-xcc|'
[root@oc1 ~]# tabdump ipmi
#node,bmc,bmcport,taggedvlan,bmcid,username,password,comments,disable
"ipmi","|(.*)|($1)-xcc|",,,,,,,

```
#### switch community strings settings in SNMPV1 version (default settings)
```
[root@oc1 ~]# chtab switch=switch switches.password=RO

[root@oc1 ~]# chtab switch=bmcsw switches.password=RO
[root@oc1 ~]# tabdump switches
#switch,snmpversion,username,password,privacy,auth,linkports,sshusername,sshpassword,protocol,switchtype,comments,disable
"switch",,,"RO",,,,,,,,,
"bmcsw",,,"RO",,,,,,,,,

```
##### use the snmpwalk to check the switches work as expected 
#####  Example: 
```
    #get sysDescr.0";
    my $ccmd = "snmpwalk -Os -v1 -c $community $ip 1.3.6.1.2.1.1.1";
    #get ipNetToMediaPhysAddress;
    my $ccmd = "snmpwalk -Os -v1 -c $community $ip 1.3.6.1.2.1.4.22.1.2 | grep $ip";
    #get sysName info;
    my $ccmd = "snmpwalk -Os -v1 -c $community $ip 1.3.6.1.2.1.1.5";


```
#### switch tables 

```
[root@oc1 ~]# tabdump switch | grep 36
"36perswitch","|\D+(\d+).*$|switch(($1-1)/36+1)|","|\D+(\d+).*$|(($1-1)%36+1)|",,,,
"36bmcpersw","|\D+(\d+).*$|bmcsw(($1-1)/36+1)|","|\D+(\d+).*$|(($1-1)%36+1)|",,,,

```

### 17 : backup the default tables for future use (/etc/xcat/ is the default location for store the tables)
```
[root@oc1 ~]# dumpxCATdb -p /root/default_without_node_xCAT_Table
 Creating /root/default_without_node_xCAT_Table for database dump
Backup Complete.
[root@oc1 ~]# ls /root/default_without_node_xCAT_Table/
bootparams.csv     hosts.csv         kvm_masterdata.csv  monsetting.csv  nodelist.csv        osimage.csv      ppcdirect.csv    statelite.csv  vmmaster.csv
boottarget.csv     hwinv.csv         kvm_nodedata.csv    mpa.csv         nodepos.csv         passwd.csv       ppchcp.csv       storage.csv    vpd.csv
cfgmgt.csv         hypervisor.csv    linuximage.csv      mp.csv          noderes.csv         pdu.csv          prescripts.csv   switch.csv     websrv.csv
chain.csv          ipmi.csv          litefile.csv        networks.csv    nodetype.csv        pduoutlet.csv    prodkey.csv      switches.csv   winimage.csv
deps.csv           iscsi.csv         litetree.csv        nics.csv        notification.csv    performance.csv  rack.csv         taskstate.csv  zone.csv
discoverydata.csv  kitcomponent.csv  mac.csv             nimimage.csv    openbmc.csv         policy.csv       routes.csv       token.csv      zvm.csv
domain.csv         kit.csv           mic.csv             nodegroup.csv   osdistro.csv        postscripts.csv  servicenode.csv  virtsd.csv
firmware.csv       kitrepo.csv       monitoring.csv      nodehm.csv      osdistroupdate.csv  ppc.csv          site.csv         vm.csv



[root@oc1 xcat]# ls
auditlog.sqlite       eventlog.sqlite      kvm_masterdata.sqlite  networks.sqlite      osdistro.sqlite        ppc.sqlite          taskstate.sqlite
......
```
---

##  Add OceanCat node , XCC , switches  for testing
```
[root@oc1 ~]# nodeadd node01-node72 groups=ipmi,36perswitch,72nodeperrack,compute,all,MFGxxxx,LeROMxxxx
[root@oc1 ~]# nodeadd node[01-72]-xcc groups=bmc,72bmcperrack,36bmcpersw
[root@oc1 ~]# nodeadd switch1-switch2 groups=switch
[root@oc1 ~]# nodeadd bmcsw1-bmcsw2 groups=bmcsw



```
###  update hosttables for the node requirement  
```
[root@oc1 ~]# tabdump hosts | grep -E '72bmc|72node|switch|bmcsw'
"72bmcperrack","|\D+(\d+).*$|172.29.(101+(($1-1)/72)).(($1-1)%72+1)|",,,,
"72nodeperrack","|\D+(\d+).*$|172.20.(101+(($1-1)/72)).(($1-1)%72+1)|",,,,
"switch","|\D+(\d+).*$|172.30.50.($1+0)|",,,,
"bmcsw","|\D+(\d+).*$|172.30.50.($1+50)|",,,,


[root@oc1 ~]# tabdump switch |grep 36
"36perswitch","|\D+(\d+).*$|switch(($1-1)/36+1)|","|\D+(\d+).*$|(($1-1)%36+1)|",,,,
"36bmcpersw","|\D+(\d+).*$|bmcsw(($1-1)/36+1)|","|\D+(\d+).*$|(($1-1)%36+1)|",,,,
[root@oc1 ~]#
	
```
###  Note :
#### 36bmcsw is use for zero power on ,and zero power on only support the XCC dedicated mode 

### here is the output for the node ,XCC and Switches       


```
check the node definition ,and check the bmc value ,switch,switchport values
[root@oc1 ~]# lsdef node01
Object name: node01
    arch=x86_64
    bmc=node01-xcc
    chain=runcmd=bmcsetup,shell
    groups=ipmi,36perswitch,72nodeperrack,compute,all,MFGxxxx,LeROMxxxx
    installnic=mac
    ip=172.20.101.1
    mgt=ipmi
    netboot=xnba
    nfsserver=172.20.0.1
    ondiscover=nodediscover
    os=rhels7.4
    postbootscripts=otherpkgs
    postscripts=syslog,remoteshell,syncfiles
    primarynic=mac
    profile=compute
    serialflow=hard
    serialport=0
    serialspeed=115200
    switch=switch1
    switchport=1


check the xcc definitions ,and check the IP,switch,siwtchport values

[root@oc1 ~]# lsdef node01-xcc
Object name: node01-xcc
    groups=bmc,72bmcperrack,36bmcpersw
    ip=172.29.101.1
    postbootscripts=otherpkgs
    postscripts=syslog,remoteshell,syncfiles
    switch=bmcsw1
    switchport=1

check the switch definitions ,and check the IP values

[root@oc1 ~]# lsdef switch1
Object name: switch1
    groups=switch
    ip=172.30.50.1
    postbootscripts=otherpkgs
    postscripts=syslog,remoteshell,syncfiles
[root@oc1 ~]# lsdef bmcsw1
Object name: bmcsw1
    groups=bmcsw
    ip=172.30.50.51
    postbootscripts=otherpkgs
    postscripts=syslog,remoteshell,syncfiles
[root@oc1 ~]# lsdef bmcsw2
Object name: bmcsw2
    groups=bmcsw
    ip=172.30.50.52
    postbootscripts=otherpkgs
    postscripts=syslog,remoteshell,syncfiles

```

---
### enable the confluent service 
```
[root@oc1 ~]# systemctl enable confluent
Created symlink from /etc/systemd/system/multi-user.target.wants/confluent.service to /usr/lib/systemd/system/confluent.service

[root@oc1 ~]# service confluent start
Starting confluent (via systemctl):                        [  OK  ]


[root@oc1 ~]#  confetty set /nodegroups/everything/attributes/current discovery.policy=open
discovery.policy="open"
nodes=[]
[root@oc1 ~]#  confetty create /nodegroups/switch
Created: switch
[root@oc1 ~]# confetty create /nodes/switch1 groups=switch
Created: switch1
[root@oc1 ~]#  confetty create /nodes/switch2 groups=switch
Created: switch2
[root@oc1 ~]#  confetty create /nodes/bmcsw1 groups=switch
Created: bmcsw1
[root@oc1 ~]#  confetty create /nodes/bmcsw2 groups=switch
Created: bmcsw2
[root@oc1 ~]# nodelist
bmcsw1
bmcsw2
switch1
switch2


[root@oc1 ~]# makeconfluentcfg all
[root@oc1 ~]# nodelist
bmcsw1
bmcsw2
node01
node02
node03
node04
node05
node06
...




```

### configure the swithc for SNMP V1 commnunity and IP settings for node discovery ,XCC autoconfigure with IP V6

```


```








###  setup name resolution related and other service 

```
[root@oc1 ~]# makehosts ipmi
[root@oc1 ~]# makehosts bmc
[root@oc1 ~]# makehosts switch
[root@oc1 ~]# makehosts bmcsw
[root@oc1 ~]# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
172.20.0.1      oc1 oc1.cluster mgt     mgt.cluster
172.20.101.1 node01 node01.cluster
172.20.101.2 node02 node02.cluster
172.20.101.3 node03 node03.cluster
172.20.101.4 node04 node04.cluster
172.20.101.5 node05 node05.cluster
...


   61  makehosts ipmi
   62  makehosts bmc
   63  makehosts switch
   64  makehosts bmcsw
   65  cat /etc/hosts
   66  makedns -n
   67  makedhcp -n
   68  service dhcpd restart
   69  history
[root@oc1 ~]# mknb x86_64
Creating genesis.fs.x86_64.gz in /tftpboot/xcat
[root@oc1 ~]#








```






## Add FPC (Fan Power Controller ) for testing

```



```





===

---


```

[root@oc1 ~]# lsdef node01-xcc
Object name: node01-xcc
    groups=bmc,72bmcperrack,36bmcpersw
    ip=172.29.101.1
    postbootscripts=otherpkgs
    postscripts=syslog,remoteshell,syncfiles
    switch=bmcsw1
    switchport=1
[root@oc1 ~]# chdef node01-xcc switch=switch1 switchport=37
1 object definitions have been created or modified.
[root@oc1 ~]# lsdef node01-xcc
Object name: node01-xcc
    groups=bmc,72bmcperrack,36bmcpersw
    ip=172.29.101.1
    postbootscripts=otherpkgs
    postscripts=syslog,remoteshell,syncfiles
    switch=switch1
    switchport=37
[root@oc1 ~]#
```

some test defined in xcat systems

```
[root@oc1 ~]# makeconfluentcfg bmc
[root@oc1 ~]# nodeattrib node01-xcc
node01-xcc: console.logging: full
node01-xcc: discovery.policy: open
node01-xcc: groups: bmc,72bmcperrack,36bmcpersw,everything
node01-xcc: net.switch: switch1
node01-xcc: net.switchport: 37
node01-xcc: secret.hardwaremanagementpassword: ********
node01-xcc: secret.hardwaremanagementuser: ********


###

```
[root@oc1 ~]# cat /var/log/confluent/events
Jan 17 11:56:54 {"error": "Timeout or bad SNMPv1 community string trying to reach switch 'switch2'"}
Jan 17 11:56:54 {"error": "Timeout or bad SNMPv1 community string trying to reach switch 'bmcsw1'"}
Jan 17 11:56:54 {"error": "Timeout or bad SNMPv1 community string trying to reach switch 'switch1'"}
Jan 17 11:56:54 {"error": "Timeout or bad SNMPv1 community string trying to reach switch 'bmcsw2'"}
Jan 17 11:56:54 {"info": "Detected unknown XCC with hwaddr 8c:0f:6f:7e:d5:61 at address fe80::8e0f:6fff:fe7e:d561%ens8"}
Jan 17 11:56:55 {"info": "Detected unknown XCC with hwaddr 8c:0f:6f:7e:d6:51 at address fe80::8e0f:6fff:fe7e:d651%ens8"}



RS G8000#show mac-address-table
Mac address Aging Time: 300

     MAC address     VLAN  Port     Trnk  State  Permanent
  -----------------  ----  -------  ----  -----  ---------
  8c:0f:6f:7e:d5:61     1  37              FWD
  8c:0f:6f:7e:d6:51     1  38              FWD
  90:e2:ba:78:f5:55     1  44              FWD


[root@oc1 ~]# snmpwalk -Os -v1 -c RO switch1 1.3.6.1.2.1.1.1
sysDescr.0 = STRING: IBM Networking Operating System RackSwitch G8000 (BW build)


```

```

