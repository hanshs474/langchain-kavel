"""Kavel image generation as a LangChain tool.

Without an API key the tool uses Kavel's free anonymous tier, so an agent can
call it on a machine with nothing configured. Set ``api_key`` (or
``KAVEL_API_KEY``) to run on a kavel.ai account.
"""

from typing import Literal, Optional, Type

import kavel
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class KavelImageInput(BaseModel):
    """Arguments for :class:`KavelImageGenerator`."""

    prompt: str = Field(
        description=(
            "What to draw, or for an edit what to change. Name the light, the material "
            "and the composition rather than stacking adjectives."
        )
    )
    aspect_ratio: Literal["1:1", "16:9", "9:16", "4:3", "3:4"] = Field(
        default="1:1", description="Shape of the image. Ignored for edits."
    )
    image_url: Optional[str] = Field(
        default=None,
        description="Public http(s) url of a photo to edit. Editing needs an API key.",
    )


class KavelImageGenerator(BaseTool):
    """Generate or edit an image with Kavel AI and return its CDN url.

    Example:
        .. code-block:: python

            from langchain_kavel import KavelImageGenerator

            tool = KavelImageGenerator()
            tool.invoke({"prompt": "a paper boat at sunrise, soft fog, 35mm film"})
    """

    name: str = "kavel_image_generator"
    description: str = (
        "Generates an image from a text prompt, or edits an image at a public url, "
        "and returns a permanent url to the result."
    )
    args_schema: Type[BaseModel] = KavelImageInput
    api_key: Optional[str] = None
    model: Optional[str] = None
    timeout: float = 360.0

    def _run(self, prompt: str, aspect_ratio: str = "1:1", image_url: Optional[str] = None, **_: object) -> str:
        try:
            return kavel.generate(
                prompt,
                image_url=image_url,
                aspect_ratio=aspect_ratio,
                api_key=self.api_key,
                model=self.model,
                timeout=self.timeout,
            )
        # Hand quota and refusals back to the agent as text so it can react
        # (wait, reword, or ask for a key) instead of crashing the run.
        except kavel.QuotaError as e:
            return f"Kavel free allowance is spent: {e}"
        except kavel.RejectedError as e:
            return f"Kavel refused the prompt, reword it: {e}"
        except kavel.SignInError as e:
            return f"This needs a Kavel account: {e}"
