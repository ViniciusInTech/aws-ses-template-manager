from fastapi import APIRouter, Query
from api_requests.template_request import (
    TemplateCreate,
    TemplateUpdate,
    SendEmailRequest,
    SendRawEmailRequest
)
from services.template_service import TemplateService

router = APIRouter()
service = TemplateService()


@router.post("/", response_model=None)
def create_template(payload: TemplateCreate):
    return service.create_template(payload)


@router.get("/", response_model=dict)
def list_templates(
    page_size: int = Query(10, ge=1, le=50),
    next_token: str | None = None
):
    return service.list_templates(page_size=page_size, next_token=next_token)


@router.get("/{name}", response_model=dict)
def get_template(name: str):
    return service.get_template(name)


@router.get("/{name}/variables", response_model=dict)
def get_template_variables(name: str):
    return service.get_template_variables(name)


@router.put("/{name}", response_model=None)
def update_template(name: str, payload: TemplateUpdate):
    return service.update_template(name, payload)


@router.delete("/{name}", response_model=None)
def delete_template(name: str):
    return service.delete_template(name)

