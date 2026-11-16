from functools import reduce

from funcoes_puras import MULTA_DIARIA, calcular_multa


def calcular_total_de_multas_imperativo(emprestimos, data_referencia):
    total = 0
    for emprestimo in emprestimos:
        if emprestimo.esta_atrasado(data_referencia):
            dias = emprestimo.dias_de_atraso(data_referencia)
            total = total + calcular_multa(dias, MULTA_DIARIA)
    return total


def calcular_total_de_multas_funcional(emprestimos, data_referencia):
    atrasados = filter(lambda emprestimo: emprestimo.esta_atrasado(data_referencia), emprestimos)
    multas = map(lambda emprestimo: calcular_multa(emprestimo.dias_de_atraso(data_referencia), MULTA_DIARIA), atrasados)
    return reduce(lambda soma, multa: soma + multa, multas, 0)