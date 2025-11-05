import pytest

from src.library.exceptions import LimiteEmprestimosAtingido, PagamentoRecusado, SemCopiasDisponiveis


def test_nao_permite_emprestimo_sem_copias(service):
    service.livro_repo.atualizar_quantidade("livro-1", 0)
    with pytest.raises(SemCopiasDisponiveis):
        service.registrar_emprestimo(usuario_id="user-1", livro_id="livro-1", dias=7)


def test_nao_permite_ultrapassar_limite(service, livro_repo, emprestimo_repo):
    for i in range(3):
        emprestimo_repo.adicionar(
            service._novo_emprestimo(
                usuario_id="user-1",
                livro_id=f"livro-{i}",
                data_prevista=service.clock.hoje() + service.periodo_padrao,
            )
        )
    with pytest.raises(LimiteEmprestimosAtingido):
        service.registrar_emprestimo(usuario_id="user-1", livro_id="livro-1", dias=7)


def test_pagamento_recusado_dispara_excecao(service, payment_gateway_mock):
    payment_gateway_mock.cobrar.return_value = {"status": "negado"}
    emprestimo = service.registrar_emprestimo(usuario_id="user-1", livro_id="livro-1", dias=1)
    service.clock.avancar(dias=3)
    with pytest.raises(PagamentoRecusado):
        service.registrar_devolucao(emprestimo.id)

