import os

from groq import Groq


class LLMClient:

    def __init__(
        self,
        model: str | None = None,
        api_key: str | None = None,
    ):
        self.model = model or os.getenv(
            "LLM_MODEL",
            "openai/gpt-oss-120b",
        )

        self.client = Groq(
            api_key=api_key or os.getenv("LLM_API_KEY"),
        )

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
        model=self.model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

        return response.choices[0].message.content