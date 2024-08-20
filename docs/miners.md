# Miner Documentation

## Who Can Be a Miner?

Only Bittensor validators can operate as miners in Comtensor.

## Hardware Requirements

| Component    | Requirement   |
| ------------ | ------------- |
| CPU          | 4 core 2.4GHz |
| RAM          | 8GB           |
| Network Up   | 400Mbps       |
| Network Down | 400Mbps       |
| Storage      | 100GB         |

> [!NOTE]
> Python 3.10 is required.

## How to Run a Miner

1) **Clone the Project**
    ```sh
    git clone https://github.com/Comtensor/comtensor-subnet.git
    ```

2) **Create a Virtual Environment**
    ```sh
    cd comtensor-subnet
    python3 -m venv venv
    . venv/bin/activate
    ```

3) **Install Dependencies**
    ```sh
    pip install -e .
    pip install -r requirements.txt
    pip install -U communex
    ```

4) **Register the Miner**
    ```sh
    comx module register <module-name> <your-key-name> 6
    ```

5) **Set Up the `.env` File**
    ```sh
    cp .env.example .env
    ```

    Update the `.env` file with your Bittensor validator wallet information:
    ```txt
    wallet_name="default"
    wallet_hotkey="default"
    ```

6) **Run the Miner**
    From the root of your project directory, run the following command:
    ```sh
    comx module serve comtensor.miner.model.Miner <name-of-your-com-key> --subnets-whitelist 6 --ip <text> --port <number>
    ```

    > [!NOTE]
    > If you have already registered the module in the subnet without specifying an address and port, you need to update the module with your running address and port.
    > ```sh
    > comx module update <name-of-your-com-key> 6 --ip <text> --port <port>
    > ```
