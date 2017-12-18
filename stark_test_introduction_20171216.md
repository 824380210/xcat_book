# stark node /Chassis introduction

1. 1 stark chassis have 4 compute node (default configure in rack )
2. 1 stark chassis have 1 SMM module 
3. the management module for compute node is XCC
4. XCC and SMM shared the same Ethernet port 
---

## Stark Compute Node in Chassis (2U with 4 Stark compute node )
![stark node in chassis ](http://img0.ph.126.net/e1wqSR56wgzUwnwkOf49uQ==/1280992619029733622.png)
## Stark chassis real view
![stark node real view](http://img1.ph.126.net/xJPogqvY4dDavKPp_E_9Cw==/6632258536795526287.png)
## Stark System Management Module
![Stark SMM module ](http://img0.ph.126.net/bptwbVteaKre35VrpdwH5A==/6632277228493198101.png)
## Stark Ethernet I/O Module : EIOM 
![EIOM :Ethernet IO Module ](http://img2.ph.126.net/loy7SQOmV1-bkyiS1fxKOg==/6632232148516465091.png)

## stark rack 

![Stark Rack ](http://img0.ph.126.net/fKClw05HFg6BaGsnXXkefw==/6632527917144333480.png)

## stark rack introduction
1. 18 stark chassis ,so 18*4 node = 72 node per Rack 
2. node01-node36 connect to the first switch port 1-36
3. smm01-smm09 connect to the first switch port 37-45
4. node37-node72 connect to the second switch port 1-36
5. smm10-smm18 connect to the second switch port 37-45
6. if the rack with OPA card ,in most case ,node01-node24 OPA port connect ot the first  OPA switch,node25-node48 connect to the second OPA switch ,node 49-node72 is ocnnect to the third switch(in general : OPA Switch provide 48 OPA port)
7. if the rack with the Mellanox EDR IB switch ,then since Mellanox Switch  have only 36 port (in general),so 18 port per group in most case ,so will have 4 IB switch configure in this rack 
8. we will base on the OPA Switch or IB switch to do the group Linpack stress test , all node in the same OPA/IB switch will be work a one Group and do the Linpack stress Test
--- 
#  === END ===  
