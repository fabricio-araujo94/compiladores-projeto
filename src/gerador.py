import ast_nodes as ast

class Visitor:
    """ Classe base para o padrão Visitor. """
    def visit(self, node):
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise NotImplementedError(f"O método visit_{node.__class__.__name__} não foi implementado.")

class GeradorDeCodigo(Visitor):
    def __init__(self):
        self.codigo_python = []
        self.nivel_indentacao = 0

    def _indentar(self, codigo):
        """ Adiciona indentação ao código gerado. """
        return "    " * self.nivel_indentacao + codigo

    def gerar(self, node, nome_arquivo_base="Resultado"):
        """ Método principal que gera o script Python completo. """
        self.codigo_python.append("import turtle")
        self.codigo_python.append("import math # Pode ser útil para novas funcionalidades")
        self.codigo_python.append("")
        self.codigo_python.append("# --- Configuração da Tela e Tartaruga ---")
        self.codigo_python.append("screen = turtle.Screen()")
        self.codigo_python.append(f'screen.title("{nome_arquivo_base}")')
        self.codigo_python.append("t = turtle.Turtle()")
        self.codigo_python.append("t.speed(0) # Velocidade máxima")
        self.codigo_python.append("")

        self.codigo_python.append("# --- Código Gerado pelo Compilador ---")
        self.visit(node)

        self.codigo_python.append("")
        self.codigo_python.append("# --- Finalização ---")
        self.codigo_python.append("turtle.done()")

        return "\n".join(self.codigo_python)

    def visit_Programa(self, node: ast.Programa):
        self.visit(node.bloco)

    def visit_Bloco(self, node: ast.Bloco):
        # Gera código para as declarações primeiro (inicialização de variáveis)
        if self.nivel_indentacao == 0: # Apenas no escopo global
            self.codigo_python.append("# Inicialização de variáveis")
            for declaracao in node.declaracoes:
                self.visit(declaracao)
            self.codigo_python.append("")

        # Gera código para os comandos
        for comando in node.comandos:
            linha_codigo = self.visit(comando)
            if linha_codigo is not None:
                self.codigo_python.append(self._indentar(linha_codigo))

    def visit_ComandoSimples(self, node: ast.ComandoSimples):
        comando = node.token.tipo
        mapa_comandos = {
            'AVANCAR': 'forward', 'RECUAR': 'backward', 'GIRAR_DIREITA': 'right',
            'GIRAR_ESQUERDA': 'left', 'LEVANTAR_CANETA': 'penup', 'ABAIXAR_CANETA': 'pendown',
            'LIMPAR_TELA': 'clear', 'DEFINIR_COR': 'pencolor', 'COR_DE_FUNDO': 'bgcolor',
            'DEFINIR_ESPESSURA': 'pensize',
        }
        comando_python = mapa_comandos.get(comando)

        if node.expressao:
            argumento = self.visit(node.expressao)
            if comando == 'COR_DE_FUNDO': # Comando de tela é chamado em 'screen'
                return f"screen.{comando_python}({argumento})"
            return f"t.{comando_python}({argumento})"
        else:
            return f"t.{comando_python}()"

    def visit_ComandoIrPara(self, node: ast.ComandoIrPara):
        x = self.visit(node.expr_x)
        y = self.visit(node.expr_y)
        return f"t.goto({x}, {y})"

    def visit_Literal(self, node: ast.Literal):
        valor = node.valor
        # Remove aspas de strings para que o Python as interprete corretamente
        if node.token.tipo == 'TEXTO':
            return f'"{valor.strip()}"'
        return valor

    def visit_Variavel(self, node: ast.Variavel):
        return node.nome

    def visit_VarDecl(self, node: ast.VarDecl):
        # Inicializa as variáveis com um valor padrão em Python
        valor_padrao = {'inteiro': 0, 'real': 0.0, 'texto': '""', 'logico': 'False'}.get(node.tipo_no.valor)
        for var in node.var_nos:
            self.codigo_python.append(f"{var.nome} = {valor_padrao}")

    def visit_Atribuicao(self, node: ast.Atribuicao):
        var_nome = self.visit(node.var_no)
        expressao = self.visit(node.expressao)
        return f"{var_nome} = {expressao}"

    def visit_BinOp(self, node: ast.BinOp):
        esq = self.visit(node.esq)
        op = node.op.valor
        dir = self.visit(node.dir)
        return f"({esq} {op} {dir})"

    def visit_Repita(self, node: ast.Repita):
        vezes = self.visit(node.vezes)
        self.codigo_python.append(self._indentar(f"for _ in range({vezes}):"))
        self.nivel_indentacao += 1
        self.visit(node.bloco)
        self.nivel_indentacao -= 1
        return None

    def visit_Se(self, node: ast.Se):
        condicao = self.visit(node.condicao)
        self.codigo_python.append(self._indentar(f"if {condicao}:"))
        self.nivel_indentacao += 1
        self.visit(node.bloco_se)
        self.nivel_indentacao -= 1

        if node.bloco_senao:
            self.codigo_python.append(self._indentar("else:"))
            self.nivel_indentacao += 1
            self.visit(node.bloco_senao)
            self.nivel_indentacao -= 1
        return None

    def visit_Enquanto(self, node: ast.Enquanto):
        condicao = self.visit(node.condicao)
        self.codigo_python.append(self._indentar(f"while {condicao}:"))
        self.nivel_indentacao += 1
        self.visit(node.bloco)
        self.nivel_indentacao -= 1
        return None
