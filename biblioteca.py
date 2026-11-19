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
        if self.consultar_livro(livro.identificador) is not None:
            raise ValueError("Já existe um livro com esse identificador")
        self._livros.append(livro)

    def cadastrar_usuario(self, usuario):
        if self.consultar_usuario(usuario.identificador) is not None:
            raise ValueError("Já existe um usuário com esse identificador")
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
            if emprestimo.ativo and emprestimo.livro.identificador == livro.identificador:
                return False
        return True

    def registrar_emprestimo(self, livro, usuario, data_emprestimo, data_prevista_devolucao):
        if self.consultar_livro(livro.identificador) is not livro:
            raise ValueError("Livro não cadastrado")
        if self.consultar_usuario(usuario.identificador) is not usuario:
            raise ValueError("Usuário não cadastrado")
        if not self.livro_disponivel(livro):
            raise ValueError("Livro já está emprestado")
        identificador = len(self._emprestimos) + 1
        emprestimo = Emprestimo(identificador, livro, usuario, data_emprestimo, data_prevista_devolucao)

        for anterior in self._emprestimos:
            if (
                anterior.livro.identificador == livro.identificador
                and anterior.data_devolucao is not None
                and data_emprestimo < anterior.data_devolucao
            ):
                raise ValueError("A retirada é anterior a uma devolução registrada para este livro")

        self._emprestimos.append(emprestimo)
        return emprestimo

    def registrar_devolucao(self, emprestimo, data_devolucao):
        if not any(registrado is emprestimo for registrado in self._emprestimos):
            raise ValueError("Empréstimo não registrado nesta biblioteca")
        emprestimo.registrar_devolucao(data_devolucao)
