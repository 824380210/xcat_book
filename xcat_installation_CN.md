### Downlaod the xCAT Packages
```
wget https://xcat.org/files/xcat/xcat-core/2.13.x_Linux/xcat-core/xcat-core-2.13.8-linux.tar.bz2
wget https://xcat.org/files/xcat/xcat-dep/2.x_Linux/xcat-dep-2.13.8-linux.tar.bz2
```
### Markdown the Package MD5 values
```

ot@test xcat2138]# md5sum xcat-core-2.13.8-linux.tar.bz2 xcat-dep-2.13.8-linux.tar.bz2
947bb8387b02a13a35d021faaabc582f  xcat-core-2.13.8-linux.tar.bz2
6ed4c1f9ae2e7d83b1d52bab776a40c1  xcat-dep-2.13.8-linux.tar.bz2


```
### extract the xcat packages
```
[root@test xcat2138]# tar xjvf xcat-core-2.13.8-linux.tar.bz2
[root@test xcat2138]# tar xjvf xcat-dep-2.13.8-linux.tar.bz2
```
