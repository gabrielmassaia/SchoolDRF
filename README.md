# Trabalho de Testes - Biblioteca (pytest)

Este repositório implementa o trabalho prático de testes de software solicitado pela disciplina. O cenário modela uma **biblioteca** com as entidades `Livro`, `Usuario` e `Emprestimo`, contemplando regras de limite por usuário, cálculo de multa progressiva e notificação por e-mail. Todo o desenvolvimento foi conduzido com foco em testes automatizados e integrações simuladas.

---

## 🚀 Como executar os testes

### 1. Preparar ambiente

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

### 2. Rodar a suíte com cobertura

```bash
coverage run -m pytest
coverage report
coverage html   # gera htmlcov/
coverage xml    # gera coverage.xml
```

- Para pular testes lentos: `pytest -m "not slow"`.
- O relatório HTML pode ser aberto em `htmlcov/index.html`.

---

## 🧪 Mapa dos testes

| Arquivo | Objetivo principal |
|---------|-------------------|
| `tests/test_multa_parametrizada.py` | Testes parametrizados do cálculo de multa e validação de valores-limite. |
| `tests/test_excecoes.py` | Garantia das exceções para estoque, limite de empréstimos e pagamento negado. |
| `tests/test_integracao.py` | Fluxo ponta-a-ponta com repositórios em memória, stub de e-mail e relógio controlado. |
| `tests/test_performance_relatorio.py` | Mede tempo de execução de relatório usando `time.perf_counter` e marcação `slow`. |

As fixtures vivem em `tests/conftest.py` e demonstram uso de `@pytest.fixture` com escopo de função, doubles de dependência e diretório temporário (`tmp_path`).

---

## 🧱 Decisões de design

- **Relógio controlado**: `FixedClock` permite simular a passagem do tempo em atrasos sem depender de relógio real.
- **Repositórios em memória**: fornecem isolamento, com `InMemoryBookRepository`, `InMemoryUserRepository` e `InMemoryLoanRepository`.
- **Doubles explícitos**: `StubEmailService` registra mensagens enviadas e `MockPaymentGateway` controla o resultado do pagamento.
- **Serviço central**: `LibraryService` concentra regras de negócio (limite, multa, cobrança e notificações) e expõe métodos claros para registrar e devolver empréstimos.
- **Integração controlada**: `exportar_relatorio` usa `tmp_path` para provar escrita em disco durante os testes.

---

## ⚙️ Integração Contínua

O workflow [`ci.yml`](.github/workflows/ci.yml) executa automaticamente em cada push/PR:

1. Instalação das dependências via `pip`.
2. Execução de `coverage run -m pytest`.
3. Geração dos relatórios `htmlcov` e `coverage.xml`.
4. Publicação dos artefatos de cobertura para consulta.

---

## 📑 Documentação complementar

- [`docs/pitch.md`](docs/pitch.md): roteiro sugerido para apresentação do projeto, incluindo destaques de regras de negócio, métricas e aprendizados.

---

## 🔮 Melhorias futuras


- Adicionar testes de propriedade para o cálculo de multa com valores aleatórios controlados.
- Automatizar análise de mutação (ex.: `mutmut`) para reforçar a qualidade.
- Expandir o serviço com relatórios para múltiplos administradores usando parametrização adicional.

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

