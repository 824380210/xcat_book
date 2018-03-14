
# LRZ 命令行参考



# LRZ要点
＃　升级ｘCAT
＃　BMC不用设置网关，要在networks表中去掉网关信息
#   OS网络掩码是22位，即255.255.252.0
#   BMC/XCC 网络掩码是22位，即255.255.252.0
#   OPA/Switch/FPC/PDU掩码是19位，即255.255.224.0 ,网关是172.16.31.240
#   其他IP信息设置参考production-hosts.txt文件，已保存到 mgt31-39的root目录下面了
#   

```
cd /etc/yum.repos.d/
rm lenovo-hpc.repo -f
cd
tar xjvf xcat-2.13.8_POST140_confluent-1.7.2_dev29_lenovo-confluent-0.7.1_post35-el7.tar.bz2
cd lenovo-hpc-el7/
bash mklocalrepo.sh
yum clean all
yum update -y
yum install confluent* -y  (如果原来没有安装confluent的话) 
yum install lenovo* -y      (如果原来没有安装confluent的话) 
grep i01r05 production-hosts.txt   （依实际柜编号查找）


chtab key=domain site.value=sng.lrz.de
ip a
chtab key=master site.value=mgt33  （按实际管理节点处理 ）
chtab key=forwarders site.value=172.16.131.254   (这个依实际配置，不同的island有不同的网络 )
chtab key=nameservers site.value=172.16.131.254  （理由如上一要）
chtab key=dhcpinterfaces site.value=eno1  (依实际处理)
chtab key=consoleservice site.value=confluent


```

#在在行配置前，建议重置默认的表（默认模板/opt/xcat/share/xcat/templates/e1350/ ）

#当节点发现完成后，不用重启机器，将IMM设置成shared模式


```
[root@mgt33 ~]# pscp asu64 all:/root/

[root@mgt33 ~]# pping bmc|xcoll
====================================
lrzbmc
====================================
noping

[root@mgt33 ~]#  nodeshell all /root/asu64 set IMM.SharedNicMode "Shared"  --kcs


[root@mgt33 ~]# pping bmc|xcoll
====================================
lrzbmc
====================================
ping


  91  ./asu64 showvalues imm.sharednicmode --kcs
  92  ./asu64 set imm.sharednicmode dedicated --kcs

```
# 配置FPC


```
[root@mgt33 ~]# grep fpc production-hosts.txt | grep i01r05
172.16.15.25 i01r05c01fpc.sng.lrz.de i01r05c01fpc
172.16.15.26 i01r05c02fpc.sng.lrz.de i01r05c02fpc
172.16.15.27 i01r05c03fpc.sng.lrz.de i01r05c03fpc
172.16.15.28 i01r05c04fpc.sng.lrz.de i01r05c04fpc
172.16.15.29 i01r05c05fpc.sng.lrz.de i01r05c05fpc
172.16.15.30 i01r05c06fpc.sng.lrz.de i01r05c06fpc


nodeadd i01r05c0[1-6]fpc  groups=fpc
chdef -t group fpc mgt=ipmi bmcpassword=PASSW0RD bmcusername=USERID cons=ipmi nodetype=fpc
chdef -t group fpc bmc='/\z//' ip='|i01r05c(\d+).*$|172.16.15.($1+24)|'


[root@mgt33 ~]# tabdump switch
#node,switch,port,vlan,interface,comments,disable
"36perswitch","|\w+-(\d+).*$|switch(($1-1)/42+1)|","|\w+-(\d+).*$|(($1-1)%42+1)|",,,,
"36perswitch1","|\w+-(\d+).*$|switch(($1-1)/42+2)|","|\w+-(\d+).*$|(($1-1)%42+1)|",,,,
"fpc","|i01r05c(\d+).*$|i01r05s(($1-1)/3+21)eth|","|i01r05c(\d+).*$|((($1-1)%3)+37)|",,,,
"lrzswitch","|i01r05c(\d+)s.*$|i01r05s(($1-1)/3+21)eth|","|i01r05c(\d+)s(\d+).*$|((($1-1)%3)*12+$2)|",,,,

```

