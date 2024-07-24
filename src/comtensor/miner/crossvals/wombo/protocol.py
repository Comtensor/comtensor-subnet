#  The MIT License (MIT)
#  Copyright © 2023 Yuma Rao
#  Copyright © 2024 WOMBO
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the “Software”), to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of
#  the Software.
#
#  THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import base64
from io import BytesIO

import bittensor as bt
from PIL import Image
import random
from typing import cast, Annotated, TypeAlias

from pydantic import BaseModel, Field

DEFAULT_WIDTH = 768
DEFAULT_HEIGHT = 1344
DEFAULT_STEPS = 20
DEFAULT_GUIDANCE = 7.0

MIN_SIZE = 512
MAX_SIZE = 1536
MAX_STEPS = 100


GenerationResolution = Annotated[int, Field(ge=MIN_SIZE, le=MAX_SIZE)]
Frames: TypeAlias = bytes | None


class ImageGenerationInputs(BaseModel):
    """Inputs that should be communicated E2E directly from the client to the image generator"""

    prompt: str = ""  # Has a default as it needs to be default constructable
    prompt_2: str | None = None
    height: GenerationResolution = DEFAULT_HEIGHT
    width: GenerationResolution = DEFAULT_WIDTH
    num_inference_steps: Annotated[int, Field(gt=0, le=MAX_STEPS)] = DEFAULT_STEPS
    guidance_scale: float = DEFAULT_GUIDANCE
    negative_prompt: str | None = None
    negative_prompt_2: str | None = None
    num_images_per_prompt: Annotated[int, Field(gt=0, le=4)] = 1
    seed: Annotated[int | None, Field(default_factory=lambda: random.randint(0, (2**32) - 1))]
    controlnet_conditioning_scale: float = 0.0

class ImageGenerationClientInputs(ImageGenerationInputs):
    watermark: bool = True
    miner_uid: int | None
    validator_uid: int | None

class ImageGenerationOutput(BaseModel):
    frames: Frames
    images: list[bytes]


class ValidationInputs(BaseModel):
    input_parameters: ImageGenerationInputs
    frames: Frames


def load_base64_image(data: bytes) -> Image.Image:
    return Image.open(BytesIO(base64.b64decode(data)))


class NeuronInfoSynapse(bt.Synapse):
    is_validator: bool | None = None


class ImageGenerationSynapse(bt.Synapse):
    inputs: ImageGenerationInputs
    output: ImageGenerationOutput | None = None


class MinerGenerationOutput(BaseModel):
    images: list[bytes]
    process_time: float
    miner_uid: int
    miner_hotkey: str


class ImageGenerationClientSynapse(bt.Synapse):
    inputs: ImageGenerationInputs
    watermark: bool
    miner_uid: int | None
    output: MinerGenerationOutput | None

    def deserialize(self) -> list[Image.Image]:
        f"""
        Assumes the {self.output} field is filled by axon
        """
        return [
            load_base64_image(data)
            for data in cast(MinerGenerationOutput, self.output).images
        ]
