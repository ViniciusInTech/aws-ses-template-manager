import json

class FileBasedEmailTemplateProvider:

    def __init__(self, base_path: str):
        self.base_path = base_path

    def get_template(self, template_key: str) -> dict:
        path = f"{self.base_path}/{template_key}.json"

        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
