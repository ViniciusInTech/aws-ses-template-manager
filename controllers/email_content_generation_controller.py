from fastapi import APIRouter, Body

from responses.generated_email_response import GeneratedEmailResponse
from services.email_content_generation_service import EmailContentGenerationService
from services.providers.file_based_email_template_provider import FileBasedEmailTemplateProvider
from services.llm.prompt_builder import PromptBuilder
from services.llm.openai_client import OpenAIClient
from config.settings import settings

router = APIRouter()

email_content_service = EmailContentGenerationService(
    template_provider=FileBasedEmailTemplateProvider(
        base_path=settings.email_template_resources_path
    ),
    prompt_builder=PromptBuilder(),
    llm_client=OpenAIClient()
)


@router.post("/generate", response_model=GeneratedEmailResponse)
def generate_email_content(
    content: str = Body(..., media_type="text/plain"),
    language: str = "pt-BR",
    template_key: str = "incident_notification"
):
    return email_content_service.generate(
        raw_content=content,
        language=language,
        template_key=template_key
    )
