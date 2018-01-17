#  2018-01-16 Oceancat Management server  create with KVM 

--

1 : install the VM with minimal installation options 
2 : configure the yum repocitory , then yum groupinstall "Server with GUI" -y
```
mkdir /tmp/install
mount -o loop ./rhel-server-7.4-x86_64-dvd.iso  /tmp/install/
vim /etc/yum.repos.d/local.repo
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
3 : boot the system,set hostnamename ,console settings as following
```
hostnamectl set-hostname oc1.cluster
getenforce  ===set to disable
systemctl status firewall
4 : disable the virbr0 
```
yum install *bin/virsh -y
virsh net-destroy default
virsh net-undefine default
```
5 : enable the "virsh console xxx " function to the virtual machine 
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
6 : enable the Gnome auto Login 
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
