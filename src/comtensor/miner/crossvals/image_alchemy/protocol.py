import typing
from typing import Optional

import pydantic

import bittensor as bt


class IsAlive(bt.Synapse):
    answer: typing.Optional[str] = None
    completion: str = pydantic.Field(
        "",
        title="Completion",
        description="Completion status of the current ImageGeneration object. This attribute is mutable and can be updated.",
    )


class ImageGeneration(bt.Synapse):
    """
    A simple dummy protocol representation which uses bt.Synapse as its base.
    This protocol helps in handling dummy request and response communication between
    the miner and the validator.

    Attributes:
    - dummy_input: An integer value representing the input request sent by the validator.
    - dummy_output: An optional integer value which, when filled, represents the response from the miner.
    """

    # Required request input, filled by sending dendrite caller.
    prompt: str = pydantic.Field("Bird in the sky", allow_mutation=False)
    negative_prompt: str = pydantic.Field(None, allow_mutation=False)
    prompt_image: Optional[bt.Tensor]
    images: typing.List[bt.Tensor] = []
    num_images_per_prompt: int = pydantic.Field(1, allow_mutation=False)
    height: int = pydantic.Field(1024, allow_mutation=False)
    width: int = pydantic.Field(1024, allow_mutation=False)
    generation_type: str = pydantic.Field("text_to_image", allow_mutation=False)
    guidance_scale: float = pydantic.Field(7.5, allow_mutation=False)
    seed: int = pydantic.Field(1024, allow_mutation=False)
    steps: int = pydantic.Field(50, allow_mutation=False)