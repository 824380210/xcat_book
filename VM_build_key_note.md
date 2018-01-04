### 1： 用virt-manager创建虚拟机，最小化安装，200G，QCOW2格式
### 2： 配置好yum内部源
### 3： virsh console 可用配置，与grub.conf相关
```
 1027  qemu-img convert -O qcow2 /data4/myrhels74minimal.qcow2 /data4/mybase.qcow2
 1033  cp mybase.qcow2 mybase_rhels7.4-minimal.qcow2
 1034  md5sum mybase_rhels7.4-minimal.qcow2
 
[root@test data4]# md5sum mybase.qcow2
be9f76ba700f2e7e1a9feb7477c5720f  mybase.qcow2
[root@test data4]# cp mybase.qcow2 mybase_rhels7.4-minimal.qcow2
[root@test data4]# md5sum mybase_rhels7.4-minimal.qcow2
be9f76ba700f2e7e1a9feb7477c5720f  mybase_rhels7.4-minimal.qcow2

[root@mgt1 ~]# cat /etc/yum.repos.d/local.repo
[base]
name=rhels7.4
baseurl=http://172.16.0.254/rhels7.4/
enabled=1
gpgcheck=0


[root@mgt1 ~]# cat /etc/sysconfig/grub
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
GRUB_DEFAULT=saved
GRUB_DISABLE_SUBMENU=true
GRUB_TERMINAL_OUTPUT="console"
GRUB_CMDLINE_LINUX="rd.lvm.lv=rhel/root rd.lvm.lv=rhel/swap rhgb quiet console=ttyS0,115200"
GRUB_DISABLE_RECOVERY="true"
[root@mgt1 ~]#
   2  vi /etc/yum.repos.d/local.repo
  10  vi /etc/sysconfig/grub
  11  grub2-mkconfig -o /boot/grub2/grub.cfg



```
### 4 生成新的虚拟机

```
[root@test 17E]# lspci | grep I350
10:00.0 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
10:00.1 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
10:00.2 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
10:00.3 Ethernet controller: Intel Corporation I350 Gigabit Network Connection (rev 01)
[root@test 17E]#  virsh nodedev-list --tree | grep -B4 10_00
  |       +- net_ib0_80_00_00_02_fe_80_00_00_00_00_00_00_00_11_75_01_01_74_73_d3
  |
  +- pci_0000_00_03_0
  |   |
  |   +- pci_0000_10_00_0
  |   |   |
  |   |   +- net_ens4f0_a0_36_9f_be_a5_68
  |   |
  |   +- pci_0000_10_00_1
  |   |   |
  |   |   +- net_ens4f1_a0_36_9f_be_a5_69
  |   |
  |   +- pci_0000_10_00_2
  |   |   |
  |   |   +- net_ens4f2_a0_36_9f_be_a5_6a
  |   |
  |   +- pci_0000_10_00_3


[root@test 17E]# virt-install -n 17E_base --ram 16384  --vcpus=8,maxvcpus=16 --disk path=/data4/mybase_rhels7.4-minimal.qcow2  --os-type=linux --noreboot --os-variant=rhel7 --network bridge=br0,mac=52:52:17:EE:17:01  --graphics spice --host-device pci_0000_10_00_1 --import &
[1] 2177
[root@test 17E]# WARNING  Unable to connect to graphical console: virt-viewer not installed. Please install the 'virt-viewer' package.
WARNING  No console to launch for the guest, defaulting to --wait -1

Starting install...
Creating domain...                                                                                                                    |    0 B  00:00:00
Domain creation completed.
You can restart your domain by running:
  virsh --connect qemu:///system start 17E_base

[1]+  Done                    virt-install -n 17E_base --ram 16384 --vcpus=8,maxvcpus=16 --disk path=/data4/mybase_rhels7.4-minimal.qcow2 --os-type=linux --noreboot --os-variant=rhel7 --network bridge=br0,mac=52:52:17:EE:17:01 --graphics spice --host-device pci_0000_10_00_1 --import
[root@test 17E]#

[root@test 17E]# virsh start 17E_base
Domain 17E_base started

[root@test 17E]# virsh console 17E_base
Connected to domain 17E_base
Escape character is ^]

Red Hat Enterprise Linux Server 7.4 (Maipo)
Kernel 3.10.0-693.el7.x86_64 on an x86_64

mgt1 login: root
Password:
Last failed login: Thu Jan  4 01:25:25 EST 2018 on ttyS0
There was 1 failed login attempt since the last successful login.
Last login: Thu Jan  4 00:45:33 on ttyS0
[root@mgt1 ~]#
[root@mgt1 ~]#
[root@mgt1 ~]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 52:52:17:ee:17:01 brd ff:ff:ff:ff:ff:ff
3: ens8: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN qlen 1000
    link/ether a0:36:9f:be:a5:69 brd ff:ff:ff:ff:ff:ff
[root@mgt1 ~]#


```
### 5 安装图形GUI和IP 默认设置,xCAT 安装
```

[root@mgt1 ~]# cat /etc/gdm/custom.conf
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

[root@mgt1 ~]# history
   17  ip address add dev eth0 172.16.0.17/24
   18  yum groupinstall  "Server with GUI" -y
   19  vim /etc/gdm/custom.conf
   20  cat /etc/gdm/custom.conf
[root@mgt1 ~]#

[root@mgt1 ~]# cat /etc/gdm/custom.conf
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
### 6 IP设置
```
   30  nmcli connection delete eth0
   31  nmcli connection add con-name eth0 ifname eth0 autoconnect yes type ethernet  ip4 172.16.0.91/24
   35  nmcli connection add con-name ens8 ifname ens8 autoconnect yes type ethernet ip4 172.20.0.1/16 ip4 172.29.0.1/16 ip4 172.30.0.1/16