```



[root@mgt33 ~]# lsdef i01r05c01fpc
Object name: i01r05c01fpc
    bmc=i01r05c01fpc
    bmcpassword=PASSW0RD
    bmcusername=USERID
    cons=ipmi
    groups=fpc
    ip=172.16.15.25
    mgt=ipmi
    nodetype=fpc
    postbootscripts=otherpkgs
    postscripts=syslog,remoteshell,syncfiles
    switch=i01r05s21eth
    switchport=37




[root@mgt33 ~]# configfpc -i eno1
Found IP 192.168.0.100 and MAC ec:aa:a0:19:87:d0
Configured FPC with MAC ec:aa:a0:19:87:d0 as i01r05c05fpc (172.16.15.29)
Verified the FPC with MAC ec:aa:a0:19:87:d0 is responding to the new IP 172.16.15.29 as node i01r05c05fpc
Found IP 192.168.0.100 and MAC ec:aa:a0:19:87:8c
Configured FPC with MAC ec:aa:a0:19:87:8c as i01r05c04fpc (172.16.15.28)
Verified the FPC with MAC ec:aa:a0:19:87:8c is responding to the new IP 172.16.15.28 as node i01r05c04fpc
Found IP 192.168.0.100 and MAC ec:aa:a0:19:87:e5
Configured FPC with MAC ec:aa:a0:19:87:e5 as i01r05c06fpc (172.16.15.30)
Verified the FPC with MAC ec:aa:a0:19:87:e5 is responding to the new IP 172.16.15.30 as node i01r05c06fpc
Found IP 192.168.0.100 and MAC ec:aa:a0:19:87:87
Configured FPC with MAC ec:aa:a0:19:87:87 as i01r05c02fpc (172.16.15.26)
Verified the FPC with MAC ec:aa:a0:19:87:87 is responding to the new IP 172.16.15.26 as node i01r05c02fpc
Found IP 192.168.0.100 and MAC ec:aa:a0:19:87:d5
Configured FPC with MAC ec:aa:a0:19:87:d5 as i01r05c03fpc (172.16.15.27)
Verified the FPC with MAC ec:aa:a0:19:87:d5 is responding to the new IP 172.16.15.27 as node i01r05c03fpc
Found IP 192.168.0.100 and MAC ec:aa:a0:19:87:e8
Configured FPC with MAC ec:aa:a0:19:87:e8 as i01r05c01fpc (172.16.15.25)
Verified the FPC with MAC ec:aa:a0:19:87:e8 is responding to the new IP 172.16.15.25 as node i01r05c01fpc
There are no more  default IP address to process

```



# 跑压力测试

```
[root@mgt33 ~]# lsdef -t osimage -z rhels7.3-x86_64-netboot-compute |sed  's/^[^ ]\+:/opa:/' |mkdef -z
1 object definitions have been created or modified.
[root@mgt33 ~]# mkdir -p /install/netboot/rhels7.3/x86_64/opa
[root@mgt33 ~]# chdef  -t osimage opa rootimgdir=/install/netboot/rhels7.3/x86_64/opa
1 object definitions have been created or modified.


[root@Rack_TestData ~]# scp /tmp/myopa74_20180312.tgz mgt33:/root/
myopa74_20180312.tgz                           71%  674MB 113.1MB/s   00:02 ETA


 preload opa osimage 
 nodeset all osimage=opa
 rsetboot all net -u
 rpower all reset
  
 


[root@mgt33 ~]# psh i01r05c0[1-2]s[01-12] opainfo | grep State |xcoll
====================================
i01r05c01s06,i01r05c02s11,i01r05c02s01,i01r05c02s06,i01r05c02s08,i01r05c01s07,i01r05c01s04,i01r05c01s08,i01r05c01s05,i01r05c01s02,i01r05c02s07,i01r05c02s09,i01r05c01s01,i01r05c01s10,i01r05c01s12,i01r05c02s02,i01r05c02s12,i01r05c01s11,i01r05c02s05,i01r05c01s03,i01r05c02s04,i01r05c02s10,i01r05c02s03,i01r05c01s09
====================================
   PortState:     Init (LinkUp)

[root@mgt33 ~]# ssh i01r05c01s01
Last login: Tue Mar 13 11:27:06 2018 from 172.16.131.254
[root@i01r05c01s01 ~]# service opafm start
Redirecting to /bin/systemctl start opafm.service
[root@i01r05c01s01 ~]# exit


[root@mgt33 ~]# psh i01r05c0[1-2]s[01-12] opainfo | grep State |xcoll
====================================
i01r05c01s06,i01r05c02s11,i01r05c02s01,i01r05c02s06,i01r05c02s08,i01r05c01s07,i01r05c01s04,i01r05c01s08,i01r05c01s05,i01r05c01s02,i01r05c02s07,i01r05c02s09,i01r05c01s01,i01r05c01s10,i01r05c01s12,i01r05c02s02,i01r05c02s12,i01r05c01s11,i01r05c02s05,i01r05c01s03,i01r05c02s04,i01r05c02s10,i01r05c02s03,i01r05c01s09
====================================
   PortState:     Active



```

