import json 
import requests

from openai import OpenAI
from ..configs.schemas import OpenRouterModelConfig

class OpenRouterModel:
    def __init__(
            self,
            model_config: OpenRouterModelConfig
    ) -> None:
        super(OpenRouterModel, self).__init__()

        self.SYSTEM_PROMPT = model_config.SYSTEM_PROMPT
        self.OPENROUTER_API_KEY = model_config.OPENROUTER_API_KEY
        self.OPENROUTER_MODEL_NAME = model_config.OPENROUTER_MODEL_NAME # "deepseek/deepseek-r1-0528:free"
        self.OPENROUTER_BASE_URL = model_config.OPENROUTER_BASE_URL # "https://openrouter.ai/api/v1/chat/completions"
        self.STREAM = model_config.STREAM
        self.TEMPERATURE = model_config.TEMPERATURE
        self.MAX_TOKENS = model_config.MAX_TOKENS
        self.RANKING_URL = model_config.RANKING_URL
        self.RANKING_NAME = model_config.RANKING_NAME
        self.INCLUDE_REASONING = model_config.INCLUDE_REASONING


        self.messages = [
            {
                "role": "system", 
                "content": self.SYSTEM_PROMPT
            }
        ]

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.OPENROUTER_API_KEY,
        )


    def calling_model(
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

        self.response = requests.post(
            url=self.OPENROUTER_BASE_URL,
            headers={
                "Authorization": f"Bearer {self.OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
                # "HTTP-Referer": self.RANKING_URL, # Optional. Site URL for rankings on openrouter.ai.
                # "X-Title": self.RANKING_NAME, # Optional. Site title for rankings on openrouter.ai.
            },
            data=json.dumps({
                "model": self.OPENROUTER_MODEL_NAME,
                "messages": self.messages,
                "stream": self.STREAM,
                "temperature": self.TEMPERATURE,
                "max_tokens": self.MAX_TOKENS,
                "response_format": "json_object",
                "include_reasoning": self.INCLUDE_REASONING, 
            })
        )

        if self.response.status_code == 404:
            return {"error_msg": "Not Found. Please check the configuration."}

        return self.response.json()['choices'][0]['message']['content']

        # self.messages.append(
        #     {
        #         "role": "user", 
        #         "content": user_prompt
        #     }
        # )

        # self.response = self.client.chat.completions.create(
        #     model=self.OPENROUTER_MODEL_NAME,
        #     messages=self.messages,
        #     stream=self.STREAM,
        #     temperature=self.TEMPERATURE,
        #     max_tokens=self.MAX_TOKENS,
        #     response_format={
        #         "type": "json_object",
        #     }

        # )

        # return self.response.choices[0].message.content



if __name__ == "__main__":
    user_prompt = "I am a poet and my task is to write a poem based on the user prompt."
    deepseek_model = OpenRouterModel(model_config=OpenRouterModelConfig())
    deepseek_model.calling_model(user_prompt=user_prompt)