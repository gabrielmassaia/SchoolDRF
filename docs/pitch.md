# Pitch do Projeto de Testes da Biblioteca

## 1. Cenário e Regras de Negócio

- **Entidades principais**: `Livro`, `Usuario` e `Emprestimo`.
- **Regras implementadas**:
  - Controle de estoque de livros e limite máximo de empréstimos por usuário.
  - Multa progressiva de R$ 2,50 por dia de atraso na devolução.
  - Cobrança automática da multa via gateway de pagamento dobrado (mockado).
  - Notificações por e-mail utilizando um stub controlado durante os testes.
  - Relógio controlado (`FixedClock`) para simular passagem do tempo sem acessar serviços reais.

## 2. Testes Parametrizados e Exceções

- `tests/test_multa_parametrizada.py` cobre diferentes valores de atraso e valida o cálculo da multa com `@pytest.mark.parametrize`.
- Exceções relevantes garantem robustez:
  - `SemCopiasDisponiveis` quando o estoque chega a zero.
  - `LimiteEmprestimosAtingido` ao exceder o limite configurado do usuário.
  - `PagamentoRecusado` ao simular retorno negativo do gateway de pagamento.

## 3. Pipeline e Relatórios de Cobertura

- Workflow **CI** (`.github/workflows/ci.yml`) executa `coverage run -m pytest -q` em cada push/PR.
- Artefatos HTML/XML de cobertura são publicados, permitindo inspeção detalhada.
- Meta sugerida: cobertura mínima de 80% linhas e 70% ramos no módulo `src/library`.

## 4. Passo a passo para demonstração

1. Criar e ativar um ambiente virtual (`python -m venv .venv` → `source .venv/bin/activate`).
2. Instalar dependências (`pip install -r requirements.txt`).
3. Executar a suíte de testes (`coverage run -m pytest -q`).
4. Gerar e analisar relatórios (`coverage report`, `coverage html`, `coverage xml`).
5. Destacar testes específicos durante o pitch:
   - Parametrização (`tests/test_multa_parametrizada.py`).
   - Exceções (`tests/test_excecoes.py`).
   - Integração ponta-a-ponta (`tests/test_integracao.py`).
   - Performance marcada como lenta (`tests/test_performance_relatorio.py`).
6. Apresentar os artefatos de cobertura publicados pelo CI (pasta `htmlcov` ou artefato do GitHub Actions).

## 5. Desafios, Aprendizados e Próximos Passos

- **Desafios**: conciliar regras de negócio (estoque, multa e limite) mantendo testes independentes e rápidos.
- **Aprendizados**: uso disciplinado de TDD (commits vermelho → verde → refatorar) e organização de doubles (stubs/mocks) para isolamento.
- **Melhorias futuras**:
  - Adicionar teste de propriedade para valores aleatórios de atraso.
  - Simular envio de relatórios para múltiplos administradores usando parametrização adicional.
  - Explorar mutação com `mutmut` como métrica complementar de qualidade.
