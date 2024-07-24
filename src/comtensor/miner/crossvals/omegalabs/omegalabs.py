import bittensor as bt
from comtensor.base.synapse_based_crossval import SynapseBasedCrossval
from comtensor.miner.crossvals.omegalabs.protocol import *
from aiohttp import ClientSession

class OmegalabsCrossVal(SynapseBasedCrossval):
    
    def __init__(self, netuid = 24, wallet_name = 'default', wallet_hotkey = 'default', network = "finney", topk = 1, subtensor = None):
        super().__init__(netuid, wallet_name, wallet_hotkey, network, topk, subtensor)
        api_root = (
            "https://dev-validator.api.omega-labs.ai"
            if network == "test" else
            "https://validator.api.omega-labs.ai"
        )
        self.dendrite = bt.dendrite( wallet = self.wallet )
        self.num_videos = 8
        self.topics_endpoint = f"{api_root}/api/topic"

    async def get_topic(self):
        try:
            async with ClientSession() as session:
                async with session.get(self.topics_endpoint) as response:
                    response.raise_for_status()
                    query = await response.json()
                    return query
        except Exception as e:
            bt.logging.error(f"Error in get_topics: {e}")
            return

    async def forward(self, private_input, timeout: float):
        axons = [self.metagraph.axons[i['uid']] for i in self.top_miners]

        input_synapse = Videos(query=private_input.query, num_videos=self.num_videos)

        response = await self.dendrite(
            # Send the query to selected miner axons in the network.
            axons=axons,
            synapse=input_synapse,
            deserialize=False,
            timeout=timeout,
        )
        
        return response

    async def run(self, private_input):
        response = await self.forward(private_input, 120)
        return response