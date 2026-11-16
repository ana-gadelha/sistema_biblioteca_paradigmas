class Usuario:
    def __init__(self, identificador, nome, matricula):
        self._identificador = identificador
        self._nome = nome
        self._matricula = matricula

    @property
    def identificador(self):
        return self._identificador

    @property
    def nome(self):
        return self._nome

    @property
    def matricula(self):
        return self._matricula