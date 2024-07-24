# Comtensor Subnet

Comtensor makes bridge between Commune-ai and Bittensor

## Overview

Comtensor facilitates the connection between Commune.ai and the Bittensor subnet. Using Comtensor, you can get the top responses from the Bittensor subnet, enabling you to perform all tasks in Commune using the Bittensor network.

## Installation

Clone the repository and install module.
```sh
cd comtensor-subnet
python3 -m venv venv
. venv/bin/activate
pip install -e .
```

### Miner

#### Who can be miner?

Only bittensor validators can be miner in comtensor.

#### Running

You need to update env file. You need to define the bittensor validator wallet information.
```txt
wallet_name="default"
wallet_hotkey="default"
```

From the root of your project, you can just call **comx module serve**. For example:

```sh
comx module serve comtensor.miner.model.Miner <name-of-your-com-key> [--subnets-whitelist <your-subnet-netuid>] [--ip <text>] [--port <number>]
```

### Validator

#### Running

To run the validator, just call the file in which you are executing `validator.validate_loop()`. For example:

```sh
python3 src/comtensor/cli.py <name-of-your-com-key> <--password >
```