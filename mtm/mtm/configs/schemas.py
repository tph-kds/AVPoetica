from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union, Any

class DeepSeekModelConfig(BaseModel):
    SYSTEM_PROMPT: str = Field(
        default = "You are a poet and your task is to write a poem based on the user prompt."
    )
    DEEPSSEEK_MODEL_NAME: str = Field(
        default = "deepseek-reasoner"
    )
    DEEPSEEK_API_KEY: str = Field(
        default = "sk-..."
    )
    BASE_URL: str = Field(
        default = "https://api.deepseek.ai"
    )
    STREAM: bool = Field(
        default = False
    )
    TEMPERATURE: float = Field(
        default = 1.5
    )
    MAX_TOKENS: int = Field(
        default = 625
    )


class OpenRouterModelConfig(BaseModel):
    SYSTEM_PROMPT: str = Field(
        default = "You are a poet and your task is to write a poem based on the user prompt."
    )
    OPENROUTER_MODEL_NAME: str = Field(
        default = "deepseek/deepseek-r1-0528:free"
    )
    OPENROUTER_API_KEY: str = Field(
        default = "sk-..."
    )
    OPENROUTER_BASE_URL: str = Field(
        default = "https://openrouter.ai/api/v1/chat/completions"
    )
    STREAM: bool = Field(
        default = False
    )
    TEMPERATURE: float = Field(
        default = 1.5
    )
    MAX_TOKENS: int = Field(
        default = 625
    )
    RANKING_URL: Optional[str] = Field(
        default = ""
    )
    RANKING_NAME: Optional[str] = Field(
        default = "Deepseek"
    )
    INCLUDE_REASONING: bool = Field(
        default = True
    )

class MaskErrorTokenizationConfig(BaseModel):
    pass 

class CountSyllablePoemsConfig(BaseModel):
    masked_words: List[Dict[str, Any]] = Field(default=[])
    idx_masked_words: set = Field(default=set())
    token_masked_words: str = Field(default="MASKED_WORD")
