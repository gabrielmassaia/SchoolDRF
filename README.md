# API Rest em Django

Este projeto é uma API REST desenvolvida em **Python** utilizando o **Django** e o **Django REST Framework (DRF)**.  
Ele serve como base para criação de aplicações escaláveis e organizadas, seguindo boas práticas de desenvolvimento.

---

## Como rodar o projeto

### 1. Clonar o repositório

Crie uma pasta para organizar o código (exemplo: `src`) e dentro dela clone o repositório:

```bash
mkdir src && cd src
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
```

---

### 2. Criar e ativar o ambiente virtual

Crie o ambiente virtual `venv`:

```bash
python -m venv env
```

Ative o ambiente virtual:

- **Linux/macOS**:

  ```bash
  source env/bin/activate
  ```

- **Windows (PowerShell)**:

  ```bash
  .\env\Scripts\activate
  ```

---

### 3. Instalar dependências

Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

---

### 4. Executar as migrações

Crie as tabelas no banco de dados:

```bash
python manage.py migrate
```

---

### 5. Rodar o servidor

Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

O projeto estará disponível em:
[http://localhost:8000](http://localhost:8000)

---

## 🛠 Tecnologias utilizadas

- Python 3.x
- Django
- Django REST Framework
- SQLite (banco padrão para dev)

---

## Estrutura do projeto

```
src/
│── env/# Ambiente virtual
        src/
            │── seu-projeto/        # Código fonte da aplicação
            │   ├── manage.py
            │   ├── settings.py
            │   ├── urls.py
            │   └── apps/...
```

---
