## stream is use to measure the bandwidth from the Memory to the CPU processor . the test result is related on the memory channel and bandwidth of each DIMM .for the best performance .you should populated with full DIMM (full channnel usage ) on the CPU 

##  example of the CPU we use  here : skylake 8160 ,24 cores per socket ,total 2 sockets , 48 cores 

```
[root@localhost peter]# lscpu
Architecture:          x86_64
CPU op-mode(s):        32-bit, 64-bit
Byte Order:            Little Endian
CPU(s):                96
On-line CPU(s) list:   0-95
Thread(s) per core:    2
Core(s) per socket:    24
Socket(s):             2
NUMA node(s):          2
Vendor ID:             GenuineIntel
CPU family:            6
Model:                 85
Model name:            Intel(R) Xeon(R) Platinum 8160 CPU @ 2.10GHz
Stepping:              4
CPU MHz:               2100.000
BogoMIPS:              4200.00
Virtualization:        VT-x
L1d cache:             32K
L1i cache:             32K
L2 cache:              1024K
L3 cache:              33792K
NUMA node0 CPU(s):     0-23,48-71
NUMA node1 CPU(s):     24-47,72-95
Flags:                 fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 ds_cpl vmx smx est tm2 ssse3 fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch epb cat_l3 cdp_l3 intel_pt tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 hle avx2 smep bmi2 erms invpcid rtm cqm mpx rdt_a avx512f avx512dq rdseed adx smap clflushopt clwb avx512cd avx512bw avx512vl xsaveopt xsavec xgetbv1 cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_local dtherm ida arat pln pts hwp_epp

```
## example of the Memory we use here : 16G memory ,12 DIMM , for skylake CPU ,it have 6 DIMM channel ,so that is what expected configure(best performance )


```
[root@localhost peter]# dmidecode -t 17 | grep -E "Size|Locator" | grep -v Bank
        Size: 16384 MB
        Locator: DIMM 6
        Size: No Module Installed
        Locator: DIMM 5
        Size: 16384 MB
        Locator: DIMM 7
        Size: 16384 MB
        Locator: DIMM 8
        Size: 16384 MB
        Locator: DIMM 3
        Size: No Module Installed
        Locator: DIMM 4
        Size: 16384 MB
        Locator: DIMM 2
        Size: 16384 MB
        Locator: DIMM 1
        Size: 16384 MB
        Locator: DIMM 14
        Size: No Module Installed
        Locator: DIMM 13
        Size: 16384 MB
        Locator: DIMM 15
        Size: 16384 MB
        Locator: DIMM 16
        Size: 16384 MB
        Locator: DIMM 11
        Size: No Module Installed
        Locator: DIMM 12
        Size: 16384 MB
        Locator: DIMM 10
        Size: 16384 MB
        Locator: DIMM 9

```
## test code we use for the node (single node only ,it is not the cluster bandwidth test )

```
[root@localhost peter]# cat myrun.sh
export OMP_NUM_THREADS=24
export KMP_AFFINITY=granularity=thread,proclist=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],explicit
./stream_c_skylake.exe
export KMP_AFFINITY=granularity=thread,proclist=[24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47],explicit
./stream_c_skylake.exe
export OMP_NUM_THREADS=48
export KMP_AFFINITY=granularity=thread,proclist=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47],explicit
./stream_c_skylake.exe
[root@localhost peter]# cp myrun.sh stream_skylake.sh
[root@localhost peter]# md5sum stream_skylake.sh myrun.sh stream_c_skylake.exe
33a0b3f325c043f5eb58658e2a637132  stream_skylake.sh
33a0b3f325c043f5eb58658e2a637132  myrun.sh
7df42148287b5cd41df1c0afc0a053a2  stream_c_skylake.exe


```

## download the test code [skylake_stream.tgz](https://github.com/824380210/xcat_book/blob/master/skylake_stream.tgz)


```
[root@localhost peter]# tar czvf /tmp/skylake_stream.tgz ./stream_skylake.sh ./stream_c_skylake.exe
./stream_skylake.sh
./stream_c_skylake.exe
[root@localhost peter]# md5sum /tmp/skylake_stream.tgz
01d40cfc4deb34a0e032df000ae58966  /tmp/skylake_stream.tgz
[root@localhost peter]#

```

## test run and result that we should focus on is the Triad result ; ==out acceptable result is more than 180G for 2 skylake sockets==  

```
[root@localhost peter]# bash myrun.sh | grep Triad
Triad:          94050.0     0.030682     0.030622     0.030890
Triad:          94360.8     0.030614     0.030521     0.031254
Triad:         187123.9     0.015426     0.015391     0.015529
```

