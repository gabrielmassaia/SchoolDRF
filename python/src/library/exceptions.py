class BibliotecaErro(Exception):
    """Excecao base para a biblioteca."""


class UsuarioNaoEncontrado(BibliotecaErro):
    pass


class LivroNaoEncontrado(BibliotecaErro):
    pass


class SemCopiasDisponiveis(BibliotecaErro):
    pass


class LimiteEmprestimosAtingido(BibliotecaErro):
    pass


class EmprestimoNaoEncontrado(BibliotecaErro):
    pass


class PagamentoRecusado(BibliotecaErro):
    pass

