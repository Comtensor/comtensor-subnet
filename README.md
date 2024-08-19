# Comtensor - CommuneAI with Bittensor Subnet

Comtensor makes bridge between Commune-ai and Bittensor

<img src="docs/images/back.jpg" alt="back" width="500" height="300">

## Documentation

[Miner Docs](docs/miners.md) | [Validator Docs](docs/validators.md) | [Discord](https://discord.com) | [Homepage](https://comtensor.io/) | [Video](https://comtensor.io/videos/comtensor.mp4)

## Overview

Comtensor facilitates the connection between Commune.ai and the Bittensor subnet. Using Comtensor, you can get the top responses from the Bittensor subnet, enabling you to perform all tasks in Commune using the Bittensor network.

## Scroing System v1.0
Validators are sending prompts to all miners. After getting all response from the miners we're using 3 simliarity checking algrithms.
After getting average simliarity score we sum with reponse time score. The rate is 8:2.
* [Jaro–Winkler](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance)
* [Dice-Sørensen coefficient](https://en.wikipedia.org/wiki/Dice-S%C3%B8rensen_coefficient)
* [Ratcliff Obershelp](https://en.wikipedia.org/wiki/Gestalt_pattern_matching)

## Roadmap
* **Implement One Subnet of bittensor** - Integrate to comtensor subnet 18 of bittensor.
* **Validation Mechanism MVP** - Similiarity checking and Response time
* **Implement Several Subnets of Bittensor** - We should randomly choose subnet Id and then, generate appropriate requests for miners and miners generate responses for that request and get rewards based on their response quality. We will integrate subnets one by one from top-emission subnets.
* **Validation Mechanism Full** - We will add bittensor validator signing. Comtensor miners should sign with their validator keys. So one miner can use only one validator hotkey. Miners who don't have bittensor validator hotkey cannot run miner in comtensor and also one bittensor validator cannot run multiple miners. There'll be not competition if all miners are the exact bittensor validator.
* **Creating Api** - we create api that run on the subnet similar to [Comtensor APIs](https://api.comtensor.io)

## Installation

### Install packages

Clone the repository and install module.
```sh
git clone https://github.com/Comtensor/comtensor-subnet.git
cd comtensor-subnet
python3 -m venv venv
. venv/bin/activate
pip install -e .
pip install -r requirements.txt
pip install -U communex
```

### Register Module on comtensor subnet (netuid 6)
```sh
comx module register --netuid 6 --key <your-key-name> <module-name> <ip> <port>
```

## License
Distributed under the MIT License. See LICENSE for more information.