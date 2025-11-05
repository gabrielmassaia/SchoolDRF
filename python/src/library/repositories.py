from __future__ import annotations

from dataclasses import replace
from typing import Dict, Iterable

from .exceptions import EmprestimoNaoEncontrado, LivroNaoEncontrado, UsuarioNaoEncontrado
from .models import Emprestimo, Livro, Usuario


class InMemoryLivroRepository:
    def __init__(self) -> None:
        self._livros: Dict[str, Livro] = {}

    def adicionar(self, livro: Livro) -> None:
        self._livros[livro.id] = livro

    def obter_por_id(self, livro_id: str) -> Livro:
        try:
            return self._livros[livro_id]
        except KeyError as exc:
            raise LivroNaoEncontrado(livro_id) from exc

    def atualizar(self, livro: Livro) -> None:
        if livro.id not in self._livros:
            raise LivroNaoEncontrado(livro.id)
        self._livros[livro.id] = livro

    def atualizar_quantidade(self, livro_id: str, quantidade: int) -> None:
        livro = self.obter_por_id(livro_id)
        self._livros[livro_id] = replace(livro, quantidade=quantidade)


class InMemoryUsuarioRepository:
    def __init__(self) -> None:
        self._usuarios: Dict[str, Usuario] = {}

    def adicionar(self, usuario: Usuario) -> None:
        self._usuarios[usuario.id] = usuario

    def obter_por_id(self, usuario_id: str) -> Usuario:
        try:
            return self._usuarios[usuario_id]
        except KeyError as exc:
            raise UsuarioNaoEncontrado(usuario_id) from exc


class InMemoryEmprestimoRepository:
    def __init__(self) -> None:
        self._emprestimos: Dict[str, Emprestimo] = {}

    def adicionar(self, emprestimo: Emprestimo) -> Emprestimo:
        self._emprestimos[emprestimo.id] = emprestimo
        return emprestimo

    def obter_por_id(self, emprestimo_id: str) -> Emprestimo:
        try:
            return self._emprestimos[emprestimo_id]
        except KeyError as exc:
            raise EmprestimoNaoEncontrado(emprestimo_id) from exc

    def listar_abertos_por_usuario(self, usuario_id: str) -> Iterable[Emprestimo]:
        return [e for e in self._emprestimos.values() if e.usuario_id == usuario_id and e.esta_aberto()]

    def atualizar(self, emprestimo: Emprestimo) -> Emprestimo:
        if emprestimo.id not in self._emprestimos:
            raise EmprestimoNaoEncontrado(emprestimo.id)
        self._emprestimos[emprestimo.id] = emprestimo
        return emprestimo

    def todos(self) -> Iterable[Emprestimo]:
        return list(self._emprestimos.values())

