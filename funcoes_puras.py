from functools import reduce

MULTA_DIARIA = 2.0

def filtrar_livros_por_categoria(livros, categoria):
    return tuple(filter(lambda livro: livro.categoria == categoria, livros))


def calcular_multa(dias_de_atraso, valor_multa_diaria):
    return dias_de_atraso * valor_multa_diaria


def filtrar_emprestimos_atrasados(emprestimos, data_referencia):
    return tuple(filter(lambda emprestimo: emprestimo.esta_atrasado(data_referencia), emprestimos))


def montar_item_de_multa(emprestimo, data_referencia):
    dias = emprestimo.dias_de_atraso(data_referencia)
    return{
        "usuario": emprestimo.usuario.nome,
        "livro": emprestimo.livro.titulo,
        "dias_de_atraso": dias,
        "multa": calcular_multa(dias, MULTA_DIARIA)
    }

def gerar_relatorio_de_multas(emprestimos, data_referencia):
    atrasados = filtrar_emprestimos_atrasados(emprestimos, data_referencia)
    itens = tuple(map(lambda emprestimo: montar_item_de_multa(emprestimo, data_referencia), atrasados))
    total = reduce(lambda soma, item: soma + item["multa"], itens, 0)
    return{"itens": itens, "total": total}


def contar_livros_por_categoria(livros):
    return reduce(
        lambda contagem, livros: {**contagem, livros.categoria: contagem.get(livros.categoria, 0) + 1}, livros,
        {}
    )


def contar_emprestimos_por_usuario(emprestimos):
    return reduce(
        lambda contagem, emprestimo: {**contagem, emprestimo.usuario.nome: contagem.get(emprestimo.usuario.nome, 0) + 1},
        emprestimos,
        {}
    )


def contar_emprestimos_ativos(emprestimos):
    return len(tuple(filter(lambda emprestimo: emprestimo.ativo, emprestimos)))


def contar_emprestimos_atrasados(emprestimos, data_referencia):
    return len(filtrar_emprestimos_atrasados(emprestimos, data_referencia))


def calcular_total_de_multas(emprestimos, data_referencia):
    return gerar_relatorio_de_multas(emprestimos, data_referencia)["total"]