from communex.module import Module, endpoint
from communex.key import generate_keypair
from keylimiter import TokenBucketLimiter
from comtensor.miner.crossvals.cortex.cortex import CortexCrossVal

from comtensor.miner.crossvals.prompting.text import PromtingCrossValidator
from comtensor.miner.crossvals.image_alchemy.alchemy import ImageAlchemyCrossVal
from comtensor.miner.crossvals.sybil.sybil import SybilCrossVal
from comtensor.miner.crossvals.openkaito.openkaito import OpenkaitoCrossVal
from comtensor.miner.crossvals.itsai.itsai import ItsaiCrossVal
from comtensor.miner.crossvals.wombo.wombo import WomboCrossVal
from comtensor.miner.crossvals.wombo.protocol import ImageGenerationClientInputs
from comtensor.miner.crossvals.fractal.fractal import FractalCrossVal
from comtensor.miner.crossvals.audiogen.audiogen import AudioGenCrossVal
from comtensor.miner.crossvals.llm_defender.llm_defender import LLMDefenderCrossVal
from comtensor.miner.crossvals.transcription.transcription import TranscriptionCrossVal
from comtensor.miner.crossvals.subvortex.subvortex import SubvortexCrossVal
from comtensor.miner.crossvals.snporacle.snporacle import SnporacleCrossVal
from comtensor.miner.crossvals.compute.compute import ComputeCrossVal
from comtensor.miner.crossvals.bitagent.bitagent import BitagentCrossVal
from comtensor.miner.crossvals.omegalabs.omegalabs import OmegalabsCrossVal
from comtensor.miner.crossvals.vision.vision import VisionCrossVal
from comtensor.miner.crossvals.omron.omron import OmronCrossVal
from comtensor.miner.crossvals.sturdy.sturdy import SturdyCrossVal

from pydantic import BaseModel
import bittensor as bt
import os
from dotenv import load_dotenv
load_dotenv()

class CortexItem(BaseModel):
    type: str
    provider: str
    prompt: str

subtensor = bt.subtensor()
wallet_name=os.getenv('wallet_name')
wallet_hotkey=os.getenv('wallet_hotkey')
cortex_crossval = CortexCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
promtingCrossval = PromtingCrossValidator(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
imagealchemy_crossval = ImageAlchemyCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
sybil_crossval = SybilCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
openkaito_crossval = OpenkaitoCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
itsai_crossval = ItsaiCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
wombo_crossval = WomboCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
fractal_crossval = FractalCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
audiogen_crossval = AudioGenCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
llmdefender_crossval = LLMDefenderCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
transcription_crossval = TranscriptionCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
subvortex_crossval = SubvortexCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
snporacle_crossval = SnporacleCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
compute_crossval = ComputeCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
bitagent_crossval = BitagentCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
omegalabs_crossval = OmegalabsCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
cortex_crossval = CortexCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
vision_crossval = VisionCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
omron_crossval = OmronCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)
sturdy_crossval = SturdyCrossVal(wallet_name=wallet_name, wallet_hotkey=wallet_hotkey, subtensor=subtensor)

class Miner(Module):
    """
    A module class for mining and generating responses to prompts.

    Attributes:
        None

    Methods:
        generate: Generates a response to a given prompt using a specified model.
    """

    @endpoint
    async def generate(self, prompt: str, type: str, netuid: int):
        """
        Generates a response to a given prompt using a specified model.

        Args:
            prompt: The prompt to generate a response for.
            model: The model to use for generating the response (default: "gpt-3.5-turbo").
            netuid: netuid

        Returns:
            None
        """

        print(f"Answering: `{prompt}` with model `{type}`")
        result = {}
        if type == "prompt":
            if netuid == 18:
                result["answer"] = await cortex_crossval.run(CortexItem(type="text", provider="OpenAI", prompt=prompt))
        return result

if __name__ == "__main__":
    """
    Example
    """
    from communex.module.server import ModuleServer
    import uvicorn

    key = generate_keypair()
    miner = Miner()
    refill_rate = 1 / 400
    # Implementing custom limit
    bucket = TokenBucketLimiter(2, refill_rate)
    server = ModuleServer(miner, key, ip_limiter=bucket, subnets_whitelist=[3])
    app = server.get_fastapi_app()

    # Only allow local connections
    uvicorn.run(app, host="127.0.0.1", port=8000)
