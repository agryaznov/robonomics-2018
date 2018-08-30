# Robonomics-2018 Day 1
# Mesh Networks & IPFS PubSub
## Resources
+ [Alexander Krupenkin blog post](https://akru.me/ipns/QmWboFP8XeBtFMbNYK3Ne8Z3gKFBSR5iQzkKgeNgQz3dz4/posts/2018-08-16-ipfs-wifi-mesh.html)
+ [Robonomics Day-1 Follow-Up](https://zen.yandex.ru/media/id/5b339f318cb56900a8eb0700/robonomika-2018-injenernyi-intensiv-den-1-5b7b2e6360e0e800a927f368?from=editor)
+ [Robonomics 2018: network resources spreadsheet](https://docs.google.com/spreadsheets/d/1xWdj2uLybi1sFnL1DLjV0iNCtIjASi99c8QiSCXVUhY/edit?pli=1#gid=0)

## Prerequisites
All job has been done on *Ubuntu 18.04.1 LTS*

All scripts presuming working folder is *~/dev/aira/* 

## Mesh Networks
Stack is: B.A.T.M.A.N + CJDNS + IPFS

+ [B.A.T.M.A.N](https://packages.debian.org/sid/batctl) builds virtual Ethernet network
+ [CJDNS](https://github.com/cjdelisle/cjdns/blob/master/README_RU.md#%D0%9A%D0%B0%D0%BA-%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%B8%D1%82%D1%8C-cjdns) builds routing over Ethernet network
+ [IPFS](https://ipfs.io/) works on top of these two above

## Purposes:

1. Setup a mesh network
2. Chat through IPFS PubSub
3. Download a film from IPFS

## Step-by-Step Guide

1. (Re-)Plugin your WiFi dongle (if you use it, though you can just use your notebook's WiFi interface)
2. Turn OFF the WiFi manager and start B.A.T.M.A.N. Run the *wifi.sh* script:
    ```
    #!/bin/bash
    iwconfig wlx503eaa70c460 mode ad-hoc
    iwconfig wlx503eaa70c460 essid fftlt-ibss
    iwconfig wlx503eaa70c460 ap 62:C2:3A:86:A6:EE
    iwconfig wlx503eaa70c460 channel 3
    modprobe batman_adv
    batctl if add wlx503eaa70c460
    ifconfig wlx503eaa70c460 up
    ```
  replace *wlx503eaa70c460* to your inteface here

3. Check B.A.T.M.A.N connectivity
     ```
     $ sudo batctl n
     ```

4. *(run once after the install)* Configure CJDNS
    ```
    $ cd cjdns
    $ ./cjdroute --genconf >> cjdroute.conf
    ```

5.  Turn CJDNS up
  ```
  $ sudo ./cjdroute < cjdroute.conf
  ```
  
6. Sometimes you'll need to restart the CJDNS for troubleshooting. To do this, kill the process and start it again:
  ```
  $ sudo pkill cjdroute
  $ sudo ./cjdroute < cjdroute.conf
  ```

7. Check CJDNS connectivity
 ```
 $ ./tools/peerStats
 ```

8. Start IPFS daemon if not started yet
```
ipfs daemon --enable-pubsub-experiment
```

9. You can check if IPFS daemon runing with
```
$ ipfs id
Error: api not running
```
It is not running if you get an *Error*

9. Connect to certain IPFS nodes of our network (and set it to do this each time on startup)
```
ipfs swarm connect "/ip6/fca2:d099:c448:8666:e3f1:f39e:aad0:ea07/tcp/4001/ipfs/QmZbznJh9bAGDptdiRYcrLN4cM8h9D2jwSCTgrKRj3KayE" ;
ipfs bootstrap add /ip6/fca2:d099:c448:8666:e3f1:f39e:aad0:ea07/tcp/4001/ipfs/QmZbznJh9bAGDptdiRYcrLN4cM8h9D2jwSCTgrKRj3KayE ;
ipfs bootstrap add /ip6/fc52:735:525b:7aa:3450:3b0b:e03f:6d1f/tcp/4001/ipfs/QmZB2JPt8bhkQbBnjpwzdgaqZMmJupx85R7r9f1e5stmKs
```

10. Check the nodes you are connected to
```
$ ipfs swarm peers
```

11. Subscribe to certain IPFS channel
```
ipfs pubsub sub --discover airalab-mesh
```
Publish a message to the channel
```
ipfs pubsub pub airalab-mesh "   F.CK THE GOVERNER\!    "

```

12. Share your file through the IPFS
```
$ ipfs add film.mkv
added QmWfHXfnQbxwqJoPnyRqSBndHR8EgWwyMAyF4FSaF1MEZx film.mkv
```
you can publish the hash to the IPFS pubsub, to let your mates to download the film
13. You can download the file from IPFS knowing its hash by
```
$ ipfs get QmWfHXfnQbxwqJoPnyRqSBndHR8EgWwyMAyF4FSaF1MEZx
```

## Troubleshooting
### Problem 1. Connection problems
Sometimes you could loose the connection to other nodes. 
This could be because of dongle channel sets back to wrong one. Or, more tricky case, the network just can loose connectivity between sub-networks.

To resolve these issues:

1. Check WiFi dongle channel 
```
$ iwconfig
```
You should see something like *Frequency=2.422 GHz* on dongle's interface, which means it is on the channel 3. Of you see *2.412 GHz* instead, this means you dropped back to channel 1. If so, go to 2.

2. Re-Plug the dongle and repeat the steps starting from the step 1.

3. To connect sub-network, take the ip of any node from other sub-network and use ``` ipfs swarm connect <node>``` to resore connectivity

### Problem 2. File downloading is tooooo sloooow
Well, the dongles we used were very slow. And moreover the more nodes the mesh networks has, the faster it works.
Hence, try to
1. Use your notebook WiFi instead of the dongle 
2. Encourage your mates to join the mesh network
3. Well, you can use the CJDNS on top of usual WiFi local network instead of mesh network

## More Tools & Tricks
+ [yrd](https://github.com/kpcyrd/yrd) - CJDNS debugging tool

## To set a WiFi connection from shell
Sometimes you probably would like to google something in the middle of the process. To not get crazy while switching your Wlan interface between mesh network and your internet provider router, you could use the WiFi dongle for the former and the notebook wlan interface for the latter. For that, use something like this
```
$ ip a
$ wpa_supplicant -i wlp3s0 -c wpa.conf
$ sudo rfkill list
$ sudo rfkill unblock all
$ sudo wpa_supplicant -i wlp3s0 -c wpa.conf
```