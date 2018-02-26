# netboot image build for the  OPA networks 
### 1: OS install with the rhels7.4-x86_64-install-compute osimage 
### 2: yum groupinstall "Server with GUI" -y
### 3: download the lastest xCAT version
```
  wget https://xcat.org/files/xcat/xcat-core/2.13.x_Linux/xcat-core/xcat-core-2.13.10-linux.tar.bz2
  wget https://xcat.org/files/xcat/xcat-dep/2.x_Linux/xcat-dep-2.13.10-linux.tar.bz2

```
### 4: check and verify the xCAT software packages
```
[root@node02 ~]# ll xcat-core-2.13.10-linux.tar.bz2 xcat-dep-2.13.10-linux.tar.bz2
-rw-r--r-- 1 root root   4496063 Jan 26 02:36 xcat-core-2.13.10-linux.tar.bz2
-rw-r--r-- 1 root root 252230229 Jan 17 20:57 xcat-dep-2.13.10-linux.tar.bz2
[root@node02 ~]# md5sum  xcat-core-2.13.10-linux.tar.bz2 xcat-dep-2.13.10-linux.tar.bz2
e890ffc96d006e89b645d9f939c85718  xcat-core-2.13.10-linux.tar.bz2
8f2bd8deb952c471bf806f3a04fc12bd  xcat-dep-2.13.10-linux.tar.bz2
```
### 5 install  the xCAT with following command
```
[root@node01 ~]# tar xjvf xcat-core-2.13.10-linux.tar.bz2
[root@node01 ~]# tar xjvf xcat-dep-2.13.10-linux.tar.bz2

[root@node01 ~]# cd xcat-core/
[root@node01 xcat-core]# bash mklocalrepo.sh

[root@node01 ~]# cd xcat-dep/rh7/x86_64/
[root@node01 x86_64]# bash mklocalrepo.sh
[root@node01 x86_64]# yum install xCAT -y

```
### 6: Verify the xCAT installation result 
```
[root@node01 x86_64]# source /etc/profile.d/xcat.sh
[root@node01 x86_64]# tabdump site

```

### 7: load the default xCAT tables 
```

[root@node01 ~]# cd /opt/xcat/share/xcat/templates/e1350/
[root@node01 e1350]# for a in *csv; do tabrestore $a; done

```

### 8: copycds to build the default osimage 
```

[root@node01 ~]# ls rhel-server-7.4-x86_64-dvd.iso
rhel-server-7.4-x86_64-dvd.iso
[root@node01 ~]# copycds rhel-server-7.4-x86_64-dvd.iso
Copying media to /install/rhels7.4/x86_64
Media copy operation successful
[root@node01 ~]#

[root@node01 ~]# lsdef -t osimage
rhels7.4-x86_64-install-compute  (osimage)
rhels7.4-x86_64-install-service  (osimage)
rhels7.4-x86_64-netboot-compute  (osimage)
rhels7.4-x86_64-stateful-mgmtnode  (osimage)
rhels7.4-x86_64-statelite-compute  (osimage)


```
 
