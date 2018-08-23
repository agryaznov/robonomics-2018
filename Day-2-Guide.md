# Robonomics-2018 Day 2
## Robonomics Ethereum fork and Smart Contracts
## Resources
+ [Alexander Krupenkin blog post](https://akru.me/ipns/QmWboFP8XeBtFMbNYK3Ne8Z3gKFBSR5iQzkKgeNgQz3dz4/posts/2018-08-17-ethereum-wifi-mesh.html)
+ [Robonomics 2018: network resources spreadsheet](https://docs.google.com/spreadsheets/d/1xWdj2uLybi1sFnL1DLjV0iNCtIjASi99c8QiSCXVUhY/edit?pli=1#gid=0)
+ [AIRALab GitHub](https://github.com/airalab)

## Install Geth
You can do it with usual way described in the [Geth project Github]
OR, in honour of the decentralized [p2p mesh networks](Day-1), let's get it from the IPFS
```
$ ipfs get QmTaTVFA5jrkngQks9YEugtHodRNKHEsG1qwSCByQjSw1U
```
## Geth Init on Robonomics network
Get *genesis.json* from the [Robonomics 2018: network resources spreadsheet](https://docs.google.com/spreadsheets/d/1xWdj2uLybi1sFnL1DLjV0iNCtIjASi99c8QiSCXVUhY/edit?pli=1#gid=0)
```
$ mkdir robonomics2018
$ geth --datadir ./robonomics2018 --networkid 63  init genesis.json

$ geth --datadir ./robonomics2018 --networkid 63 console
```
## Create an Ethereum account
```
> personal.newAccount('qwe')
"0x1b9b499c6fc70d8d327104c59dc0dea3a8ba9f32"

> admin.addPeer("enode://8753ced723978dd965b68d482b57e46c3eee5c98974edeb6888b1796e74b4ffe22e7aaeeb61293a25ce0d8ce148fa81178414f785cd507f3e4ea417ddad5b3c5@[fca2:d099:c448:8666:e3f1:f39e:aad0:ea07]:30303")

> admin.addPeer("enode://d17b3ea4d97974bc24ddab78add7aad4fd80f9cb95187d29efd43221fee7874b833a182575c6b6eceb6b9297680497c3a3ab8ab87a1c2b581d0d64176365cf68@[fc52:735:525b:7aa:3450:3b0b:e03f:6d1f]:30303")
```

## Start Geth Node

```
$ geth --datadir ./robonomics2018 --networkid 63 --bootnodes ""enode://8753ced723978dd965b68d482b57e46c3eee5c98974edeb6888b1796e74b4ffe22e7aaeeb61293a25ce0d8ce148fa81178414f785cd507f3e4ea417ddad5b3c5@[fca2:d099:c448:8666:e3f1:f39e:aad0:ea07]:30303,enode://d17b3ea4d97974bc24ddab78add7aad4fd80f9cb95187d29efd43221fee7874b833a182575c6b6eceb6b9297680497c3a3ab8ab87a1c2b581d0d64176365cf68@[fc52:735:525b:7aa:3450:3b0b:e03f:6d1f]:30303"" --mine --minerthreads 1 --rpc console

> personal.unlockAccount(eth.accounts[0], "qwe", 0)
```
Wait the Node to get synced with the Robonomics network (Ethereum  fork)

## Get The AIRA robonomics smart contracts
```
$ git clone https://github.com/airalab/robonomics_contracts
```

## Compile & Deploy contracts
```
$ truffle migrate
```

## Setup the Contracts
Lighthouse is the major contract in the Robonomics stack: it matches the Ask orders for the robot jobs (coming from customers) with the Bid orders coming from the robots. (See [AIRA docs](aira docs) for more info)
```
truffle --network robonomics2018 console
```
Get the XRT token (AIRA token used in Robonomics)
```
> xrt = XRT.at("0xFAc8dFd86E64a59b4A3572469fBb20c4C3793990")
> xrt.transfer(web3.eth.accounts[1], 10000)
> xrt.balanceOf(web3.eth.accounts[0])
```

Get the Lighthouse contract instance
```
> tx = factory.createLighthouse(1000, 10, "test")
> tx.then(x => x.logs)
> l = LighthouseLib.at('0x849a78e703c39948e77603609b644cbeb3f565b3')
```
Approve the Lighhouse to spend the customer's tokens
```
> xrt.approve(l.address,1000)
```
Check the spending allowance
```
> xrt.allowance(web3.eth.accounts[0],l.address)
```
Add a worker to the Lighthouse
```
> l.refill(1000)
```
<what?>
```
> l.quotaOf(web3.eth.accounts[1])
```
## ROS install method 1
```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116

sudo apt-get update

sudo apt-get install ros-melodic-desktop-full
```