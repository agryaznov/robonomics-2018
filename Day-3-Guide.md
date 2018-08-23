# Robonomics-2018 Day 3
# ROS + Ethereum = Robonomics
## Stack
+ Dapp for 3D printer for placing print orders
+ Robonomics SC for matching Ask and Bids
+ ROS services for arranging process
+ IPFS Pub Sub for communication channels and G-code files download
+ Python scripts for connecting ROS topics with Octoprint API
+ Raspberry Pi connected to 3d Printer (TBD: printer model) with Octoprint unboard

## Resources
+ [robonimics-js](https://github.com/airalab/robonomics-js)
+ [vue dapp instructions](https://github.com/airalab/vue-dapp-robonomics-template)
+ [ROS](http://ros.org)
+ [Octoprint REST API](http://docs.octoprint.org/en/master/api/index.html)

## Dapp Side
TBD: add Anatoly's notes
### Robonomics-js Dapp template

```
$ npm install -g vue-cli
$ vue init airalab/vue-dapp-robonomics-template my-project
$ cd my-project
$ npm install
$ npm run dev
```

## Robot (service provider) Side
### ROS install with Nix Packages
Install Nix package manager
```
$ curl https://nixos.org/nix/install | sh
```
install ROS Nix packages
```
$ nix-channel --add https://hydra.aira.life/project/aira/channel/latest aira
$ nix-channel --update
$ nix-env -i robonomics_comm --option binary-caches https://hydra.aira.life --option trusted-public-keys hydra.aira.life-1:StgkxSYBh18tccd4KUVmxHQZEUF7ad8m10Iw4jNt5ak=
$ source .nix-profile/setup.bash
```

### Setting things UP
1. Start ROS infochan with Lighthouse
    ```
    $ roslaunch robonomics_lighthouse lighthouse.launch lighthouse_contract:=cyberprinter42.lighthouse.1.robonomics.eth ens_contract:=0x0E8C00046B6821410031D4461054c67B39e2ee33
    ```

    *Infochan* - is an adapter between ROS and IPFS Pub Sub 

2. Ask message from Customer side (Dapp) comes to the */infochan/incoming/ask* topic
    We can listen this topic from terminal for debugging purposes
    ```
    $ rostopic echo /infochan/incoming/ask 
    model: "QmdFh1HPVe7H4LrDio899mxA7NindgxqiNUM9BNnBD7ryS"
    objective: "QmbSW1E73DKUvGDrgx8GirEVfHJLvj8RBijtH9iEZ7UecU"
    token: "0xFAc8dFd86E64a59b4A3572469fBb20c4C3793990"
    cost: 1
    validator: "0x0000000000000000000000000000000000000000"
    validatorFee: 0
    deadline: 37278
    nonce: b'xpV\xf9\xbf\x1e\x01(!<\xed3\xbdw\xc8j\x86\x91K\xfcy\x9e\xbb\x84\x9bO>/V3Wz'
    signature: b'\xe3gL\x84\xf6M\xea\x9f!\xe5(\xf9\x9d%p\xfa=\xd94\x90\xd1o\x03O\x03J\x1e\xf7\x8d\xfc-jT\xe8Z\x90\xebd*\xeb*\xcd\xac\xb3V\x850~*\x9e\x95\xce\x94\xb5\xdb\x9d\xd2\xb7\xc5~)64-\x1b'
    ```

    Check IPFS topic messages (useful for debugging)
    ```
    $ ipfs pubsub sub --discover cyberprinter42.lighthouse.1.robonomics.eth
    ```

3. Forming Bid manually (will do it with python scipt below)
```
$ rostopic pub /infochan/signing/bid robonomics_lighthouse/Bid "model: 'QmdFh1HPVe7H4LrDio899mxA7NindgxqiNUM9BNnBD7ryS'
objective: 'QmbSW1E73DKUvGDrgx8GirEVfHJLvj8RBijtH9iEZ7UecU'
token: '0xFAc8dFd86E64a59b4A3572469fBb20c4C3793990'
cost: 1
lighthouseFee: 0
deadline: 40000"

```

4. Liability node start
TBD: what is Liability 
```
$ roslaunch robonomics_liability liability.launch lighthouse_contract:=cyberprinter42.lighthouse.1.robonomics.eth ens_contract:=0x0E8C00046B6821410031D4461054c67B39e2ee33 factory_contract:=factory.1.robonomics.eth
```

5. Register to the Lighthouse contract
    See [Day-2[(Day-2)] for details
    ```
    > l = LighthouseLib.at('0x849a78e703c39948e77603609b644cbeb3f565b3')
    > l.refill(1000)
    ```

6. Pin the G-code files for our models, to make IPFS getting it smoothly during the process
    ```
    $ ipfs pin add QmWprKRhAFdZ25auDfhd2gZzQNJeLiexpkmnmV4DB5JWvHpinned QmWprKRhAFdZ25auDfhd2gZzQNJeLiexpkmnmV4DB5JWvH recursively
    greez@polka:~/dev/aira$ ipfs pin add QmbGybrBQoKPvv3MDc9mwACuvMHHk4PihYKgMdo6WL97Jopinned QmbGybrBQoKPvv3MDc9mwACuvMHHk4PihYKgMdo6WL97Jo recursively

    $ ipfs pin add QmNeiGb1hoJiA9czhWGtt7YGmKtnYVwU8Vs7jtieBZeuSupinned QmNeiGb1hoJiA9czhWGtt7YGmKtnYVwU8Vs7jtieBZeuSu recursively
    ```

7. Get the Ask message from */liability/infochan/incoming/ask* ros queue, and put the Bid to it to */liability/infochan/signing/bid* queue
    Look at *zenit_pub_bid.py* for details

8. Listen for *task* ros queue for printer task, get the model file, send it to printer with POST request
    Can use curl for that or API tools like Postman for that
    Look at *zenit_print.py* for request endpoint and params

9. After ~~printing task done~~ sending the task to printer, finish the liability
    ```
    $ rosservice call /liability/finish
    ```

### Automating the process with Python scripts
+ *zenit_pub_bid.py*
+ *zenit_print.py*

## Troubleshooting
### Debugging ROS services
```
$ rosservice list
$ rosservice call /liability/executor/set_logger_level "{logger: 'rosout', level: 'debug'"} && \
rosservice call /liability/infochan/signer/set_logger_level "{logger: 'rosout', level: 'debug'"} && \
rosservice call /liability/infochan/signer/set_logger_level "{logger: 'rosout', level: 'debug'"} && \
rosservice call /liability/listener/set_logger_level "{logger: 'rosout', level: 'debug'"}
```
### Nix bug: gas_price
Freeze gas price to 10
```
$ roslaunch robonomics_lighthouse lighthouse.launch lighthouse_contract:=cyberprinter42.lighthouse.1.robonomics.eth ens_contract:=0x0E8C00046B6821410031D4461054c67B39e2ee33 gas_price_gwei:=10
```

### Errors on Lighthouse side
We got this error somewhere in the process 
```
[ERROR] [1535015999.323287]: Broken transaction: {'code': -32000, 'message': 'gas required exceeds allowance or always failing transaction'}
```

Solved by switching to Master Ligthghouse node
```
$ roslaunch robonomics_liability liability.launch lighthouse_contract:=airalab.lighthouse.1.robonomics.eth ens_contract:=0x0E8C00046B6821410031D4461054c67B39e2ee33 factory_contract:=factory.1.robonomics.eth
```

Every time Lighthouse or your Node gets rebooted - check IPFS connections
```
$ ipfs swarm connect /ip6/fca2:d099:c448:8666:e3f1:f39e:aad0:ea07/tcp/4001/ipfs/QmZbznJh9bAGDptdiRYcrLN4cM8h9D2jwSCTgrKRj3KayE
$ ping fca2:d099:c448:8666:e3f1:f39e:aad0:ea07
```
