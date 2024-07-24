import bittensor as bt
from comtensor.base.synapse_based_crossval import SynapseBasedCrossval
from comtensor.miner.crossvals.wombo.protocol import *

class WomboCrossVal(SynapseBasedCrossval):
    
    def __init__(self, netuid = 30, wallet_name = 'default', wallet_hotkey = 'default', network = "finney", topk = 1, subtensor = None):
        super().__init__(netuid, wallet_name, wallet_hotkey, network, topk, subtensor)
        self.dendrite = bt.dendrite( wallet = self.wallet )

    def prepare_synapse(self, inputs: ImageGenerationClientInputs):
        # print(self.top_miners[0]['uid'])
        # inputs.miner_uid = self.top_miners[0]['uid']
        # return ImageGenerationClientSynapse(
        #     inputs=inputs,
        #     watermark=inputs.watermark,
        #     miner_uid=self.top_miners[0]['uid'],
        # )
        return ImageGenerationSynapse(
            inputs=inputs
        )

    async def forward(self, inputs, timeout: float):
        axons = [self.metagraph.axons[i['uid']] for i in self.top_miners]
        synapse = self.prepare_synapse(inputs)

        responses = await self.dendrite(
            axons=axons,
            synapse=synapse,
            deserialize=False,
            timeout=timeout,
        )
        return responses

    async def run(self, inputs):
        response = await self.forward(inputs, 60)
        return response