### 9: create the custom osimage
```
[root@node01 ~]# lsdef -t osimage -z rhels7.4-x86_64-netboot-compute | sed  's/^[^ ]\+:/myopa74:/' |mkdef -z
1 object definitions have been created or modified.
[root@node01 ~]# chdef -t osimage myopa74 pkglist=/opt/xcat/share/xcat/netboot/rh/compute.rhels7.x86_64.myopa74.pkglist
1 object definitions have been created or modified.
[root@node01 ~]# chdef -t osimage myopa74 rootimgdir=/install/netboot/rhels7.4/x86_64/myopa74
1 object definitions have been created or modified.
[root@node01 ~]# mkdir -p /install/netboot/rhels7.4/x86_64/myopa74

``` 
#### [compute.rhels7.x86_64.myopa74.pkglist](https://github.com/824380210/xcat_book/blob/master/compute.rhels7.x86_64.myopa74.pkglist)
###  10:  build the custom osimage with special settings 
```
[root@node01 ~]# genimage myopa74
Generating image:
cd /opt/xcat/share/xcat/netboot/rh; ./genimage -a x86_64 -o rhels7.4 -p compute --srcdir "/install/rhels7.4/x86_64" --pkglist /opt/xcat/share/xcat/netboot/rh/compute.rhels7.x86_64.myopa74.pkglist --otherpkgdir "/install/post/otherpkgs/rhels7.4/x86_64" --postinstall /opt/xcat/share/xcat/netboot/rh/compute.rhels7.x86_64.postinstall --rootimgdir /install/netboot/rhels7.4/x86_64/myopa74 --tempfile /tmp/xcat_genimage.12936 myopa74
210 blocks
/opt/xcat/share/xcat/netboot/rh
210 blocks
/opt/xcat/share/xcat/netboot/rh
 yum -y -c /tmp/genimage.12942.yum.conf --installroot=/install/netboot/rhels7.4/x86_64/myopa74/rootimg/ --disablerepo=* --enablerepo=rhels7.4-x86_64-0 --enablerepo=rhels7.4-x86_64-1 --enablerepo=rhels7.4-x86_64-2  install  bash dracut-network nfs-utils openssl dhclient kernel openssh-server openssh-clients iputils bc irqbalance procps-ng wget vim-minimal ntp rpm rsync rsyslog e2fsprogs parted net-tools gzip tar xz yum pciutils gtk2 atk cairo gcc-gfortran tcsh lsof tcl tk usbutils kernel-devel gcc-c++ tmux screen libnl3 ethtool libxml2-python dmidecode ipmitool vim util-linux file
Resolving Dependencies
--> Running transaction check
---> Package atk.x86_64 0:2.22.0-3.el7 will be installed
--> Processing Dependency: /sbin/ldconfig for package: atk-2.22.0-3.el7.x86_64
--> Processing Dependency: /sbin/ldconfig for package: atk-2.22.0-3.el7.x86_64
--> Processing Dependency: rtld(GNU_HASH) for package: atk-2.22.0-3.el7.x86_64
--> Processing Dependency: libc.so.6(GLIBC_2.4)(64bit) for package: atk-2.22.0-3.el7.x86_64
--> Processing Dependency: libglib-2.0.so.0()(64bit) for package: atk-2.22.0-3.el7.x86_64
...
....
.....
....
Complete!
Enter the dracut mode. Dracut version: 033. Dracut directory: dracut_033.
Try to load drivers: tg3 bnx2 bnx2x e1000 e1000e igb mlx_en virtio_net be2net ext3 ext4 to initrd.
chroot /install/netboot/rhels7.4/x86_64/myopa74/rootimg dracut  -f /tmp/initrd.12942.gz 3.10.0-693.el7.x86_64
No '/dev/log' or 'logger' included for syslog logging
Turning off host-only mode: '/sys' is not mounted!
Turning off host-only mode: '/proc' is not mounted!
Turning off host-only mode: '/run' is not mounted!
Turning off host-only mode: '/dev' is not mounted!
grep: /etc/udev/rules.d/*: No such file or directory
Failed to install module mlx_en
the initial ramdisk for stateless is generated successfully.
Try to load drivers: tg3 bnx2 bnx2x e1000 e1000e igb mlx_en virtio_net be2net ext3 ext4 to initrd.
chroot /install/netboot/rhels7.4/x86_64/myopa74/rootimg dracut  -f /tmp/initrd.12942.gz 3.10.0-693.el7.x86_64
No '/dev/log' or 'logger' included for syslog logging
Turning off host-only mode: '/sys' is not mounted!
Turning off host-only mode: '/proc' is not mounted!
Turning off host-only mode: '/run' is not mounted!
Turning off host-only mode: '/dev' is not mounted!
grep: /etc/udev/rules.d/*: No such file or directory
Failed to install module mlx_en
the initial ramdisk for statelite is generated successfully.



```


###  11: update the myopa74 osimage with the OPA IFS package pre-requirement  
```

yum install opensm-libs -y
yum install libibmad libibcm ibacm atlas expect qperf perftest infinipath-psm opensm-libs papi elfutils-libelf-devel sysfsutils -y
yum install  rdma-core-devel -y



```
####  above RPM Packages should be fixed in the File [  compute.rhels7.x86_64.myopa74.pkglist  ]

### 12: install the IFS package in the diskless image 

```

[root@node01 ~]# mount -o bind /sys /install/netboot/rhels7.4/x86_64/myopa74/rootimg/sys/
[root@node01 ~]# mount -o bind /proc/ /install/netboot/rhels7.4/x86_64/myopa74/rootimg/proc/
[root@node01 ~]# mount -o bind /dev/ /install/netboot/rhels7.4/x86_64/myopa74/rootimg/dev
[root@node01 ~]# chroot /install/netboot/rhels7.4/x86_64/myopa74/rootimg/
##

[root@node01 /]# cd root/
[root@node01 ~]# cd IntelOPA-IFS.RHEL74-x86_64.10.6.1.0.2/
[root@node01 IntelOPA-IFS.RHEL74-x86_64.10.6.1.0.2]# ./IntelOPA-
IntelOPA-FM.RHEL74-x86_64.10.6.1.0.2/         IntelOPA-OFED_DELTA.RHEL74-x86_64.10.6.1.0.2/ IntelOPA-Tools-FF.RHEL74-x86_64.10.6.1.0.2/
[root@node01 IntelOPA-IFS.RHEL74-x86_64.10.6.1.0.2]# ./INSTALL -a
Installing All OPA Software
Determining what is installed on system...
...
...
...
Installing Pre-Boot Components 10_6_1_0_2 release...
installing hfi1-uefi-1.6.0.0-0.x86_64...
Enabling autostart for OFA OPA Stack (opa)
-------------------------------------------------------------------------------
A System Reboot is recommended to activate the software changes
Done Installing OPA Software.
Rebuilding boot image with "/usr/bin/dracut -f"...Turning off host-only mode: '/run' is not mounted!

Failed to install module mlx_en
done.
##

[root@node01 IntelOPA-IFS.RHEL74-x86_64.10.6.1.0.2]# exit
exit
[root@node01 ~]# umount  /install/netboot/rhels7.4/x86_64/myopa74/rootimg/dev
[root@node01 ~]# umount  /install/netboot/rhels7.4/x86_64/myopa74/rootimg/proc
[root@node01 ~]# umount  /install/netboot/rhels7.4/x86_64/myopa74/rootimg/sys
##
```

### 13 pack the diskless image and verify in the compute node 

