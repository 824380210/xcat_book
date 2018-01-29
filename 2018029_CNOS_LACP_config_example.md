# CNOS LACP configure example 
```

First switch:
interface Ethernet1/49
aggregation-group 1 mode active
!
interface Ethernet1/50
aggregation-group 1 mode active
!
interface Ethernet1/51
aggregation-group 1 mode active
!
interface Ethernet1/52
aggregation-group 1 mode active

Second switch:
interface Ethernet1/10
aggregation-group 1 mode active
!
interface Ethernet1/11
aggregation-group 1 mode active
!
interface Ethernet1/12
aggregation-group 1 mode active
!
interface Ethernet1/13
aggregation-group 1 mode active

```
## The aggreation group number doesn’t have to be the same on both switches, but it does have to be the same on all ports desired to be in the same aggregration on the same switch.
##This doesn’t include VLANs settings etc.—you can set that up as would be done without a port aggregation, but those settings would need to be the same for each port in an aggregation.
## END

