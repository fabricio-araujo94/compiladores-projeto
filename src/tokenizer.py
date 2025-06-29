import re
from typing import List, NamedTuple, Pattern

class Token(NamedTuple):
    """
    Representa um token, com um tipo, um valor (lexema) e a linha onde foi encontrado.
    """
    tipo: str
    valor: str
    linha: int

def tokenizar(codigo_fonte: str) -> List[Token]:
    """
    Função principal que transforma o código-fonte em uma lista de tokens.

    Args:
        codigo_fonte: O código em TurtleScript como uma string.

    Returns:
        Uma lista de Tokens.
    """

    # Especificação dos tokens com expressões regulares
    # A ordem é importante, pois algumas regras podem ter prefixos em comum.
    especificacao_tokens = [
        ('COMENTARIO',      r'//.*'),                  # Comentários
        ('NUMERO_REAL',     r'\d+\.\d+'),              # Números reais, ex: 10.5 [cite: 19, 32]
        ('NUMERO_INTEIRO',  r'\d+'),                   # Números inteiros, ex: 100 [cite: 16, 30]
        ('TEXTO',           r'"[^"]*"'),               # Strings de texto, ex: "blue" [cite: 18, 31]
        ('ID',              r'[a-zA-Z_]\w*'),           # Identificadores (variáveis e palavras-chave)
        ('ATRIBUICAO',      r'='),                     # Operador de atribuição
        ('OP_ARITMETICO',   r'[+\-*/%]'),              # Operadores aritméticos
        ('OP_RELACIONAL',   r'==|!=|<|>|<=|>='),       # Operadores relacionais
        ('PONTO_VIRGULA',   r';'),                     # Delimitador de comando [cite: 14]
        ('DOIS_PONTOS',     r':'),                     # Usado em declarações 'var tipo: id;'
        ('VIRGULA',         r','),                     # Separador de variáveis em declarações
        ('PARENTESES',      r'[()]'),                  # Parênteses para expressões
        ('NOVA_LINHA',      r'\n'),                    # Quebra de linha
        ('ESPACO',          r'[ \t\r]+'),              # Espaços em branco
        ('ERRO',            r'.'),                     # Qualquer outro caractere é um erro
    ]

    # Palavras-chave da linguagem TurtleScript
    palavras_chave = {
        'inicio', 'fim', 'var', 'inteiro', 'real', 'texto', 'logico', 'verdadeiro', 'falso',
        'repita', 'vezes', 'fim_repita', 'enquanto', 'faca', 'fim_enquanto', 'se', 'entao',
        'senao', 'fim_se', 'avancar', 'recuar', 'girar_direita', 'girar_esquerda',
        'ir_para', 'levantar_caneta', 'abaixar_caneta', 'definir_cor', 'definir_espessura',
        'cor_de_fundo', 'limpar_tela'
    }

    # Compila as expressões regulares em um único padrão
    regex_tokens = '|'.join(f'(?P<{par[0]}>{par[1]})' for par in especificacao_tokens)
    padrao: Pattern[str] = re.compile(regex_tokens)

    tokens: List[Token] = []
    numero_linha = 1

    # Itera sobre todas as correspondências encontradas no código
    for match in padrao.finditer(codigo_fonte):
        tipo_token = match.lastgroup
        valor = match.group()

        if tipo_token == 'ID' and valor in palavras_chave:
            # Se o ID for uma palavra-chave, mude seu tipo
            tipo_token = valor.upper() # Converte para MAIÚSCULAS para diferenciar (ex: INICIO)
        elif tipo_token in ['NOVA_LINHA', 'ESPACO', 'COMENTARIO']:
            # Ignora espaços, comentários e novas linhas (exceto para contar linhas)
            if tipo_token == 'NOVA_LINHA':
                numero_linha += 1
            continue
        elif tipo_token == 'ERRO':
            # Se um caractere inválido for encontrado, informa o erro
            print(f"Erro léxico na linha {numero_linha}: caractere inesperado '{valor}'")
            continue # Ou poderia levantar uma exceção

        tokens.append(Token(tipo_token, valor, numero_linha))

    tokens.append(Token('EOF', '', numero_linha)) # Adiciona o token de Fim de Arquivo
    return tokens

# Exemplo de como usar o tokenizador
if __name__ == '__main__':
    # Usando o Exemplo 3 do PDF
    codigo_exemplo_3 = """
inicio
    var inteiro: lado;
    var texto: cor;

    lado = 5;
    cor_de_fundo "black";
    definir_espessura 2;

    repita 50 vezes
        // Muda a cor da linha a cada iteracao
        definir_cor "cyan";

        // Desenha e aumenta o lado
        avancar lado;
        girar_direita 90;
        lado = lado + 5;
    fim_repita;
fim
"""
    tokens_gerados = tokenizar(codigo_exemplo_3)
    for token in tokens_gerados:
        print(token)
