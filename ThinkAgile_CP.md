# 1 : prepare the VM for as a test server (or L1 Server )
#### a: install the VM with 8G memory and 40G hdd ,minimal install with default network NAT to connect to the Host Linux
#### b: update the yum for software update (tftp/dhcp/http/vim/...)
```
vi /etc/yum.repos.d/local.repo
yum install xinetd -y
yum install tftp-server -y
yum install tftp -y
yum install dhcp -y
yum install httpd -y
systemctl enable dhcpd
systemctl enable httpd
systemctl enabled xinetd
chkconfig xinetd on
vi /etc/xinetd.d/tftp
yum install vim -y
vim /etc/sysconfig/grub
vim /etc/sysconfig/grub
grub2-mkconfig -o /boot/grub2/grub.cfg
vim /etc/sysconfig/network-scripts/ifcfg-eth0

```
#### c: some output example for verify above command
```
# check the yum repo
[root@thinkagile_cp ~]# cat /etc/yum.repos.d/local.repo
[base7.5]
name=rhels7.5
baseurl=http://192.168.122.1/rhels7.5/
enabled=1
gpgcheck=0

# check the rpm that have been install 
[root@thinkagile_cp ~]# rpm -aq | grep -E 'tftp|xinetd|dhcp|httpd|vim'
tftp-server-5.2-22.el7.x86_64
dhcp-4.2.5-68.el7.x86_64
vim-common-7.4.160-4.el7.x86_64
vim-enhanced-7.4.160-4.el7.x86_64
dhcp-libs-4.2.5-68.el7.x86_64
xinetd-2.3.15-13.el7.x86_64
tftp-5.2-22.el7.x86_64
httpd-tools-2.4.6-80.el7.x86_64
vim-minimal-7.4.160-4.el7.x86_64
httpd-2.4.6-80.el7.x86_64
vim-filesystem-7.4.160-4.el7.x86_64
dhcp-common-4.2.5-68.el7.x86_64

# check the service that enable when system boot
[root@thinkagile_cp ~]# cat /etc/xinetd.d/tftp
# default: off
# description: The tftp server serves files using the trivial file transfer \
#       protocol.  The tftp protocol is often used to boot diskless \
#       workstations, download configuration files to network-aware printers, \
#       and to start the installation process for some operating systems.
service tftp
{
        socket_type             = dgram
        protocol                = udp
        wait                    = yes
        user                    = root
        server                  = /usr/sbin/in.tftpd
        server_args             = -s /var/lib/tftpboot
        disable                 = no
        per_source              = 11
        cps                     = 100 2
        flags                   = IPv4
}

#
[root@thinkagile_cp ~]# systemctl is-enabled xinetd
enabled
[root@thinkagile_cp ~]# systemctl is-enabled httpd
enabled
[root@thinkagile_cp ~]# systemctl is-enabled dhcpd
enabled
[root@thinkagile_cp ~]#




```
# dhcpd.conf example 
```
default-lease-time 600;
max-lease-time 7200;
#log-facility local7;
subnet 172.20.0.0 netmask 255.255.0.0 {
    max-lease-time 43200;
    min-lease-time 43200;
    default-lease-time 43200;
    option routers  172.20.0.1;
    next-server  172.20.0.1;
    option domain-name "cluster";
    option domain-name-servers  172.20.0.1;
    option domain-search  "cluster";
 #   filename "gpxelinux.0";
    range dynamic-bootp 172.20.255.1 172.20.255.254;
}

```

# test the DHCP service 
```
1: put you labtop RJ45 port to the switch which have a ethernet connect to the VM
2: verify the labtop if it can obtail the IP from the VM or not 

```

# test the tftp service 
```
# create a file in the /var/lib/tftpboot directory or other directory that tftp service should be access 
# the default tftp chroot directory is define in /etc/xinetd.d/tftp and you can change it base on your need 

[root@thinkagile_cp ~]# echo `date` >/var/lib/tftpboot/test_date
[root@thinkagile_cp ~]# md5sum /var/lib/tftpboot/test_date
18909c1732e4b2a7677304dff4c1fe42  /var/lib/tftpboot/test_date

# make sure current directory without the target file ,here the target file test_date
[root@thinkagile_cp ~]# pwd
/root
[root@thinkagile_cp ~]# ls test_date*
ls: cannot access test_date*: No such file or directory

# download the target file and check
[root@thinkagile_cp ~]# tftp localhost -c get test_date
[root@thinkagile_cp ~]# ls test_date*
test_date
[root@thinkagile_cp ~]# md5sum test_date
18909c1732e4b2a7677304dff4c1fe42  test_date
[root@thinkagile_cp ~]#


```
