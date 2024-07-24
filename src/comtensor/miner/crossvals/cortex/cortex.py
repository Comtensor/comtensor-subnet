import bittensor as bt
from comtensor.base.synapse_based_crossval import SynapseBasedCrossval
from comtensor.miner.crossvals.cortex.protocol import *
import random

class CortexCrossVal(SynapseBasedCrossval):
    
    def __init__(self, netuid = 18, wallet_name = 'default', wallet_hotkey = 'default', network = "finney", topk = 1, subtensor = None):
        super().__init__(netuid, wallet_name, wallet_hotkey, network, topk, subtensor)
        self.dendrite = bt.dendrite( wallet = self.wallet )
        self.max_tokens = 4096
        self.model = "gpt-4-turbo-2024-04-09"
        self.provider = "OpenAI"
        self.top_p = 0.01
        self.top_k = 1
        self.temperature = 0.0001
        self.seed = 1234
        self.style = "vivid"
        self.steps = 30
        self.streaming = True
        self.size = "1792x1024"
        self.quality = "standard"

    async def handle_response(self, responses):
        full_response = ""
        for resp in responses:
            async for chunk in resp:    
                if isinstance(chunk, str):
                    bt.logging.trace(chunk)
                    full_response += chunk
            bt.logging.debug(f"full_response for uid: {full_response}")
            break
        return { "response": full_response }

    async def query_text(self, axons, private_input, timeout):
        self.provider = private_input.provider
        if self.provider == "Anthropic":
            self.model = "anthropic.claude-v2:1"

        elif self.provider == "OpenAI":
            self.model = "gpt-4-1106-preview"
            # self.model = "gpt-3.5-turbo"

        elif self.provider == "Gemini":
            self.model = "gemini-pro"

        elif self.provider == "Claude":
            self.model = "claude-3-opus-20240229"

        self.streaming = True
        messages = [{'role': 'user', 'content': private_input.prompt}]
        syn = StreamPrompting(messages=messages, model=self.model, seed=self.seed, max_tokens=self.max_tokens, temperature=self.temperature, provider=self.provider, top_p=self.top_p, top_k=self.top_k)
        dendrite_responses = await self.dendrite(axons, syn, deserialize=False, timeout=timeout, streaming=self.streaming)
        responses = await self.handle_response(dendrite_responses)
        return responses

    async def query_image(self, axons, private_input, timeout):
        self.provider = private_input.provider

        if self.provider == "Stability":
            self.seed = random.randint(1000, 1000000)
            self.model = "stable-diffusion-xl-1024-v1-0"

        elif self.provider == "OpenAI":
            self.model = "dall-e-3"
        self.streaming = False
        messages = private_input.prompt
        syn = ImageResponse(messages=messages, model=self.model, size=self.size, quality=self.quality, style=self.style, provider=self.provider, seed=self.seed, steps=self.steps)
        dendrite_responses = await self.dendrite(axons, syn, deserialize=False, timeout=timeout, streaming=self.streaming)
        # responses = await self.handle_response(dendrite_responses)
        return dendrite_responses

    async def forward(self, private_input, timeout: float)-> tuple[list]:
        axons = [self.metagraph.axons[i['uid']] for i in self.top_miners]
        if ( private_input.type == 'text'):
            return await self.query_text(axons, private_input, timeout)
        elif ( private_input.type == 'image'):
            return await self.query_image(axons, private_input, timeout)

    async def run(self, private_input):
        response = await self.forward(private_input,60)
        return response