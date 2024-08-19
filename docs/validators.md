# Validator Documentation

## Hardware requirements

| Component    | Requirement   |
| ------------ | ------------- |
| CPU          | 8 core 2.4GHz |
| RAM          | 32GB          |
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

4) Register Validator
```
comx module register <name> <your_commune_key> --netuid 6
```

5) Run Validator

To run the validator, just call the file in which you are executing `validator.validate_loop()`.
```sh
python3 src/comtensor/cli.py <name-of-your-com-key> [--password <your-password>]
```