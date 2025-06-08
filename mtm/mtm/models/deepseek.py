import json 
from openai import OpenAI
from ..configs.schemas import DeepSeekModelConfig

class DeepSeekModel:
    def __init__(
            self,
            model_config: DeepSeekModelConfig
    ) -> None:
        super(DeepSeekModel, self).__init__()

        self.SYSTEM_PROMPT = model_config.SYSTEM_PROMPT
        self.DEEPSEEK_MODEL_NAME = model_config.DEEPSSEEK_MODEL_NAME
        self.DEEPSEEK_API_KEY = model_config.DEEPSEEK_API_KEY
        self.BASE_URL = model_config.BASE_URL
        self.STREAM = model_config.STREAM
        self.TEMPERATURE = model_config.TEMPERATURE
        self.MAX_TOKENS = model_config.MAX_TOKENS

        self.client = OpenAI(
            api_key=self.DEEPSEEK_API_KEY, 
            base_url=self.BASE_URL
        )

        self.messages = [
            {
                "role": "system", 
                "content": self.SYSTEM_PROMPT
            }
        ]


    def calling_deepseek(
            self, 
            user_prompt: str
    ):
        """
        Calling Deepseek API to get the response poems which are similar to the user prompt

        Args:
            user_prompt (str): user prompt
            
        Returns:
            Dict[str, Any]: The response from Deepseek - Return top 10 poems from Deepseek
        """
        self.messages.append(
            {
                "role": "user", 
                "content": user_prompt
            }
        )

        self.response = self.client.chat.completions.create(
            model=self.DEEPSEEK_MODEL_NAME,
            messages=self.messages,
            stream=self.STREAM,
            temperature=self.TEMPERATURE,
            max_tokens=self.MAX_TOKENS,
            response_format={
                "type": "json_object",
            }

        )

        return self.response.choices[0].message



if __name__ == "__main__":
    user_prompt = "I am a poet and my task is to write a poem based on the user prompt."
    deepseek_model = DeepSeekModel(model_config=DeepSeekModelConfig())
    deepseek_model.calling_deepseek(user_prompt=user_prompt)