import bittensor as bt
from comtensor.base.synapse_based_crossval import SynapseBasedCrossval
import random
from comtensor.miner.crossvals.sturdy.protocol import *
from comtensor.miner.crossvals.sturdy.constants import (
    NUM_POOLS,
    MIN_BASE_RATE,
    MAX_BASE_RATE,
    BASE_RATE_STEP,
    MIN_SLOPE,
    MAX_SLOPE,
    MIN_KINK_SLOPE,
    MAX_KINK_SLOPE,
    SLOPE_STEP,
    OPTIMAL_UTIL_RATE,
    OPTIMAL_UTIL_STEP,
    TOTAL_ASSETS,
    MIN_BORROW_AMOUNT,
    MAX_BORROW_AMOUNT,
    BORROW_AMOUNT_STEP,
    GREEDY_SIG_FIGS,
    QUERY_TIMEOUT
)

class SturdyCrossVal(SynapseBasedCrossval):
    
    def __init__(self, netuid = 10, wallet_name = 'default', wallet_hotkey = 'default', network = "finney", topk = 1, subtensor = None):
        super().__init__(netuid, wallet_name, wallet_hotkey, network, topk, subtensor)
        self.dendrite = bt.dendrite( wallet = self.wallet )

    def format_num_prec(
        self, num: float, sig: int = GREEDY_SIG_FIGS, max_prec: int = GREEDY_SIG_FIGS
    ) -> float:
        return float(f"{{0:.{max_prec}f}}".format(float(format(num, f".{sig}f"))))

    def randrange_float(
        self, start, stop, step, sig: int = GREEDY_SIG_FIGS, max_prec: int = GREEDY_SIG_FIGS
    ):
        num = random.randint(0, int((stop - start) / step)) * step + start
        return self.format_num_prec(num, sig, max_prec)

    def generate_assets_and_pools(self) -> typing.Dict:  # generate pools
        assets_and_pools = {}
        pools = {
            str(x): {
                "pool_id": str(x),
                "base_rate": self.randrange_float(MIN_BASE_RATE, MAX_BASE_RATE, BASE_RATE_STEP),
                "base_slope": self.randrange_float(MIN_SLOPE, MAX_SLOPE, SLOPE_STEP),
                "kink_slope": self.randrange_float(
                    MIN_KINK_SLOPE, MAX_KINK_SLOPE, SLOPE_STEP
                ),  # kink rate - kicks in after pool hits
                "optimal_util_rate": OPTIMAL_UTIL_RATE,  # optimal utility rate - after which the kink slope kicks in >:)
                "borrow_amount": self.randrange_float(
                    MIN_BORROW_AMOUNT,
                    MAX_BORROW_AMOUNT,
                    BORROW_AMOUNT_STEP,
                ),
            }
            for x in range(NUM_POOLS)
        }

        assets_and_pools["total_assets"] = TOTAL_ASSETS
        assets_and_pools["pools"] = pools

        return assets_and_pools

    async def forward(self, timeout: float):
        axons = [self.metagraph.axons[i['uid']] for i in self.top_miners]

        assets_and_pools = self.generate_assets_and_pools()

        synapse = AllocateAssets(assets_and_pools=assets_and_pools)

        responses = await self.dendrite.forward(
            axons=axons,
            synapse=synapse,
            timeout=timeout,
            deserialize=False,
            streaming=False,
        )

        return responses

    async def run(self):
        response = await self.forward(QUERY_TIMEOUT)
        return response