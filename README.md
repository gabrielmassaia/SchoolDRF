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

---

## Trabalho de Testes - Biblioteca (pytest)

Este repositório também inclui um módulo independente em `python/` utilizado para o trabalho de testes da disciplina. Ele não depende do backend Django existente e pode ser executado isoladamente.

### 📦 Instalação das dependências de testes

```bash
cd python
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

### ▶️ Executando os testes e medindo cobertura

```bash
cd python
coverage run -m pytest
coverage report
coverage html  # gera htmlcov/
coverage xml   # gera cobertura em XML para a CI
```

- Os testes usam `pytest` com fixtures (`tests/conftest.py`) e marcadores personalizados (`slow`).
- Para pular testes lentos: `pytest -m "not slow"`.
- O relatório HTML fica em `python/htmlcov/index.html`.

### 🧪 Mapa dos testes

| Arquivo | Objetivo principal |
|---------|-------------------|
| `tests/test_multa_parametrizada.py` | Testes parametrizados do cálculo de multa e validação de valores inválidos. |
| `tests/test_excecoes.py` | Tratamento de exceções para estoque, limite de empréstimos e pagamento negado. |
| `tests/test_integracao.py` | Fluxo ponta-a-ponta com repositórios em memória, stub de e-mail e relógio controlado. |
| `tests/test_performance_relatorio.py` | Assegura execução rápida da devolução e geração de relatório usando `time.perf_counter`. |

### 🧱 Decisões de design

- **Doubles explícitos**: `FixedClock` controla o tempo; `StubEmailService` registra mensagens; o gateway de pagamento é mockado com `pytest-mock`.
- **Serviço coeso**: `LibraryService` concentra regras (limite de empréstimos, multa, notificações) e possui métodos privados (_cobrar_multa, _formatar_relatorio) para facilitar manutenção.
- **Repositórios em memória**: garantem isolamento dos testes sem dependências externas.
- **Relatórios exportáveis**: `exportar_relatorio` escreve em disco (via `tmp_path`) provando integração simples com I/O controlado.

### ⚠️ Limitações conhecidas

- Não há persistência real; os repositórios são reiniciados a cada execução.
- O gateway de pagamento é apenas simulado; não existe integração real com serviços externos.
- Regras de multa utilizam valor fixo (R$ 2,50/dia); novas políticas exigiriam ajustes adicionais.

### 🔁 Integração Contínua

O workflow `.github/workflows/ci.yml` executa automaticamente:
1. Instalação das dependências em `python/`.
2. `coverage run -m pytest`.
3. Geração dos relatórios `htmlcov` e `coverage.xml`.
4. Publicação dos artefatos de cobertura.

### 📣 Preparação para o pitch

Um roteiro detalhado está disponível em [`docs/pitch.md`](docs/pitch.md) com os principais tópicos da apresentação.

