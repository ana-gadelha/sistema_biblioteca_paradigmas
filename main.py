from datetime import date
from livro import Livro
from usuario import Usuario
from biblioteca import Biblioteca
from funcoes_puras import (
    filtrar_livros_por_categoria,
    gerar_relatorio_de_multas,
    contar_livros_por_categoria,
    contar_emprestimos_por_usuario,
    contar_emprestimos_ativos,
    contar_emprestimos_atrasados,
    calcular_total_de_multas
)
from comparacao import(
    calcular_total_de_multas_imperativo,
    calcular_total_de_multas_funcional
)

biblioteca = Biblioteca()

dom_casmurro = Livro(1, "Dom Casmurro", "Machado de Assis", "Romance")
codigo_limpo = Livro(2, "Código Limpo", "Robert Martin", "Tecnologia")
capitaes_da_areia = Livro(3, "Capitães da Areia", "Jorge Amado", "Romance")
python_fluente = Livro(4, "Python Fluente", "Luciano Ramalho", "Tecnologia")
sapiens = Livro(5, "Sapiens", "Yuval Harari", "História")

ana = Usuario(1, "Ana", "2023001")
bruno = Usuario(2, "Bruno", "2023002")
carla = Usuario(3, "Carla", "2023003")

for livro in (dom_casmurro, codigo_limpo, capitaes_da_areia, python_fluente, sapiens):
    biblioteca.cadastrar_livro(livro)

for usuario in (ana, bruno, carla):
    biblioteca.cadastrar_usuario(usuario)

biblioteca.registrar_emprestimo(dom_casmurro, ana, date(2026, 11, 1), date(2026, 11, 8))
biblioteca.registrar_emprestimo(codigo_limpo, bruno, date(2026, 10, 28), date(2026, 11, 4))
biblioteca.registrar_emprestimo(sapiens, ana, date(2026, 11, 5), date(2026, 11, 12))
emprestimo_devolvido = biblioteca.registrar_emprestimo(capitaes_da_areia, carla, date(2026, 10, 20), date(2026, 10, 27))
biblioteca.registrar_devolucao(emprestimo_devolvido, date(2026, 10, 30))

data_referencia = date(2026, 11, 11)

print("=== Regra: livro já emprestado ===")
try:
    biblioteca.registrar_emprestimo(dom_casmurro, carla, date(2026, 11, 10), date(2026, 11, 17))
except ValueError as erro:
    print("Recusado:", erro)

print("=== Filtragem por categoria ===")
romances = filtrar_livros_por_categoria(biblioteca.livros, "Romance")
print("Romances:", tuple(map(lambda livro: livro.titulo, romances)))
print("Livros no acervo após o filtro:", len(biblioteca.livros))

print("=== Relatório de multas ===")
relatorio = gerar_relatorio_de_multas(biblioteca.emprestimos, data_referencia)
for item in relatorio["itens"]:
    print(item["usuario"], "-", item["livro"], "-", item["dias_de_atraso"], "dias - R$", item["multa"])
print("Total de multas: R$", relatorio["total"])

print("=== Estatísticas ===")
print("Livros por categoria:", contar_livros_por_categoria(biblioteca.livros))
print("Empréstimos por usuário:", contar_emprestimos_por_usuario(biblioteca.emprestimos))
print("Empréstimos ativos:", contar_emprestimos_ativos(biblioteca.emprestimos))
print("Empréstimos ativos em atraso:", contar_emprestimos_atrasados(biblioteca.emprestimos, data_referencia))
print("Valor total das multas: R$", calcular_total_de_multas(biblioteca.emprestimos, data_referencia))

print("=== Comparação entre paradigmas ===")
total_imperativo = calcular_total_de_multas_imperativo(biblioteca.emprestimos, data_referencia)
total_funcional = calcular_total_de_multas_funcional(biblioteca.emprestimos, data_referencia)
print("Versão imperativa: R$", total_imperativo)
print("Versão funcional: R$", total_funcional)
print("Resultados equivalentes:", total_imperativo == total_funcional)