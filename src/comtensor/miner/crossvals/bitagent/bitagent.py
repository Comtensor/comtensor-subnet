import bittensor as bt
from comtensor.base.synapse_based_crossval import SynapseBasedCrossval
from comtensor.miner.crossvals.bitagent.protocol import *
from comtensor.miner.crossvals.bitagent.task import *
import torch

class BitagentCrossVal(SynapseBasedCrossval):
    
    def __init__(self, netuid = 20, wallet_name = 'default', wallet_hotkey = 'default', network = "finney", topk = 1, subtensor = None):
        super().__init__(netuid, wallet_name, wallet_hotkey, network, topk, subtensor)
        self.dendrite = bt.dendrite( wallet = self.wallet )

    def forward(self):
        axons = [self.metagraph.axons[i['uid']] for i in self.top_miners]
        miner_uids = [i['uid'] for i in self.top_miners]
        print(f"Miner uids: {miner_uids}")
        organic_miner_uids, task = get_random_task(self)
        print(task)
        if task.task_type == "organic" and len(organic_miner_uids) > 0:
            #bt.logging.debug('Received organic task with miner uids: ', organic_miner_uids)
            miner_uids = torch.tensor(organic_miner_uids)
        elif task.task_type == "organic":
            #bt.logging.debug('Received organic task without miner uids')
            # use random miner uids
            pass
        elif len(organic_miner_uids) > 0:
            #bt.logging.debug('Received generated task with miner uids that will require evaluation: ', organic_miner_uids)
            miner_uids = torch.tensor(organic_miner_uids)
        else:
            # use random miner uids
            #bt.logging.debug('Received generated task that will require evaluation')
            pass
        task_synapse = task.synapse
        task_timeout = task.timeout

        responses = self.dendrite.query(
            # Send the query to selected miner axons in the network.
            axons=[self.metagraph.axons[uid] for uid in miner_uids],
            # Construct a query. 
            synapse=task_synapse,
            # All responses have the deserialize function called on them before returning.
            # You are encouraged to define your own deserialization function.
            deserialize=False,
            timeout=task_timeout,
        )

        print(responses)

        return responses

    def run(self):
        response = self.forward()
        return response