# 加载ASU设置，注意先加载step1.asu，加载完后重启生效后,刷新OPA卡版本，再加载step2.asu,再重启 （注意每刷新一次ASU设置都要重启才能生效的）
# OPA 卡刷新包包含在opa osimage中的，可以直接刷

```
[root@mgt33 ~]# cat update_opa_lrz.sh
 nodeshell all   hfi1_eprom -w -o /usr/share/opa/bios_images/HfiPcieGen3Loader_1.6.0.0.0.rom
 nodeshell all   hfi1_eprom -w -b  /usr/share/opa/bios_images/HfiPcieGen3_1.6.0.0.0.efi
 nodeshell all   hfi1_eprom -w -c /lib/firmware/updates/hfi1_platform.dat
 nodeshell all  opatmmtool -f /lib/firmware/updates/hfi1_smbus.fw update
 
 
 [root@node04 ~]# opatmmtool
Current Firmware Version=10.4.0.0.146
[root@node04 ~]# hfi1_eprom -V -o
Using device: /sys/bus/pci/devices/0000:06:00.0/resource0
loader file version: 1.6.0.0.0
[root@node04 ~]# hfi1_eprom -V -b
Using device: /sys/bus/pci/devices/0000:06:00.0/resource0
driver file version: 1.6.0.0.0
[root@node04 ~]# hfi1_eprom -V -c
Using device: /sys/bus/pci/devices/0000:06:00.0/resource0
config file version: HFI_TYPE1 v1.0.1.0
[root@node04 ~]#

```


```
[root@mgt33 ~]# md5sum step1.asu step2.asu
bec97fb914bd8822199939a045ff6d8d  step1.asu
73bec0ae708caf530d42407d71ab3947  step2.asu

```
# setp 2不支持TDP设置，现在需要手动设置(在完成step 2后)
```
[root@mgt33 ~]# pasu i01r05c04s[11-12] set Processors.TDP 240 --override
i01r05c04s12: Processors.TDP=240
i01r05c04s12: Waiting for command completion status.
i01r05c04s11: Processors.TDP=240
i01r05c04s11: Waiting for command completion status.
i01r05c04s12: Command completed successfully.
i01r05c04s11: Command completed successfully.

```
# 在跑压力测试之前，要对系统做一个健康检查 ，确保所有节点设置一致
# 检查脚本在python_tools/LRZ/目录下，执行之前先同步一下
```
[root@mgt33 ~]# md5sum python_tools/LRZ/sys-health-check /install/johnw/sys-health-check
c410fcacd669ca6b798135d79f40c2d8  python_tools/LRZ/sys-health-check
c410fcacd669ca6b798135d79f40c2d8  /install/johnw/sys-health-check


[root@mgt33 ~]# /install/johnw/sys-health-check all | tee /tmp/health-check-201803142357.log
====================================
compute
====================================
                                Expected                                  Actual  Status        Description
                             -----------                                  ------  ------        -----------
                                    1.50                                    1.50      OK        Node XCC Firmware Version
                                 OTE106I                                 OTE106I      OK        Node UEFI Firmware Version
                                 VT-UTF8                                 VT-UTF8      OK        DevicesandIOPorts.Com1TerminalEmulation
                                  Enable                                  Enable      OK        DevicesandIOPorts.Com1ActiveAfterBoot
                                Hardware                                Hardware      OK        DevicesandIOPorts.Com1FlowControl
                             Cooperative                             Cooperative      OK        Processors.CPUPstateControl
                                 Disable                                 Disable      OK        Processors.SNC
                                    UEFI                                    UEFI      OK        EnableDisableAdapterOptionROMSupport.OnboardVideo
                                    None                                    None      OK        DiskGPTRecovery.DiskGPTRecovery
                             Custom Mode                             Custom Mode      OK        OperatingModes.ChooseOperatingMode
                                    240W                                    240W      OK        Processor Power
                              3.10.0-693                              3.10.0-693      OK        Linux Kernel Version
                            96@powersave                            96@powersave      OK        CPU scaling_govenor
                              96@1200000                              96@1200000      OK        CPU scaling_min_freq
                              96@3900000                              96@3900000      OK        CPU scaling_max_freq
                                    94GB                                    94GB      OK        MEMORY Total
                  [always] madvise never                  [always] madvise never      OK        MEMORY Huge Transparent Pages
                                       1                                       1      OK        OPA Ports visible to Operating System
                                (rev 11)                                (rev 11)      OK        OPA Card Level(s)
                                     x16                                     x16      OK        OPA PCI Lanes
                              10.6.1.0.2                              10.6.1.0.2      OK        OPA Driver Version
                                  Active                                  Active      OK        OPA Link Status
                                       4                                       4      OK        OPA Tx LaneWidth
                                       4                                       4      OK        OPA Rx LaneWidth
                           5 (Excellent)                           5 (Excellent)      OK        OPA Link Quality
                                datagram                                datagram      OK        OPA mode
                                    4092                                    4092      OK        OPA MTU
                                     128                                     128      OK        OPA Send Queue Size
                                     256                                     256      OK        OPA Receive Queue Size
                                v1.0.1.0                                v1.0.1.0      OK        OPA Adapter Config Version
                               1.6.0.0.0                               1.6.0.0.0      OK        OPA Adapter Loader Version
                               1.6.0.0.0                               1.6.0.0.0      OK        OPA Adapter Config Version
                            10.4.0.0.146                            10.4.0.0.146      OK        OPA Adapter TMM Version

[root@mgt33 ~]#

```
# 跑单机测试(可选)

