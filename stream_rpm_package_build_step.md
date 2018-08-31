## 安装RPM包所需要的环境

```
[root@mgt ~]# yum install *bin/rpmbuild



```

## 创建所需要的rpmbuild目录，注意执行命令的先后顺序 

```
[root@mgt ~]# cat .rpmmacros
%_topdir    /root/rpmbuild
[root@mgt ~]#
# 注意上面不要用变量代替实际路径，如~，$HOM这样，系统处理不好


[root@mgt ~]# rpmbuild /dev/null
error: File /dev/null is not a regular file.
# 上面这条命令的目的就是创建一个rpmbuild目录，及它对应下面的子目录
[root@mgt ~]# ls
code  local.repo  mlxfwmanager_LeSI_18B_OFED_4.4-1_build2  rpmbuild  stark1.cmos  stark2.cmos
[root@mgt ~]# ls -lF rpmbuild/
total 0
drwxr-xr-x 2 root root 6 Aug 30 12:28 BUILD/
drwxr-xr-x 2 root root 6 Aug 30 12:28 BUILDROOT/
drwxr-xr-x 2 root root 6 Aug 30 12:28 RPMS/
drwxr-xr-x 2 root root 6 Aug 30 12:28 SOURCES/
drwxr-xr-x 2 root root 6 Aug 30 12:28 SPECS/
drwxr-xr-x 2 root root 6 Aug 30 12:28 SRPMS/


其实你也可以通过下面的命令来创建
mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
```

# 生成tar.gz源包

```
[root@node01 ~]# tar -czvf stream_skylake-1.0.tar.tz stream_skylake-1.0/
stream_skylake-1.0/
stream_skylake-1.0/run_mystream_skylake.sh
stream_skylake-1.0/stream_simple_example
stream_skylake-1.0/stream_example
stream_skylake-1.0/build_stream_scripts.sh
stream_skylake-1.0/run_stream.sh
stream_skylake-1.0/stream_skylake.sh
stream_skylake-1.0/stream_c_skylake.exe
stream_skylake-1.0/libsvml.so
stream_skylake-1.0/libirng.so
stream_skylake-1.0/libiomp5.so
stream_skylake-1.0/libintlc.so.5
stream_skylake-1.0/libimf.so
stream_skylake-1.0/copy_library.sh
[root@node01 ~]# cp stream_skylake-1.0.tar.tz rpmbuild/
BUILD/     BUILDROOT/ RPMS/      SOURCES/   SPECS/     SRPMS/

```
# 将安装源放入/root/rpmbuild/SOURCES目录
```
其实你也可以将spec文件放入这个tar.gz的文件中
[root@node01 ~]# cp stream_skylake-1.0.tar.tz rpmbuild/SOURCES/

```
# 编辑SPEC文件

