# CSV Converter

Aplicação web para conversão e processamento de arquivos CSV.

O projeto possui um backend desenvolvido em Python com FastAPI, responsável pelo processamento dos dados, e um frontend desenvolvido com HTML com bootstrap, JavaScript, responsável pela interação com o usuário.

## Tecnologias

### Backend

- Python 3.14+
- FastAPI
- Pydantic
- uv

### Frontend

- HTML5
- JavaScript
- Bootstrap
- Papa Parse

## Estrutura do projeto

```text

├── backend/
│   ├── src/
│   │   └── convert_csv/
│   │       ├── api/
│   │       │   └── routes/
│   │       │       └── post.py
│   │       │
│   │       └── __init__.py
│   │
│   ├── .gitignore
│   ├── .python-version
│   ├── README.md
│   ├── pyproject.toml
│   └── uv.lock
│
├── frontend/
│   ├── favicon.ico
│   ├── index.html
│   └── script.js
│
└── LICENSE