from requests.template_request import TemplateCreate, TemplateUpdate, SendEmailRequest
from services.aws_client import AWSClient

class TemplateService:
    def __init__(self):
        self.client = AWSClient()

    def create_template(self, data: TemplateCreate):
        template = data.dict()
        return self.client.create_template(template)

    def list_templates(self):
        return self.client.list_templates()

    def get_template(self, name: str):
        template = self.client.get_template(name)
        html = template.get("HtmlPart", "")
        variables = self.client.extract_variables(html)

        return {
            "name": template.get("TemplateName"),
            "subject": template.get("SubjectPart"),
            "html": html,
            "text": template.get("TextPart"),
            "variables": variables
        }

    def get_template_variables(self, name: str):
        template = self.client.get_template(name)
        html = template.get("HtmlPart", "")
        return {"variables": self.client.extract_variables(html)}

    def update_template(self, current_name: str, data: TemplateUpdate):
        if data.TemplateName != current_name:
            old_template = self.client.get_template(current_name)
            new_template = {
                "TemplateName": data.TemplateName,
                "SubjectPart": data.SubjectPart,
                "HtmlPart": data.HtmlPart,
                "TextPart": data.TextPart
            }
            self.client.create_template(new_template)
            self.client.delete_template(current_name)

            return {"message": f"Template '{current_name}' renomeado para '{data.TemplateName}'"}
        template = data.dict()
        return self.client.update_template(template)

    def delete_template(self, name: str):
        return self.client.delete_template(name)

    def send_email(self, data: SendEmailRequest):
        return self.client.send_templated_email(
            to_email=data.to_email,
            from_email=data.from_email,
            template_name=data.template_name,
            variables=data.variables
        )

