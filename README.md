# Compilador TurtleScript

Este é o repositório para o projeto final da disciplina de Compiladores (2025.1) do Instituto Federal do Ceará (IFCE) - Campus Maracanaú. O objetivo é desenvolver um compilador completo para a linguagem didática TurtleScript.

O compilador será responsável por realizar as análises léxica, sintática e semântica de um código-fonte em TurtleScript e traduzi-lo para um código Python funcional que utiliza a biblioteca Turtle Graphics para gerar desenhos vetoriais. 

## To-Do
### Analisador Léxico (tokenizer.py):
- [ ] Implementar o tokenizador manual para reconhecer todos os elementos da linguagem TurtleScript.

### Analisador Sintático (parser.py): 
- [ ] Verificar se a gramática da linguagem é LL(1) e fazer as modificações necessárias.
- [ ] Implementar o parser recursivo descendente LL(1). 
- [ ] Construir a Árvore Sintática Abstrata (AST) durante a análise. 

### Analisador Semântico (semantico.py): 
- [ ] Implementar a Tabela de Símbolos para armazenar variáveis e seus tipos.
- [ ] Implementar a verificação de declaração de variáveis (evitar uso antes da declaração e redeclarações).
- [ ] Implementar a verificação de tipos estática para atribuições e argumentos de comandos.

### Gerador de Código (gerador.py): 
- [ ] Implementar o percurso na AST para gerar código Python.
- [ ] Garantir que o código gerado utilize a biblioteca Turtle Graphics corretamente.
- [ ] Salvar o código gerado em arquivos .py executáveis.

### Funcionalidades Adicionais:
- [ ] Criar e implementar pelo menos dois novos comandos para a linguagem.
- [ ] Informar erros léxicos, sintáticos ou semânticos de forma clara.

### Testes e Automação: 
- [ ] Criar no mínimo 3 arquivos de teste.
- [ ] Criar um script de automação para compilar os arquivos de teste.

##  Equipe
  * Felipe Amorim Barbosa
  * Renan Carneiro Batista
  * Fabricio Araújo Dias
