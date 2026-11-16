class Livro:
    def __init__(self, identificador, titulo, autor, categoria):
        self._identificador = identificador
        self._titulo = titulo
        self._autor = autor
        self._categoria = categoria

    @property
    def identificador(self):
        return self._identificador

    @property
    def titulo(self):
        return self._titulo

    @property
    def autor(self):
        return self._autor

    @property
    def categoria(self):
        return self._categoria