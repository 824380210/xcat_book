# CNOS switches common configure task 
---

####  CNOS switch default ip is 192.168.50.50 for the management port 
####  CNOS default only support the SSH with user and password is admin/admin
#### default console port is 9600 N8R1
##  


```
witch> enable
Switch# configure device
Switch(config)#
Switch(config)# interface mgmt 0
Switch(config-if)# ip address <IPv4 address>/ <IPv4 network mask length>
Switch(config-if)# exit
Switch(config)# vrf context management
Switch(config-vrf)# ip route 0.0.0.0 0.0.0.0 <default gateway IPv4 address>
Switch(config-vrf)# exit

```
### update the CNOS 

```
Switch> enable
Switch# ping  <target  IPv4  address>  vrf management
Switch#  cp tftp tftp://<TFTP server address> /Switch-CNOS-10.3.1.0.imgs system-image all vrf management

Switch# reload
reboot system? (y/n) y
```
## check the update FW version
```
Switch> enable
Switch# display boot
```


### incomfing FW show 

```
[root@oc1 ~]# ssh admin@172.30.50.99
Password:
Last login: Thu Jan 25 08:26:32 2018

NOS 10.4.2.0 Lenovo ThinkSystem NE10032 RackSwitch, Jun 15 18:02:51 PDT 2017
NE10032>enable
NE10032#configure device
Enter configuration commands, one per line.  End with CNTL/Z.
NE10032(config)#interface mgmt 0
NE10032(config-if)#display boot

NE10032(config-if)#display boot
Current ZTP State: Enable
Current FLASH software:
  active image: version 10.4.2.0, downloaded 06:37:30 UTC Sat Oct 14 2017
  standby image: version unknown, downloaded unknown
  Grub: version 10.4.2.0, downloaded 06:37:30 UTC Sat Oct 14 2017
  BIOS: version ALPHA.5.33.0206B, release date 05/10/2017
  Secure Boot: Enabled
  ONIE: version unknown, downloaded unknown
Currently set to boot software active image
Current port mode: default mode

```

### check the tftp server is ping by the management port or not 
```
NE10032(config-if)#ping 172.30.0.1  vrf management
PING 172.30.0.1 (172.30.0.1) from 172.30.50.99 : 56(84) bytes of data.
64 bytes from 172.30.0.1: icmp_seq=1 ttl=64 time=0.217 ms
64 bytes from 172.30.0.1: icmp_seq=2 ttl=64 time=0.253 ms
```
### download the FW image to upload to update
```
[root@oc1 tftpboot]# md5sum lnvgy_fw_torsw_ne10032-cnos-10.6.1.0_anyos_noarch.zip
382865a81a447fc3d15140b3fbeb70d9  lnvgy_fw_torsw_ne10032-cnos-10.6.1.0_anyos_noarch.zip
[root@oc1 tftpboot]# unzip lnvgy_fw_torsw_ne10032-cnos-10.6.1.0_anyos_noarch.zip
Archive:  lnvgy_fw_torsw_ne10032-cnos-10.6.1.0_anyos_noarch.zip
  inflating: MIBs/BFD-STD-MIB.mib
...
  inflating: MIBs/UDP-MIB.mib
  inflating: MIBs/VRRP-MIB.mib
  inflating: NE10032-CNOS-10.6.1.0.imgs

```
### start to upload and flash
```
[root@oc1 tftpboot]# ll
total 361284
-rw-r--r-- 1 root root 183979708 Jan 26 09:32 lnvgy_fw_torsw_ne10032-cnos-10.6.1.0_anyos_noarch.zip
drwxr-xr-x 3 root root      4096 Jan 26 09:32 MIBs
-rw-r--r-- 1 root root 185930799 Dec 12 15:46 NE10032-CNOS-10.6.1.0.imgs
-rw-r--r-- 1 root root     26826 Jan 17 11:44 pxelinux.0
drwxr-xr-x 2 root root      4096 Jan 17 05:50 pxelinux.cfg
drwxr-xr-x 3 root root      4096 Jan 17 05:50 xcat



[root@oc1 tftpboot]# ssh admin@172.30.50.99
Password:
Last login: Fri Jan 26 05:57:26 2018 from 172.30.0.1

NOS 10.4.2.0 Lenovo ThinkSystem NE10032 RackSwitch, Jun 15 18:02:51 PDT 2017
NE10032>enable
NE10032#cp tftp tftp://172.30.0.1/NE10032-CNOS-10.6.1.0.imgs system-image all vrf management
Confirm download operation? (y/n) [n] y
Download in progress
.................................................................................................................................................................................
Copy Success

Install image...This takes about 90 seconds. Please wait
Creating system development key....
Creating system key....
Check image signature succeeded
Extracting image: 100%
Installing system image to slot 2:
Installing image: 100%
Extracting image: 100%
Installing grub:
Installing GRUB and secure shim boot loaders...
Create rescue mount
Make boot directory
Done
Boot image installation succeeded.
OS image installation succeeded.

Boot loader now contains Software Version 10.6.1.0
Standby image now contains Software Version 10.6.1.0
Switch is currently set to boot active image.
Do you want to change that to the standby image? (y/n) [n] y
Switch is to be booted with standby image.
NE10032#
NE10032#reload
WARNING: There is unsaved configuration!!!
reboot system? (y/n): y


```
###

