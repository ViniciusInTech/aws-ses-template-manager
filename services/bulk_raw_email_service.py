import csv
import re
import time
import logging
from io import TextIOWrapper, BytesIO
from services.aws_client import AWSClient


class BulkRawEmailService:

    def __init__(self):
        self.aws = AWSClient()
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def render_variables(text: str | None, variables: dict):
        if not text:
            return text

        def replace(match):
            key = match.group(1).strip()
            return str(variables.get(key, ""))

        return re.sub(r"{{\s*(.*?)\s*}}", replace, text)

    def send_bulk_async(
        self,
        csv_file: bytes,
        subject: str,
        html_body: str,
        text_body: str | None,
        from_email: str,
        delay_ms: int
    ) -> None:

        buffer = BytesIO(csv_file)
        wrapped = TextIOWrapper(buffer, encoding="utf-8", newline="")
        reader = csv.DictReader(wrapped)

        if "email" not in reader.fieldnames:
            raise ValueError("CSV must contain 'email' column")

        for row in reader:
            email = row.get("email")
            variables = {k: v for k, v in row.items() if k != "email"}

            rendered_subject = self.render_variables(subject, variables)
            rendered_html = self.render_variables(html_body, variables)
            rendered_text = self.render_variables(text_body, variables)

            try:
                self.aws.send_raw_email(
                    to_email=email,
                    from_email=from_email,
                    subject=rendered_subject,
                    html_body=rendered_html,
                    text_body=rendered_text
                )

                self.logger.info("Email sent successfully", extra={"email": email})

            except Exception as exc:
                self.logger.error(
                    "Failed to send email",
                    extra={"email": email, "error": str(exc)}
                )

            if delay_ms > 0:
                time.sleep(delay_ms / 1000)
