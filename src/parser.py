from tokenizer import Token, tokenizar
from ast_nodes import *
import json

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
        self.token_atual = self.tokens[self.pos]

    def _avancar(self):
        """ Avança para o próximo token na lista. """
        self.pos += 1
        self.token_atual = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _consumir(self, tipo_esperado: str):
        """ Consome o token atual se for do tipo esperado, senão lança um erro. """
        if self.token_atual and self.token_atual.tipo == tipo_esperado:
            token = self.token_atual
            self._avancar()
            return token
        else:
            linha = self.token_atual.linha if self.token_atual else 'desconhecida'
            tipo_encontrado = self.token_atual.tipo if self.token_atual else 'EOF'
            raise SyntaxError(
                f"Erro de Sintaxe na linha {linha}: Esperado '{tipo_esperado}', mas encontrou '{tipo_encontrado}'"
            )

    def parse(self) -> ASTNode:
        """ Inicia a análise sintática. """
        return self.programa()

    def programa(self) -> Programa:
        """ programa ::= INICIO bloco FIM """
        self._consumir('INICIO')
        bloco_node = self.bloco()
        self._consumir('FIM')
        if self.token_atual and self.token_atual.tipo != 'EOF':
             raise SyntaxError(f"Código encontrado após o 'fim' do programa na linha {self.token_atual.linha}")
        return Programa(bloco=bloco_node)

    def bloco(self) -> Bloco:
        """ bloco ::= { declaracao_variaveis } { comando } """
        declaracoes = []
        comandos = []

        # Tipos de token que não finalizam um bloco
        tokens_de_parada = {'FIM', 'FIM_REPITA', 'FIM_SE', 'FIM_ENQUANTO', 'SENAO', 'EOF'}

        while self.token_atual and self.token_atual.tipo == 'VAR':
            declaracoes.append(self.declaracao_variaveis())

        while self.token_atual and self.token_atual.tipo not in tokens_de_parada:
            comandos.append(self.comando())

        return Bloco(declaracoes, comandos)

    def declaracao_variaveis(self) -> VarDecl:
        """ declaracao_variaveis ::= VAR tipo DOIS_PONTOS lista_ids PONTO_VIRGULA """
        self._consumir('VAR')
        tipo_node = self.tipo()
        self._consumir('DOIS_PONTOS')

        var_nodes = [Variavel(self._consumir('ID'))]
        while self.token_atual.tipo == 'VIRGULA':
            self._consumir('VIRGULA')
            var_nodes.append(Variavel(self._consumir('ID')))

        self._consumir('PONTO_VIRGULA')
        return VarDecl(tipo_node, var_nodes)

    def tipo(self) -> Tipo:
        """ tipo ::= INTEIRO | REAL | TEXTO | LOGICO """
        token = self.token_atual
        if token.tipo in ('INTEIRO', 'REAL', 'TEXTO', 'LOGICO'):
            self._avancar()
            return Tipo(token)
        raise SyntaxError(f"Tipo de variável inválido '{token.valor}' na linha {token.linha}")

    def comando(self) -> ASTNode:
        """ Distribui o parsing para o tipo de comando correto. """
        token = self.token_atual

        comandos_com_expressao = {'AVANCAR', 'RECUAR', 'GIRAR_DIREITA', 'GIRAR_ESQUERDA', 'DEFINIR_COR', 'DEFINIR_ESPESSURA', 'COR_DE_FUNDO'}
        comandos_sem_expressao = {'LEVANTAR_CANETA', 'ABAIXAR_CANETA', 'LIMPAR_TELA'}

        if token.tipo == 'ID': return self.atribuicao()
        if token.tipo in comandos_com_expressao:
            self._avancar()
            expr = self.expressao()
            self._consumir('PONTO_VIRGULA')
            return ComandoSimples(token, expressao=expr)
        if token.tipo in comandos_sem_expressao:
            self._avancar()
            self._consumir('PONTO_VIRGULA')
            return ComandoSimples(token)
        if token.tipo == 'IR_PARA': return self.comando_ir_para()
        if token.tipo == 'REPITA': return self.estrutura_repita()
        if token.tipo == 'SE': return self.estrutura_se()
        if token.tipo == 'ENQUANTO': return self.estrutura_enquanto()

        raise SyntaxError(f"Comando inesperado '{token.valor}' na linha {token.linha}")

    def comando_ir_para(self) -> ComandoIrPara:
        """ comando_movimento ::= IR_PARA expressao expressao PONTO_VIRGULA """
        token = self._consumir('IR_PARA')
        expr_x = self.expressao()
        expr_y = self.expressao()
        self._consumir('PONTO_VIRGULA')
        return ComandoIrPara(token, expr_x, expr_y)

    def atribuicao(self) -> Atribuicao:
        """ atribuicao ::= ID ATRIBUICAO expressao PONTO_VIRGULA """
        var_no = Variavel(self._consumir('ID'))
        self._consumir('ATRIBUICAO')
        expr = self.expressao()
        self._consumir('PONTO_VIRGULA')
        return Atribuicao(var_no, expr)

    def estrutura_repita(self) -> Repita:
        """ estrutura_repita ::= REPITA expressao VEZES bloco FIM_REPITA PONTO_VIRGULA """
        self._consumir('REPITA')
        vezes_expr = self.expressao()
        self._consumir('VEZES')
        bloco_node = self.bloco()
        self._consumir('FIM_REPITA')
        self._consumir('PONTO_VIRGULA')
        return Repita(vezes_expr, bloco_node)

    def estrutura_se(self) -> Se:
        """ estrutura_se ::= SE expressao ENTAO bloco [ SENAO bloco ] FIM_SE PONTO_VIRGULA """
        self._consumir('SE')
        condicao = self.expressao()
        self._consumir('ENTAO')
        bloco_se = self.bloco()
        bloco_senao = None
        if self.token_atual.tipo == 'SENAO':
            self._consumir('SENAO')
            bloco_senao = self.bloco()
        self._consumir('FIM_SE')
        self._consumir('PONTO_VIRGULA')
        return Se(condicao, bloco_se, bloco_senao)

    def estrutura_enquanto(self) -> Enquanto:
        """ estrutura_enquanto ::= ENQUANTO expressao FACA bloco FIM_ENQUANTO PONTO_VIRGULA """
        self._consumir('ENQUANTO')
        condicao = self.expressao()
        self._consumir('FACA')
        bloco = self.bloco()
        self._consumir('FIM_ENQUANTO')
        self._consumir('PONTO_VIRGULA')
        return Enquanto(condicao, bloco)

    def expressao(self) -> ASTNode:
        """ expressao ::= termo { (OP_ARITMETICO | OP_RELACIONAL) termo } """
        node = self.termo()
        while self.token_atual and self.token_atual.tipo in ('OP_ARITMETICO', 'OP_RELACIONAL'):
            op = self.token_atual
            self._avancar()
            dir = self.termo()
            node = BinOp(esq=node, op=op, dir=dir)
        return node

    def termo(self) -> ASTNode:
        """ termo ::= fator { (OP_ARITMETICO_MUL) fator } """
        # Nota: Esta implementação ainda é simplificada e não trata a precedência completa (ex: * vs +)
        # Para isso, seria necessário um método para cada nível de precedência.
        node = self.fator()
        while self.token_atual and self.token_atual.valor in ('*', '/'):
            op = self.token_atual
            self._avancar()
            dir = self.fator()
            node = BinOp(esq=node, op=op, dir=dir)
        return node

    def fator(self) -> ASTNode:
        """ fator ::= NUMERO_INTEIRO | NUMERO_REAL | TEXTO | ID | ( expressao ) """
        token = self.token_atual
        if token.tipo in ('NUMERO_INTEIRO', 'NUMERO_REAL', 'TEXTO', 'VERDADEIRO', 'FALSO'):
            self._avancar()
            return Literal(token)
        elif token.tipo == 'ID':
            self._avancar()
            return Variavel(token)
        elif token.tipo == 'PARENTESES' and token.valor == '(':
            self._avancar()
            node = self.expressao()
            if self.token_atual.valor == ')':
                self._avancar()
                return node
            else:
                raise SyntaxError(f"Erro de Sintaxe: Esperado ')' mas encontrou '{self.token_atual.valor}'")
        else:
            raise SyntaxError(f"Fator inesperado na expressão: '{token.valor}' na linha {token.linha}")


