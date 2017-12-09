#use to update the SB7890 Mellanox IB unmanaged Switch
```

[root@stark23 sync]# cat sb7890_fw_check.sh
#!/bin/bash
mst start
mst ib add
mst status
dev=`mst status | grep SW_MT`
flint -d $dev q
flint -d $dev q | grep 15.1300.0126
if [ $? -ne 0 ];then
        echo -e "============================================"
        flint -d $dev -i fw-SwitchIB-2-rel-15_1300_0126-00WE092_00WE096_Ax.bin b
        flint -d $dev  swreset
        sleep 60
        flint -d $dev q
else
        echo -e "========FW check OK========"
fi
```
### 1 : make sure the FW image is in the current working directory 
### 2 : make sure the mst /flint tools is available 
### 3 : update the FW in need 

