# 1 : 17E  BR  default did not support the NVME SSD ,so when use the xCAT to OS install ,it will failed in find the HDD
# 2 : update the /install/autoinst/nodexx configure file as follwoing ,and retry the os provisioning 
```
[root@stark21 peter]# nl /install/autoinst/node029 | grep -B3 nvme0n1

   446  # Cannot find proper disk for OS install, select the default one "/dev/sda"
   447  if [ -z "$install_disk" ]; then
   448      install_disk="/dev/nvme0n1"
[root@stark21 peter]#

```
---

# 3 some info of the NVME SSD discovery by the diskless image load 
```
[root@stark21 postscripts]# psh node029-node032 fdisk -l | grep /dev
node029: Disk /dev/nvme0n1: 800.2 GB, 800166076416 bytes, 1562824368 sectors
node030: Disk /dev/nvme0n1: 800.2 GB, 800166076416 bytes, 1562824368 sectors
node032: Disk /dev/nvme0n1: 800.2 GB, 800166076416 bytes, 1562824368 sectors
node031: Disk /dev/nvme0n1: 800.2 GB, 800166076416 bytes, 1562824368 sectors
```
# 4 

```
 modprobe nvme

```
