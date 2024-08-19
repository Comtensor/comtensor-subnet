# Miner Documentation

## Who can be miner?

Only bittensor validators can be miner in comtensor.

## Hardware requirements

| Component    | Requirement   |
| ------------ | ------------- |
| CPU          | 4 core 2.4GHz |
| RAM          | 8GB           |
| Network Up   | 400Mbps       |
| Network Down | 400Mbps       |
| Storage      | 100GB         |

> [!NOTE]
> Requires python3.10

## How to run a Validator

1) Clone Project
```
git clone https://github.com/Comtensor/comtensor-subnet.git
```

2) Create Vitural Environment
```
cd comtensor-subnet
python3 -m venv venv
. venv/bin/activate
```

3) Install dependencies
```
pip install -e .
pip install -r requirements.txt
pip install -U communex
```

4) Register Miner
```
comx module register <name> <your_commune_key> --netuid 6
```

5) Set '.env' file
```
cp .env.example .env
```

You need to update env file. You need to define the bittensor validator wallet information.
```txt
wallet_name="default"
wallet_hotkey="default"
```
6) Run Miner
From the root of your project, you can just call **comx module serve**.
```sh
comx module serve comtensor.miner.model.Miner <name-of-your-com-key> --subnets-whitelist 6 --ip <text> --port <number>
```

> Note: If you already have the module that regitered in the subnet without none address and port. You need to update that module with your running address and port.
> ```sh
> comx module update <name-of-your-com-key> --ip <text> --port <port> --netuid 6
> ```