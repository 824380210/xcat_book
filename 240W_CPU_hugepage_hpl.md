## setup the os environment with hugepage set 

```
[root@mgt39 hpl_hugepage]# chdef c3 -p addkcmdline="hugepagesz=1G hugepages=80 default_hugepagesz=1G"
12 object definitions have been created or modified.
[root@mgt39 hpl_hugepage]# nodeset c3 osimage=opa
i04r02c03s01: netboot rhels7.4-x86_64-compute
i04r02c03s02: netboot rhels7.4-x86_64-compute
i04r02c03s03: netboot rhels7.4-x86_64-compute
i04r02c03s04: netboot rhels7.4-x86_64-compute
i04r02c03s05: netboot rhels7.4-x86_64-compute
i04r02c03s06: netboot rhels7.4-x86_64-compute
i04r02c03s07: netboot rhels7.4-x86_64-compute
i04r02c03s08: netboot rhels7.4-x86_64-compute
i04r02c03s09: netboot rhels7.4-x86_64-compute
i04r02c03s10: netboot rhels7.4-x86_64-compute
i04r02c03s11: netboot rhels7.4-x86_64-compute
i04r02c03s12: netboot rhels7.4-x86_64-compute
[root@mgt39 hpl_hugepage]# rsetboot c3 net -u
i04r02c03s01: Network
i04r02c03s08: Network
i04r02c03s03: Network
i04r02c03s07: Network
i04r02c03s04: Network
i04r02c03s05: Network
i04r02c03s10: Network
i04r02c03s12: Network
i04r02c03s02: Network
i04r02c03s09: Network
i04r02c03s11: Network
i04r02c03s06: Network
[root@mgt39 hpl_hugepage]# rpower c3 reset

[root@mgt39 hpl_hugepage]# psh c3 cat /proc/meminfo | grep HugePages_ |xcoll
====================================
c3
====================================
HugePages_Total:      80
HugePages_Free:       80
HugePages_Rsvd:        0
HugePages_Surp:        0

```
## update the yum repo and install necessary packages 


```
[root@mgt39 hpl_hugepage]# pscp /root/lrz.repo c3:/etc/yum.repos.d/

[root@mgt39 hpl_hugepage]# xdsh c3 /root/hpl_hugepage/setup_node

```
## simple xhpl runing 

```
[root@mgt39 hpl_hugepage]# xdsh c3  /root/hpl_hugepage/run_hpl |tee single.out
i04r02c03s08: i04r02c03s08.sng.lrz.de, 3.38107e+03, Fri Apr 13 15:41:00 EDT 2018
i04r02c03s11: i04r02c03s11.sng.lrz.de, 3.32246e+03, Fri Apr 13 15:41:00 EDT 2018
i04r02c03s06: i04r02c03s06.sng.lrz.de, 3.32095e+03, Fri Apr 13 15:41:00 EDT 2018
i04r02c03s07: i04r02c03s07.sng.lrz.de, 3.31955e+03, Fri Apr 13 15:41:01 EDT 2018
i04r02c03s02: i04r02c03s02.sng.lrz.de, 3.31873e+03, Fri Apr 13 15:41:00 EDT 2018
i04r02c03s09: i04r02c03s09.sng.lrz.de, 3.30877e+03, Fri Apr 13 15:41:04 EDT 2018
i04r02c03s01: i04r02c03s01.sng.lrz.de, 3.30357e+03, Fri Apr 13 15:41:02 EDT 2018
i04r02c03s10: i04r02c03s10.sng.lrz.de, 3.30447e+03, Fri Apr 13 15:41:02 EDT 2018
i04r02c03s12: i04r02c03s12.sng.lrz.de, 3.29360e+03, Fri Apr 13 15:40:58 EDT 2018
i04r02c03s04: i04r02c03s04.sng.lrz.de, 3.29047e+03, Fri Apr 13 15:41:01 EDT 2018
i04r02c03s03: i04r02c03s03.sng.lrz.de, 3.28987e+03, Fri Apr 13 15:41:00 EDT 2018
i04r02c03s05: i04r02c03s05.sng.lrz.de, 3.26415e+03, Fri Apr 13 15:41:00 EDT 2018

```
##  study the source code 

```
[root@mgt39 hpl_hugepage]# cat run_hpl
#!/bin/bash

cd /root/hpl_hugepage
hn=$(hostname)
dat=$(date)
da=$(echo $dat |awk '{print $4}')
export HPL_LARGEPAGE=2
#echo $hn $da hplout.$hn.$da
#exit
mpiexec.hydra -np 2 ./run.sh > hplout.$hn.$da
res=$(grep WC hplout.$hn.$da | awk '{print $7}')
echo $hn, $res, $dat

```
## run 10 loop 


```
[root@mgt39 hpl_hugepage]# xdsh c3  /root/hpl_hugepage/run_loop 10
i04r02c03s08: i04r02c03s08.sng.lrz.de, 3.36400e+03, Fri Apr 13 16:22:01 EDT 2018
i04r02c03s11: i04r02c03s11.sng.lrz.de, 3.30832e+03, Fri Apr 13 16:08:03 EDT 2018
i04r02c03s07: i04r02c03s07.sng.lrz.de, 3.30164e+03, Fri Apr 13 16:18:41 EDT 2018
i04r02c03s02: i04r02c03s02.sng.lrz.de, 3.30393e+03, Fri Apr 13 16:16:55 EDT 2018
i04r02c03s06: i04r02c03s06.sng.lrz.de, 3.29833e+03, Fri Apr 13 16:13:23 EDT 2018
i04r02c03s01: i04r02c03s01.sng.lrz.de, 3.30240e+03, Fri Apr 13 16:16:57 EDT 2018
i04r02c03s09: i04r02c03s09.sng.lrz.de, 3.30012e+03, Fri Apr 13 16:13:27 EDT 2018
i04r02c03s12: i04r02c03s12.sng.lrz.de, 3.28983e+03, Fri Apr 13 16:24:04 EDT 2018
i04r02c03s10: i04r02c03s10.sng.lrz.de, 3.27476e+03, Fri Apr 13 16:11:38 EDT 2018
i04r02c03s03: i04r02c03s03.sng.lrz.de, 3.27668e+03, Fri Apr 13 16:24:07 EDT 2018
i04r02c03s04: i04r02c03s04.sng.lrz.de, 3.26847e+03, Fri Apr 13 16:22:22 EDT 2018
i04r02c03s05: i04r02c03s05.sng.lrz.de, 3.25767e+03, Fri Apr 13 16:11:39 EDT 2018

```