```
[root@mgt ~]# cat  stream_skylake-1.0/stream_skylake.spec
Name: stream_skylake
Version:        1.0
Release:        1%{?dist}
Summary:        stream test for skylake CPU

License:        GLPv3
URL:    https://github.com/824380210/xcat_book
Source0:        stream_skylake-1.0.tar.gz
%description
stream memory bandwidth test by pengcz1@lenovo.com 2018-08-30  LSTC
%prep
%setup
#%build
%install
install -m 0755 -d $RPM_BUILD_ROOT/usr
install -m 0755 -d $RPM_BUILD_ROOT/usr/lib64
install -m 0755 -d $RPM_BUILD_ROOT/usr/share
install -m 0755 -d $RPM_BUILD_ROOT/usr/share/doc
install -m 0755 -d $RPM_BUILD_ROOT/usr/share/doc/stream_skylake-1.0
install -m 0755  libimf.so     $RPM_BUILD_ROOT/usr/lib64/libimf.so
install -m 0755  libintlc.so.5 $RPM_BUILD_ROOT/usr/lib64/libintlc.so.5
install -m 0755  libirng.so    $RPM_BUILD_ROOT/usr/lib64/libirng.so
install -m 0755  libiomp5.so   $RPM_BUILD_ROOT/usr/lib64/libiomp5.so
install -m 0755  libsvml.so    $RPM_BUILD_ROOT/usr/lib64/libsvml.so
install -m 0755 -d $RPM_BUILD_ROOT/usr/local
install -m 0755 -d $RPM_BUILD_ROOT/usr/local/bin
install -m 0755 build_stream_scripts.sh $RPM_BUILD_ROOT/usr/local/bin/build_stream_scripts.sh
install -m 0755 copy_library.sh  $RPM_BUILD_ROOT/usr/local/bin/copy_library.sh
install -m 0755 stream_c_skylake.exe $RPM_BUILD_ROOT/usr/local/bin/stream_c_skylake.exe
install -m 0755 stream_simple_example $RPM_BUILD_ROOT/usr/share/doc/stream_skylake-1.0/stream_simple_example
install -m 0755 stream_example $RPM_BUILD_ROOT/usr/share/doc/stream_skylake-1.0/stream_example
install -m 0755 stream_skylake.sh $RPM_BUILD_ROOT/usr/share/doc/stream_skylake-1.0/stream_skylake.sh
install -m 0755 run_stream.sh  $RPM_BUILD_ROOT/usr/share/doc/stream_skylake-1.0/run_stream.sh
install -m 0755 run_mystream_skylake.sh $RPM_BUILD_ROOT/usr/share/doc/stream_skylake-1.0/run_mystream_skylake.sh

%files
/usr/lib64/libimf.so
/usr/lib64/libintlc.so.5
/usr/lib64/libirng.so
/usr/lib64/libiomp5.so
/usr/lib64/libsvml.so
%dir /usr/local/
%dir /usr/local/bin/
/usr/local/bin/build_stream_scripts.sh
/usr/local/bin/copy_library.sh
/usr/local/bin/stream_c_skylake.exe
%dir /usr/share/
%dir /usr/share/doc/
%dir /usr/share/doc/stream_skylake-1.0
/usr/share/doc/stream_skylake-1.0/stream_simple_example
/usr/share/doc/stream_skylake-1.0/stream_example
/usr/share/doc/stream_skylake-1.0/stream_skylake.sh
/usr/share/doc/stream_skylake-1.0/run_stream.sh
/usr/share/doc/stream_skylake-1.0/run_mystream_skylake.sh
%changelog
* Thu Aug 30 2018 Peter CZ Peng  <pengcz1@lenovo.com> - LSTC
- the init version of the stream


# 一些注意事项，如创建目录
# 注意%file中如果是目录，则需要在前面添加%dir 来说明，不然会有warning 
# 注意将库文件的权限为可读可执行，不然也会有问题，会提示库文件依赖关系有问题

```
# 将源文件打包成一个tar.gz文件

```
[root@mgt ~]# ls stream_skylake-1.0
build_stream_scripts.sh  libimf.so      libiomp5.so  libsvml.so               run_stream.sh         stream_example         stream_skylake.sh
copy_library.sh          libintlc.so.5  libirng.so   run_mystream_skylake.sh  stream_c_skylake.exe  stream_simple_example  stream_skylake.spec


[root@mgt ~]# tar  czvf stream_skylake-1.0.tar.gz stream_skylake-1.0/
stream_skylake-1.0/
stream_skylake-1.0/build_stream_scripts.sh
stream_skylake-1.0/copy_library.sh
stream_skylake-1.0/libimf.so
stream_skylake-1.0/libintlc.so.5
stream_skylake-1.0/libiomp5.so
stream_skylake-1.0/libirng.so
stream_skylake-1.0/libsvml.so
stream_skylake-1.0/stream_c_skylake.exe
stream_skylake-1.0/stream_skylake.sh
stream_skylake-1.0/run_stream.sh
stream_skylake-1.0/stream_example
stream_skylake-1.0/stream_simple_example
stream_skylake-1.0/run_mystream_skylake.sh
stream_skylake-1.0/stream_skylake.spec
[root@mgt ~]#


```
# 将tar.gz文件打包成rpm包

