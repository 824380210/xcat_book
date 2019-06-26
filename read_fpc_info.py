#
import subprocess
import logging
import sys

#
def runcmd(cmd,timeout=None):
    """
    run command for subprocess and return the output 
    """
    if not timeout:
        timeout = 30
    proc = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
    if proc.returncode != 0:
        raise Exception("cmd run failed with {}".format(cmd))
    else:
        return(proc.stdout)
#
IP = sys.argv[1]
cmd  = "ipmitool -I lanplus -H " + IP + " -U USERID  -P PASSW0RD raw 0x0C 0x02 0x01 0xC3 0x00 0x00"
result = runcmd(cmd)
cur_str = []
for char in result.decode().split():
    cur_str.append(chr(int("0x"+char,16)))
# change the iem in the list to string
mylist = [ str(i) for i in cur_str[2:] ]
str3 = ''.join(mylist)
fpc_hostname = str3.strip().strip('\r\n\t')
cmd_spec = """

0x0c 0x01  =  set lan config parameter
0x0c 0x02  =  get lan config parameter
#3 channel number ,should be always 0x01 
#3 0xc3 for hostname ,0xc4 for dns domain name



"""
cmd =  "ipmitool -I lanplus -H " + IP + " -U USERID  -P PASSW0RD raw 0x0C 0x02 0x01 0xC4 0x00 0x00" 
result =  runcmd(cmd)
cur_str = []
for char in result.decode().split():
    cur_str.append(chr(int("0x"+char,16)))
# change the iem in the list to string
mylist = [ str(i) for i in cur_str[2:] ]
str3 = ''.join(mylist)
fpc_domainname = str3.strip().strip('\r\n\t')
#print("the current FPC hostname is {} and the domain name is {} ".format(fpc_hostname,fpc_domainname))


cmd = "ipmitool -I lanplus -H " + IP + " -U USERID  -P PASSW0RD raw 0x32 0xa8"
result = runcmd(cmd)
cur_ver_list = [ str(i) for i in result.decode().split()]
# ['00', '02', '31', '01', '32', '01', '38', '42']

fpc_main_ver        = int(cur_ver_list[1])
fpc_minor_ver       = int(cur_ver_list[2])
fpc_build_main_ver       = int(cur_ver_list[6])
fpc_build_minor_ver = chr(int(cur_ver_list[7],16))
print("FPC Version:  fhet{}{}-{}.{}\t Hostname:  {}\tDomain Name:  {}".format(fpc_build_main_ver,fpc_build_minor_ver,fpc_main_ver,fpc_minor_ver,fpc_hostname,fpc_domainname))
