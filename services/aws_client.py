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

    def create_template(self, template):
        return self.client.create_template(Template=template)

    def list_templates(self):
        return self.client.list_templates()["TemplatesMetadata"]

    def get_template(self, name):
        return self.client.get_template(TemplateName=name)["Template"]

    def update_template(self, template):
        return self.client.update_template(Template=template)

    def delete_template(self, name):
        return self.client.delete_template(TemplateName=name)

    def send_templated_email(self, to_email: str, from_email: str, template_name: str, variables: dict):
        return self.client.send_templated_email(
            Source=from_email,
            Destination={"ToAddresses": [to_email]},
            Template=template_name,
            TemplateData=json.dumps(variables)
        )

    def extract_variables(self, html):
        return list(set(re.findall(r"{{\s*(\w+)\s*}}", html)))
