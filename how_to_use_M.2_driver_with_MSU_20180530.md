# NVME RAID CARD SETTINGS

## introduce by LeROM LeROM201700655
### Basic INFO for the systems
####  key parts ==   B11V	-SB- ThinkSystem M.2 5100 480GB SATA 6Gbps Non-Hot Swap SSD
```
For use in the SR630 and SR850:

    The use of the 480GB drive requires the ThinkSystem M.2 with Mirroring Enablement Kit, 7Y37A01093. Not supported with ThinkSystem M.2 Enablement Kit, 7Y37A01092.
    
    
    AUMV	ThinkSystem M.2 with Mirroring Enablement Kit

"The M.2 adapters are also referred to as enablement kits"
```
![M.2 SSD driver ](https://lenovopress.com/assets/images/LP0645/M_2%20Adapter.jpg)
```
ThinkSystem SR630
J30097MV


	Server_Arema
7X02CTO1WW	ThinkSystem SR630 - 3yr Warranty
AUWC	ThinkSystem SR530/SR570/SR630 x8/x16 PCIe LP+LP Riser 1 Kit
B0MJ	Feature Enable TPM 1.2
AUPW	ThinkSystem XClarity Controller Standard to Enterprise Upgrade
ATRP	Mellanox ConnectX-4 2x100GbE/EDR IB QSFP28 VPI Adapter
AUKX	ThinkSystem Intel X710-DA2 PCIe 10Gb 2-Port SFP+ Ethernet Adapter
5053	SFP+ SR Transceiver
"AUMV	ThinkSystem M.2 with Mirroring Enablement Kit"
AVW8	ThinkSystem 550W (230V/115V) Platinum Hot-Swap Power Supply
5977	Select Storage devices - no configured RAID required
AXCA	ThinkSystem Toolless Slide Rail
AUKG	ThinkSystem 1Gb 2-port RJ45 LOM
AUWQ	Lenovo ThinkSystem 1U LP+LP BF Riser Bracket
AUW0	ThinkSystem SR630 2.5 Chassis with 8 Bays
AWDU	Intel Xeon Gold 5115 10C 85W 2.4GHz Processor
"B11V	-SB- ThinkSystem M.2 5100 480GB SATA 6Gbps Non-Hot Swap SSD"
AUNC	ThinkSystem 16GB TruDDR4 2666 MHz (2Rx8 1.2V) RDIMM
6311	2.8m, 10A/100-250V, C13 to C14 Jumper Cord
2305	Integration 1U Component
......

```


### check the tools MD5

```
[root@node06 ~]# md5sum MSU-4.1.10.2040-1.x86_64.rpm
c62c994d4a5b44b274d82ba7d1da1281  MSU-4.1.10.2040-1.x86_64.rpm
[root@node06 ~]#


```
### install the rpm packages 


```

[root@node06 ~]# rpm -ivh M
MegaSAS.log                   MSU-4.1.10.2040-1.x86_64.rpm
[root@node06 ~]# rpm -ivh MSU-4.1.10.2040-1.x86_64.rpm
Preparing...                          ################################# [100%]
Updating / installing...
   1:MSU-4.1.10.2040-1                ################################# [100%]
Starting Marvell Storage Utility Web Service.
Starting Marvell Storage Event Agent.
[root@node06 ~]#

```
### check RAID settings 

```
[root@node06 ~]# /opt/marvell/storage/cli/mvcli info -o vd|more
SG driver version 3.5.36.

Virtual Disk Information
-------------------------
id:                  0
name:                VD_R1_1
status:              functional
Stripe size:         64
RAID mode:           RAID1
Cache mode:          Not Support
size:                457798 M
BGA status:          not running
Block ids:           0 4
# of PDs:            2
PD RAID setup:       0 1
Running OS:          no
VD status:           optimal

Total # of VD:       1


```

### other command usage example 

```
 /opt/marvell/storage/cli/mvcli info -o pd -i 0             "check the physical driver infor by the ID "
 /opt/marvell/storage/cli/mvcli info -o hba                 "show BHA informations "
 /opt/marvell/storage/cli/mvcli adapter                     "check the avaiable adapters "
 /opt/marvell/storage/cli/mvcli smart -p 0                  "check driver SMART  errors "
 
```
## create RAID (not verify yet )
```
   /opt/marvell/storage/cli/mvcli smart -p 0  create -o vd -r1 -n "MyVirtualDisk" -d 0,1

```
### read the driver informations 


```
[root@node06 ~]# /opt/marvell/storage/cli/mvcli info -o pd
SG driver version 3.5.36.

Physical Disk Information
----------------------------
Adapter:             0
PD ID:               0
Type:                SATA PD
Linked at:           HBA port 0
Size:                468851544 K
Write cache:         not supported
SMART:               supported (on)
NCQ:                 supported (on)
48 bits LBA:         supported
supported speed:     1.5 3 6 Gb/s
Current speed:       6 Gb/s
model:               MTFDDAV480TCB-1AR1ZA
FRU:                  01KR465
MFA:                 LEN
8S l2 PN:            SSS7A06699
8S SN:               1C5830EA
Serial:              1C5830EA
Firmware version:        MD44
Locate LED status:   Not Support
Running OS:          no
SSD Type:            SSD
WWN:                 500a07511c5830ea
PD status:           online
block ids:           0
associated VDs:      0
PD valid size:       0 K


Adapter:             0
PD ID:               1
Type:                SATA PD
Linked at:           HBA port 1
Size:                468851544 K
Write cache:         not supported
SMART:               supported (on)
NCQ:                 supported (on)
48 bits LBA:         supported
supported speed:     1.5 3 6 Gb/s
Current speed:       6 Gb/s
model:               MTFDDAV480TCB-1AR1ZA
FRU:                  01KR465
MFA:                 LEN
8S l2 PN:            SSS7A06699
8S SN:               1C58308F
Serial:              1C58308F
Firmware version:        MD44
Locate LED status:   Not Support
Running OS:          no
SSD Type:            SSD
WWN:                 500a07511c58308f
PD status:           online
block ids:           4
associated VDs:      0
PD valid size:       0 K


Total # of PD:       2





[root@node06 ~]# /opt/marvell/storage/cli/mvcli info -o hba
SG driver version 3.5.36.

Adapter ID:                          0
Product:                             1b4b-9230
Sub Product:                         1d49-300
Chip revision:                       A1
slot number:                         0
Max PCIe speed:                      5Gb/s
Current PCIe speed:                  5Gb/s
Max PCIe link:                       2
Current PCIe link:                   2
Firmware version:                    2.3.10.1088
Boot loader version:                 2.1.0.1009
# of ports:                          3
Buzzer:                              Not supported
Supported port type:                 SATA
Supported RAID mode:                 RAID0 RAID1
Maximum disk in one VD:              2
PM:                                  Not supported
Expander:                            Not supported
Rebuild:                             Supported
Background init:                     Not supported
Sync:                                Supported
Migrate:                             Not supported
Media patrol:                        Not supported
Foreground init:                     Not supported
Copy back:                           Not supported
Maximum supported disk:              2
Maximum supported VD:                2
Max total blocks:                    128
Features:                            rebuild,synchronize
Advanced features:                   event sense code,config in flash,multi VD,spc 4,image health,timer,smart poll,bga rate,spare,ata pass through,access register,oem data
Advanced features 2:                 scsi pass through,flash
Max buffer size:                     3
Stripe size supported:               32K 64K
Image health:                        Healthy
Autoload image health:               Healthy
Boot loader image health:            Healthy
Firmware image health:               Healthy
Boot ROM image health:               Healthy
HBA info image health:               Healthy

SerialNo:                            W1ZS83R00SM
ModelNumber:                         M.2 + Mirroring Kit
PartNumber:                          SR17A04514
WWN:                                 19a2aef5e92fe81188018fb1b5fb61e7
SKU:                                 01KN512


[root@node06 ~]# /opt/marvell/storage/cli/mvcli adapter
SG driver version 3.5.36.
Total number of adapters: 1
Current default adapter ID for CLI commands: 0



[root@node06 ~]# /opt/marvell/storage/cli/mvcli smart -p 0
SG driver version 3.5.36.
SMART STATUS RETURN: OK.

Smart Info
ID      Attribute Name          RawValue        Status
01      Read Error Rate         000000000000    OK
05      Reallocated Sectors     000000000000    OK
09      Power-On Hours Count    00000000004A    OK
0C      Power Cycle Count       000000000034    OK
AA      Grown Bad Blocks        000000000000    OK
AB      Program Fail Count(Total)       000000000000    OK
AC      Erase Fail Count(Total) 000000000000    OK
AE      Unexpected Power Loss Count     00000000002D    OK
C0      Unsafe Shutdown Count   00000000002D    OK
B8      End-to-End Data Errors Correcte 000000000000    OK
BB      Uncorrectable Error Count       000000000000    OK
BC      Command Timeout         00000000004B    OK
BE      Airflow Temperature     000000000035    OK
C3      ECC Error Rate          000000000000    OK
C4      Reallocation count      000000000000    OK
C6      Uncorrectable Sector Count      000000000000    OK
C7      CRC Error Count         000000000000    OK
AD      Average Program/Erase Count     000000000000    OK
F1      Total Host Written      000000001C86    OK
F2      Total Host Read         00000000DA1F    OK
C5      Current Pending Sector Count    000000000000    OK
B1      Wear Leveling Count     000000000000    OK
C2      SSD Temperature         00000000003F    OK



```


### interactive shell with mvcli 

```
[root@node06 ~]# /opt/marvell/storage/cli/mvcli
SG driver version 3.5.36.
CLI Version: 4.1.10.36   RaidAPI Version: 2.3.10.1071
Welcome to RAID Command Line Interface.

> help

Legend:
  [options] - the options within [] are optional.
  <x|y|z>   - choose one of the x, y or z.
  [<x|y|z>] - choose none or one of the x, y or z.

Abbreviation:
    VD  - Virtual Disk,   Array  - Disk Array
    PD  - Physical Disk,  BGA - BackGround Activity

Type '-output [filename]' to output to a file.
Type 'help' to display this page.
Type 'help command' to display the help page of 'command'.
Type 'command -h' to display help for 'command'.

Command name is not case sensitive and may be abbreviated if the
abbreviation is unique. Most commands support both short (-) and
long (--) options.Long option names may be abbreviated if the abbreviation
is unique. A long option may take a parameter of the form '--arg=param'
or '--arg param'. Option name is case sensitive, option parameter is not.

COMMAND   BRIEF DESCRIPTION
-----------------------------------------------------------------
?            :Get brief help for all commands.
help         :Get brief help for all commands or detail help for one command.
assign       :Assign a disk as spare drive.
cc           :Start, stop, pause or resume VD Consistency Check.
rebuild      :Start, stop, pause, resume rebuilding VD.
smart        :Display the smart info of physical disk.
sat          :Send SCSI command.
flash        :Update, backup or erase flash image and erase hba or pd page.
enc          :Get enclosure, enclosure element or enclosure config information.
forceonline  :Forceonline the physical disk
adapter      :Default adapter the following CLI commands refers to.
create       :Create virtual disk.
delete       :Delete virtual disk or spare drive.
event        :Get events.
get          :Get configuration information of VD, PD, Array, HBA or Driver.
info         :Display adapter(hba), virtual disk(vd), disk array,
              physical disk(pd), Port multiplexer(pm), expander(exp),
              block disk(blk) or spare drive information.
set          :Set configuration parameters of VD, PD or HBA.
import       :Import a virtual disk.
locate       :Locate the specified PD.
report       :report a conflicted virtual disk to OS.
devmap       :Map device ID to device magic number in the OS.
> quit
[root@node06 ~]#


```


### 

## Reference Link 
[ThinkSystem M.2 Drives and M.2 Adapters](https://lenovopress.com/lp0769.pdf)
######
[ MSU : Marvell Storage Utility for Linux ](https://support.lenovo.com/us/zh/downloads/DS502620)

##
##
