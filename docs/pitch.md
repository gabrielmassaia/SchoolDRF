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
- Workflow **CI** (`.github/workflows/ci.yml`) executa `coverage run -m pytest` em cada push/PR.
- Artefatos HTML/XML de cobertura são publicados, permitindo inspeção detalhada.
- Meta atingida: cobertura mínima de 80% linhas e 70% ramos no módulo `src/library`.

## 4. Desafios, Aprendizados e Próximos Passos
- **Desafios**: conciliar regras de negócio (estoque, multa e limite) mantendo testes independentes e rápidos.
- **Aprendizados**: uso disciplinado de TDD (commits vermelho → verde → refatorar) e organização de doubles (stubs/mocks) para isolamento.
- **Melhorias futuras**:
  - Adicionar teste de propriedade para valores aleatórios de atraso.
  - Simular envio de relatórios para múltiplos administradores usando parametrização adicional.
  - Explorar mutação com `mutmut` como métrica complementar de qualidade.

