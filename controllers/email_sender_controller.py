from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from requests.bulk_raw_email_request import BulkRawEmailRequest
from requests.template_request import SendEmailRequest, SendRawEmailRequest
from services.bulk_raw_email_service import BulkRawEmailService
from services.template_service import TemplateService
import json

router = APIRouter(prefix="/email", tags=["Email"])

template_service = TemplateService()
bulk_service = BulkRawEmailService()


@router.post(
    "/send-template",
    response_model=dict,
    summary="Send an email using an AWS SES template",
    description="""
Send an email using an existing AWS SES Template.

### Example payload
```json
{
  "template_name": "welcome_template",
  "to_email": "user@example.com",
  "from_email": "noreply@empresa.com",
  "variables": {
    "name": "John Doe",
    "link": "https://example.com/activate"
  }
}
```
"""
)
def send_email_with_template(payload: SendEmailRequest):
    return template_service.send_email_with_template(payload)


@router.post(
    "/send-raw",
    response_model=dict,
    summary="Send a raw email without using SES templates",
    description="""
Send a raw email using custom HTML and text content.

### Example payload
```json
{
  "to_email": "user@example.com",
  "from_email": "noreply@empresa.com",
  "subject": "Hello {{name}}",
  "html_body": "<h1>Hello {{name}}</h1>",
  "text_body": "Hello {{name}}"
}
```
"""
)
def send_email_without_template(payload: SendRawEmailRequest):
    return template_service.send_email_without_template(payload)


@router.post(
    "/send-csv-raw",
    response_model=dict,
    summary="Send multiple raw emails using CSV as variable source",
    description="""
This endpoint sends multiple emails **without SES templates**, using a CSV file
to dynamically substitute variables in the email content.

## CSV Requirements
- The file **must be .csv**
- Column **email** is required  
- Other columns are treated as variables  

### Example CSV
```
email,name,coupon,city
ana@mail.com,Ana,10%,São Paulo
john@mail.com,John,15%,New York
```

### Example payload (TEXT field in multipart/form-data)
```json
{
  "subject": "Olá {{name}}, você ganhou um cupom!",
  "from_email": "noreply@empresa.com",
  "html_body": "<h1>Olá {{name}}</h1><p>Cupom: <b>{{coupon}}</b></p>",
  "text_body": "Olá {{name}}, cupom: {{coupon}}",
  "delay_ms": 500
}
```

### Response Example
```json
{
  "total_sent": 2,
  "emails": [
    { "email": "ana@mail.com", "status": { "MessageId": "..." } },
    { "email": "john@mail.com", "status": { "MessageId": "..." } }
  ]
}
```
"""
)
async def send_raw_email_from_csv(
    payload: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format in payload")

    parsed = BulkRawEmailRequest(**data)

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV file")

    content = await file.read()

    return bulk_service.send_bulk(
        csv_file=content,
        subject=parsed.subject,
        html_body=parsed.html_body,
        text_body=parsed.text_body,
        from_email=parsed.from_email,
        delay_ms=parsed.delay_ms
    )