```
102144      Ns
1            # of NBs
384          NBs
0            PMAP process mapping (0=Row-,1=Column-major)
1            # of process grids (P x Q)
1            Ps
1            Qs


[root@mgt33 ~]# md5sum peter/cluster/HPL.dat.1n
8aa31f171cd8b23509132c065e38da0d  peter/cluster/HPL.dat.1n
[root@mgt33 ~]# pscp peter/cluster/HPL.dat.1n all:/root/peter/HPL.dat


[root@mgt33 ~]# cat peter/lrz_single.sh
#!/bin/bash
#
mount | grep mgt | grep install  &>/dev/null
if [ $? -eq 0 ];then
        echo -e "mgt is mount"
else
        mount mgt33:/install /install
fi
timefmt=`date +%Y%m%d%H%M%s`
mkdir -p /install/mgt33
#mount mgt33:/install /install
/opt/intel/compilers_and_libraries_2018.1.163/linux/mkl/benchmarks/mp_linpack/xhpl_intel64_static | tee /install/mgt33/single-$(hostname -s)-${timefmt}.log
#

[root@mgt33 ~]#


[root@mgt33 ~]# pscp peter/lrz_single.sh all:/root/peter/
i01r05c01s01: done


[root@mgt33 ~]# nodeshell i01r05c[01-02]s[01-12] "cd /root/peter; bash lrz_single.sh"


```
# 提取各个传感器值 
```


for a in `seq 1 100`; do timefmt=`date +%Y%m%d%H%M%S`; mkdir -p /install/mgt33; nodesensors i01r05c[01-02]s[01-12] >/install/mgt33/sensors_${timefmt}.log; sleep 60; done

```

#

```
[root@mgt33 ~]# psh all opainfo | grep State | xcoll
====================================
compute
====================================
   PortState:     Active


```

# 跑集群linpack
```
生成hostfile 
复制到指定节点的:/root/peter/cluster下面
将/root/peter/HPL.dat.xn(注意：HPL.dat.36node是给768G FAT NODE用的，96G的Thin node 要用HPL.dat.36n)复制到跑linpack节点的:/root/peter/cluster/HPL.dat
进入某节点/root/peter/cluster/下跑对应的脚本，如bash 36node.sh


[root@mgt33 ~]# psh i01r05c[01-06]s01 service opafm start
i01r05c02s01: Redirecting to /bin/systemctl start opafm.service
i01r05c03s01: Redirecting to /bin/systemctl start opafm.service
i01r05c01s01: Redirecting to /bin/systemctl start opafm.service
i01r05c05s01: Redirecting to /bin/systemctl start opafm.service
i01r05c06s01: Redirecting to /bin/systemctl start opafm.service
i01r05c04s01: Redirecting to /bin/systemctl start opafm.service



[root@mgt33 mgt33]# nodelist i01r05c0[1-3]s[01-12] >hostfile
[root@mgt33 mgt33]# pscp hostfile i01r05c01s01:/root/peter/cluster/
i01r05c01s01: done
[root@mgt33 mgt33]# nodelist i01r05c0[4-6]s[01-12] >hostfile
[root@mgt33 mgt33]# pscp hostfile i01r05c04s01:/root/peter/cluster/



[root@mgt33 ~]# pscp peter/cluster/HPL.dat.36n all:/root/peter/cluster/HPL.dat

[root@mgt33 ~]# ssh i01r05c01s01
[root@i01r05c01s01 ~]# cd peter/cluster/
[root@i01r05c01s01 cluster]# cat hostfile
[root@i01r05c01s01 cluster]#bash 36node.sh

```
# 36个节点压力测试只能一组跑，chiller功率不足，不支持两组同时跑 
power cycle测试
数据收集