[root@mgt1 ~]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 52:52:17:ee:17:01 brd ff:ff:ff:ff:ff:ff
    inet 172.16.0.91/24 brd 172.16.0.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::7f42:f9c8:b788:a62f/64 scope link
       valid_lft forever preferred_lft forever
3: ens8: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN qlen 1000
    link/ether a0:36:9f:be:a5:69 brd ff:ff:ff:ff:ff:ff
    inet 172.20.0.1/16 brd 172.20.255.255 scope global ens8
       valid_lft forever preferred_lft forever
    inet 172.29.0.1/16 brd 172.29.255.255 scope global ens8
       valid_lft forever preferred_lft forever
    inet 172.30.0.1/16 brd 172.30.255.255 scope global ens8
       valid_lft forever preferred_lft forever
    inet6 fe80::15c2:707b:47e6:8de2/64 scope link tentative
       valid_lft forever preferred_lft forever
4: virbr0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN qlen 1000
    link/ether 52:54:00:47:b9:5d brd ff:ff:ff:ff:ff:ff
    inet 192.168.122.1/24 brd 192.168.122.255 scope global virbr0
       valid_lft forever preferred_lft forever
5: virbr0-nic: <BROADCAST,MULTICAST> mtu 1500 qdisc pfifo_fast master virbr0 state DOWN qlen 1000
    link/ether 52:54:00:47:b9:5d brd ff:ff:ff:ff:ff:ff
[root@mgt1 ~]#


```
### 7  xCAT安装到17E版本
```
   39  vim /etc/yum.repos.d/xCAT.repo
   40  yum install xCAT -y
   41  yum install confluent* -y
   42  source /etc/profile.d/xcat.sh
   43  tabdump site
   50  cd /opt/xcat/share/xcat/templates/e1350/
   51  for a in *csv; do tabrestore $a; echo $a; done
   52  tabdump chain
[root@mgt1 ~]# cat /etc/yum.repos.d/xCAT.repo
[xCAT_17E]
name=xCAT_17E
baseurl=http://172.16.0.254/xcat/17E
enabled=1
gpgcheck=0
[root@mgt1 ~]#

```

