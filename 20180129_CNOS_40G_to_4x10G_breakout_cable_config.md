# 40G to 10G breakout cable configure in CNOS
### [Part Number for the cable ](https://lenovopress.com/lp0607-lenovo-thinksystem-ne1072t-rackswitch)
```

QSFP+ breakout cables - 40 GbE to 4x 10 GbE
Lenovo 1m Passive QSFP+ to SFP+ Breakout DAC Cable 	49Y7886 	A1DL 	6
Lenovo 3m Passive QSFP+ to SFP+ Breakout DAC Cable 	49Y7887 	A1DM 	6
Lenovo 5m Passive QSFP+ to SFP+ Breakout DAC Cable 	49Y7888 	A1DN 	6
```
### If a 40 GbE to 4x10 GbE breakout cable is being used, then the port on the switch does have to be configured to 4x10G mode—the switch doesn’t auto-detect that a breakout cable is installed and change mode automatically
```
NE1072T(config)# hardware profile portmode custom 4x10G ethernet 1/53

```

