class Emprestimo:
    def __init__(self, identificador, livro, usuario, data_emprestimo, data_prevista_devolucao):
        self._identificador = identificador
        self._livro = livro
        self._usuario = usuario
        self._data_emprestimo = data_emprestimo
        self._data_prevista_devolucao = data_prevista_devolucao
        self._data_devolucao = None


    @property
    def identificador(self):
        return self._identificador

    @property
    def livro(self):
        return self._livro

    @property
    def usuario(self):
        return self._usuario

    @property
    def data_emprestimo(self):
        return self._data_emprestimo

    @property
    def data_prevista_devolucao(self):
        return self._data_prevista_devolucao

    @property
    def data_devolucao(self):
        return self._data_devolucao

    @property
    def ativo(self):
        return self._data_devolucao is None

    def esta_atrasado(self, data_referencia):
        return self.ativo and data_referencia > self._data_prevista_devolucao

    def dias_de_atraso(self, data_referencia):
        if not self.esta_atrasado(data_referencia):
            return 0
        return (data_referencia - self._data_prevista_devolucao).days

    def registrar_devolucao(self, data_devolucao):
        self._data_devolucao = data_devolucao