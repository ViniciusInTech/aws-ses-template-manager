from fastapi import APIRouter

from requests.template_request import TemplateCreate, TemplateUpdate, SendEmailRequest
from services.template_service import TemplateService

router = APIRouter()
service = TemplateService()

@router.post("/", response_model=None)
def create_template(template: TemplateCreate):
    return service.create_template(template)

@router.get("/", response_model=list[dict])
def list_templates():
    return service.list_templates()

@router.get("/{name}", response_model=dict)
def get_template(name: str):
    return service.get_template(name)

@router.get("/{name}/variables", response_model=dict)
def get_template_variables(name: str):
    return service.get_template_variables(name)

@router.put("/{name}", response_model=None)
def update_template(name: str, update: TemplateUpdate):
    return service.update_template(name, update)

@router.delete("/{name}", response_model=None)
def delete_template(name: str):
    return service.delete_template(name)

@router.post("/send-email")
def send_email_template(template_data: SendEmailRequest):
    return service.send_email(template_data)
