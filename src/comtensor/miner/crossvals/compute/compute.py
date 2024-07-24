import bittensor as bt
from comtensor.base.synapse_based_crossval import SynapseBasedCrossval
from comtensor.miner.crossvals.compute.protocol import *
from comtensor.miner.crossvals.compute.pow import run_validator_pow

class ComputeCrossVal(SynapseBasedCrossval):
    
    def __init__(self, netuid = 27, wallet_name = 'default', wallet_hotkey = 'default', network = "finney", topk = 1, subtensor = None):
        super().__init__(netuid, wallet_name, wallet_hotkey, network, topk, subtensor)
        self.dendrite = bt.dendrite( wallet = self.wallet )

    def forward(self, private_input, timeout: float):
        axons = [self.metagraph.axons[i['uid']] for i in self.top_miners]   

        password, _hash, _salt, mode, chars, mask = run_validator_pow(length=private_input.difficulty)

        synapse = Challenge(
            challenge_hash=_hash,
            challenge_salt=_salt,
            challenge_mode=mode,
            challenge_chars=chars,
            challenge_mask=mask,
            challenge_difficulty=private_input.difficulty,
        )

        response = self.dendrite.query(
            axons=axons,
            synapse=synapse,
            timeout=timeout,
        )

        return response

    def run(self, private_input):
        response = self.forward(private_input,60)
        return response