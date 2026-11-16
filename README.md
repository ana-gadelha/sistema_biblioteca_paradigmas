# Sistema de Gerenciamento de Biblioteca

Atividade prática da disciplina Paradigmas de Linguagens de Programação (UNIPÊ).
O sistema gerencia livros, usuários e empréstimos de uma biblioteca universitária,
integrando Programação Orientada a Objetos e Programação Funcional.

## Linguagem

Python 3 (somente biblioteca padrão, sem dependências externas).

## Como executar

1. Tenha o Python 3 instalado.
2. Abra um terminal na pasta do projeto.
3. Execute:

    python main.py

O programa cadastra dados de exemplo em memória e exibe a demonstração de todas as funcionalidades.

## Funcionalidades

- Cadastro e consulta de livros e usuários
- Registro de empréstimos e devoluções
- Bloqueio de empréstimo de livro já emprestado
- Identificação de empréstimos ativos em atraso a partir de uma data de referência
- Cálculo de multa de R$ 2,00 por dia de atraso
- Relatório de multas com filter, map e reduce
- Estatísticas: livros por categoria, empréstimos por usuário, empréstimos ativos,
  empréstimos ativos em atraso e valor total das multas
- Comparação entre uma implementação imperativa e uma funcional do total de multas

## Estrutura do projeto

| Arquivo | Conteúdo |
| --- | --- |
| livro.py | Classe Livro |
| usuario.py | Classe Usuario |
| emprestimo.py | Classe Emprestimo |
| biblioteca.py | Classe Biblioteca, com as operações que alteram o estado |
| funcoes_puras.py | Funções puras de filtragem, cálculo, relatório e estatísticas |
| comparacao.py | Total de multas nas versões imperativa e funcional |
| main.py | Demonstração do sistema |

## Decisões de projeto

- A data de referência é sempre recebida por parâmetro, nunca lida do sistema.
- As funções puras não alteram as coleções recebidas e devolvem novas estruturas.
- A estatística de empréstimos por usuário considera todos os empréstimos, ativos ou devolvidos.
- Empréstimos já devolvidos não geram multa.

## Integrantes

- Ana Maria Lucio de Sousa Dantas
- Joao Victor Barbosa Perazzo
- Mirela Ferraz de A. G. de Souza
- Ramon Fhelipe Vieira Marques