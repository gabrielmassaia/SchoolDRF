import pytest

from src.library.exceptions import (
    EmprestimoNaoEncontrado,
    LivroNaoEncontrado,
    UsuarioNaoEncontrado,
)
from src.library.models import Emprestimo, Livro
from src.library.repositories import (
    InMemoryEmprestimoRepository,
    InMemoryLivroRepository,
    InMemoryUsuarioRepository,
)


def test_livro_repository_erro_quando_inexistente():
    repo = InMemoryLivroRepository()
    with pytest.raises(LivroNaoEncontrado):
        repo.obter_por_id("desconhecido")
    with pytest.raises(LivroNaoEncontrado):
        repo.atualizar(Livro(id="x", titulo="Falso", quantidade=1))


def test_livro_repository_atualiza_quantidade(livro_repo):
    livro_repo.atualizar_quantidade("livro-1", 5)
    livro = livro_repo.obter_por_id("livro-1")
    assert livro.quantidade == 5


def test_usuario_repository_erro_quando_nao_encontra():
    repo = InMemoryUsuarioRepository()
    with pytest.raises(UsuarioNaoEncontrado):
        repo.obter_por_id("nao-existe")


def test_emprestimo_repository_fluxo_completo(clock_stub):
    repo = InMemoryEmprestimoRepository()
    emprestimo = Emprestimo(
        id="emprestimo-1",
        usuario_id="u1",
        livro_id="l1",
        data_emprestimo=clock_stub.hoje(),
        data_prevista=clock_stub.hoje(),
    )
    repo.adicionar(emprestimo)

    assert repo.obter_por_id("emprestimo-1").id == "emprestimo-1"
    assert list(repo.listar_abertos_por_usuario("u1")) == [emprestimo]
    assert repo.todos() == [emprestimo]

    emprestimo.marcar_devolucao(clock_stub.hoje(), multa=0)
    repo.atualizar(emprestimo)

    assert list(repo.listar_abertos_por_usuario("u1")) == []

    with pytest.raises(EmprestimoNaoEncontrado):
        repo.obter_por_id("desconhecido")
    with pytest.raises(EmprestimoNaoEncontrado):
        repo.atualizar(
            Emprestimo(
                id="nao-tem",
                usuario_id="u2",
                livro_id="l2",
                data_emprestimo=clock_stub.hoje(),
                data_prevista=clock_stub.hoje(),
            )
        )
