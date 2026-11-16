from emprestimo import Emprestimo

class Biblioteca:
    def __init__(self):
        self._livros = []
        self._usuarios = []
        self._emprestimos = []

    @property
    def livros(self):
        return tuple(self._livros)

    @property
    def usuarios(self):
        return tuple(self._usuarios)

    @property
    def emprestimos(self):
        return tuple(self._emprestimos)

    def cadastrar_livro(self, livro):
        self._livros.append(livro)

    def cadastrar_usuario(self, usuario):
        self._usuarios.append(usuario)

    def consultar_livro(self, identificador):
        for livro in self._livros:
            if livro.identificador == identificador:
                return livro
        return None

    def consultar_usuario(self, identificador):
        for usuario in self._usuarios:
            if usuario.identificador == identificador:
                return usuario
        return None

    def livro_disponivel(self, livro):
        for emprestimo in self._emprestimos:
            if emprestimo.ativo and emprestimo.livro is livro:
                return False
        return True

    def registrar_emprestimo(self, livro, usuario, data_emprestimo, data_prevista_devolucao):
        if not self.livro_disponivel(livro):
            raise ValueError("Livro já está emprestado")
        identificador = len(self._emprestimos) + 1
        emprestimo = Emprestimo(identificador, livro, usuario, data_emprestimo, data_prevista_devolucao)
        self._emprestimos.append(emprestimo)
        return emprestimo

    def registrar_devolucao(self, emprestimo, data_devolucao):
        emprestimo.registrar_devolucao(data_devolucao)