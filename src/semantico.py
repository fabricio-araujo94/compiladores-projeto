import src.ast_nodes as ast

class TabelaSimbolos:
    """ Armazena informações sobre as variáveis (símbolos), como seu tipo. """
    def __init__(self):
        self._simbolos = {}

    def declarar(self, nome_var, tipo_var, linha):
        if nome_var in self._simbolos:
            raise NameError(f"Erro Semântico na linha {linha}: Variável '{nome_var}' já declarada.")
        self._simbolos[nome_var] = tipo_var

    def buscar(self, nome_var, linha):
        if nome_var not in self._simbolos:
            raise NameError(f"Erro Semântico na linha {linha}: Variável '{nome_var}' não foi declarada.")
        return self._simbolos[nome_var]

class Visitor:
    """ Classe base para o padrão Visitor. """
    def visit(self, node):
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise NotImplementedError(f"O método visit_{node.__class__.__name__} não foi implementado.")

class AnalisadorSemantico(Visitor):
    def __init__(self):
        self.tabela_simbolos = TabelaSimbolos()
        # --- ATUALIZE ESTE DICIONÁRIO ---
        self.regras_comandos = {
            'AVANCAR': ['inteiro', 'real'],
            'RECUAR': ['inteiro', 'real'],
            'GIRAR_DIREITA': ['inteiro', 'real'],
            'GIRAR_ESQUERDA': ['inteiro', 'real'],
            'DEFINIR_ESPESSURA': ['inteiro', 'real'],
            'DEFINIR_COR': ['texto'],
            'COR_DE_FUNDO': ['texto'],
            'CIRCULO': ['inteiro', 'real'] # Adicionado
        }

    def visit_Programa(self, node: ast.Programa):
        self.visit(node.bloco)

    def visit_Bloco(self, node: ast.Bloco):
        for declaracao in node.declaracoes:
            self.visit(declaracao)
        for comando in node.comandos:
            self.visit(comando)

    def visit_VarDecl(self, node: ast.VarDecl):
        tipo_var = node.tipo_no.valor
        for var_node in node.var_nos:
            nome_var = var_node.nome
            self.tabela_simbolos.declarar(nome_var, tipo_var, var_node.token.linha)

    def visit_Atribuicao(self, node: ast.Atribuicao):
        nome_var = node.var_no.nome
        linha = node.var_no.token.linha
        tipo_declarado = self.tabela_simbolos.buscar(nome_var, linha)
        tipo_expressao = self.visit(node.expressao)

        # Regra especial: permite atribuir inteiro a real, mas não o contrário
        if tipo_declarado == 'real' and tipo_expressao == 'inteiro':
            pass # Isso é permitido (promoção de tipo)
        elif tipo_declarado != tipo_expressao:
            raise TypeError(
                f"Erro Semântico na linha {linha}: Tipos incompatíveis. Não é possível atribuir '{tipo_expressao}' a uma variável do tipo '{tipo_declarado}' ('{nome_var}')."
            )

    def visit_Variavel(self, node: ast.Variavel):
        nome_var = node.nome
        linha = node.token.linha
        return self.tabela_simbolos.buscar(nome_var, linha)

    def visit_Literal(self, node: ast.Literal):
        if node.token.tipo == 'NUMERO_INTEIRO': return 'inteiro'
        if node.token.tipo == 'NUMERO_REAL': return 'real'
        if node.token.tipo == 'TEXTO': return 'texto'
        if node.token.tipo in ('VERDADEIRO', 'FALSO'): return 'logico'
        return 'desconhecido'

    def visit_BinOp(self, node: ast.BinOp):
        linha = node.op.linha
        tipo_esq = self.visit(node.esq)
        tipo_dir = self.visit(node.dir)

        op_logicos = ['==', '!=', '<', '>', '<=', '>=']
        if node.op.valor in op_logicos:
            if tipo_esq != tipo_dir:
                 raise TypeError(f"Erro Semântico na linha {linha}: Comparação entre tipos incompatíveis ('{tipo_esq}' e '{tipo_dir}').")
            return 'logico'

        if tipo_esq != tipo_dir:
            # Permitir operações entre inteiro e real, resultando em real
            if {tipo_esq, tipo_dir} == {'inteiro', 'real'}:
                return 'real'
            raise TypeError(f"Erro Semântico na linha {linha}: Operação com tipos incompatíveis ('{tipo_esq}' e '{tipo_dir}').")
        return tipo_esq

    def visit_Repita(self, node: ast.Repita):
        linha = node.vezes.token.linha if hasattr(node.vezes, 'token') else 'desconhecida'
        if not isinstance(node.vezes, ast.Literal) or node.vezes.token.tipo != 'NUMERO_INTEIRO':
            raise TypeError(f"Erro Semântico na linha {linha}: O comando 'repita' espera um número inteiro literal como argumento.")
        self.visit(node.bloco)

    def visit_ComandoSimples(self, node: ast.ComandoSimples):
        linha = node.token.linha
        comando = node.token.tipo

        # Comandos que não têm argumento
        if not node.expressao:
            return

        # Comandos que têm argumento
        tipo_argumento = self.visit(node.expressao)
        tipos_esperados = self.regras_comandos.get(comando)

        if tipos_esperados and tipo_argumento not in tipos_esperados:
            raise TypeError(f"Erro Semântico na linha {linha}: O comando '{node.token.valor}' esperava um argumento do tipo '{' ou '.join(tipos_esperados)}', mas recebeu '{tipo_argumento}'.")

    def visit_ComandoIrPara(self, node: ast.ComandoIrPara):
        linha = node.token.linha
        tipo_x = self.visit(node.expr_x)
        tipo_y = self.visit(node.expr_y)
        tipos_validos = ['inteiro', 'real']
        if tipo_x not in tipos_validos or tipo_y not in tipos_validos:
            raise TypeError(f"Erro Semântico na linha {linha}: O comando 'ir_para' espera dois argumentos numéricos (inteiro/real).")

    def visit_Se(self, node: ast.Se):
        tipo_condicao = self.visit(node.condicao)
        if tipo_condicao != 'logico':
            raise TypeError(f"Erro Semântico: A condição da estrutura 'se' deve ser do tipo 'logico', mas é '{tipo_condicao}'.")
        self.visit(node.bloco_se)
        if node.bloco_senao:
            self.visit(node.bloco_senao)

    def visit_Enquanto(self, node: ast.Enquanto):
        tipo_condicao = self.visit(node.condicao)
        if tipo_condicao != 'logico':
            raise TypeError(f"Erro Semântico: A condição da estrutura 'enquanto' deve ser do tipo 'logico', mas é '{tipo_condicao}'.")
        self.visit(node.bloco)