```
[root@mgt ~]# rpmbuild -tb stream_skylake-1.0.tar.gz
Executing(%prep): /bin/sh -e /var/tmp/rpm-tmp.a9O02C
+ umask 022
+ cd /root/rpmbuild/BUILD
+ cd /root/rpmbuild/BUILD
+ rm -rf stream_skylake-1.0
+ /usr/bin/gzip -dc /root/stream_skylake-1.0.tar.gz
+ /usr/bin/tar -xvvf -
drwxr-xr-x root/root         0 2018-08-30 22:11 stream_skylake-1.0/
-rwxr-xr-x root/root       944 2018-08-30 10:46 stream_skylake-1.0/build_stream_scripts.sh
-rwxr-xr-x root/root        78 2018-08-30 06:34 stream_skylake-1.0/copy_library.sh
-rwxr-xr-x root/root   3338733 2018-08-30 06:34 stream_skylake-1.0/libimf.so
-rwxr-xr-x root/root    466074 2018-08-30 06:34 stream_skylake-1.0/libintlc.so.5
-rwxr-xr-x root/root   1842818 2018-08-30 06:34 stream_skylake-1.0/libiomp5.so
-rwxr-xr-x root/root   1631796 2018-08-30 06:34 stream_skylake-1.0/libirng.so
-rwxr-xr-x root/root  14860735 2018-08-30 06:34 stream_skylake-1.0/libsvml.so
-rwxr-xr-x root/root     28552 2018-08-30 06:34 stream_skylake-1.0/stream_c_skylake.exe
-rwxr-xr-x root/root       566 2018-08-30 06:34 stream_skylake-1.0/stream_skylake.sh
-rwxr-xr-x root/root       725 2018-08-30 06:58 stream_skylake-1.0/run_stream.sh
-rwxr-xr-x root/root      5302 2018-08-30 08:37 stream_skylake-1.0/stream_example
-rwxr-xr-x root/root       762 2018-08-30 08:37 stream_skylake-1.0/stream_simple_example
-rwxr-xr-x root/root       614 2018-08-30 07:27 stream_skylake-1.0/run_mystream_skylake.sh
-rwxr-xr-x root/root      2472 2018-08-30 22:11 stream_skylake-1.0/stream_skylake.spec
+ STATUS=0
+ '[' 0 -ne 0 ']'
+ cd stream_skylake-1.0
+ /usr/bin/chmod -Rf a+rX,u+w,g-w,o-w .
+ exit 0
Executing(%install): /bin/sh -e /var/tmp/rpm-tmp.7qBZdg
+ umask 022
+ cd /root/rpmbuild/BUILD
+ '[' /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64 '!=' / ']'
+ rm -rf /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64
++ dirname /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64
+ mkdir -p /root/rpmbuild/BUILDROOT
+ mkdir /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64
+ cd stream_skylake-1.0
+ install -m 0755 -d /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr
+ install -m 0755 -d /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/lib64
+ install -m 0755 -d /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/share
+ install -m 0755 -d /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/share/doc
+ install -m 0755 -d /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/share/doc/stream_skylake-1.0
+ install -m 0755 libimf.so /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/lib64/libimf.so
+ install -m 0755 libintlc.so.5 /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/lib64/libintlc.so.5
+ install -m 0755 libirng.so /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/lib64/libirng.so
+ install -m 0755 libiomp5.so /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/lib64/libiomp5.so
+ install -m 0755 libsvml.so /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/lib64/libsvml.so
+ install -m 0755 -d /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/local
+ install -m 0755 -d /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/local/bin
+ install -m 0755 build_stream_scripts.sh /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/local/bin/build_stream_scripts.sh
+ install -m 0755 copy_library.sh /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/local/bin/copy_library.sh
+ install -m 0755 stream_c_skylake.exe /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/local/bin/stream_c_skylake.exe
+ install -m 0755 stream_simple_example /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/share/doc/stream_skylake-1.0/stream_simple_example
+ install -m 0755 stream_example /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/share/doc/stream_skylake-1.0/stream_example
+ install -m 0755 stream_skylake.sh /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/share/doc/stream_skylake-1.0/stream_skylake.sh
+ install -m 0755 run_stream.sh /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/share/doc/stream_skylake-1.0/run_stream.sh
+ install -m 0755 run_mystream_skylake.sh /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64/usr/share/doc/stream_skylake-1.0/run_mystream_skylake.sh
+ /usr/lib/rpm/check-buildroot
+ /usr/lib/rpm/redhat/brp-compress
+ /usr/lib/rpm/redhat/brp-strip /usr/bin/strip
+ /usr/lib/rpm/redhat/brp-strip-comment-note /usr/bin/strip /usr/bin/objdump
+ /usr/lib/rpm/redhat/brp-strip-static-archive /usr/bin/strip
+ /usr/lib/rpm/brp-python-bytecompile /usr/bin/python 1
+ /usr/lib/rpm/redhat/brp-python-hardlink
+ /usr/lib/rpm/redhat/brp-java-repack-jars
Processing files: stream_skylake-1.0-1.el7.x86_64
Provides: libimf.so()(64bit) libintlc.so.5()(64bit) libiomp5.so()(64bit) libiomp5.so(GOMP_1.0)(64bit) libiomp5.so(GOMP_2.0)(64bit) libiomp5.so(GOMP_3.0)(64bit) libiomp5.so(GOMP_4.0)(64bit) libiomp5.so(OMP_1.0)(64bit) libiomp5.so(OMP_2.0)(64bit) libiomp5.so(OMP_3.0)(64bit) libiomp5.so(OMP_3.1)(64bit) libiomp5.so(OMP_4.0)(64bit) libiomp5.so(VERSION)(64bit) libirng.so()(64bit) libsvml.so()(64bit) stream_skylake = 1.0-1.el7 stream_skylake(x86-64) = 1.0-1.el7
Requires(rpmlib): rpmlib(CompressedFileNames) <= 3.0.4-1 rpmlib(FileDigests) <= 4.6.0-1 rpmlib(PayloadFilesHavePrefix) <= 4.0-1
Requires: /bin/bash ld-linux-x86-64.so.2()(64bit) ld-linux-x86-64.so.2(GLIBC_2.3)(64bit) libc.so.6()(64bit) libc.so.6(GLIBC_2.11)(64bit) libc.so.6(GLIBC_2.2.5)(64bit) libc.so.6(GLIBC_2.3)(64bit) libc.so.6(GLIBC_2.3.2)(64bit) libc.so.6(GLIBC_2.3.4)(64bit) libc.so.6(GLIBC_2.4)(64bit) libc.so.6(GLIBC_2.7)(64bit) libdl.so.2()(64bit) libdl.so.2(GLIBC_2.2.5)(64bit) libgcc_s.so.1()(64bit) libimf.so()(64bit) libintlc.so.5()(64bit) libiomp5.so()(64bit) libiomp5.so(VERSION)(64bit) libirng.so()(64bit) libm.so.6()(64bit) libpthread.so.0()(64bit) libpthread.so.0(GLIBC_2.2.5)(64bit) libpthread.so.0(GLIBC_2.3.2)(64bit) libpthread.so.0(GLIBC_2.3.4)(64bit) libsvml.so()(64bit)
Checking for unpackaged file(s): /usr/lib/rpm/check-files /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64
Wrote: /root/rpmbuild/RPMS/x86_64/stream_skylake-1.0-1.el7.x86_64.rpm
Executing(%clean): /bin/sh -e /var/tmp/rpm-tmp.dSwd5C
+ umask 022
+ cd /root/rpmbuild/BUILD
+ cd stream_skylake-1.0
+ /usr/bin/rm -rf /root/rpmbuild/BUILDROOT/stream_skylake-1.0-1.el7.x86_64
+ exit 0
[root@mgt ~]#

```
# 验证生成的RPM文件

