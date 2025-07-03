class ASTNode:
    """ Nó base para a AST. """
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"

class Programa(ASTNode):
    def __init__(self, bloco):
        self.bloco = bloco

class Bloco(ASTNode):
    def __init__(self, declaracoes, comandos):
        self.declaracoes = declaracoes
        self.comandos = comandos

class VarDecl(ASTNode):
    def __init__(self, tipo_no, var_nos):
        self.tipo_no = tipo_no
        self.var_nos = var_nos

class Tipo(ASTNode):
    def __init__(self, token):
        self.token = token
        self.valor = token.valor

class Variavel(ASTNode):
    def __init__(self, token):
        self.token = token
        self.nome = token.valor

class Atribuicao(ASTNode):
    def __init__(self, var_no, expressao):
        self.var_no = var_no
        self.expressao = expressao

class ComandoSimples(ASTNode):
    def __init__(self, token, expressao=None):
        self.token = token
        self.expressao = expressao

class ComandoIrPara(ASTNode):
    def __init__(self, token, expr_x, expr_y):
        self.token = token
        self.expr_x = expr_x
        self.expr_y = expr_y

class Repita(ASTNode):
    def __init__(self, vezes, bloco):
        self.vezes = vezes
        self.bloco = bloco

class Se(ASTNode):
    def __init__(self, condicao, bloco_se, bloco_senao=None):
        self.condicao = condicao
        self.bloco_se = bloco_se
        self.bloco_senao = bloco_senao

class Enquanto(ASTNode):
    def __init__(self, condicao, bloco):
        self.condicao = condicao
        self.bloco = bloco

class Literal(ASTNode):
    def __init__(self, token):
        self.token = token
        self.valor = token.valor

class UnaryOp(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.token = op
        self.expr = expr

class BinOp(ASTNode):
    def __init__(self, esq, op, dir):
        self.esq = esq
        self.op = op
        self.dir = dir
