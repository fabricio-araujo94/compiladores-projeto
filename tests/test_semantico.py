import unittest
from src.semantico import AnalisadorSemantico
from src.ast_nodes import *
from src.tokenizer import Token

class TestAnalisadorSemantico(unittest.TestCase):

    def setUp(self):
        """
        Este método é executado antes de cada teste, garantindo que cada um
        comece com uma instância limpa do analisador e da tabela de símbolos.
        """
        self.analisador = AnalisadorSemantico()

    def _criar_token_dummy(self, tipo, valor, linha=1):
        """
        Função auxiliar para criar tokens simples, já que os nós da AST
        precisam de um token, mas não precisamos de um tokenizador completo aqui.
        """
        return Token(tipo, valor, linha)

    def test_declaracao_e_uso_validos(self):
        # Código: inicio var inteiro: x; x = 5; fim
        no_decl = VarDecl(
            tipo_no=Tipo(self._criar_token_dummy('INTEIRO', 'inteiro')),
            var_nos=[Variavel(self._criar_token_dummy('ID', 'x'))]
        )
        no_atrib = Atribuicao(
            var_no=Variavel(self._criar_token_dummy('ID', 'x')),
            expressao=Literal(self._criar_token_dummy('NUMERO_INTEIRO', '5'))
        )
        arvore = Programa(bloco=Bloco(declaracoes=[no_decl], comandos=[no_atrib]))
        
        try:
            self.analisador.visit(arvore)
        except (NameError, TypeError) as e:
            self.fail(f"Análise semântica falhou inesperadamente: {e}")

    def test_erro_variavel_nao_declarada(self):
        # Código: inicio x = 5; fim
        no_atrib = Atribuicao(
            var_no=Variavel(self._criar_token_dummy('ID', 'x')),
            expressao=Literal(self._criar_token_dummy('NUMERO_INTEIRO', '5'))
        )
        arvore = Programa(bloco=Bloco(declaracoes=[], comandos=[no_atrib]))

        with self.assertRaisesRegex(NameError, "Variável 'x' não foi declarada"):
            self.analisador.visit(arvore)
            
    def test_erro_redeclaracao_variavel(self):
        # Código: inicio var inteiro: x; var real: x; fim
        decl1 = VarDecl(
            Tipo(self._criar_token_dummy('INTEIRO', 'inteiro')), 
            [Variavel(self._criar_token_dummy('ID', 'x', 2))]
        )
        decl2 = VarDecl(
            Tipo(self._criar_token_dummy('REAL', 'real')),
            [Variavel(self._criar_token_dummy('ID', 'x', 3))]
        )
        arvore = Programa(bloco=Bloco(declaracoes=[decl1, decl2], comandos=[]))

        with self.assertRaisesRegex(NameError, "Variável 'x' já declarada"):
            self.analisador.visit(arvore)

    def test_erro_atribuicao_tipo_incompativel(self):
        # Código: inicio var inteiro: x; x = "ola"; fim
        no_decl = VarDecl(
            Tipo(self._criar_token_dummy('INTEIRO', 'inteiro')), 
            [Variavel(self._criar_token_dummy('ID', 'x', 2))]
        )
        no_atrib = Atribuicao(
            Variavel(self._criar_token_dummy('ID', 'x', 3)),
            Literal(self._criar_token_dummy('TEXTO', '"ola"'))
        )
        arvore = Programa(bloco=Bloco(declaracoes=[no_decl], comandos=[no_atrib]))

        with self.assertRaisesRegex(TypeError, "Tipos incompatíveis. Não é possível " \
        "atribuir 'texto' a uma variável do tipo 'inteiro'"):
            self.analisador.visit(arvore)

    def test_atribuicao_inteiro_para_real_valida(self):
        # Código: inicio var real: r; r = 10; fim
        no_decl = VarDecl(
            Tipo(self._criar_token_dummy('REAL', 'real')), 
            [Variavel(self._criar_token_dummy('ID', 'r'))]
        )
        no_atrib = Atribuicao(
            Variavel(self._criar_token_dummy('ID', 'r')),
            Literal(self._criar_token_dummy('NUMERO_INTEIRO', '10'))
        )
        arvore = Programa(bloco=Bloco(declaracoes=[no_decl], comandos=[no_atrib]))
        
        try:
            self.analisador.visit(arvore)
        except (NameError, TypeError) as e:
            self.fail(f"A atribuição de inteiro para real falhou inesperadamente: {e}")

    def test_erro_operacao_tipos_incompativeis(self):
        # Código: inicio var inteiro: x; x = 5 + "oi"; fim
        decl = VarDecl(Tipo(self._criar_token_dummy('INTEIRO', 'inteiro')), 
                       [Variavel(self._criar_token_dummy('ID', 'x'))])
        expressao = BinOp(
            esq=Literal(self._criar_token_dummy('NUMERO_INTEIRO', '5')),
            op=self._criar_token_dummy('OP_ARITMETICO', '+', 2),
            dir=Literal(self._criar_token_dummy('TEXTO', '"oi"'))
        )
        atrib = Atribuicao(Variavel(self._criar_token_dummy('ID', 'x')), expressao)
        arvore = Programa(bloco=Bloco(declaracoes=[decl], comandos=[atrib]))

        with self.assertRaisesRegex(TypeError, "Operação com tipos incompatíveis"):
            self.analisador.visit(arvore)

    def test_erro_condicao_se_nao_logica(self):
        # Código: se 10 entao fim_se;
        no_se = Se(
            condicao=Literal(self._criar_token_dummy('NUMERO_INTEIRO', '10')),
            bloco_se=Bloco([], [])
        )
        arvore = Programa(bloco=Bloco(declaracoes=[], comandos=[no_se]))

        with self.assertRaisesRegex(TypeError, "A condição da estrutura 'se' deve ser do tipo 'logico'"):
            self.analisador.visit(arvore)

    def test_comando_com_argumento_invalido(self):
        # Código: avancar "muito";
        comando = ComandoSimples(
            token=self._criar_token_dummy('AVANCAR', 'avancar', 2),
            expressao=Literal(self._criar_token_dummy('TEXTO', '"muito"'))
        )
        arvore = Programa(bloco=Bloco(declaracoes=[], comandos=[comando]))

        with self.assertRaisesRegex(TypeError, "esperava um argumento do tipo 'inteiro ou real', " \
        "mas recebeu 'texto'"):
            self.analisador.visit(arvore)

if __name__ == '__main__':
    unittest.main(verbosity=2)