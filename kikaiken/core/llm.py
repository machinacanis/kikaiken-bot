from typing import Dict, Optional, Union, Type

import openai
from langchain_core.messages import AIMessageChunk
from langchain_core.outputs import ChatResult, ChatGenerationChunk
from langchain_core.utils import from_env
from langchain_openai.chat_models.base import BaseChatOpenAI
from pydantic import Field, ConfigDict, model_validator
from typing_extensions import Self

SILICONFLOW_API_BASE = "https://api.siliconflow.cn/v1"


class ChatSiliconFlow(BaseChatOpenAI):
    model_name: str = Field(alias="model")
    """模型名称"""
    api_key: str = Field(
        default_factory=from_env("SILICONFLOW_API_KEY", default=None)
    )
    """硅基流动 API key"""
    api_base: str = Field(
        default_factory=from_env("SILICONFLOW_API_BASE", default=SILICONFLOW_API_BASE)
    )
    """硅基流动 API base URL"""

    model_config = ConfigDict(populate_by_name=True)

    @property
    def _llm_type(self) -> str:
        """Return type of chat model."""
        return "chat-siliconflow"

    @property
    def lc_secrets(self) -> Dict[str, str]:
        """A map of constructor argument names to secret ids."""
        return {"api_key": "SILICONFLOW_API_KEY"}

    @model_validator(mode="after")
    def validate_environment(self) -> Self:
        if self.api_base == SILICONFLOW_API_BASE and not (
                self.api_key
        ):
            raise ValueError("If using default api base, SILICONFLOW_API_KEY must be set.")
        client_params: dict = {
            k: v
            for k, v in {
                "api_key": self.api_key,
                "base_url": self.api_base,
                "timeout": self.request_timeout,
                "max_retries": self.max_retries,
                "default_headers": self.default_headers,
                "default_query": self.default_query,
            }.items()
            if v is not None
        }

        if not (self.client or None):
            sync_specific: dict = {"http_client": self.http_client}
            self.client = openai.OpenAI(
                **client_params, **sync_specific
            ).chat.completions
        if not (self.async_client or None):
            async_specific: dict = {"http_client": self.http_async_client}
            self.async_client = openai.AsyncOpenAI(
                **client_params, **async_specific
            ).chat.completions
        return self

    def _create_chat_result(
            self,
            response: Union[dict, openai.BaseModel],
            generation_info: Optional[Dict] = None,
    ) -> ChatResult:
        rtn = super()._create_chat_result(response, generation_info)

        if not isinstance(response, openai.BaseModel):
            return rtn

        if hasattr(response.choices[0].message, "reasoning_content"):  # type: ignore
            rtn.generations[0].message.additional_kwargs["reasoning_content"] = (
                response.choices[0].message.reasoning_content  # type: ignore
            )

        return rtn

    def _convert_chunk_to_generation_chunk(
            self,
            chunk: dict,
            default_chunk_class: Type,
            base_generation_info: Optional[Dict],
    ) -> Optional[ChatGenerationChunk]:
        generation_chunk = super()._convert_chunk_to_generation_chunk(
            chunk,
            default_chunk_class,
            base_generation_info,
        )
        if (choices := chunk.get("choices")) and generation_chunk:
            top = choices[0]
            if reasoning_content := top.get("delta", {}).get("reasoning_content"):
                if isinstance(generation_chunk.message, AIMessageChunk):
                    generation_chunk.message.additional_kwargs["reasoning_content"] = (
                        reasoning_content
                    )
        return generation_chunk
