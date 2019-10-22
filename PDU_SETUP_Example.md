# pdu test example for Lesi 
```

#!/usr/bin/expect

###############################
#   Simple PDU setup script   #
###############################
# 1.0   2019.08.21      Andor Miklos


# usage:
# ./pdu_setup [PDU_NAME] [IP] [Gateway] [Mask]
# ./pdu_setup a7pdu-c 172.30.107.93 0.0.0.0 255.255.0.0


set pduname [lindex $argv 0]
set ipaddress [lindex $argv 1]
set ipgateway [lindex $argv 2]
set ipmask [lindex $argv 3]

#spawn ssh $usrname@$ipaddress
#spawn telnet 172.30.108.92
spawn telnet 192.168.1.1
expect "Please Login:"
send "ADMIN\r"
expect "Password:"
send "1001\r"
expect "Please Enter Your Selection =>"
#Select: 1. System Configuration
send "1\r"
expect "Please Enter Your Selection =>"
#Select: 1. System Information
send "1\r"
expect "Please Enter Your Selection =>"
#Select:  1. Site Name :
send "1\r"
expect "Please Enter New Site Name"
send "$pduname\r"
# 0.Return to Previous Menu
expect "Please Enter Your Selection =>"
send "0\r"
#  2. Network Information
expect "Please Enter Your Selection =>"
send "2\r"
# 1. Network IP Address, Gateway, and Subnet Mask
expect "Please Enter Your Selection =>"
send "1\r"
#Please Enter New IP Address ==>
expect "Please Enter New IP Address ==>"
send "$ipaddress\r"
expect "Please Enter New Gateway ==>"
send "$ipgateway\r"
expect "Please Enter New Subnet Mask ==>"
send "$ipmask\r"
expect "Are You Sure to Change Them \[Y\/N\]\? \(Default is N\) ==>"
send "Y\r"



```

