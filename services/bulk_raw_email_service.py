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
        reader = list(csv.DictReader(wrapped))

        if not reader or "email" not in reader[0]:
            raise ValueError("CSV must contain 'email' column")

        total = len(reader)
        sent = 0

        self.logger.info(
            "Bulk email sending started",
            extra={"total_emails": total}
        )

        for index, row in enumerate(reader, start=1):
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

                sent += 1

                self.logger.info(
                    "Email sent",
                    extra={
                        "email": email,
                        "current": index,
                        "sent": sent,
                        "remaining": total - index,
                        "total": total
                    }
                )

            except Exception as exc:
                self.logger.error(
                    "Failed to send email",
                    extra={
                        "email": email,
                        "current": index,
                        "sent": sent,
                        "remaining": total - index,
                        "total": total,
                        "error": str(exc)
                    }
                )

            if delay_ms > 0 and index < total:
                self.logger.info(
                    "Waiting before next email",
                    extra={"delay_ms": delay_ms}
                )
                time.sleep(delay_ms / 1000)

        self.logger.info(
            "Bulk email sending finished",
            extra={
                "total": total,
                "sent": sent,
                "failed": total - sent
            }
        )

