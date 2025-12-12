import csv
import re
import time
from services.aws_client import AWSClient
from io import TextIOWrapper, BytesIO


class BulkRawEmailService:
    def __init__(self):
        self.aws = AWSClient()

    @staticmethod
    def render_variables(text: str | None, variables: dict):
        if not text:
            return text

        def replace(match):
            key = match.group(1).strip()
            return str(variables.get(key, ""))

        return re.sub(r"{{\s*(.*?)\s*}}", replace, text)

    def send_bulk(self, csv_file: bytes, subject: str, html_body: str, text_body: str | None,
                  from_email: str, delay_ms: int):

        buffer = BytesIO(csv_file)

        wrapped = TextIOWrapper(
            buffer,
            encoding="utf-8",
            newline=""
        )

        reader = csv.DictReader(wrapped)

        if "email" not in reader.fieldnames:
            raise ValueError("CSV must contain 'email' column")

        responses = []

        for row in reader:
            email = row.get("email")
            variables = {k: v for k, v in row.items() if k != "email"}

            rendered_html = self.render_variables(html_body, variables)
            rendered_text = self.render_variables(text_body, variables)
            rendered_subject = self.render_variables(subject, variables)

            result = self.aws.send_raw_email(
                to_email=email,
                from_email=from_email,
                subject=rendered_subject,
                html_body=rendered_html,
                text_body=rendered_text
            )

            responses.append({
                "email": email,
                "status": result
            })

            if delay_ms > 0:
                time.sleep(delay_ms / 1000)

        return {
            "total_sent": len(responses),
            "emails": responses
        }
