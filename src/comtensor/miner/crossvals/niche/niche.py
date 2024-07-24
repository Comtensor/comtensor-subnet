import bittensor as bt
import requests
from comtensor.base.synapse_based_crossval import SynapseBasedCrossval
from comtensor.miner.crossvals.niche.protocol import *
import random
from crossvals.niche.offline_challenge import (
    get_backup_image,
    get_backup_prompt,
    get_backup_llm_prompt,
    get_promptGoJouney
)


MODEL_CONFIGS = yaml.load(
    open("./crossvals/niche/model_config.yaml"), yaml.FullLoader
)

def initialize_nicheimage_catalogue():
    nicheimage_catalogue = {
        "GoJourney": {
            "model_incentive_weight": 0.04,
            "supporting_pipelines": MODEL_CONFIGS["GoJourney"]["params"][
                "supporting_pipelines"
            ],
            # "reward_url": ig_subnet.validator.get_reward_GoJourney,
            "timeout": 12,
            "inference_params": {},
            "synapse_type": ImageGenerating,
        },
        "DreamShaper": {
            "model_incentive_weight": 0.06,
            "supporting_pipelines": MODEL_CONFIGS["DreamShaper"]["params"][
                "supporting_pipelines"
            ],
            # "reward_url": config.reward_url.DreamShaper,
            "inference_params": {
                "num_inference_steps": 30,
                "width": 512,
                "height": 768,
                "guidance_scale": 7,        
                "negative_prompt": "out of frame, nude, duplicate, watermark, signature, mutated, text, blurry, worst quality, low quality, artificial, texture artifacts, jpeg artifacts",
            },
            "timeout": 12,
            "synapse_type": ImageGenerating,
        },
        "RealisticVision": {
            "supporting_pipelines": MODEL_CONFIGS["RealisticVision"]["params"][
                "supporting_pipelines"
            ],
            "model_incentive_weight": 0.20,
            # "reward_url": config.reward_url.RealisticVision,
            "inference_params": {
                "num_inference_steps": 30,
                "negative_prompt": "out of frame, nude, duplicate, watermark, signature, mutated, text, blurry, worst quality, low quality, artificial, texture artifacts, jpeg artifacts",
            },
            "timeout": 12,
            "synapse_type": ImageGenerating,
        },
        "RealitiesEdgeXL": {
            "supporting_pipelines": MODEL_CONFIGS["RealitiesEdgeXL"]["params"][
                "supporting_pipelines"
            ],
            "model_incentive_weight": 0.30,
            # "reward_url": config.reward_url.RealitiesEdgeXL,
            "inference_params": {
                "num_inference_steps": 7,
                "width": 1024,
                "height": 1024,
                "guidance_scale": 5.5,
            },
            "timeout": 12,
            "synapse_type": ImageGenerating,
        },
        "AnimeV3": {
            "supporting_pipelines": MODEL_CONFIGS["AnimeV3"]["params"][
                "supporting_pipelines"
            ],
            "model_incentive_weight": 0.34,
            # "reward_url": config.reward_url.AnimeV3,
            "inference_params": {
                "num_inference_steps": 25,
                "width": 1024,
                "height": 1024,
                "guidance_scale": 7.0,
                "negative_prompt": "out of frame, nude, duplicate, watermark, signature, mutated, text, blurry, worst quality, low quality, artificial, texture artifacts, jpeg artifacts",
            },
            "timeout": 12,
            "synapse_type": ImageGenerating,
        },
        "Gemma7b": {
            "supporting_pipelines": MODEL_CONFIGS["Gemma7b"]["params"][
                "supporting_pipelines"
            ],
            "model_incentive_weight": 0.03,
            "timeout": 64,
            "synapse_type": TextGenerating,
            # "reward_url": config.reward_url.Gemma7b,
            "inference_params": {},
        },
        "StickerMaker": {
            "supporting_pipelines": MODEL_CONFIGS["StickerMaker"]["params"][
                "supporting_pipelines"
            ],
            "model_incentive_weight": 0.03,
            "timeout": 64,
            "synapse_type": ImageGenerating,
            # "reward_url": config.reward_url.StickerMaker,
            "inference_params": {"is_upscale": False},
        },
        # "FaceToMany": {
        #     "supporting_pipelines": MODEL_CONFIGS["FaceToMany"]["params"][
        #         "supporting_pipelines"
        #     ],
        #     "model_incentive_weight": 0.00,
        #     "timeout": 48,
        #     "synapse_type": ig_subnet.protocol.ImageGenerating,
        #     "reward_url": config.reward_url.FaceToMany,
        #     "inference_params": {},
        # },
    }
    return nicheimage_catalogue

