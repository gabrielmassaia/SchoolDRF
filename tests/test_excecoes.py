import pytest
from datetime import date, timedelta
from src.library.clock import FixedClock
from src.library.clock import Clock

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

def test_avancar_dias_padrao():
    hoje = date(2024, 1, 1)
    clock = FixedClock(hoje)

    clock.avancar()

    assert clock.hoje() == hoje + timedelta(days=1)


def test_avancar_dias_personalizado():
    hoje = date(2024, 1, 1)
    clock = FixedClock(hoje)
    clock.avancar(5)
    assert clock.hoje() == hoje + timedelta(days=5)

def test_clock_hoje_retorna_data_atual(monkeypatch):
    fixed_date = date(2024, 1, 1)
    monkeypatch.setattr("src.library.clock.date", type("MockDate", (), {"today": staticmethod(lambda: fixed_date)}))
    
    clock = Clock()
    assert clock.hoje() == fixed_date