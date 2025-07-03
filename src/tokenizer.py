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

    # A ordem é importante, pois algumas regras podem ter prefixos em comum.
    especificacao_tokens = [
        ('COMENTARIO',      r'//.*'),                  
        ('NUMERO_REAL',     r'[+-]?\d+\.\d+'),         
        ('NUMERO_INTEIRO',  r'[+-]?\d+'),         
        ('TEXTO',           r'"[^"]*"'),               
        ('ID',              r'[a-zA-Z_]\w*'),          
        ('OP_ARITMETICO',   r'[+\-*/%]'),              
        ('OP_RELACIONAL',   r'==|!=|<|>|<=|>='),       
        ('ATRIBUICAO',      r'='),                     
        ('PONTO_VIRGULA',   r';'),                     
        ('DOIS_PONTOS',     r':'),                     
        ('VIRGULA',         r','),                     
        ('PARENTESES',      r'[()]'),                  
        ('NOVA_LINHA',      r'\n'),                    
        ('ESPACO',          r'[ \t\r]+'),              
        ('ERRO',            r'.'),                 
    ]

    palavras_chave = {
        'inicio', 'fim', 'var', 'inteiro', 'real', 'texto', 'logico', 'verdadeiro', 'falso',
        'repita', 'vezes', 'fim_repita', 'enquanto', 'faca', 'fim_enquanto', 'se', 'entao',
        'senao', 'fim_se', 'avancar', 'recuar', 'girar_direita', 'girar_esquerda',
        'ir_para', 'levantar_caneta', 'abaixar_caneta', 'definir_cor', 'definir_espessura',
        'cor_de_fundo', 'limpar_tela', 'circulo', 'empurrar_posicao', 'restaurar_posicao'
    }

    # Compila as expressões regulares em um único padrão
    regex_tokens = '|'.join(f'(?P<{par[0]}>{par[1]})' for par in especificacao_tokens)
    padrao: Pattern[str] = re.compile(regex_tokens)

    tokens: List[Token] = []
    numero_linha = 1

    for match in padrao.finditer(codigo_fonte):
        tipo_token = match.lastgroup
        valor = match.group()

        if tipo_token == 'ID' and valor in palavras_chave:
            tipo_token = valor.upper() 
        elif tipo_token in ['NOVA_LINHA', 'ESPACO', 'COMENTARIO']:
            if tipo_token == 'NOVA_LINHA':
                numero_linha += 1
            continue
        elif tipo_token == 'ERRO':
            raise SyntaxError(f"Erro Léxico na linha {numero_linha}: Caractere inválido '{valor}' não reconhecido.")

        tokens.append(Token(tipo_token, valor, numero_linha))

    tokens.append(Token('EOF', '', numero_linha))
    return tokens