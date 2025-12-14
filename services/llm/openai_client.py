from openai import OpenAI
from config.settings import settings
import json


class OpenAIClient:

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

    def generate_email_content(self, prompt: str) -> dict:
        response = self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=settings.openai_max_tokens,
            response_format={"type": "json_object"}
        )

        parsed = self._parse_response(response)

        self._validate(parsed)

        return parsed

    def _parse_response(self, response) -> dict:
        message = response.choices[0].message

        if message.content is None:
            raise ValueError("Model returned empty content")

        try:
            return json.loads(message.content)
        except json.JSONDecodeError as exc:
            raise ValueError("Model response is not valid JSON") from exc

    def _validate(self, content: dict) -> None:
        if not isinstance(content, dict):
            raise ValueError("Invalid response type")

        required_keys = {"subject", "html_body", "text_body"}

        if not required_keys.issubset(content.keys()):
            raise ValueError("Missing required email fields")
