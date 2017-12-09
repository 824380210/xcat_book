## Make sure the HPL.dat is correct configure 
## make sure the host1.file is corrct configure (Group linpack need )
## make sure the IB adatpere is active and the speed is correct (Group linpack need )
## make sure all the node in the Group Linpack have the IB cable to connect to the same IB Switches

# Single node Linpack run example
```


[root@stark23 sync]# cat single.sh
#!/bin/bash
myname=`hostname  -s`
fmt=`date +%Y%m%d%H%M`
mkdir -p /tmp/master/
mount | grep 172.16.0.1  >/dev/null
if [ $? -ne 0 ] ; then
        mkdir  -p /tmp/master
        mount 172.16.0.1:/install/sci /tmp/master
fi
#
/opt/intel-test/compilers_and_libraries_2017.4.196/linux/mkl/benchmarks/mp_linpack/xhpl_intel64_static | tee /tmp/master/single_node/${myname}_${fmt}.log



```




# group node Linpack run example 
```
root@stark23 sync]# cat run_linpack_group1.sh
#!/bin/bash
fmt=`date +%Y%m%d%H%M`
mount | grep 172.16.0.1  >/dev/null
if [ $? -ne 0 ] ; then
        mkdir /tmp/master
        mount 172.16.0.1:/install/sci /tmp/master
fi
#
mpirun -genv I_MPI_FABRICS=dapl -machinefile host1 -ppn 1  -np 18 /opt/intel-test/compilers_and_libraries_2017.4.196/linux/mkl/benchmarks/mp_linpack/xhpl_intel64_static | tee /tmp/master/$(hostname -s)_18node_${fmt}.log
echo $(hostname -s)_18node_${fmt}.log



```
