#
 drive disk driver load with netboot image 


```
[root@mgt13 ~]#ls lnvgy_dd_sraidmr_7.700.26.00-1_rhel7_x86-64.tgz


[root@mgt13 ~]#ls lnvgy_dd_sraidmr_7.700.26.00-1_rhel7_x86-64.tgz
lnvgy_dd_sraidmr_7.700.26.00-1_rhel7_x86-64.tgz
[root@mgt13 ~]#



```
### put the driver to all node 

```
 1004  tar xzvf lnvgy_dd_sraidmr_7.700.26.00-1_rhel7_x86-64.tgz
 1005  pscp RPMS/redhat-release-server-7.3/kmod-megaraid_sas-07.700.26.00_el7.3-1.x86_64.rpm all:/root/
 1006  psh all rpm -ivh kmod-megaraid_sas-07.700.26.00_el7.3-1.x86_64.rpm
 psh all modprobe  megaraid_sas


```




### install the rpm package to all node 

```
pscp storcli-1.14.12-1.noarch.rpm  all:/root    

psh all "rpm -ivh /root/storcli-1.14.12-1.noarch.rpm"

```



###  check the node slotid and number ,remove the JBOD flags
```
[root@mgt13 ~]#psh all "/opt/MegaRAID/storcli/storcli64 /c0 show | grep ST3" | xcoll
====================================
login,nia-sn01,nia-gpfssrv01,nia-serv02
====================================
69:0      8 JBOD  -  278.464 GB SAS  HDD N   N  512B ST300MM0048      U
69:1      9 JBOD  -  278.464 GB SAS  HDD N   N  512B ST300MM0048      U

====================================
nia-serv04,nia-sch01,nia-gpfssrv02,nia-xcat01,nia-serv03,nia-gw01,nia-serv01
====================================
69:0      9 JBOD  -  278.464 GB SAS  HDD N   N  512B ST300MM0048      U
69:1      8 JBOD  -  278.464 GB SAS  HDD N   N  512B ST300MM0048      U

```
### remove the jbod functions

```
[root@nia-login01 ~]# /opt/MegaRAID/storcli/storcli64 -h |grep jbod
storcli /cx[/ex]/sx set jbod
storcli /cx show jbod
storcli /cx set jbod=<on|off>


[root@mgt13 ~]#psh all " /opt/MegaRAID/storcli/storcli64 /c0 show jbod" | xcoll
====================================
compute
====================================
Controller = 0
Status = Success
Description = None


Controller Properties :
=====================

----------------
Ctrl_Prop Value
----------------
JBOD      ON
----------------


[root@mgt13 ~]#psh all " /opt/MegaRAID/storcli/storcli64 /c0 set  jbod=off" | xcoll
====================================
compute
====================================
Controller = 0
Status = Success
Description = None


Controller Properties :
=====================

----------------
Ctrl_Prop Value
----------------
JBOD      OFF
----------------



[root@mgt13 ~]#psh all " /opt/MegaRAID/storcli/storcli64 /c0 show jbod" | xcoll
====================================
compute
====================================
Controller = 0
Status = Success
Description = None


Controller Properties :
=====================

----------------
Ctrl_Prop Value
----------------
JBOD      OFF
----------------


```
### create the raid for all node

```
[root@nia-login01 ~]# /opt/MegaRAID/storcli/storcli64 /c0 add vd type=raid1 size=all names=raid1 drives=69:0-1
Controller = 0
Status = Success
Description = Add VD Succeeded

[root@nia-login01 ~]# fdisk -l

Disk /dev/sda: 299.0 GB, 298999349248 bytes, 583983104 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 65536 bytes / 65536 bytes

[root@nia-login01 ~]# exit
logout
Connection to nia-login01 closed.
[root@mgt13 ~]#psh all,-nia-login01 "/opt/MegaRAID/storcli/storcli64 /c0 add vd type=raid1 size=all names=raid1 drives=69:0-1"

[root@mgt13 ~]#psh all fdisk -l | xcoll
====================================
compute
====================================

Disk /dev/sda: 299.0 GB, 298999349248 bytes, 583983104 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 65536 bytes / 65536 bytes




```
#### start to provisioning the OS 

```
[root@mgt13 ~]#nodeset all osimage=rhels7.3-x86_64-install-compute
The driver update disk:/install/driverdisk/rhels7.3/x86_64/megaraid_sas-07.700.26.00_el7.3-1.x86_64.iso have been injected to initrd.
nia-gpfssrv01: install rhels7.3-x86_64-compute
nia-gpfssrv02: install rhels7.3-x86_64-compute
nia-gw01: install rhels7.3-x86_64-compute
nia-login01: install rhels7.3-x86_64-compute
nia-login02: install rhels7.3-x86_64-compute
nia-login03: install rhels7.3-x86_64-compute
nia-login04: install rhels7.3-x86_64-compute
nia-sch01: install rhels7.3-x86_64-compute
nia-serv01: install rhels7.3-x86_64-compute
nia-serv02: install rhels7.3-x86_64-compute
nia-serv03: install rhels7.3-x86_64-compute
nia-serv04: install rhels7.3-x86_64-compute
nia-sn01: install rhels7.3-x86_64-compute
nia-xcat01: install rhels7.3-x86_64-compute
[root@mgt13 ~]#rsetboot all net -u
nia-serv04: Network
nia-login03: Network
nia-login02: Network
nia-sch01: Network
nia-gw01: Network
nia-serv01: Network
nia-login04: Network
nia-serv03: Network
nia-serv02: Network
nia-xcat01: Network
nia-login01: Network
nia-gpfssrv01: Network
nia-gpfssrv02: Network
nia-sn01: Network
[root@mgt13 ~]#rpower all reset
nia-login01: reset
nia-sn01: reset
nia-serv02: reset
nia-gpfssrv01: reset
nia-serv03: reset
nia-gw01: reset
nia-gpfssrv02: reset
nia-serv01: reset
nia-serv04: reset
nia-login04: reset
nia-login02: reset
nia-xcat01: reset
nia-login03: reset
nia-sch01: reset
[root@mgt13 ~]#

```
