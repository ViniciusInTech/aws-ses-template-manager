# 📨 AWS SES Template Manager API

Uma API REST simples e extensível para **criação**, **listagem**, **edição** e **remoção** de **templates de e-mail** do AWS SES, com suporte à extração automática de variáveis (`{{name}}`, `{{code}}`, etc).

---

## 📦 Tecnologias

- [Python 3.12+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Pydantic Settings](https://docs.pydantic.dev/latest/usage/pydantic_settings/)
- [Uvicorn](https://www.uvicorn.org/)
- `.env` para configuração segura

---

## 📁 Estrutura

```
aws_template_manager/
├── controllers/        # Rotas da aplicação
├── services/           # Lógica de negócio e cliente AWS
├── config/             # Configurações centralizadas (.env)
├── requests            # Esquemas Pydantic (entrada)
├── main.py             # Ponto de entrada
└── README.md
```

---

## ⚙️ Configuração

1. Crie um arquivo `.env` com suas credenciais AWS:

```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

> ⚠️ Se as variáveis não forem informadas, será usado o comportamento padrão do boto3 (ex: IAM Role, ~/.aws/credentials, etc).

---

## 📌 Instalação

### Crie o ambiente virtual
```bash
  python -m venv .venv
```

### Ative o ambiente
```bash
  source .venv/bin/activate  # Linux/macOS
  .venv\Scripts\activate     # Windows
```


### Instale dependências
```bash
  pip install -r requirements.txt
```

---

## ▶️ Executar localmente

```bash
  uvicorn main:app --reload
```

- Documentação interativa (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)
- Documentação ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📬 Endpoints disponíveis

| Método | Rota                                 | Descrição                             |
|--------|--------------------------------------|---------------------------------------|
| GET    | `/aws-ses/template/`                 | Lista templates + variáveis           |
| GET    | `/aws-ses/template/{name}`           | Retorna um template com variáveis     |
| GET    | `/aws-ses/template/{name}/variables` | Extrai só as variáveis de um template |
| POST   | `/aws-ses/template/`                 | Cria um novo template                 |
| PUT    | `/aws-ses/template/{name}`           | Atualiza um template                  |
| DELETE | `/aws-ses/template/{name}`           | Remove um template                    |
| POST   | `/aws-ses/template/send-email`       | Envio de email usando template        |

---

## 🧪 Exemplo de Payload (POST /aws-ses)

```json
{
  "TemplateName": "welcome_user",
  "SubjectPart": "Olá, {{name}}!",
  "HtmlPart": "<html><body>Bem-vindo, {{name}}!</body></html>",
  "TextPart": "Bem-vindo, {{name}}!"
}
```

---

## 🧠 Licença

Este projeto é de uso livre e educacional. Customize conforme necessário para seu ambiente.