```
[root@mgt ~]# scp /root/rpmbuild/RPMS/x86_64/stream_skylake-1.0-1.el7.x86_64.rpm node07:/root/
Warning: Permanently added 'node07,172.20.101.7' (ECDSA) to the list of known hosts.
stream_skylake-1.0-1.el7.x86_64.rpm                                                                                                                                                                        100% 3904KB  85.2MB/s   00:00
[root@mgt ~]# ssh node07
[root@node07 ~]# rpm -ivh stream_skylake-1.0-1.el7.x86_64.rpm
Preparing...                          ################################# [100%]
Updating / installing...
   1:stream_skylake-1.0-1.el7         ################################# [100%]
[root@node07 ~]#

```
# 执行脚本看结果

```
[root@node07 ~]# build_stream_scripts.sh
16
CPU1 CORES is   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
CPU2 CORES is   [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
CPUS CORES is   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]


[root@node07 ~]# bash run_mystream.sh |grep Triad
Triad:          81019.5     0.035591     0.035547     0.035665
Triad:          82620.9     0.034955     0.034858     0.035269
Triad:         157241.4     0.018389     0.018316     0.018830
[root@node07 ~]#
# another example for stream ,but with different config
#
[root@node01 ~]# lscpu | grep Intel
Vendor ID:             GenuineIntel
Model name:            Intel(R) Xeon(R) Platinum 8176 CPU @ 2.10GHz
[root@node01 ~]# rpm -ivh stream_skylake-1.0-1.el7.x86_64.rpm
Preparing...                          ################################# [100%]
        package stream_skylake-1.0-1.el7.x86_64 is already installed
[root@node01 ~]# build_stream_scripts.sh
28
CPU1 CORES is   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
CPU2 CORES is   [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55]
CPUS CORES is   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55]
[root@node01 ~]# bash run_mystream.sh | grep Triad
Triad:         101042.2     0.028560     0.028503     0.028612
Triad:         102640.8     0.028136     0.028059     0.028190
Triad:         199418.8     0.014506     0.014442     0.014553
[root@node01 ~]#

# 
# 从结果看，CPU核数越多，成绩越好，不知道这个是不是正确的，毕竟这里只有两个配置  
# 
#
# 
```

