# Sistema de Escalas COOPEX

Sistema para gerenciamento e envio de escalas de trabalho para cooperados.

## Funcionalidades

- Login de administrador com credenciais fixas (COOPEX/05062721)
- Upload de planilha Excel com escalas
- Processamento automático dos dados
- Envio individualizado de escalas por e-mail para cada cooperado

## Estrutura do Projeto

### Frontend
- `admin-login.html` - Página de login do administrador
- `admin.html` - Painel administrativo para upload e envio de escalas
- `style.css` - Estilos da aplicação
- `firebase.js` - Configuração do Firebase

### Backend (Flask)
- `src/main.py` - Aplicação principal
- `src/routes/escalas.py` - Rotas para processamento e envio de escalas
- `requirements.txt` - Dependências Python

## Formato da Planilha Excel

A planilha deve conter as seguintes colunas:
- **Nome Cooperado** - Nome do cooperado
- **Email** - E-mail do cooperado
- **Data** - Data da escala
- **Turno** - Turno de trabalho
- **Horário** - Horário de trabalho
- **Nome Contrato** - Nome do contrato

## Como Usar

### 1. Configurar Backend

```bash
cd coopex-backend
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar E-mail

Edite o arquivo `src/routes/escalas.py` e configure:
- `EMAIL_USER` - Seu e-mail Gmail
- `EMAIL_PASSWORD` - Senha de app do Gmail

### 3. Executar Backend

```bash
python src/main.py
```

### 4. Acessar Sistema

1. Abra `admin-login.html` no navegador
2. Faça login com:
   - Usuário: COOPEX
   - Senha: 05062721
3. No painel administrativo, faça upload da planilha Excel
4. Revise os dados processados
5. Clique em "Confirmar e Enviar E-mails"

## Credenciais de Administrador

- **Usuário:** COOPEX
- **Senha:** 05062721

## Tecnologias Utilizadas

- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Banco de dados: SQLite (via Flask template)
- E-mail: SMTP Gmail
- Processamento de planilhas: Pandas, OpenPyXL

