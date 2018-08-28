#  Lenovo LeSI rack solution AC power cycle Work Instruction 
#
## 0: clear all SEL log in XCC and in SMM
```
[root@mgt ~]# reventlog all clear
node06: SEL cleared
node01: SEL cleared
node04: SEL cleared
node03: SEL cleared
node02: SEL cleared
node08: SEL cleared
node07: SEL cleared
node05: SEL cleared
[root@mgt ~]# reventlog smm clear
smm02: SEL cleared
smm01: SEL cleared


```
## 1: power all node off with ipmi command (node DC off )
```
[root@mgt ~]# rpower all off
node04: off
node03: off
node02: off
node07: off
node08: off
node01: off
node06: off
node05: off
```
##  2: wait 1 minutes ,disconnect the PDU by turn off the switch for whole rack ( AC off )
##
##  3: wait for 3-5 minutes ,turn on the switch to PDU (AC on ) for whole rack 
##
##  4: wait the smm and XCC is up and running 
```
[root@mgt ~]# pping xcc
node01-xcc: ping
node02-xcc: ping
node03-xcc: ping
node04-xcc: ping
node05-xcc: ping
node06-xcc: ping
node07-xcc: ping
node08-xcc: ping
```
## 5: power all node on (DC on)

```
[root@mgt ~]# rpower all on
node04: on
node05: on
node06: on
node01: on
node03: on
node02: on
node07: on
node08: on

```
## 6:  check the node state 
```
[root@mgt ~]# nodestat all
node01: rdp,sshd
node02: rdp,sshd
node03: rdp,sshd
node04: rdp,sshd
node05: rdp,sshd
node06: rdp,sshd
node07: rdp,sshd
node08: rdp,sshd


```
## 7: check the SEL log for XCC and SMM
```
[root@mgt ~]# reventlog smm | grep -E "Error|error|Fail|fail|Corruption|corruption|ECC"
# should be no output from SMM SEL LOG
[root@mgt ~]# reventlog all | grep -E "Error|error|Fail|fail|Corruption|corruption|ECC"
# should be no output from XCC SEL LOG 


```

## step 1 to step 7 is call a AC Power cycle for rack ,repeat the AC power cycle for rack 5 times 
