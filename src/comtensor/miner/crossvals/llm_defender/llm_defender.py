import bittensor as bt
from comtensor.base.synapse_based_crossval import SynapseBasedCrossval
from comtensor.miner.crossvals.llm_defender.protocol import LLMDefenderProtocol
from uuid import uuid4
import secrets
import time

class LLMDefenderCrossVal(SynapseBasedCrossval):
    
    def __init__(self, netuid = 14, wallet_name = 'default', wallet_hotkey = 'default', network = "finney", topk = 1, subtensor = None):
        super().__init__(netuid, wallet_name, wallet_hotkey, network, topk, subtensor)
        self.dendrite = bt.dendrite( wallet = self.wallet )
        self.subnet_version = 50

    def sign_data(self, hotkey: bt.Keypair, data: str) -> str:
        try:
            signature = hotkey.sign(data.encode()).hex()
            return signature
        except TypeError as e:
            bt.logging.error(f'Unable to sign data: {data} with wallet hotkey: {hotkey.ss58_address} due to error: {e}')
            raise TypeError from e
        except AttributeError as e:
            bt.logging.error(f'Unable to sign data: {data} with wallet hotkey: {hotkey.ss58_address} due to error: {e}')
            raise AttributeError from e

    def forward(self, query, timeout: float):
        axons = [self.metagraph.axons[i['uid']] for i in self.top_miners]

        synapse_uuid = str(uuid4())
        nonce = secrets.token_hex(24)
        timestamp = str(int(time.time()))
        data_to_sign = f'{synapse_uuid}{nonce}{self.wallet.hotkey.ss58_address}{timestamp}'

        print(self.wallet.hotkey)
    
        responses = self.dendrite.query(
            axons,
            LLMDefenderProtocol(
                analyzer=query["analyzer"],
                subnet_version=self.subnet_version,
                synapse_uuid=synapse_uuid,
                synapse_signature=self.sign_data(self.wallet.hotkey, data_to_sign),
                synapse_nonce=nonce,
                synapse_timestamp=timestamp
            ),
            timeout=timeout,
            deserialize=True,
        )

        return responses

    def run(self, query):
        response = self.forward(query, 60)
        return response