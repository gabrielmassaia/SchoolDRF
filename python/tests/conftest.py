import datetime as dt
import pathlib
import sys
from unittest.mock import Mock

import pytest

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from src.library.services import LibraryService
from src.library.repositories import (
    InMemoryEmprestimoRepository,
    InMemoryLivroRepository,
    InMemoryUsuarioRepository,
)
from src.library.models import Livro, Usuario
from src.library.clock import FixedClock


class StubEmailService:
    def __init__(self) -> None:
        self.mensagens = []

    def enviar_notificacao(self, destinatario: str, assunto: str, corpo: str) -> None:
        self.mensagens.append((destinatario, assunto, corpo))


@pytest.fixture
def mocker():
    class SimpleMocker:
        def Mock(self, *args, **kwargs):
            return Mock(*args, **kwargs)

    return SimpleMocker()


@pytest.fixture
def email_stub():
    return StubEmailService()


@pytest.fixture
def clock_stub():
    return FixedClock(dt.date(2024, 5, 10))


@pytest.fixture
def usuario_repo():
    repo = InMemoryUsuarioRepository()
    repo.adicionar(Usuario(id="user-1", nome="Ana", email="ana@example.com", limite_emprestimos=3))
    return repo


@pytest.fixture
def livro_repo():
    repo = InMemoryLivroRepository()
    repo.adicionar(Livro(id="livro-1", titulo="Testes", quantidade=2))
    return repo


@pytest.fixture
def emprestimo_repo():
    return InMemoryEmprestimoRepository()


@pytest.fixture
def payment_gateway_mock(mocker):
    gateway = mocker.Mock()
    gateway.cobrar.return_value = {"status": "aprovado", "transacao": "tx-1"}
    return gateway


@pytest.fixture
def service(emprestimo_repo, livro_repo, usuario_repo, email_stub, clock_stub, payment_gateway_mock):
    return LibraryService(
        emprestimo_repo=emprestimo_repo,
        livro_repo=livro_repo,
        usuario_repo=usuario_repo,
        email_service=email_stub,
        clock=clock_stub,
        payment_gateway=payment_gateway_mock,
    )

