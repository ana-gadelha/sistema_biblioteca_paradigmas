import subprocess
import sys
import unittest
from datetime import date
from pathlib import Path

from biblioteca import Biblioteca
from comparacao import calcular_total_de_multas_funcional, calcular_total_de_multas_imperativo
from funcoes_puras import contar_emprestimos_por_usuario, gerar_relatorio_de_multas
from livro import Livro
from usuario import Usuario


def dia(numero):
    return date(2026, 11, numero)


class TestBiblioteca(unittest.TestCase):
    def setUp(self):
        self.biblioteca = Biblioteca()
        self.livro = Livro(1, "Dom Casmurro", "Machado de Assis", "Romance")
        self.usuario = Usuario(1, "Ana", "2023001")
        self.biblioteca.cadastrar_livro(self.livro)
        self.biblioteca.cadastrar_usuario(self.usuario)

    def emprestar_livro(self):
        return self.biblioteca.registrar_emprestimo(self.livro, self.usuario, dia(1), dia(8))

    def test_cadastros_rejeitam_identificadores_duplicados(self):
        with self.assertRaises(ValueError):
            self.biblioteca.cadastrar_livro(Livro(1, "Outro título", "Outro autor", "Romance"))
        with self.assertRaises(ValueError):
            self.biblioteca.cadastrar_usuario(Usuario(1, "Bruno", "2023002"))

        self.assertEqual(self.biblioteca.livros, (self.livro,))
        self.assertEqual(self.biblioteca.usuarios, (self.usuario,))

    def test_disponibilidade_considera_o_identificador_do_livro(self):
        emprestimo = self.emprestar_livro()
        copia = Livro(1, self.livro.titulo, self.livro.autor, self.livro.categoria)

        self.assertFalse(self.biblioteca.livro_disponivel(copia))
        for candidato in (self.livro, copia):
            with self.subTest(livro=candidato), self.assertRaises(ValueError):
                self.biblioteca.registrar_emprestimo(candidato, self.usuario, dia(2), dia(9))
        self.assertEqual(self.biblioteca.emprestimos, (emprestimo,))

    def test_emprestimo_exige_livro_e_usuario_cadastrados(self):
        livro_externo = Livro(2, "Sapiens", "Yuval Harari", "História")
        usuario_externo = Usuario(2, "Bruno", "2023002")
        for livro, usuario in ((livro_externo, self.usuario), (self.livro, usuario_externo)):
            with self.subTest(livro=livro, usuario=usuario), self.assertRaises(ValueError):
                self.biblioteca.registrar_emprestimo(livro, usuario, dia(1), dia(8))
        self.assertEqual(self.biblioteca.emprestimos, ())

    def test_emprestimo_rejeita_prazo_invalido(self):
        for prazo in (dia(5), None, "2026-11-12"):
            with self.subTest(prazo=prazo), self.assertRaises(ValueError):
                self.biblioteca.registrar_emprestimo(self.livro, self.usuario, dia(10), prazo)
        self.assertEqual(self.biblioteca.emprestimos, ())

    def test_emprestimo_rejeita_sobreposicao_e_permite_retirada_no_dia_da_devolucao(self):
        primeiro = self.emprestar_livro()
        self.biblioteca.registrar_devolucao(primeiro, dia(9))

        with self.assertRaises(ValueError):
            self.biblioteca.registrar_emprestimo(self.livro, self.usuario, dia(5), dia(12))
        self.assertEqual(self.biblioteca.emprestimos, (primeiro,))

        segundo = self.biblioteca.registrar_emprestimo(self.livro, self.usuario, dia(9), dia(12))
        self.assertFalse(primeiro.ativo)
        self.assertTrue(segundo.ativo)

    def test_devolucao_rejeita_data_invalida_e_emprestimo_de_outra_biblioteca(self):
        emprestimo = self.biblioteca.registrar_emprestimo(self.livro, self.usuario, dia(3), dia(8))
        for data_invalida in (dia(2), None):
            with self.subTest(data=data_invalida), self.assertRaises(ValueError):
                self.biblioteca.registrar_devolucao(emprestimo, data_invalida)
        with self.assertRaises(ValueError):
            Biblioteca().registrar_devolucao(emprestimo, dia(8))
        self.assertTrue(emprestimo.ativo)

    def test_segunda_devolucao_preserva_o_historico_e_nao_reabre_emprestimo(self):
        primeiro = self.emprestar_livro()
        self.biblioteca.registrar_devolucao(primeiro, dia(9))
        segundo = self.biblioteca.registrar_emprestimo(self.livro, self.usuario, dia(10), dia(18))

        for data_repetida in (dia(12), None):
            with self.subTest(data=data_repetida), self.assertRaises(ValueError):
                self.biblioteca.registrar_devolucao(primeiro, data_repetida)
        self.assertEqual(primeiro.data_devolucao, dia(9))
        self.assertFalse(primeiro.ativo)
        self.assertTrue(segundo.ativo)

    def test_contagem_separa_homonimos_e_inclui_emprestimos_devolvidos(self):
        homonima = Usuario(2, "Ana", "2023002")
        self.biblioteca.cadastrar_usuario(homonima)
        primeiro = self.emprestar_livro()
        self.biblioteca.registrar_devolucao(primeiro, dia(8))
        self.biblioteca.registrar_emprestimo(self.livro, homonima, dia(9), dia(16))

        self.assertEqual(contar_emprestimos_por_usuario(self.biblioteca.emprestimos), {1: 1, 2: 1})

    def test_multa_no_vencimento_em_atraso_e_apos_a_devolucao(self):
        emprestimo = self.emprestar_livro()
        referencia = dia(11)
        self.assertEqual(gerar_relatorio_de_multas(self.biblioteca.emprestimos, dia(8))["total"], 0)
        self.assertEqual(gerar_relatorio_de_multas(self.biblioteca.emprestimos, referencia)["total"], 6)
        self.assertEqual(calcular_total_de_multas_imperativo(self.biblioteca.emprestimos, referencia), 6)
        self.assertEqual(calcular_total_de_multas_funcional(self.biblioteca.emprestimos, referencia), 6)

        self.biblioteca.registrar_devolucao(emprestimo, referencia)
        self.assertEqual(gerar_relatorio_de_multas(self.biblioteca.emprestimos, referencia)["total"], 0)


class TestDemonstracao(unittest.TestCase):
    def test_importar_main_nao_executa_demonstracao(self):
        resultado = subprocess.run(
            [sys.executable, "-B", "-c", "import main"],
            cwd=Path(__file__).resolve().parent,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(resultado.stdout, "")


if __name__ == "__main__":
    unittest.main()
