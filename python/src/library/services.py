from __future__ import annotations

import json
import uuid
from datetime import timedelta
from typing import Dict, Optional

from .exceptions import LimiteEmprestimosAtingido, PagamentoRecusado, SemCopiasDisponiveis
from .models import Emprestimo, Livro, Usuario


class LibraryService:
    def __init__(
        self,
        emprestimo_repo,
        livro_repo,
        usuario_repo,
        email_service,
        clock,
        payment_gateway,
        multa_diaria: float = 2.5,
        periodo_padrao: Optional[timedelta] = None,
    ) -> None:
        self.emprestimo_repo = emprestimo_repo
        self.livro_repo = livro_repo
        self.usuario_repo = usuario_repo
        self.email = email_service
        self.clock = clock
        self.payment_gateway = payment_gateway
        self.multa_diaria = multa_diaria
        self.periodo_padrao = periodo_padrao or timedelta(days=7)

    def calcular_multa(self, dias_atraso: int) -> float:
        if dias_atraso < 0:
            raise ValueError("Dias de atraso nao podem ser negativos")
        return dias_atraso * self.multa_diaria

    def registrar_emprestimo(self, usuario_id: str, livro_id: str, dias: int) -> Emprestimo:
        usuario = self.usuario_repo.obter_por_id(usuario_id)
        livro = self.livro_repo.obter_por_id(livro_id)
        self._garantir_disponibilidade(livro)
        self._garantir_limite(usuario)

        data_emprestimo = self.clock.hoje()
        data_prevista = data_emprestimo + timedelta(days=dias)
        emprestimo = self._novo_emprestimo(usuario_id, livro_id, data_prevista)
        emprestimo.data_emprestimo = data_emprestimo

        livro.reservar_copia()
        self.livro_repo.atualizar(livro)
        self.emprestimo_repo.adicionar(emprestimo)

        self._notificar(
            usuario.email,
            "Emprestimo registrado",
            f"Livro {livro.titulo} emprestado ate {emprestimo.data_prevista.isoformat()}",
        )
        return emprestimo

    def registrar_devolucao(self, emprestimo_id: str) -> Emprestimo:
        emprestimo = self.emprestimo_repo.obter_por_id(emprestimo_id)
        livro = self.livro_repo.obter_por_id(emprestimo.livro_id)
        usuario = self.usuario_repo.obter_por_id(emprestimo.usuario_id)

        data_devolucao = self.clock.hoje()
        dias_atraso = self._calcular_dias_atraso(data_devolucao, emprestimo.data_prevista)
        multa = self.calcular_multa(dias_atraso)

        if multa > 0:
            self._cobrar_multa(usuario, livro, multa)

        emprestimo.marcar_devolucao(data_devolucao, multa)
        self.emprestimo_repo.atualizar(emprestimo)
        livro.devolver_copia()
        self.livro_repo.atualizar(livro)

        self._notificar(usuario.email, "Devolucao processada", f"Multa cobrada: {multa:.2f}")
        return emprestimo

    def gerar_relatorio_emprestimos(self) -> Dict[str, Dict[str, object]]:
        relatorio = {}
        for emprestimo in self.emprestimo_repo.todos():
            relatorio[emprestimo.id] = self._formatar_relatorio(emprestimo)
        return relatorio

    def exportar_relatorio(self, caminho) -> None:
        relatorio = self.gerar_relatorio_emprestimos()
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(relatorio, arquivo, ensure_ascii=False, indent=2)

    def _garantir_disponibilidade(self, livro: Livro) -> None:
        if not livro.possui_copias():
            raise SemCopiasDisponiveis(f"Livro {livro.id} sem estoque")

    def _garantir_limite(self, usuario: Usuario) -> None:
        emprestimos_abertos = list(self.emprestimo_repo.listar_abertos_por_usuario(usuario.id))
        if len(emprestimos_abertos) >= usuario.limite_emprestimos:
            raise LimiteEmprestimosAtingido(usuario.id)

    def _novo_emprestimo(self, usuario_id: str, livro_id: str, data_prevista) -> Emprestimo:
        return Emprestimo(
            id=str(uuid.uuid4()),
            usuario_id=usuario_id,
            livro_id=livro_id,
            data_emprestimo=self.clock.hoje(),
            data_prevista=data_prevista,
        )

    def _calcular_dias_atraso(self, data_devolucao, data_prevista) -> int:
        return max(0, (data_devolucao - data_prevista).days)

    def _cobrar_multa(self, usuario: Usuario, livro: Livro, multa: float) -> None:
        resultado = self.payment_gateway.cobrar(
            usuario_id=usuario.id,
            valor=multa,
            descricao=f"Multa por atraso do livro {livro.titulo}",
        )
        if resultado.get("status") != "aprovado":
            raise PagamentoRecusado("Pagamento da multa nao aprovado")

    def _notificar(self, destinatario: str, assunto: str, corpo: str) -> None:
        self.email.enviar_notificacao(destinatario, assunto, corpo)

    def _formatar_relatorio(self, emprestimo: Emprestimo) -> Dict[str, object]:
        return {
            "usuario_id": emprestimo.usuario_id,
            "livro_id": emprestimo.livro_id,
            "status": emprestimo.status,
            "data_prevista": emprestimo.data_prevista.isoformat(),
            "data_devolucao": emprestimo.data_devolucao.isoformat() if emprestimo.data_devolucao else None,
            "multa": emprestimo.multa_cobrada,
        }

