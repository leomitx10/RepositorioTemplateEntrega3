# Sistema de Eventos - API FastAPI

Este projeto implementa uma API para gerenciamento de eventos, festas, convites e sugestões usando FastAPI.

## Estrutura do Projeto

- `main.py` - Aplicação principal com endpoints FastAPI
- `models.py` - Modelos Pydantic que representam as entidades do sistema
- `requirements.txt` - Dependências do projeto

## Instalação

1. Crie um ambiente virtual Python:
   ```
   python -m venv venv
   ```

2. Ative o ambiente virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Executando a API

Execute o seguinte comando:

```
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`.

A documentação interativa estará disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Recursos Implementados

- Gerenciamento de usuários
- Criação e gestão de festas
- Adição de convidados
- Lista de desejos
- Sistema de convites
- Recomendação de fornecedores
```
