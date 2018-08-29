## 1:   use asu tools to flash the first step  CMOS settings 
```
[root@mgt ~]# cat stark1.cmos
loaddefault BootOrder
loaddefault uEFI
set OperatingModes.ChooseOperatingMode "Maximum Performance"

[root@mgt ~]# pasu all batch stark1.cmos

```
## 2:   reboot to make sure the stark1.cmos take effect
## 3:   use asu tools to flash the second step CMOS settings 
```
[root@mgt ~]# cat stark2.cmos
set OperatingModes.ChooseOperatingMode "Custom Mode"
set Processors.CPUPstateControl Cooperative
set Processors.SNC Disable
set DevicesandIOPorts.Com1TerminalEmulation VT-UTF8
set DevicesandIOPorts.Com1ActiveAfterBoot Enable
set DevicesandIOPorts.Com1FlowControl Hardware
set DiskGPTRecovery.DiskGPTRecovery None
set EnableDisableAdapterOptionROMSupport.OnboardVideo UEFI

[root@mgt ~]#  pasu all batch stark2.cmos

```
## 4:   use the edr741 osimage  for netboot all the node;reboot will cause the second cmos setting take effect 

```
nodeset all osimage=edr741
rsetboot all net -u
rpower all reset

```
## 5:   after all node up and running , update the opensm.conf to all compute node 

```
 [root@mgt ~]# cat opensm.conf
 virt_enabled 2
 qos true

 [root@mgt ~]# pscp opensm.conf all:/etc/opensm/
 [root@mgt ~]# ssh node01 service opensmd restart
 
```
## 6:   check all node to make sure the ib port is up and active 

```
[root@mgt install]#  psh all ibstat | grep Active
node05:                 State: Active
node04:                 State: Active
node06:                 State: Active
node07:                 State: Active
node03:                 State: Active
node02:                 State: Active
node01:                 State: Active
node08:                 State: Active

## if you have problem to active the ib port ,retry the step 5 & 5

```
## 7:   update the hostfile and sync to compute node 

```
[root@mgt ~]# cat hostfile
node01
node02
node03
node04

[root@mgt ~]# pscp hostfile c1:/root/peter/cluster/
node02: done
node01: done
node03: done
node04: done

```
## 8:  update the HPL.dat file ,then sync to all node 

```
[root@mgt ~]# cat HPL.dat
HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out      output file name (if any)
6            device out (6=stdout,7=stderr,file)
1            # of problems sizes (N)
408576       Ns
1            # of NBs
384          NBs
0            PMAP process mapping (0=Row-,1=Column-major)
1            # of process grids (P x Q)
2            Ps
2            Qs
16.0         threshold
1            # of panel fact
0            PFACTs (0=left, 1=Crout, 2=Right)
1            # of recursive stopping criterium
4            NBMINs (>= 1)
1            # of panels in recursion
2            NDIVs
1            # of recursive panel fact.
0            RFACTs (0=left, 1=Crout, 2=Right)
1            # of broadcast
0            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM,6=Psh,7=Spush,8=Psh2)
1            # of lookahead depth
0            DEPTHs (>=0)
0            SWAP (0=bin-exch,1=long,2=mix)
1            swapping threshold
1            L1 in (0=transposed,1=no-transposed) form
1            U  in (0=transposed,1=no-transposed) form
0            Equilibration (0=no,1=yes)
8            memory alignment in double (> 0)
[root@mgt ~]# pscp HPL.dat c1:/root/peter/cluster/
node01: done
node02: done
node03: done
node04: done

```
## 9:  go to the one of the compute node and start to run the linpack test 

```
[root@mgt ~]# ssh node01
Last login: Tue Aug 28 17:32:27 2018 from 172.20.0.1
[root@node01 ~]# cd peter/cluster/
[root@node01 cluster]# cat run_2node_EDR.sh
#source ./edr_env.sh
fmt=`date +%Y%m%d%H%M%S`
mount | grep mgt >/dev/null
if [ $? -ne 0 ];then
        echo -e "Start to mount the mgt node for log store "
        mount mgt:/install /install
fi
mount | grep mgt
#
#mpirun -genv I_MPI_FABRICS=dapl -machinefile hostfile   -genv I_MPI_FALLBACK=disable -genv I_MPI_OFA_ADAPTER_NAME='mlx5_0' -np 2 -ppn 1 /opt/intel/compilers_and_libraries_2017.5.239/linux/mkl/benchmarks/mp_linpack/xhpl_intel64_dynamic | tee /install/linpack-${fmt}.log
mpirun -genv I_MPI_FABRICS=dapl -machinefile hostfile   -genv I_MPI_FALLBACK=disable -genv I_MPI_OFA_ADAPTER_NAME='mlx5_0' -np 2 -ppn 1 /opt/intel/compilers_and_libraries_2018.0.128/linux/mkl/benchmarks/mp_linpack/xhpl_intel64_dynamic | tee /install/linpack-${fmt}.log
# mpirun -genv I_MPI_FABRICS=dapl -genv I_MPI_FALLBACK=disable -genv I_MPI_OFA_ADAPTER_NAME='mlx5_0'  -machinefile hostfile -np 2 -ppn 1 /opt/intel/compilers_and_libraries_2018.1.163/linux/mkl/benchmarks/mp_linpack/xhpl_intel64_static | tee /install/static_74_edr.log
echo -e "LOG FILE IS  /install/linpack-${fmt}.log  \n"
[root@node01 cluster]#

## 10:  you should update the code to use the /root/peter/cluster/xhpl for scinet version xhpl linpack run 

```
## 11:	  hugepage setup for CPU core bigger than 24 node ,use following to enable the hugepage 
```

 chdef  noderange  addkcmdline="hugepagesz=1G hugepages=360 default_hugepagesz=1G" 
 nodeset all osimage=edr741
 rsetboot all net -u
 rpower all reset

```
## 12:	setup the hugepage related settings after node is up and running 
```
psh c1  hugeadm --create-global-mounts --set-recommended-shmmax
psh c1  cpupower frequency-set -g performance

```
## 13:	you should use the special xhpl version (scinet version xhpl in /root/peter/cluster ) with hugepage linpack run 
## 14:  disabe the hugepage settings 
```
 chdef  noderange  addkcmdline=""
 nodeset all osimage=edr741
 rsetboot all net -u
 rpower all reset
```
## 