# --- Função auxiliar para imprimir a AST de forma legível ---
def ast_para_dict(node):
    if not isinstance(node, ASTNode):
        return node
    result = {'node_type': node.__class__.__name__}
    for key, value in node.__dict__.items():
        if isinstance(value, list):
            result[key] = [ast_para_dict(v) for v in value]
        elif key == 'token':
             result[key] = {'tipo': value.tipo, 'valor': value.valor, 'linha': value.linha}
        else:
            result[key] = ast_para_dict(value)
    return result

# --- Exemplo de uso ---
if __name__ == '__main__':
    # Testando com o Exemplo 3 do PDF, que é mais completo
    codigo_exemplo_3 = """
inicio
    var inteiro: lado;
    var texto: cor;

    lado = 5;
    cor_de_fundo "black";
    definir_espessura 2;

    repita 50 vezes
        definir_cor "cyan";
        avancar lado;
        girar_direita 90;
        lado = lado + 5;
    fim_repita;
fim
"""
    try:
        tokens = tokenizar(codigo_exemplo_3)
        parser = Parser(tokens)
        arvore_sintatica = parser.parse()
        print("Análise Sintática concluída com sucesso!")

        # Imprimir a AST em formato JSON para visualização
        print(json.dumps(ast_para_dict(arvore_sintatica), indent=2))

    except SyntaxError as e:
        print(e)
