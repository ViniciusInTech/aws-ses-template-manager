from pydantic import BaseModel
from typing import Dict

class TemplateCreate(BaseModel):
    TemplateName: str
    SubjectPart: str
    HtmlPart: str
    TextPart: str

class TemplateUpdate(BaseModel):
    TemplateName: str
    SubjectPart: str
    HtmlPart: str
    TextPart: str

class SendEmailRequest(BaseModel):
    template_name: str
    to_email: str
    from_email: str
    variables: Dict[str, str]
