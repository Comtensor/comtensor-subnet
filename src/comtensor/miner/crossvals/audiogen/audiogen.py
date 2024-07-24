import bittensor as bt
from comtensor.base.synapse_based_crossval import SynapseBasedCrossval
from comtensor.miner.crossvals.audiogen.protocol import *

class AudioGenCrossVal(SynapseBasedCrossval):

    def __init__(self, netuid = 16, wallet_name = 'default', wallet_hotkey = 'default', network = "finney", topk = 1, subtensor = None):
        super().__init__(netuid, wallet_name, wallet_hotkey, network, topk, subtensor)
        self.dendrite = bt.dendrite( wallet = self.wallet )
    
    async def forward(self, type, prompt):
        axons = [self.metagraph.axons[i['uid']] for i in self.top_miners]
        self.duration = 755
        self.sample_rate = 14400
        responses = 0

        if type == 'tts':
            responses = await self.dendrite(
                axons=axons,
                synapse=TextToSpeech(text_input=prompt),
                deserialize=True,
                timeout=50,
            )
            # Query Text to Speech
        elif type == 'ttm':
            # Music Generation
            responses = await self.dendrite(
                axons=axons,
                synapse=MusicGeneration(text_input=prompt, duration=self.duration ),
                deserialize=True,
                timeout=1400,
            )

        else:
            # Voice Cloning
            responses = await self.dendrite(
                axons=axons,
                synapse=VoiceClone(text_input=prompt, clone_input=clone_input, sample_rate=self.sample_rate, hf_voice_id="name"), 
                deserialize=True,
                timeout=150,
            )

        return responses

    async def run(self, type, prompt):
        response = await self.forward(type, prompt)
        # print(response)
        return response
    