# 📨 AWS SES Email Manager API

API REST para **gerenciamento de templates**, **envio de emails via AWS
SES** e **geração automática de conteúdo por IA**, com foco em
**padronização, escalabilidade e auditabilidade**.

------------------------------------------------------------------------

## 🚀 Funcionalidades

-   📄 Gerenciamento completo de templates do AWS SES
-   📬 Envio de emails com ou sem template
-   📊 Envio em massa via CSV (bulk send)
-   🤖 Geração de conteúdo de email via IA (OpenAI)
-   🧩 Substituição dinâmica de variáveis (`{{name}}`, `{{email}}`)
-   🪵 Logs estruturados para auditoria
-   ⚙️ Configuração via `.env`

------------------------------------------------------------------------

## 🧰 Tecnologias

-   Python 3.11+
-   FastAPI
-   AWS SES (Boto3)
-   OpenAI API
-   Pydantic Settings
-   Uvicorn
-   uv (Astral) para gerenciamento de dependências

------------------------------------------------------------------------

## 📁 Estrutura do Projeto

    .
    ├── controllers/
    ├── services/
    │   ├── llm/
    │   ├── aws_client.py
    │   └── bulk_raw_email_service.py
    ├── config/
    │   └── settings.py
    ├── email-templates/
    ├── requests/
    ├── main.py
    ├── pyproject.toml
    ├── uv.lock
    ├── .env.example
    └── README.md

------------------------------------------------------------------------

## ⚙️ Configuração

Crie um arquivo `.env` baseado no `.env.example`:

``` bash
cp .env.example .env
```

------------------------------------------------------------------------

## 📦 Instalação (usando uv)

``` bash
uv venv
uv sync
```

------------------------------------------------------------------------

## ▶️ Executar a aplicação

``` bash
uvicorn main:app --reload
```

------------------------------------------------------------------------

## 📄 Licença

Projeto livre para uso educacional e corporativo.