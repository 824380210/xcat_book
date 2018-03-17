# LRZ HPL stess test instruction
===
# 0 one chassis 12 node per groups to run the HPL 

# 1 sync the file from you git repocitory 

# 2 check the important file is ready or not 
```
[root@mgt33 LRZ]# md5sum HPL.dat xhpl_scinet
de3134eca63a649feb2f98051fa91251  HPL.dat
24ae6c04516af062c7680b5fd5a63ff1  xhpl_scinet
```
# 3 sync the HPL.dat and xhpl_scinet file to all node (or the node need to run the group linpack test )

# 4 build the hostfile ,and sync the hostfile to nodes
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
# 5 in each compute node ,mount the mgt:/install /install , xCAT management node may have different name like mgt33 
```
[root@mgt33 LRZ]# psh c4 mount mgt33:/install /install
```
# 6 run the strss test 

## Example of the stress test scripts 
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
# check the result . we run 5 cycle of the hpl test by default ,and if the performance reach 65% target ,you can terminal the session and save the log 
## our target score is more than 37140.48 GFlops per groups
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
