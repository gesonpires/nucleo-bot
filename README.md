# Chatbot Narrativo para Telegram

Um bot interativo para Telegram que conta uma história através de escolhas do usuário, criando uma experiência narrativa ramificada.

## Sobre o Projeto

Este bot implementa uma história interativa dividida em capítulos, onde o usuário pode fazer escolhas que afetam o desenvolvimento da narrativa. A estrutura modular permite fácil expansão com novos capítulos e ramificações.

## Estrutura

- **main.py**: Ponto de entrada da aplicação e configuração dos handlers
- **chapters/**: Módulos contendo cada capítulo da história
  - Capítulos principais (0-6)
  - Capítulos alternativos (2B, 3B, 4A, 4B)

## Configuração

1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente virtual:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Instale as dependências: `pip install -r requirements.txt`
5. Crie um arquivo `.env` com seu token do Telegram Bot:
   ```
   BOT_TOKEN=seu_token_aqui
   ```
6. Execute o bot: `python main.py`

## Tecnologias

- Python 3.x
- python-telegram-bot
- python-dotenv
```

## 4. Criar um requirements.txt

Crie um arquivo `requirements.txt` com as dependências do projeto:

```
python-telegram-bot>=20.0
python-dotenv>=1.0.0
```

## 5. Adicionar os Arquivos ao Staging

```bash
git add main.py
git add chapters/
git add .gitignore
git add README.md
git add requirements.txt
# Não adicione o arquivo .env se ele contiver seu token
```

## 6. Fazer o Primeiro Commit

```bash
git commit -m "Commit inicial: Estrutura base do chatbot narrativo para Telegram"
```

## 7. Configurar um Repositório Remoto (opcional neste momento)

Se você já tiver criado um repositório no GitHub, GitLab ou outro serviço:

```bash
git remote add origin https://github.com/seu-usuario/nome-do-repositorio.git
git branch -M main
git push -u origin main
