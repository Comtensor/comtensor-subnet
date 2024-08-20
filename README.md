
# Comtensor - Integrating CommuneAI with the Bittensor Subnet

<img src="docs/images/back.jpg" alt="back" width="500" height="300">

## Documentation

[Miner Docs](docs/miners.md) | [Validator Docs](docs/validators.md) | [Homepage](https://comtensor.io/) | [Video](https://comtensor.io/videos/comtensor.mp4)

## Overview

Comtensor bridges the gap between CommuneAI and the Bittensor subnet, allowing you to leverage the power of Bittensor within the CommuneAI ecosystem.
With Comtensor, you can access top responses from Bittensor subnets and seamlessly perform tasks within Commune using the Bittensor network.

## Scoring System v1.0

Our scoring system involves validators sending prompts to all miners and evaluating their responses using three similarity-checking algorithms. The final score is a weighted average, with 80% based on similarity and 20% on response time.

- [Jaro–Winkler](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance)
- [Dice-Sørensen coefficient](https://en.wikipedia.org/wiki/Dice-S%C3%B8rensen_coefficient)
- [Ratcliff/Obershelp](https://en.wikipedia.org/wiki/Gestalt_pattern_matching)

## Roadmap

- **Integrate a Bittensor Subnet**: Connect Comtensor with Bittensor subnet 18, laying the foundation for deeper integration.
- **Validation Mechanism MVP**:
    - Implement a basic validation mechanism focusing on similarity checks and response time.
    - Introduce cryptographic signature verification. Each Comtensor miner must sign with their Bittensor validator key, ensuring that one miner can only use one Bittensor validator hotkey. Miners without a Bittensor validator hotkey won't be able to run on Comtensor, and a single Bittensor validator cannot run multiple miners. This prevents massive miner registration by a single Bittensor validator.
- **Expand to Multiple Bittensor Subnets**: Integrate other Bittensor subnets one by one, starting with the top-emission subnets.
- **Create API**: Develop an API that operates on the subnet, similar to [Comtensor APIs](https://api.comtensor.io/docs).
- **Create User Interface**: Develop an intuitive interface that allows users to access Bittensor subnets with ease using the Comtensor API.

## Installation

### Install Packages

Clone the repository and install the necessary modules.

```sh
git clone https://github.com/Comtensor/comtensor-subnet.git
cd comtensor-subnet
python3 -m venv venv
. venv/bin/activate
pip install -e .
pip install -r requirements.txt
pip install -U communex
```

### Register Module on Comtensor Subnet (netuid 6)

```sh
comx module register <module-name> <your-key-name> 6
```

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
