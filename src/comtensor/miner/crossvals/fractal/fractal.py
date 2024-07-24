import bittensor as bt
from comtensor.base.synapse_based_crossval import SynapseBasedCrossval
from comtensor.miner.crossvals.fractal.protocol import *

class FractalCrossVal(SynapseBasedCrossval):
    
    def __init__(self, netuid = 29, wallet_name = 'default', wallet_hotkey = 'default', network = "finney", topk = 1, subtensor = None):
        super().__init__(netuid, wallet_name, wallet_hotkey, network, topk, subtensor)
        self.dendrite = bt.dendrite( wallet = self.wallet )

    def forward(self, private_input, timeout: float):
        axons = [self.metagraph.axons[i['uid']] for i in self.top_miners]
        sampling_params= ChallengeSamplingParams()

        synapse = Challenge(
            query = private_input,
            sampling_params = sampling_params,
        )

        response = self.dendrite.query(
            axons = axons,
            synapse = synapse,
            deserialize = False,
            timeout = timeout,
        )
        
        return response

    def run(self, private_input):
        response = self.forward(private_input, 60)
        return response