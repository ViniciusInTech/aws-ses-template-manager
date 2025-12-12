import json
import boto3
import re

from config.settings import settings


class AWSClient:
    def __init__(self):
        kwargs = {}

        if settings.aws_region:
            kwargs["region_name"] = settings.aws_region

        if settings.aws_access_key_id and settings.aws_secret_access_key:
            kwargs["aws_access_key_id"] = settings.aws_access_key_id
            kwargs["aws_secret_access_key"] = settings.aws_secret_access_key

        self.client = boto3.client("ses", **kwargs)

    def create_template(self, template: dict):
        return self.client.create_template(Template=template)

    def list_templates(self, page_size: int = 10, next_token: str | None = None):
        params = {"MaxItems": page_size}
        if next_token:
            params["NextToken"] = next_token
        response = self.client.list_templates(**params)
        return {
            "items": response.get("TemplatesMetadata", []),
            "next_token": response.get("NextToken")
        }

    def get_template(self, name: str):
        return self.client.get_template(TemplateName=name)["Template"]

    def update_template(self, template: dict):
        return self.client.update_template(Template=template)

    def delete_template(self, name: str):
        return self.client.delete_template(TemplateName=name)

    def send_templated_email(self, to_email: str, from_email: str, template_name: str, variables: dict):
        return self.client.send_templated_email(
            Source=from_email,
            Destination={"ToAddresses": [to_email]},
            Template=template_name,
            TemplateData=json.dumps(variables)
        )

    def send_raw_email(self, to_email: str, from_email: str, subject: str, html_body: str, text_body: str | None = None):
        body = {}
        if html_body:
            body["Html"] = {"Data": html_body}
        if text_body:
            body["Text"] = {"Data": text_body}

        return self.client.send_email(
            Source=from_email,
            Destination={"ToAddresses": [to_email]},
            Message={
                "Subject": {"Data": subject},
                "Body": body
            }
        )

    @staticmethod
    def extract_variables(html: str):
        return list(set(re.findall(r"{{\s*(\w+)\s*}}", html)))
