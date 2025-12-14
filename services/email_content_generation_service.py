class EmailContentGenerationService:

    def __init__(self, template_provider, prompt_builder, llm_client):
        self.template_provider = template_provider
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client

    def generate(self, template_key: str, raw_content: str, language: str) -> dict:
        template = self.template_provider.get_template(template_key)

        prompt = self.prompt_builder.build(
            template=template,
            content=raw_content,
            language=language
        )

        generated_email = self.llm_client.generate_email_content(prompt)

        return self._validate(generated_email)

    def _validate(self, generated_email: dict) -> dict:
        if not generated_email.get("subject"):
            raise ValueError("Missing subject")

        if not generated_email.get("html_body"):
            raise ValueError("Missing html body")

        return generated_email
