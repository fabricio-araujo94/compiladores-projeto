import unittest
from src.tokenizer import Token
from src.parser import Parser
from src.ast_nodes import *

class TestParser(unittest.TestCase):

    def test_programa_vazio(self):
        tokens = [
            Token('INICIO', 'inicio', 1),
            Token('FIM', 'fim', 1),
            Token('EOF', '', 1)
        ]
        parser = Parser(tokens)
        arvore_gerada = parser.parse()
        arvore_esperada = Programa(
            bloco=Bloco(declaracoes=[], comandos=[])
        )
        self.assertEqual(arvore_gerada, arvore_esperada)

    def test_declaracao_variavel(self):
        tokens = [
            Token('INICIO', 'inicio', 1),
            Token('VAR', 'var', 2),
            Token('INTEIRO', 'inteiro', 2),
            Token('DOIS_PONTOS', ':', 2),
            Token('ID', 'a', 2),
            Token('VIRGULA', ',', 2),
            Token('ID', 'b', 2),
            Token('PONTO_VIRGULA', ';', 2),
            Token('FIM', 'fim', 3),
            Token('EOF', '', 3)
        ]
        parser = Parser(tokens)
        arvore_gerada = parser.parse()

        arvore_esperada = Programa(
            bloco=Bloco(
                declaracoes=[
                    VarDecl(
                        tipo_no=Tipo(Token('INTEIRO', 'inteiro', 2)),
                        var_nos=[
                            Variavel(Token('ID', 'a', 2)),
                            Variavel(Token('ID', 'b', 2))
                        ]
                    )
                ],
                comandos=[]
            )
        )
        self.assertEqual(arvore_gerada, arvore_esperada)

    def test_atribuicao_simples(self):
        tokens = [
            Token('INICIO', 'inicio', 1),
            Token('ID', 'x', 2),
            Token('ATRIBUICAO', '=', 2),
            Token('NUMERO_INTEIRO', '10', 2),
            Token('PONTO_VIRGULA', ';', 2),
            Token('FIM', 'fim', 3),
            Token('EOF', '', 3)
        ]
        parser = Parser(tokens)
        arvore_gerada = parser.parse()

        arvore_esperada = Programa(
            bloco=Bloco(
                declaracoes=[],
                comandos=[
                    Atribuicao(
                        var_no=Variavel(Token('ID', 'x', 2)),
                        expressao=Literal(Token('NUMERO_INTEIRO', '10', 2))
                    )
                ]
            )
        )
        self.assertEqual(arvore_gerada, arvore_esperada)

    def test_expressao_aritmetica(self):
        tokens = [
            Token('INICIO', 'inicio', 1),
            Token('ID', 'x', 2),
            Token('ATRIBUICAO', '=', 2),
            Token('NUMERO_INTEIRO', '5', 2),
            Token('OP_ARITMETICO', '+', 2),
            Token('NUMERO_INTEIRO', '3', 2),
            Token('PONTO_VIRGULA', ';', 2),
            Token('FIM', 'fim', 3),
            Token('EOF', '', 3)
        ]
        parser = Parser(tokens)
        arvore_gerada = parser.parse()

        arvore_esperada = Programa(
            bloco=Bloco(
                declaracoes=[],
                comandos=[
                    Atribuicao(
                        var_no=Variavel(Token('ID', 'x', 2)),
                        expressao=BinOp(
                            esq=Literal(Token('NUMERO_INTEIRO', '5', 2)),
                            op=Token('OP_ARITMETICO', '+', 2),
                            dir=Literal(Token('NUMERO_INTEIRO', '3', 2))
                        )
                    )
                ]
            )
        )
        self.assertEqual(arvore_gerada, arvore_esperada)


    def test_estrutura_repita(self):
        tokens = [
            Token('INICIO', 'inicio', 1),
            Token('REPITA', 'repita', 2),
            Token('NUMERO_INTEIRO', '10', 2),
            Token('VEZES', 'vezes', 2),
            Token('LEVANTAR_CANETA', 'levantar_caneta', 3),
            Token('PONTO_VIRGULA', ';', 3),
            Token('FIM_REPITA', 'fim_repita', 4),
            Token('PONTO_VIRGULA', ';', 4),
            Token('FIM', 'fim', 5),
            Token('EOF', '', 5)
        ]
        parser = Parser(tokens)
        arvore_gerada = parser.parse()

        arvore_esperada = Programa(
            bloco=Bloco(
                declaracoes=[],
                comandos=[
                    Repita(
                        vezes=Literal(Token('NUMERO_INTEIRO', '10', 2)),
                        bloco=Bloco(
                            declaracoes=[],
                            comandos=[
                                ComandoSimples(Token('LEVANTAR_CANETA', 'levantar_caneta', 3))
                            ]
                        )
                    )
                ]
            )
        )
        self.assertEqual(arvore_gerada, arvore_esperada)

    def test_erro_sintaxe_token_inesperado(self):
        tokens = [
            Token('INICIO', 'inicio', 1),
            Token('REPITA', 'repita', 2),
            Token('NUMERO_INTEIRO', '10', 2),
            # Token 'VEZES' faltando aqui
            Token('FIM_REPITA', 'fim_repita', 3),
            Token('FIM', 'fim', 4),
            Token('EOF', '', 4)
        ]
        parser = Parser(tokens)
        with self.assertRaisesRegex(SyntaxError, "Esperado 'VEZES', mas encontrou 'FIM_REPITA'"):
            parser.parse()
            
    def test_erro_codigo_apos_fim(self):
        tokens = [
            Token('INICIO', 'inicio', 1),
            Token('FIM', 'fim', 2),
            Token('ID', 'codigo_extra', 3),
            Token('PONTO_VIRGULA', ';', 3),
            Token('EOF', '', 3)
        ]
        parser = Parser(tokens)
        with self.assertRaisesRegex(SyntaxError, "Código encontrado após o 'fim' do programa"):
            parser.parse()

if __name__ == '__main__':
    unittest.main(verbosity=2)