## the full test result of the Stream test 
```

[root@localhost peter]# bash myrun.sh
-------------------------------------------------------------
STREAM version $Revision: 5.10 $
-------------------------------------------------------------
This system uses 8 bytes per array element.
-------------------------------------------------------------
Array size = 120000000 (elements), Offset = 0 (elements)
Memory per array = 915.5 MiB (= 0.9 GiB).
Total memory required = 2746.6 MiB (= 2.7 GiB).
Each kernel will be executed 20 times.
 The *best* time for each kernel (excluding the first iteration)
 will be used to compute the reported bandwidth.
-------------------------------------------------------------
Number of Threads requested = 24
Number of Threads counted = 24
-------------------------------------------------------------
Your clock granularity/precision appears to be 1 microseconds.
Each test below will take on the order of 20005 microseconds.
   (= 20005 clock ticks)
Increase the size of the arrays if this shows that
you are not getting at least 20 clock ticks per test.
-------------------------------------------------------------
WARNING -- The above is only a rough guideline.
For best results, please be sure you know the
precision of your system timer.
-------------------------------------------------------------
Function    Best Rate MB/s  Avg time     Min time     Max time
Copy:           84362.4     0.022815     0.022759     0.022908
Scale:          85756.6     0.022462     0.022389     0.022523
Add:            94408.0     0.030572     0.030506     0.030638
Triad:          94102.0     0.030677     0.030605     0.030880
-------------------------------------------------------------
Solution Validates: avg error less than 1.000000e-13 on all three arrays
-------------------------------------------------------------
-------------------------------------------------------------
STREAM version $Revision: 5.10 $
-------------------------------------------------------------
This system uses 8 bytes per array element.
-------------------------------------------------------------
Array size = 120000000 (elements), Offset = 0 (elements)
Memory per array = 915.5 MiB (= 0.9 GiB).
Total memory required = 2746.6 MiB (= 2.7 GiB).
Each kernel will be executed 20 times.
 The *best* time for each kernel (excluding the first iteration)
 will be used to compute the reported bandwidth.
-------------------------------------------------------------
Number of Threads requested = 24
Number of Threads counted = 24
-------------------------------------------------------------
Your clock granularity/precision appears to be 1 microseconds.
Each test below will take on the order of 19994 microseconds.
   (= 19994 clock ticks)
Increase the size of the arrays if this shows that
you are not getting at least 20 clock ticks per test.
-------------------------------------------------------------
WARNING -- The above is only a rough guideline.
For best results, please be sure you know the
precision of your system timer.
-------------------------------------------------------------
Function    Best Rate MB/s  Avg time     Min time     Max time
Copy:           83835.4     0.022931     0.022902     0.022974
Scale:          85572.6     0.022491     0.022437     0.022537
Add:            94385.9     0.030560     0.030513     0.030678
Triad:          94216.5     0.030628     0.030568     0.030766
-------------------------------------------------------------
Solution Validates: avg error less than 1.000000e-13 on all three arrays
-------------------------------------------------------------
-------------------------------------------------------------
STREAM version $Revision: 5.10 $
-------------------------------------------------------------
This system uses 8 bytes per array element.
-------------------------------------------------------------
Array size = 120000000 (elements), Offset = 0 (elements)
Memory per array = 915.5 MiB (= 0.9 GiB).
Total memory required = 2746.6 MiB (= 2.7 GiB).
Each kernel will be executed 20 times.
 The *best* time for each kernel (excluding the first iteration)
 will be used to compute the reported bandwidth.
-------------------------------------------------------------
Number of Threads requested = 48
Number of Threads counted = 48
-------------------------------------------------------------
Your clock granularity/precision appears to be 1 microseconds.
Each test below will take on the order of 9881 microseconds.
   (= 9881 clock ticks)
Increase the size of the arrays if this shows that
you are not getting at least 20 clock ticks per test.
-------------------------------------------------------------
WARNING -- The above is only a rough guideline.
For best results, please be sure you know the
precision of your system timer.
-------------------------------------------------------------
Function    Best Rate MB/s  Avg time     Min time     Max time
Copy:          168066.3     0.011465     0.011424     0.011518
Scale:         169956.8     0.011345     0.011297     0.011449
Add:           187231.2     0.015437     0.015382     0.015836
Triad:         186950.1     0.015464     0.015405     0.015510
-------------------------------------------------------------
Solution Validates: avg error less than 1.000000e-13 on all three arrays
-------------------------------------------------------------
[root@localhost peter]#

```

