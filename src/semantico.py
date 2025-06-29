# Aqui é a parte da analisador semântico.

# A AST criada pelo parser será verificada para saber se é coerente
# e o qual é o seu significado.

# Uma tabela de símbolos será usada para saber se as variáveis foram
# declaradas antes do uso, se não houve redeclaração de variáveis e
# validar se as atribuições são condicentes com os tipos e comandos.