import bittensor as bt
from comtensor.base.synapse_based_crossval import SynapseBasedCrossval
from comtensor.miner.crossvals.omron.protocol import *
import random

class OmronCrossVal(SynapseBasedCrossval):
    
    def __init__(self, netuid = 2, wallet_name = 'default', wallet_hotkey = 'default', network = "finney", topk = 1, subtensor = None):
        super().__init__(netuid, wallet_name, wallet_hotkey, network, topk, subtensor)
        self.dendrite = bt.dendrite( wallet = self.wallet )

    def forward(self, timeout: float):
        axons = [self.metagraph.axons[i['uid']] for i in self.top_miners]
        synapse = QueryZkProof(
            query_input={
                "model_id": [0],
                "public_inputs": [random.uniform(-1, 1) for _ in range(5)],
            }
        )
        try:
            response = self.dendrite.query(
                axons=axons,
                synapse = synapse,
                timeout=timeout,
                deserialize=True
            )
            
            return response
        except Exception as e:
            bt.logging.exception("Error while querying axons. \n", e)
            return None
        
    def run(self):
        response = self.forward(300)
        return response