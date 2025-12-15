class PromptBuilder:

    def build(self, template: dict, content: str, language: str) -> str:
        return f"""
You are a system that formats email content using a strict reference example.

You MUST treat the provided template as the single source of truth.
You MUST replicate the structure, hierarchy, HTML tags, inline styles, and wording style.
You MUST NOT add new information.
You MUST NOT remove information.
You MUST NOT rephrase unless strictly necessary to fit placeholders.
You MUST inject the provided content into the template placeholders.

Language: {language}

REFERENCE SUBJECT:
{template["subject"]}

REFERENCE HTML TEMPLATE:
{template["html"]}

REFERENCE TEXT TEMPLATE:
{template["text"]}

SOURCE CONTENT (AUTHORITATIVE):
{content}

Return ONLY a valid JSON object with exactly the following keys:

{{
  "subject": "string",
  "html_body": "string",
  "text_body": "string"
}}
"""
