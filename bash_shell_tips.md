# 这个用于记录老男孩编程实战中个人认为有用的一些记录
####  2018-05-17

### 执行成功提示什么，执行失败提示什么，提示信息可以用{}将多行内容括起来
 ```

[root@test ~]# cat and_or_test.sh
lspci | grep MegaRAID >/dev/null || {
echo -e "No RAID card Found" ;
 } && {
 echo -e "Found RAID crad ";
echo -e " this is showcase for multiple line ";
}
[root@test ~]# bash and_or_test.sh
Found RAID crad
 this is showcase for multiple line
[root@test ~]#



```
###### 注意是将{}将多行内容括起来，有时候加一个分号，多实践！！

### source 和 . 的功能：加载并执行相关脚本的文件中的命令及语句，而不是产生一个新的 shell来执行文件中的命令，执行后会将脚本中的变量值和函数传递到当前的 shell中

### $#是脚本后面带的参数的个数
### $*是当前脚本的所有传参的参数，不加引号时与$@相同，加双引号时将所有参数当作一个字符串，这个字符串中各个参参数是用空格分开的，如 "$1 $2 $3"
### $@ 加双引号时将所有参数作为独立的字符串，如"$1","$2","$3"
### 查帮助man bash , 查找 Special Parameters 来看有关这些参数的帮助
### shift命令丢弃第一个参数，这样每执行一次，参数列表都会少第一个参数，依此类推


### shell中变量的子字符串提取方法，可以man bash 中查parameter Expansion











































