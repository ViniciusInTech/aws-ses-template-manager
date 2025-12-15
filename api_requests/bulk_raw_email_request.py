from pydantic import BaseModel

class BulkRawEmailRequest(BaseModel):
    subject: str
    from_email: str
    html_body: str
    text_body: str | None = None
    delay_ms: int = 0