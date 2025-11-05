import datetime as dt


def test_fluxo_completo(service, email_stub, emprestimo_repo, clock_stub):
    emprestimo = service.registrar_emprestimo(usuario_id="user-1", livro_id="livro-1", dias=2)
    assert emprestimo_repo.obter_por_id(emprestimo.id).usuario_id == "user-1"
    assert email_stub.mensagens[-1][1] == "Emprestimo registrado"

    clock_stub.avancar(dias=4)
    devolucao = service.registrar_devolucao(emprestimo.id)

    assert devolucao.data_devolucao == dt.date(2024, 5, 14)
    assert devolucao.multa_cobrada > 0
    assert email_stub.mensagens[-1][1] == "Devolucao processada"

    relatorio = service.gerar_relatorio_emprestimos()
    assert relatorio[emprestimo.id]["status"] == "devolvido"

