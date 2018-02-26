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
[root@node01 ~]# chdef  -t osimage myopa74 pkglist=/opt/xcat/share/xcat/netboot/rh/compute.rhels7.x86_64.myopa74.pkglist

[root@node01 ~]# chdef -t osimage myopa74 pkglist=/opt/xcat/share/xcat/netboot/rh/compute.rhels7.x86_64.myopa74.pkglist
1 object definitions have been created or modified.
[root@node01 ~]# chdef -t osimage myopa74 rootimgdir=/install/netboot/rhels7.4/x86_64/myopa74
1 object definitions have been created or modified.
[root@node01 ~]# mkdir -p /install/netboot/rhels7.4/x86_64/myopa74

``` 
#### [compute.rhels7.x86_64.myopa74.pkglist](https://github.com/824380210/xcat_book/blob/master/compute.rhels7.x86_64.myopa74.pkglist)
###  build the custom osimage with special settings 
