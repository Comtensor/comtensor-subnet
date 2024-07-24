import bittensor as bt
from comtensor.base.synapse_based_crossval import SynapseBasedCrossval
from comtensor.miner.crossvals.snporacle.protocol import Challenge
from datetime import datetime, timedelta
import time
from pytz import timezone

class SnporacleCrossVal(SynapseBasedCrossval):
    
    def __init__(self, netuid = 28, wallet_name = 'default', wallet_hotkey = 'default', network = "finney", topk = 1, subtensor = None):
        super().__init__(netuid, wallet_name, wallet_hotkey, network, topk, subtensor)
        self.dendrite = bt.dendrite( wallet = self.wallet )

    def forward(self):
        axons = [self.metagraph.axons[i['uid']] for i in self.top_miners]

        ny_timezone = timezone('America/New_York')
        current_time_ny = datetime.now(ny_timezone)
        bt.logging.info("Current time: ", current_time_ny)

        current_time_ny = datetime.now(ny_timezone)
        timestamp = current_time_ny.isoformat()

        synapse = Challenge(
            timestamp=timestamp,
        )

        responses = self.dendrite.query(
            axons=axons,
            synapse=synapse,
            deserialize=False,
        )

        return responses

    def run(self):
        response = self.forward()
        return response