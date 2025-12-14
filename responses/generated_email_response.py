from pydantic import BaseModel


class GeneratedEmailResponse(BaseModel):
    subject: str
    html_body: str
    text_body: str
