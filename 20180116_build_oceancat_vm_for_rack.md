#  2018-01-16 Oceancat Management server  create with KVM 
---
### 1 : install the VM with minimal installation options 
### 2 : configure the yum repocitory , then yum groupinstall "Server with GUI" -y
```
mkdir /tmp/install
mount -o loop ./rhel-server-7.4-x86_64-dvd.iso  /tmp/install/
vi /etc/yum.repos.d/local.repo
yum groupinstall "Server with GUI" -y

```
example of yum repocitory configure
```
[root@base ~]# cat /etc/yum.repos.d/local.repo
[base]
name=rhels74
baseurl=file:///tmp/install/
enabled=1
gpgcheck=0

```
### 3 : boot the system,set hostname ,console settings as following
```
hostnamectl set-hostname oc1.cluster
getenforce  ===set to disable
systemctl status firewall
```
### 4 : disable the virbr0 
```
yum install *bin/virsh -y
virsh net-destroy default
virsh net-undefine default
```
### 5 : enable the "virsh console oc1 " function to the virtual machine 
```
[root@base ~]# cat /etc/sysconfig/grub
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
GRUB_DEFAULT=saved
GRUB_DISABLE_SUBMENU=true
GRUB_TERMINAL_OUTPUT="console"
GRUB_CMDLINE_LINUX="rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet console=ttyS0,115200n8r"
GRUB_DISABLE_RECOVERY="true"

vi /etc/sysconfig/grub
grub2-mkconfig -o /boot/grub2/grub.cfg
```
### 6 : enable the Gnome auto Login 
```
[root@base ~]# cat /etc/gdm/custom.conf
# GDM configuration storage

[daemon]
AutomaticLogin=root
AutomaticLoginEnable=True


[security]

[xdmcp]

[chooser]

[debug]
# Uncomment the line below to turn on debugging
#Enable=true


```
### 7: configure the network settings

```
nmcli connection add con-name eth0 ifname eth0 type ethernet autoconnect yes ip4 192.168.122.20/24
nmcli connection add con-name ens8 ifname ens8 type ethernet autoconnect yes ip4 172.20.0.1/16 ip4 172.29.0.1/16 ip4 172.30.0.1/16

```
 example of the output should look likes
```
[root@oc1 ~]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 52:00:00:74:11:11 brd ff:ff:ff:ff:ff:ff
    inet 192.168.122.20/24 brd 192.168.122.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::aff:6bee:7ce3:d24b/64 scope link
       valid_lft forever preferred_lft forever
3: ens8: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN qlen 1000
    link/ether 90:e2:ba:78:f5:55 brd ff:ff:ff:ff:ff:ff
    inet 172.20.0.1/16 brd 172.20.255.255 scope global ens8
       valid_lft forever preferred_lft forever
    inet 172.29.0.1/16 brd 172.29.255.255 scope global ens8
       valid_lft forever preferred_lft forever
    inet 172.30.0.1/16 brd 172.30.255.255 scope global ens8
       valid_lft forever preferred_lft forever
    inet6 fe80::ad3f:8620:5ed9:ac25/64 scope link tentative
       valid_lft forever preferred_lft forever

```
### 8 xCAT installations
[Lenovo xCAT 17E link is ](https://hpc.lenovo.com/downloads/latest/xcat-2.13.7.lenovo2_confluent-1.7.2_lenovo-confluent-0.7.1-el7.tar.bz2https://hpc.lenovo.com/downloads/latest/xcat-2.13.7.lenovo2_confluent-1.7.2_lenovo-confluent-0.7.1-el7.tar.bz2)
```
[root@oc1 ~]# tar  jxvf xcat-2.13.7.lenovo2_confluent-1.7.2_lenovo-confluent-0.7.1-el7.tar.bz2
[root@oc1 lenovo-hpc-el7]# bash mklocalrepo.sh
[root@oc1 lenovo-hpc-el7]# cat /etc/yum.repos.d/
lenovo-hpc.repo  local.repo       redhat.repo
[root@oc1 lenovo-hpc-el7]# cat /etc/yum.repos.d/lenovo-hpc.repo
[lenovo-hpc]
name=Lenovo recommended packages for HPC
baseurl=file:///root/lenovo-hpc-el7
enabled=1
gpgcheck=1
gpgkey=file:///root/lenovo-hpc-el7/lenovohpckey.pub
[root@oc1 lenovo-hpc-el7]#



```
start to install the xCAT and confluent packages

```
yum install xCAT.x86_64 lenovo-confluent confluent_* -y
[root@oc1 ~]# source /etc/profile.d/xcat.sh
```
verify the installations is ok or not 
```
[root@oc1 ~]# tabdump site
#key,value,comments,disable
"blademaxp","64",,
"domain","cluster",,
"fsptimeout","0",,
"installdir","/install",,
"ipmimaxp","64",,
"ipmiretries","3",,
"ipmitimeout","2",,
"consoleondemand","no",,
"master","192.168.122.20",,
"nameservers","192.168.122.20",,
"maxssh","8",,
"ppcmaxp","64",,
"ppcretry","3",,
"ppctimeout","0",,
"powerinterval","0",,
"syspowerinterval","0",,
"sharedtftp","1",,
"SNsyncfiledir","/var/xcat/syncfiles",,
"nodesyncfiledir","/var/xcat/node/syncfiles",,
"tftpdir","/tftpboot",,
"xcatdport","3001",,
"xcatiport","3002",,
"xcatconfdir","/etc/xcat",,
"timezone","US/Eastern",,
"useNmapfromMN","no",,
"enableASMI","no",,
"db2installloc","/mntdb2",,
"databaseloc","/var/lib",,
"sshbetweennodes","ALLGROUPS",,
"dnshandler","ddns",,
"vsftp","n",,
"cleanupxcatpost","no",,
"dhcplease","43200",,
"auditnosyslog","0",,
"xcatsslversion","TLSv1",,
"auditskipcmds","ALL",,

```

### 9 : restore the default tables settings (very import to all of us)
```
[root@oc1 ~]# cd /opt/xcat/share/xcat/templates/e1350/
[root@oc1 e1350]# for a in *csv; do tabrestore $a; echo $a; done
chain.csv
hosts.csv
ipmi.csv
mp.csv
nodehm.csv
nodepos.csv
noderes.csv
nodetype.csv
passwd.csv
servicenode.csv
switch.csv
[root@oc1 e1350]#
### 10 : build the osimage for future use
```
[root@oc1 ~]# copycds rhel-server-7.4-x86_64-dvd.iso
Copying media to /install/rhels7.4/x86_64
Media copy operation successful
[root@oc1 ~]# lsdef -t osimage
rhels7.4-x86_64-install-compute  (osimage)
rhels7.4-x86_64-install-service  (osimage)
rhels7.4-x86_64-netboot-compute  (osimage)
rhels7.4-x86_64-stateful-mgmtnode  (osimage)
rhels7.4-x86_64-statelite-compute  (osimage)
```

### 11 : xCAT site Table configure example
```
[root@oc1 ~]# chtab key=domain site.value=cluster
[root@oc1 ~]# chtab key=dhcpinterfaces site.value=ens8
[root@oc1 ~]# chtab key=nameservers site.value=172.20.0.1
[root@oc1 ~]# chtab key=master site.value=oc1

```
### 12 : xCAT networks Table configure example
```
```
### 13 : xCAT networks Table configure example
```
```

### 14 : xCAT networks Table configure example
```
```
### 15 : xCAT networks Table configure example
```
```
### 16 : xCAT networks Table configure example
```
```
