from pydantic import BaseModel
from typing import Dict


class GenerateEmailContentRequest(BaseModel):
    message_type: str
    content: str
    context: Dict[str, str]
    language: str
