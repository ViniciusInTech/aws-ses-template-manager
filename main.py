from fastapi import FastAPI
from starlette.responses import RedirectResponse

from controllers.template_controller import router as template_router
from controllers.email_sender_controller import router as email_router
from controllers.email_content_generation_controller import router as email_content_generation
import logging


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


configure_logging()

app = FastAPI(
    title="AWS SES Email Manager",
    description="REST API for managing email templates and sending emails through AWS SES.",
    version="1.0.0"
)

app.include_router(template_router, prefix="/aws-ses/templates", tags=["Templates"])
app.include_router(email_router, prefix="/aws-ses/email", tags=["Email"])
app.include_router(email_content_generation, prefix="/aws-ses/email/ia", tags=["Email generate"])


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")
