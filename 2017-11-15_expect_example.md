# 2017-11-15 expect cmd example for check the FW level

## 1 install the epxect cmd 
## 2 write your script here 
```
[root@mgt ~]# cat check_fw_level.exp
#!/usr/bin/expect
#
set timeout 90
set ip [lindex $argv 0]
#set f [lindex $argv 1]
#set user admin
#set password admin
# Enter login username: admin
# Enter login password:
# s03r2msw1>

spawn ssh USERID@$ip
expect "*Password:"
send "PASSW0RD\r";
expect "system>"
send "vpd fw\r"
expect "system>"
send "exit\r"
send "\r"
#send "exit\r"

``` 
## 3 update the scripte with execute permission  "chmod 755 xxx"
## 4 vefify the result 

```

[root@mgt ~]# ./check_fw_level.exp node21-bmc
spawn ssh USERID@node21-bmc
Password:

system> vpd fw
Type                     Status       Version      BuildID          ReleaseDate
----                     ------       -------      -------          -----------
BMC(Primary)             Active       1.50         TEI317A          2017-10-25
BMC(Backup)              Inactive     1.50         TEI317A          2017-10-25
UEFI                     Active       1.00         OTE105A          2017-11-03
LXPM                     Active       1.01         PDL106W          2017-08-01
LXPM Windows Drivers     Active       1.01         PDL304T          2017-07-31
LXPM Linux Drivers       Active       1.01         PDL204O          2017-07-29
system> [root@mgt ~]#
[root@mgt ~]#

```
##  another example for the FFDC log download
### make sure tftp server with download permissions "man tftpd"
### chmod -R 777 /tftpboot
### 
## Code Example for Lenovo ThinkSystem Stark SD530 


```
[root@mgt32 ~]# cat ffdc_get.sh
#!/usr/bin/expect
#
set timeout 90
set ip [lindex $argv 0]
#set f [lindex $argv 1]
#set user admin
#set password admin
# Enter login username: admin
# Enter login password:
# s03r2msw1>

spawn ssh USERID@$ip
expect "*Password:"
send "PASSW0RD\r";
expect "system>"
send "ffdc generate -t 1 -ip 10.3.0.254 -pn 69\r"
expect "system>"
send "exit\r"
#send "exit\r"
```
