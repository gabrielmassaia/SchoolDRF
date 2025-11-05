from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Livro:
    id: str
    titulo: str
    quantidade: int = 0

    def possui_copias(self) -> bool:
        return self.quantidade > 0

    def reservar_copia(self) -> None:
        self.quantidade -= 1

    def devolver_copia(self) -> None:
        self.quantidade += 1


@dataclass
class Usuario:
    id: str
    nome: str
    email: str
    limite_emprestimos: int = 3


@dataclass
class Emprestimo:
    id: str
    usuario_id: str
    livro_id: str
    data_emprestimo: date
    data_prevista: date
    data_devolucao: Optional[date] = None
    multa_cobrada: float = 0.0
    status: str = field(default="aberto")

    def esta_aberto(self) -> bool:
        return self.status == "aberto"

    def marcar_devolucao(self, data: date, multa: float) -> None:
        self.data_devolucao = data
        self.multa_cobrada = multa
        self.status = "devolvido"

