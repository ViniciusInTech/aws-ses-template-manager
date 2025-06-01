from fastapi import FastAPI
from starlette.responses import RedirectResponse

from controllers.template_controller import router as template_router

app = FastAPI(
    title="AWS SES Template Manager",
    description="API REST para gerenciar templates de e-mail na AWS SES de forma simples e sem linha de comando.",
    version="1.0.0"
)
app.include_router(template_router, prefix="/aws-ses/template", tags=["Templates"])

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")