def initialize_challenge_urls():
    prompt = "http://nicheimage.nichetensor.com/challenge/prompt"
    image = "http://nicheimage.nichetensor.com/challenge/image"
    llm_prompt = "http://nicheimage.nichetensor.com/challenge/llm_prompt"
    challenge_urls = {
        "txt2img": {
            "main": [prompt],
            "backup": [get_backup_prompt],
        },
        "img2img": {
            "main": [prompt, image],
            "backup": [get_backup_prompt, get_backup_image],
        },
        "controlnet_txt2img": {
            "main": [
                prompt,
                image,
            ],
            "backup": [get_backup_prompt, get_backup_image],
        },
        "gojourney": {
            "main": [
                prompt,
                get_promptGoJouney,
            ],
            "backup": [get_backup_prompt, get_promptGoJouney],
        },
        "text_generation": {
            "main": [llm_prompt],
            "backup": [get_backup_llm_prompt],
        },
    }
    return challenge_urls

class NicheCrossVal(SynapseBasedCrossval):
    
    def __init__(self, netuid = 23, wallet_name = 'default', wallet_hotkey = 'default', network = "finney", topk = 1, subtensor = None):
        super().__init__(netuid, wallet_name, wallet_hotkey, network, topk, subtensor)
        self.dendrite = bt.dendrite( wallet = self.wallet )
        self.nicheimage_catalogue = initialize_nicheimage_catalogue()
        self.challenge_urls = initialize_challenge_urls()

    def get_challenge(self, url: str, synapse: ImageGenerating, backup_func: callable) -> ImageGenerating:
        try:
            data = synapse.deserialize()
            response = requests.post(url, json=data)
            if response.status_code != 200:
                challenge = backup_func()
            else:
                challenge = response.json()
        except Exception as e:
            bt.logging.warning(f"Error in get_challenge: {e}")
            challenge = None
        if challenge:
            return synapse.copy(update=challenge)
        else:
            return None

    def prepare_challenge(self, input, pipeline_type):
        synapse_type = self.nicheimage_catalogue[input.model_name]["synapse_type"]
        synapse = synapse_type(pipeline_type=pipeline_type, model_name=input.model_name)
        synapse.pipeline_params.update(self.nicheimage_catalogue[input.model_name]["inference_params"])
        synapse.prompt = input.prompt

        synapse.seed = random.randint(0, 1e9)
        
        # for challenge_url, backup_func in zip(
        #     self.challenge_urls[pipeline_type]["main"],
        #     self.challenge_urls[pipeline_type]["backup"],
        # ):
        #     print(challenge_url)
        #     if callable(challenge_url):
        #         synapse = challenge_url(synapse)
        #     else:
        #         assert isinstance(challenge_url, str)
        #         synapse = self.get_challenge(challenge_url, synapse, backup_func)
        
        return synapse

    def forward(self, input, timeout: float):
        axons = [self.metagraph.axons[i['uid']] for i in self.top_miners]
        pipeline_type = random.choice(self.nicheimage_catalogue[input.model_name]["supporting_pipelines"])
        synapse = self.prepare_challenge(input, pipeline_type)

        responses = self.dendrite.query(
            axons = axons,
            synapse = synapse,
            deserialize = False,
            timeout = timeout,
        )

        return responses

    def run(self, input):
        response = self.forward(input,60)
        return response