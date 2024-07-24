import bittensor as bt
from comtensor.base.synapse_based_crossval import SynapseBasedCrossval
from comtensor.miner.crossvals.subvortex.protocol import *
from substrateinterface.base import SubstrateInterface
from comtensor.miner.crossvals.subvortex.localisation import get_country
from comtensor.miner.crossvals.subvortex.subtensor import get_current_block
import time
from comtensor.miner.crossvals.subvortex.constants import (
    AVAILABILITY_FAILURE_REWARD,
    LATENCY_FAILURE_REWARD,
    DISTRIBUTION_FAILURE_REWARD,
    AVAILABILITY_WEIGHT,
    LATENCY_WEIGHT,
    RELIABILLITY_WEIGHT,
    DISTRIBUTION_WEIGHT,
)
from comtensor.miner.crossvals.subvortex.score import (
    compute_reliability_score,
    compute_latency_score,
    compute_distribution_score,
)

class SubvortexCrossVal(SynapseBasedCrossval):
    
    def __init__(self, netuid = 7, wallet_name = 'default', wallet_hotkey = 'default', network = "finney", topk = 1, subtensor = None):
        super().__init__(netuid, wallet_name, wallet_hotkey, network, topk, subtensor)
        self.dendrite = bt.dendrite( wallet = self.wallet )
        self.country = get_country(self.dendrite.external_ip)
        
    async def handle_synapse(self, uid: int):
        # Get miner ip
        ip = self.metagraph.axons[uid].ip

        CHALLENGE_NAME = 'Challenge'

        # Get the country of the subtensor via a free api
        country = get_country(ip)
        bt.logging.debug(f"[{uid}] Subtensor country {country}")

        process_time = None
        try:
            # Create a subtensor with the ip return by the synapse
            substrate = SubstrateInterface(
                ss58_format=bt.__ss58_format__,
                use_remote_preset=True,
                url=f"ws://{ip}:9944",
                type_registry=bt.__type_registry__,
            )

            # Start the timer
            start_time = time.time()

            # Get the current block from the miner subtensor
            miner_block = substrate.get_block()
            if miner_block != None: 
                miner_block = miner_block["header"]["number"]

            # Compute the process time
            process_time = time.time() - start_time

            # Get the current block from the validator subtensor
            validator_block = get_current_block(self.subtensor)

            # Check both blocks are the same
            verified = miner_block == validator_block or miner_block is not None

            bt.logging.trace(
                f"[{CHALLENGE_NAME}][{uid}] Verified ? {verified} - val: {validator_block}, miner:{miner_block}"
            )
        except Exception as err:
            verified = False
            process_time = 5 if process_time is None else process_time
            bt.logging.warning(f"[{CHALLENGE_NAME}][{uid}] Verified ? False")

        return verified, country, process_time

    async def forward(self):
        axons = [self.metagraph.axons[i['uid']] for i in self.top_miners]

        event = EventSchema(
            successful=[],
            completion_times=[],
            availability_scores=[],
            latency_scores=[],
            reliability_scores=[],
            distribution_scores=[],
            moving_averaged_scores=[],
            countries=[],
            block=self.subtensor.get_current_block(),
            uids=[],
            step_length=0.0,
            best_uid=-1,
            best_hotkey="",
            rewards=[],
        )

        CHALLENGE_NAME = 'Challenge'
        
        response = await self.handle_synapse(self.top_miners[0]['uid'])

        availability_score = 0
        latency_score = 0
        reliability_score = 0
        distribution_score = 0

        uid = self.top_miners[0]['uid']
        ip = self.metagraph.axons[uid].ip
        verified = response[0]
        number_of_miners = 1
        idx = 0

        # Compute score for availability
        availability_score = (
            1.0 if verified and number_of_miners else AVAILABILITY_FAILURE_REWARD
        )
        # availability_scores.append(availability_score)
        bt.logging.debug(
            f"[{CHALLENGE_NAME}][{uid}] Availability score {availability_score}"
        )

        # Compute score for latency
        latency_score = (
            compute_latency_score(uid, self.country, response)
            if verified
            else LATENCY_FAILURE_REWARD
        )
        # latency_scores.append(latency_score)
        bt.logging.debug(f"[{CHALLENGE_NAME}][{uid}] Latency score {latency_score}")

        # Compute score for reliability
        # reliability_score = await compute_reliability_score(
        #     uid, self.database, hotkey
        # )
        reliability_score = 0
        # reliability_scores.append(reliability_score)
        bt.logging.debug(
            f"[{CHALLENGE_NAME}][{uid}] Reliability score {reliability_score}"
        )

        # Compute score for distribution
        distribution_score = (
            compute_distribution_score(response)
            if response[2] is not None
            else DISTRIBUTION_FAILURE_REWARD
        )
        # distribution_scores.append((uid, distribution_score))
        bt.logging.debug(
            f"[{CHALLENGE_NAME}][{uid}] Distribution score {distribution_score}"
        )

        # Compute final score
        rewards = (
            (AVAILABILITY_WEIGHT * availability_score)
            + (LATENCY_WEIGHT * latency_score)
            + (RELIABILLITY_WEIGHT * reliability_score)
            + (DISTRIBUTION_WEIGHT * distribution_score)
        ) / 6.0

        return {
            "availability": availability_score,
            "latency": latency_score,
            "reliability": reliability_score,
            "distribution": distribution_score,
            "score": rewards,
        }

        # responses = self.dendrite.query(
        #     axons = axons,
        #     synapse = synapse,
        #     deserialize = False,
        #     timeout = timeout,
        # )
        # return responses

    async def run(self):
        response = await self.forward()
        return response