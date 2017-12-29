#code to read SMM version with IPMI command 
# use for Lenovo ThinkSystem SD530 SMM only
## exmaple here 
```
[root@mgt31 ~]# ./p.py 172.17.255.2
the current IP is 172.17.255.2
the ipmi command output is :  01 01 00 07 01 54 45 53 4d 30 32 4d

Handle the output to ASCII coding
['\x01', '\x01', '\x00', '\x07', '\x01', 'T', 'E', 'S', 'M', '0', '2', 'M']
TESM02M
[root@mgt31 ~]#
```
## the source code is here
```
#!/usr/bin/env python
#
#cmd = " ipmitool -H 172.17.255.1 -U USERID -P PASSW0RD -I lanplus raw 0x32 0xa8"
import subprocess
import sys
IP = sys.argv[1]
print ("the current IP is {}".format(IP) )
cmd = " ipmitool -H " +IP + "   -U USERID -P PASSW0RD -I lanplus raw 0x32 0xa8"
a=subprocess.check_output(cmd,shell=True)
#c=str(a.strip())
print "the ipmi command output is : {}".format(a)
print "Handle the output to ASCII coding"
b = a.strip().split(" ")
result = []
for line in b:
#    print line
    info = chr(int(line,16 ))
    result.append(info)
print str(result).strip()
mystr = "".join(result)
print mystr

```