# 添加特别版本xhpl测试
# xhpl程序由intel特别提供，用于捕捉更多信息
# 程序放在python_tools/HPL目录下面
##  执行36个节点单机测试如下
```

[root@mgt33 ~]# ls HPL
HPL.dat  parse.sh  run.sh  single_run.sh  skl3_HPL_2018-03-12_17-23  xhpl
[root@mgt33 ~]# scp -r HPL  python_tools/
[root@mgt33 ~]# cat HPL/single_run.sh
#!/bin/bash
hostname=`hostname -s`
fmt=`date +%Y%m%d%H%M%S`
./xhpl | tee /install/mgt33/single_hpl/single_${hostname}_${fmt}.log

[root@mgt33 ~]# pscp -r HPL all:/root/

[root@mgt33 ~]# psh all mount mgt33:/install /install
[root@mgt33 ~]# ls /install/mgt33/single_hpl/

[root@mgt33 ~]# psh i01r05c0[1-3]s[01-12] "cd /root/HPL; bash single_run.sh"

```
## 可以监控/install/mgt33/single_hpl/下的文件，正常情况下单节点linpack可以在5分钟内跑完呵！

## 分两组跑单机的压力测试，测试完一组后才能跑另一组（因chiller功率不足导致）

```
[root@mgt33 ~]# grep WR /install/mgt33/single_hpl/single_i01r05c0* |sort -k7 -n
/install/mgt33/single_hpl/single_i01r05c01s12_20180314202740.log:WR00L2L4      103296   384     1     1             260.48            2.82091e+03
/install/mgt33/single_hpl/single_i01r05c02s10_20180314202744.log:WR00L2L4      103296   384     1     1             253.41            2.89959e+03
/install/mgt33/single_hpl/single_i01r05c03s04_20180314202738.log:WR00L2L4      103296   384     1     1             248.33            2.95899e+03
/install/mgt33/single_hpl/single_i01r05c03s11_20180314202742.log:WR00L2L4      103296   384     1     1             248.15            2.96114e+03
/install/mgt33/single_hpl/single_i01r05c02s02_20180314202742.log:WR00L2L4      103296   384     1     1             246.98            2.97517e+03
/install/mgt33/single_hpl/single_i01r05c01s08_20180314202742.log:WR00L2L4      103296   384     1     1             246.49            2.98107e+03
/install/mgt33/single_hpl/single_i01r05c01s10_20180314202742.log:WR00L2L4      103296   384     1     1             245.63            2.99146e+03
/install/mgt33/single_hpl/single_i01r05c01s09_20180314202742.log:WR00L2L4      103296   384     1     1             242.60            3.02889e+03
/install/mgt33/single_hpl/single_i01r05c03s12_20180314202743.log:WR00L2L4      103296   384     1     1             242.56            3.02937e+03
/install/mgt33/single_hpl/single_i01r05c01s04_20180314202743.log:WR00L2L4      103296   384     1     1             240.56            3.05459e+03
/install/mgt33/single_hpl/single_i01r05c02s05_20180314202741.log:WR00L2L4      103296   384     1     1             239.26            3.07110e+03
/install/mgt33/single_hpl/single_i01r05c02s11_20180314202741.log:WR00L2L4      103296   384     1     1             234.09            3.13903e+03
/install/mgt33/single_hpl/single_i01r05c03s02_20180314202743.log:WR00L2L4      103296   384     1     1             233.00            3.15364e+03


```
# 跑 36个节点的组压力测试
## 1： 同步HPL目录的xhpl到所有节点的/root/peter/cluster目录去
## 2： 生成hostfile文件，并同步到相应的节点中去
## 3： 生成测试的脚本
## 4： 同步HPL.dat到各个节点去（注意HPL.dat.36node 与 HPL.dat.36n的区别）
## 5:  同步指定的xhpl 到所有节点的/root/peter/cluster目录