```
NE10032#display boot
Current ZTP State: Enable
Current FLASH software:
  active image: version 10.6.1.0, downloaded 06:47:46 UTC Fri Jan 26 2018
  standby image: version 10.4.2.0, downloaded 06:37:30 UTC Sat Oct 14 2017
  Grub: version 10.6.1.0, downloaded 06:47:47 UTC Fri Jan 26 2018
  BIOS: version ALPHA.5.33.0206B, release date 05/10/2017
  Secure Boot: Enabled
  ONIE: version unknown, downloaded unknown
Currently set to boot software active image
Current port mode: default mode
Next boot port mode: default mode

Currently scheduled reboot time: none


```
### update the update the non-running bank image (standby image) 
#### same producre 
```
LenovoNE10032-001>en
LenovoNE10032-001#cp tftp tftp://172.30.0.1/NE10032-CNOS-10.6.1.0.imgs system-image all vrf management
Confirm download operation? (y/n) [n] y
Download in progress
.................................................................................................................................................................................
Copy Success

Install image...This takes about 90 seconds. Please wait
Check image signature succeeded
Extracting image: 100%
Installing system image to slot 1:
Installing image: 100%
Extracting image: 100%
Installing grub:
Boot image update not required: Skipping
Boot image installation succeeded.
OS image installation succeeded.

Boot loader now contains Software Version 10.6.1.0
Standby image now contains Software Version 10.6.1.0
Switch is currently set to boot active image.
Do you want to change that to the standby image? (y/n) [n] y
Switch is to be booted with standby image.
LenovoNE10032-001#save
Building configuration...
[OK]
LenovoNE10032-001#cp running-config startup-config
Building configuration...
[OK]
LenovoNE10032-001#reload
reboot system? (y/n): y
2018-01-26T15:30:36+00:00 LenovoNE10032-001(cnos:data) %IMISH-4-REBOOT: The system will be rebooted.


```


### snmp configure  

```
NE10032>enable
NE10032#configure device
Enter configuration commands, one per line.  End with CNTL/Z.
NE10032(config)#interface mgmt 0
NE10032(config-if)#ip address 172.30.55.1 255.255.0.0
NE10032(config-if)#end

NE10032#configure device
Enter configuration commands, one per line.  End with CNTL/Z.
NE10032(config)#snmp-server community RO group network-operator
NE10032(config)#snmp-server version v1v2v3
NE10032(config)#save
Building configuration...
[OK]
NE10032(config)#

```
### use snmpwalk to check the snmp settings

```
[root@oc1 ~]# ping -c2 172.30.55.1
PING 172.30.55.1 (172.30.55.1) 56(84) bytes of data.
64 bytes from 172.30.55.1: icmp_seq=1 ttl=64 time=0.465 ms
64 bytes from 172.30.55.1: icmp_seq=2 ttl=64 time=0.167 ms

--- 172.30.55.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1000ms
rtt min/avg/max/mdev = 0.167/0.316/0.465/0.149 ms


[root@oc1 ~]#  snmpwalk -Os -v1 -c RO 172.30.55.1  1.3.6.1.2.1.1.1
sysDescr.0 = STRING: Lenovo ThinkSystem NE10032 RackSwitch
[root@oc1 ~]#

```
### clear the switch configurations to the factory default 


```
NE10032#save ?
  erase     Destroys the configuration on persistent media
  file      Write to file
  memory    Write to NV memory
  terminal  Write to terminal
  <cr>

NE10032#save erase

```
### backup the configure file 

```
LenovoNE10032-001#cp startup-config scp
Enter vrf name [default]:management
Enter IP:172.30.0.1
Enter Username:root
Enter filename:myconfig
Enter timeout value 0..150 - 0 means default TCP timeout:3
root@172.30.0.1's password:
nosx.conf                                                                                                                  100% 1154     1.5MB/s   00:00
Copy Success
LenovoNE10032-001#

```
### odd issue here===

```
LenovoNE10032-001#cp startup-config scp scp://root@172.30.0.1/tmp/startup-config timeout 3 vrf management
root@172.30.0.1's password:
Error: No such file or directory




```


### specify boot image 


```
LenovoNE10032-001#configure device
Enter configuration commands, one per line.  End with CNTL/Z.
LenovoNE10032-001(config)#startup ?
  image      Configure system image
  zerotouch  Configure ZTP boot mode

LenovoNE10032-001(config)#startup image ?
  active      Active image
  onie-image  ONIE image
  standby     Standby image

LenovoNE10032-001(config)#startup image

```


### some wront informations


```
lenovoNE10032-001#display logging last 30

...

670 2018-01-26T14:39:16+00:00 lenovoNE10032-001(cnos:data) %LLI-4-DEVICE_REMOVED: [PLATFORM_MGR] PasZD_3m removed at port Ethernet1/ 2
671 2018-01-26T14:39:19+00:00 lenovoNE10032-001(cnos:data) %LLI-5-DEVICE_INSERTED: [PLATFORM_MGR] Ethernet1/ 2 Device Inserted
672 2018-01-26T14:39:19+00:00 lenovoNE10032-001(cnos:data) %LLI-5-DEVICE_INSTALLED: [PLATFORM_MGR] Ethernet1/ 2 PasZD_3m Installed
673 2018-01-26T14:39:19+00:00 lenovoNE10032-001(cnos:data) %LLI-5-DEVICE_ENABLE: [PLATFORM_MGR] PasZD_3m inserted at port Ethernet1/ 2 is Approved.


674 2018-01-26T14:39:29+00:00 lenovoNE10032-001(cnos:data) %LLI-4-DEVICE_REMOVED: [PLATFORM_MGR]        removed at port Ethernet1/ 3
675 2018-01-26T14:39:29+00:00 lenovoNE10032-001(cnos:data) %LLI-5-DEVICE_INSERTED: [PLATFORM_MGR] Ethernet1/ 3 Device Inserted
676 2018-01-26T14:39:29+00:00 lenovoNE10032-001(cnos:data) %LLI-2-ERROR_TYPE: [PLATFORM_MGR] Ethernet1/ 3 Wrong Transceiver Type

```
