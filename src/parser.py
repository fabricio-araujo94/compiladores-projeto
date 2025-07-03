from src.tokenizer import Token
from src.ast_nodes import *

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
        self.token_atual = self.tokens[self.pos]

    def _avancar(self):
        self.pos += 1
        self.token_atual = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _consumir(self, tipo_esperado: str):
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
        return self.programa()

    def programa(self) -> Programa:
        self._consumir('INICIO')
        bloco_node = self.bloco()
        self._consumir('FIM')
        if self.token_atual and self.token_atual.tipo != 'EOF':
             raise SyntaxError(f"Código encontrado após o 'fim' do programa na linha {self.token_atual.linha}")
        return Programa(bloco=bloco_node)

    def bloco(self) -> Bloco:
        declaracoes = []
        comandos = []
        tokens_de_parada = {'FIM', 'FIM_REPITA', 'FIM_SE', 'FIM_ENQUANTO', 'SENAO', 'EOF'}

        while self.token_atual and self.token_atual.tipo not in tokens_de_parada:
            if self.token_atual.tipo == 'VAR':
                nodes_gerados = self.declaracao_variaveis()
                for node in nodes_gerados:
                    if isinstance(node, VarDecl):
                        declaracoes.append(node)
                    else: 
                        comandos.append(node)
            else:
                comandos.append(self.comando())

        return Bloco(declaracoes, comandos)

    def declaracao_variaveis(self) -> list[ASTNode]:
        nodes_gerados = []
        self._consumir('VAR')
        tipo_node = self.tipo()
        self._consumir('DOIS_PONTOS')
        
        variaveis_declaradas = []
        
        while True:
            var_token = self._consumir('ID')
            variaveis_declaradas.append(Variavel(var_token))
            
            if self.token_atual and self.token_atual.tipo == 'ATRIBUICAO':
                self._consumir('ATRIBUICAO')
                expressao_node = self.expressao()
                atribuicao_node = Atribuicao(var_no=Variavel(var_token), expressao=expressao_node)
                nodes_gerados.append(atribuicao_node)
            
            if self.token_atual.tipo != 'VIRGULA':
                break
            self._consumir('VIRGULA')
        self._consumir('PONTO_VIRGULA')

        declaracao_node = VarDecl(tipo_node, variaveis_declaradas)
        nodes_gerados.insert(0, declaracao_node)

        return nodes_gerados

    def tipo(self) -> Tipo:
        token = self.token_atual
        if token.tipo in ('INTEIRO', 'REAL', 'TEXTO', 'LOGICO'):
            self._avancar()
            return Tipo(token)
        raise SyntaxError(f"Tipo de variável inválido '{token.valor}' na linha {token.linha}")

    def comando(self) -> ASTNode:
        token = self.token_atual
        comandos_com_expressao = {
            'AVANCAR', 'RECUAR', 'GIRAR_DIREITA', 'GIRAR_ESQUERDA',
            'DEFINIR_COR', 'DEFINIR_ESPESSURA', 'COR_DE_FUNDO', 'CIRCULO'
        }
        comandos_sem_expressao = {
            'LEVANTAR_CANETA', 'ABAIXAR_CANETA', 'LIMPAR_TELA',
            'EMPURRAR_POSICAO', 'RESTAURAR_POSICAO'
        }

        if token.tipo == 'ID': return self.atribuicao()
        if token.tipo in comandos_com_expressao:
            cmd_token = self._consumir(token.tipo)
            expr = self.expressao()
            self._consumir('PONTO_VIRGULA')
            return ComandoSimples(cmd_token, expressao=expr)
        if token.tipo in comandos_sem_expressao:
            cmd_token = self._consumir(token.tipo)
            self._consumir('PONTO_VIRGULA')
            return ComandoSimples(cmd_token)
        if token.tipo == 'IR_PARA': return self.comando_ir_para()
        if token.tipo == 'REPITA': return self.estrutura_repita()
        if token.tipo == 'SE': return self.estrutura_se()
        if token.tipo == 'ENQUANTO': return self.estrutura_enquanto()

        raise SyntaxError(f"Comando inesperado '{token.valor}' na linha {token.linha}")

    def comando_ir_para(self) -> ComandoIrPara:
        token = self._consumir('IR_PARA')
        expr_x = self.expressao()
        expr_y = self.expressao()
        self._consumir('PONTO_VIRGULA')
        return ComandoIrPara(token, expr_x, expr_y)

    def atribuicao(self) -> Atribuicao:
        var_no = Variavel(self._consumir('ID'))
        self._consumir('ATRIBUICAO')
        expr = self.expressao()
        self._consumir('PONTO_VIRGULA')
        return Atribuicao(var_no, expr)

    def estrutura_repita(self) -> Repita:
        self._consumir('REPITA')
        vezes_expr = self.expressao()
        self._consumir('VEZES')
        bloco_node = self.bloco()
        self._consumir('FIM_REPITA')
        self._consumir('PONTO_VIRGULA')
        return Repita(vezes_expr, bloco_node)

    def estrutura_se(self) -> Se:
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
        self._consumir('ENQUANTO')
        condicao = self.expressao()
        self._consumir('FACA')
        bloco = self.bloco()
        self._consumir('FIM_ENQUANTO')
        self._consumir('PONTO_VIRGULA')
        return Enquanto(condicao, bloco)

    def expressao(self) -> ASTNode:
        node = self.expressao_soma()
        if self.token_atual and self.token_atual.tipo == 'OP_RELACIONAL':
            op = self.token_atual
            self._avancar()
            dir = self.expressao_soma()
            node = BinOp(esq=node, op=op, dir=dir)
        return node

    def expressao_soma(self) -> ASTNode:
        node = self.termo()
        while self.token_atual and self.token_atual.tipo == 'OP_ARITMETICO':
            op = self.token_atual
            self._avancar()
            dir = self.termo()
            node = BinOp(esq=node, op=op, dir=dir)
        return node

    def termo(self) -> ASTNode:
        node = self.fator()
        while self.token_atual and self.token_atual.valor in ('*', '/'):
            op = self.token_atual
            self._avancar()
            dir = self.fator()
            node = BinOp(esq=node, op=op, dir=dir)
        return node

    def fator(self) -> ASTNode:
        token = self.token_atual
        if token.tipo == 'OP_ARITMETICO' and token.valor in ('+', '-'):
            op_token = self.token_atual
            self._avancar()
            node = self.fator()
            return UnaryOp(op=op_token, expr=node)

        if token.tipo in ('NUMERO_INTEIRO', 'NUMERO_REAL', 'TEXTO', 'VERDADEIRO', 'FALSO'):
            self._avancar()
            return Literal(token)
        elif token.tipo == 'ID':
            self._avancar()
            return Variavel(token)
        elif token.tipo == 'PARENTESES' and token.valor == '(':
            self._avancar()
            node = self.expressao()
            if self.token_atual and self.token_atual.tipo == 'PARENTESES' and self.token_atual.valor == ')':
                self._avancar() 
            else:
                valor_encontrado = self.token_atual.valor if self.token_atual else 'EOF'
                raise SyntaxError(f"Erro de Sintaxe na linha {self.token_atual.linha}: Esperado ')' mas encontrou '{valor_encontrado}'")
            return node
        else:
            raise SyntaxError(f"Fator inesperado na expressão: '{token.valor}' na linha {token.linha}")
