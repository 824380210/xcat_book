# LRZ HPL 压力测试指导说明
===
# 0： 12台机器一个组进行压力测试

# 1：同步你的git服务器

# 2 检查下面两个文件，我们需要将它同步到所有计算节点的/root/peter/cluster目录下面 
```
[root@mgt33 LRZ]# md5sum HPL.dat xhpl_scinet
de3134eca63a649feb2f98051fa91251  HPL.dat
24ae6c04516af062c7680b5fd5a63ff1  xhpl_scinet
```

# 3： 生成做集群压力测试的hostfile ,并同步到所有计算节点
```
[root@mgt33 LRZ]# nodelist c4
i01r05c04s01
i01r05c04s02
i01r05c04s03
i01r05c04s04
i01r05c04s05
i01r05c04s06
i01r05c04s07
i01r05c04s08
i01r05c04s09
i01r05c04s10
i01r05c04s11
i01r05c04s12
[root@mgt33 LRZ]# nodelist c4 >hostfile
[root@mgt33 LRZ]# pscp hostfile c4:/root/peter/cluster/
```
# 4: 在计算节点中挂载管理节点的/install 目录， 用于保存压力测试日志，如mount  mgt:/install /install ,注意管理节点名称可能不一样，按实际进行操作 
```
[root@mgt33 LRZ]# psh c4 mount mgt33:/install /install
```
# 5: 开始跑压力测试

## 压力测试参考脚本 
```
[root@i01r05c04s01 ~]# cat peter/cluster/sci_run.sh
#!/bin/bash
source ./tools_cluster.sh
# . o/root/peter/cluster/tools_cluster.sh
host=`hostname -s`
fm=`date +%Y%m%d%H%M%S`
echo -e " make sure all OPA port is up and running "
#echo -e "ln -s /usr/lib/systemd/system/opafm.service /etc/systemd/system/multi-user.target.wants/opafm.service"
# systemctl restart opafm.service
# opainfo
# opafabricinfo
#
mkdir -p /install/tmp/
echo -e "Test log is store in the /install/tmp/linpack_${fm}.log"
echo -e "\n\n***********************************************************************************************\n"
mpirun -genvall -f hostfile -np 12 -ppn 1 /root/peter/cluster/xhpl_scinet | tee /install/tmp/12node-scinet-${host}-linpack_${fm}_${a}.log
#
echo -e "***********************************************************************************************"
echo -e "\n\n\nTest log is store in the /install/tmp/linpack_${fm}.log\n\n\n"
#
#


```
# 在测试中检查结果，默认我们会跑5次压力测试，在HPL.dat中已定义了5次了，我们可以每隔14分钟左右就检查一下，只要性能达到37140.48GFlops ,那么测试就通过
## 测试通过后，保存log，如果5次没有跑完也可以中断程序 ，进行下一步操作。
```
12node-scinet-i01r05c04s01-linpack_20180317054150_.log:WR00L2L4      353856   384     3     4             784.04            3.76750e+04
12node-scinet-i01r05c04s01-linpack_20180317054150_.log:WR00L2L4      353856   384     3     4             783.55            3.76987e+04
12node-scinet-i01r05c04s01-linpack_20180317054150_.log:WR00L2L4      353856   384     3     4             783.72            3.76902e+04
12node-scinet-i01r05c04s01-linpack_20180317054150_.log:WR00L2L4      353856   384     3     4             783.50            3.77009e+04
12node-scinet-i01r05c05s01-linpack_20180317052641_1.log:WR00L2L4      353856   384     3     4             778.73            3.79319e+04
12node-scinet-i01r05c05s01-linpack_20180317052641_2.log:WR00L2L4      353856   384     3     4             777.87            3.79740e+04
12node-scinet-i01r05c05s01-linpack_20180317052641_3.log:WR00L2L4      353856   384     3     4             856.41            3.44911e+04
12node-scinet-i01r05c05s01-linpack_20180317052641_4.log:WR00L2L4      353856   384     3     4             776.28            3.80513e+04
12node-scinet-i01r05c05s01-linpack_20180317052641_5.log:WR00L2L4      353856   384     3     4             775.59            3.80856e+04
12node-scinet-i01r05c05s01-linpack_20180317052641_6.log:WR00L2L4      353856   384     3     4             778.69            3.79340e+04
12node-scinet-i01r05c05s01-linpack_20180317052641_7.log:WR00L2L4      353856   384     3     4             777.25            3.80043e+04


```
