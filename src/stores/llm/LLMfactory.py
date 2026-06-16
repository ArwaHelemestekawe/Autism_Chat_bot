from src.stores.llm.llm_enum import LLM_ENUMS
from src.stores.llm.providers.OpenAIProvider import OpenAIProvider
from src.stores.llm.providers.CoherProvider import Cohere


class LLMProviderFactory:
    def __init__(self, config: dict):
        self.config = config

    def create(self, provider: str):
        if provider == LLM_ENUMS.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_API_URL,
                default_input_max_tokens=self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_output_max_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_tempreture=self.config.TEMPRETURE
            )
        


        if provider == LLM_ENUMS.COHERE.value:
            return Cohere(
                api_key=self.config.COHERE_API_KEY,
                default_input_max_tokens=self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_output_max_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_tempreture=self.config.TEMPRETURE
            )

        return None
