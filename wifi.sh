#!/bin/bash
iwconfig wlx503eaa70c460 mode ad-hoc
iwconfig wlx503eaa70c460 essid fftlt-ibss
iwconfig wlx503eaa70c460 ap 62:C2:3A:86:A6:EE
iwconfig wlx503eaa70c460 channel 3
modprobe batman_adv
batctl if add wlx503eaa70c460
ifconfig wlx503eaa70c460 up
