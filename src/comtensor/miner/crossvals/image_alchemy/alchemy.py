import bittensor as bt
from comtensor.base.synapse_based_crossval import SynapseBasedCrossval
from comtensor.miner.crossvals.image_alchemy.protocol import ImageGeneration
import typing


class ImageAlchemyCrossVal(SynapseBasedCrossval):

    def __init__(self, netuid = 26, wallet_name = 'default', wallet_hotkey = 'default', network = "finney", topk = 1, subtensor = None):
        super().__init__(netuid, wallet_name, wallet_hotkey, network, topk, subtensor)
        self.dendrite = bt.dendrite( wallet = self.wallet )

    def forward(self, prompt, timeout:float, task_type="text_to_image", image=None):
        axons = [self.metagraph.axons[i['uid']] for i in self.top_miners]

        synapse = (
            ImageGeneration(
                generation_type=task_type,
                prompt=prompt,
                prompt_image=image,
                seed=-1,
            )
            if image is not None
            else ImageGeneration(
                generation_type=task_type,
                prompt=prompt,
                seed=-1,
            )
        )

        responses = self.dendrite.query(
            axons=axons,
            synapse=synapse,
            deserialize=True,
            timeout=timeout,
        )

        print(responses)

        return responses


    def run(self, query):
        response = self.forward(query, 60)
        return response
