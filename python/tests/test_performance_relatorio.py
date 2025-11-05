import time
import pytest


@pytest.mark.slow
def test_devolucao_e_geracao_relatorio_rapida(service, tmp_path):
    emprestimo = service.registrar_emprestimo("user-1", "livro-1", dias=1)
    service.clock.avancar(dias=1)

    t0 = time.perf_counter()
    service.registrar_devolucao(emprestimo.id)
    duracao = time.perf_counter() - t0
    assert duracao < 0.2

    arquivo = tmp_path / "relatorio.json"
    service.exportar_relatorio(arquivo)
    assert arquivo.exists()
    assert arquivo.read_text()

