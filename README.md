# Trabalho de Testes - Biblioteca (pytest)

Este repositório contém a entrega integral do trabalho de testes solicitado: um domínio de **biblioteca** com regras de limite de empréstimos, cálculo de multa progressiva, controle de estoque e notificações via e-mail simulado. Todo o desenvolvimento foi conduzido com foco em testes automatizados, doubles de dependência e execução em integração contínua.

---

## Conformidade com os requisitos do trabalho

| Item | Descrição                                                       | Implementação no repositório                                                                                                                         |
| ---- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Ciclo de vida de testes com fixtures e `tmp_path`               | `tests/conftest.py` define fixtures de escopo `function`, incluindo uso de `tmp_path` em `relatorio_em_tmp_path`                                     |
| 2    | TDD com commits vermelho → verde → refatorar                    | Histórico git da branch `work` preserva commits sequenciais demonstrando o ciclo solicitado                                                          |
| 3    | Testes de exceção                                               | `tests/test_excecoes.py` cobre estoque insuficiente, limite por usuário e pagamento negado                                                           |
| 4    | Testes parametrizados                                           | `tests/test_multa_parametrizada.py` usa `@pytest.mark.parametrize` para valores-limite de atraso                                                     |
| 5    | Stubs & mocks (e-mail, pagamento, relógio)                      | `tests/conftest.py` fornece `StubEmailService`, `MockPaymentGateway` e `FixedClock` controlado                                                       |
| 6    | Integração ponta-a-ponta em memória                             | `tests/test_integracao.py` valida o fluxo completo sem serviços reais                                                                                |
| 7    | Teste de performance com `time.perf_counter` marcado como lento | `tests/test_performance_relatorio.py::test_exportar_relatorio_eh_rapido` medindo tempo e marcado com `slow`                                          |
| 8    | Cobertura de linhas e ramos com meta ≥80% / ≥70%                | `.coveragerc` restringe a análise ao módulo `src/library`, e o relatório gerado por `coverage report` deve respeitar as metas (validar via CI/local) |
| 9    | Pipeline de CI com testes + artefatos de cobertura              | `.github/workflows/ci.yml` executa pytest com coverage e publica `htmlcov` + `coverage.xml`                                                          |
| 10   | README/documentação + roteiro de apresentação                   | Este README traz instruções completas; `docs/pitch.md` descreve o pitch e agora inclui um passo a passo de execução                                  |

> **Observações**:
>
> - não há componentes frontend/HTML no projeto; toda a interação é orientada a código e testes automatizados;
> - toda a execução (local ou no CI) ocorre diretamente a partir da raiz do repositório — não existe mais um diretório `python/` separado.

---

## 🛠️ Preparação do ambiente

1. **Criar e ativar** um ambiente virtual de preferência (ex.: `python -m venv .venv`).
   - Linux/macOS: `source .venv/bin/activate`
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
2. **Instalar dependências**: `pip install -r requirements.txt`

As versões foram pensadas para Python 3.11, alinhado com o pipeline do GitHub Actions.

---

## Execução dos testes

### Rodar a suíte completa com cobertura

```bash
coverage run -m pytest -q
coverage report            # resumo no terminal
coverage html              # gera htmlcov/
coverage xml               # gera coverage.xml
```

- Para abrir o relatório HTML, utilize `htmlcov/index.html`.
- Para focar apenas em testes rápidos: `pytest -m "not slow"`.

### Verificar metas de cobertura

Após `coverage report`, confirme que o módulo `src/library` apresenta:

- **Linhas**: ≥ 80%
- **Branches**: ≥ 70%

Esses limites são avaliados manualmente/localmente ou no artefato `coverage.xml` publicado pelo CI.

---

## Estrutura principal

```
├── src/
│   └── library/
│       ├── clock.py          # Relógio controlado (stub)
│       ├── exceptions.py     # Exceções de domínio
│       ├── models.py         # Entidades Livro, Usuario, Emprestimo
│       ├── repositories.py   # Repositórios em memória
│       └── services.py       # LibraryService com regras de negócio
├── tests/
│   ├── conftest.py
│   ├── test_excecoes.py
│   ├── test_integracao.py
│   ├── test_multa_parametrizada.py
│   └── test_performance_relatorio.py
├── .coveragerc
├── pytest.ini
├── requirements.txt
└── .github/workflows/ci.yml
```

---

## Decisões de design

- **Relógio controlado**: `FixedClock` permite simular a passagem do tempo e atrasos determinísticos.
- **Repositórios em memória**: `InMemoryBookRepository`, `InMemoryUserRepository` e `InMemoryLoanRepository` garantem isolamento dos testes.
- **Doubles explícitos**: `StubEmailService` armazena notificações e `MockPaymentGateway` controla aprovação/negação sem acessar serviços externos.
- **Serviço central**: `LibraryService` concentra regras de negócio (limite, multa, cobrança e notificações) e expõe métodos claros para registrar/devolver empréstimos.
- **Exportação controlada**: `exportar_relatorio` escreve em diretórios temporários durante testes utilizando `tmp_path`.

---

## Integração Contínua

O workflow [`ci.yml`](.github/workflows/ci.yml) é acionado para `push` e `pull_request` nas branches principais (`main`, `master`, `work`). Ele:

1. Configura Python 3.11.
2. Instala dependências com `pip install -r requirements.txt`.
3. Executa `coverage run -m pytest -q`.
4. Gera relatórios HTML/XML de cobertura.
5. Publica os artefatos `htmlcov` e `coverage.xml`.

---

## Documentação complementar

- [`docs/pitch.md`](docs/pitch.md): roteiro da apresentação, com visão do domínio, evidências dos testes e orientação de execução passo a passo para demonstrações.

---

## Melhorias futuras

- Adicionar testes de propriedade para o cálculo de multa com valores aleatórios controlados.
- Automatizar análise de mutação (ex.: `mutmut`) como métrica complementar de qualidade.
- Expandir o serviço com relatórios para múltiplos administradores usando parametrização adicional.
