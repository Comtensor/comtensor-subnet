import bittensor as bt
from comtensor.base.synapse_based_crossval import SynapseBasedCrossval
from comtensor.miner.crossvals.transcription.protocol import Transcription
from pytube import YouTube
import os
import random
import base64

class TranscriptionCrossVal(SynapseBasedCrossval):
    
    def __init__(self, netuid = 11, wallet_name = 'default', wallet_hotkey = 'default', network = "finney", topk = 1, subtensor = None):
        super().__init__(netuid, wallet_name, wallet_hotkey, network, topk, subtensor)
        self.dendrite = bt.dendrite( wallet = self.wallet )

    def encode_audio_to_base64(self, audio_data):
        # Encode binary audio data to Base64 string
        return base64.b64encode(audio_data).decode('utf-8')

    def get_video_duration(self, url):
        try:
            # Create a YouTube object with the URL
            yt = YouTube(url)
            
            # Fetch the duration of the video in seconds
            duration_seconds = yt.length
            return duration_seconds
        except Exception as e:
            print(f"Error fetching video duration: {e}")
            return 0

    def select_random_url(directory='Youtube_urls'):
        # List all .txt files in the specified directory
        txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
        if not txt_files:
            raise FileNotFoundError("No text files found in the directory.")

        # Select a random .txt file
        random_file = random.choice(txt_files)
        file_path = os.path.join(directory, random_file)

        # Read URLs from the selected file
        with open(file_path, 'r') as file:
            urls = file.readlines()
        
        if not urls:
            raise ValueError("The selected file is empty.")

        return random.choice(urls).strip()

    def generate_validator_segment(self, duration):
        if duration <= 100:
            return [0, duration]
        else:
            start = random.randint(0, duration - 100)
            return [start, start + 100]

    def forward(self, input, timeout: float):
        axons = [self.metagraph.axons[i['uid']] for i in self.top_miners]
        
        if input['type'] == 'url':
            duration = self.get_video_duration(input['audio_url'])
            validator_segment = self.generate_validator_segment(duration)
            responses = self.dendrite.query(
                axons=axons,
                synapse=Transcription(input_type='url', audio_input=input['audio_url'], segment=validator_segment),
                deserialize=False,
                timeout=timeout
            )

        else:
            audio_sample_base64 = self.encode_audio_to_base64(input['audio_sample'])
            responses = self.dendrite.query(
                axons=axons,
                synapse=Transcription(audio_input=audio_sample_base64),
                deserialize=False,
                timeout=timeout
            )

        return responses

    def run(self, input):
        response = self.forward(input,60)
        return response