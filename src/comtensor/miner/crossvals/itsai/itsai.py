import os
import bittensor as bt
from comtensor.base.synapse_based_crossval import SynapseBasedCrossval
from comtensor.miner.crossvals.itsai.protocol import TextSynapse
import asyncio

class ItsaiCrossVal(SynapseBasedCrossval):
    def __init__(self, netuid = 32, wallet_name = 'default', wallet_hotkey = 'default', network = "finney", topk = 1, subtensor = None):
        super().__init__(netuid, wallet_name, wallet_hotkey, network, topk, subtensor)
        self.dendrite = bt.dendrite( wallet = self.wallet )
        self.timeout = 60

    async def forward(self, texts):
        axons = [self.metagraph.axons[i['uid']] for i in self.top_miners]

        response = await self.dendrite(
            axons=axons,
            synapse=TextSynapse(texts=texts, predictions=[]),
            deserialize=True,
            timeout=self.timeout
        )
        return response

    async def run(self, texts):
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # response = loop.run_until_complete(self.forward(texts))
        # loop.close()
        response = await self.forward(texts)

        return response