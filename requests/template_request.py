from pydantic import BaseModel
from typing import Dict, Optional


class TemplateCreate(BaseModel):
    name: str
    subject: str
    html: str
    text: str

    def dict(self, *args, **kwargs):
        return {
            "TemplateName": self.name,
            "SubjectPart": self.subject,
            "HtmlPart": self.html,
            "TextPart": self.text,
        }


class TemplateUpdate(BaseModel):
    name: str
    subject: str
    html: str
    text: str

    def dict(self, *args, **kwargs):
        return {
            "TemplateName": self.name,
            "SubjectPart": self.subject,
            "HtmlPart": self.html,
            "TextPart": self.text,
        }


class SendEmailRequest(BaseModel):
    template_name: str
    to_email: str
    from_email: str
    variables: Dict[str, str]


class SendRawEmailRequest(BaseModel):
    to_email: str
    from_email: str
    subject: str
    html_body: str
    text_body: Optional[str] = None
