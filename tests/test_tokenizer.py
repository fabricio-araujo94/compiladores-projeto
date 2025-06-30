import unittest
from src.tokenizer import tokenizar, Token

class TestTokenizer(unittest.TestCase):

    def test_codigo_vazio(self):
        tokens = tokenizar("")
        esperado = [Token('EOF', '', 1)]
        self.assertEqual(tokens, esperado)

    def test_palavras_chave_basicas(self):
        codigo = "inicio fim"
        tokens = tokenizar(codigo)
        esperado = [
            Token('INICIO', 'inicio', 1),
            Token('FIM', 'fim', 1),
            Token('EOF', '', 1)
        ]
        self.assertEqual(tokens, esperado)

    def test_declaracao_variaveis(self):
        codigo = "var inteiro: contador;"
        tokens = tokenizar(codigo)
        esperado = [
            Token('VAR', 'var', 1),
            Token('INTEIRO', 'inteiro', 1),
            Token('DOIS_PONTOS', ':', 1),
            Token('ID', 'contador', 1),
            Token('PONTO_VIRGULA', ';', 1),
            Token('EOF', '', 1)
        ]
        self.assertEqual(tokens, esperado)

    def test_atribuicao_valores(self):
        codigo = """
        x = 100;
        y = 25.5;
        msg = "ola";
        """
        tokens = tokenizar(codigo)
        esperado = [
            Token('ID', 'x', 2),
            Token('ATRIBUICAO', '=', 2),
            Token('NUMERO_INTEIRO', '100', 2),
            Token('PONTO_VIRGULA', ';', 2),
            Token('ID', 'y', 3),
            Token('ATRIBUICAO', '=', 3),
            Token('NUMERO_REAL', '25.5', 3),
            Token('PONTO_VIRGULA', ';', 3),
            Token('ID', 'msg', 4),
            Token('ATRIBUICAO', '=', 4),
            Token('TEXTO', '"ola"', 4),
            Token('PONTO_VIRGULA', ';', 4),
            Token('EOF', '', 5)
        ]
        self.assertEqual(tokens, esperado)

    def test_comandos_turtle(self):
        codigo = 'avancar 100;\ngirar_direita 90;'
        tokens = tokenizar(codigo)
        esperado = [
            Token('AVANCAR', 'avancar', 1),
            Token('NUMERO_INTEIRO', '100', 1),
            Token('PONTO_VIRGULA', ';', 1),
            Token('GIRAR_DIREITA', 'girar_direita', 2),
            Token('NUMERO_INTEIRO', '90', 2),
            Token('PONTO_VIRGULA', ';', 2),
            Token('EOF', '', 2)
        ]
        self.assertEqual(tokens, esperado)

    def test_estrutura_repita(self):
        codigo = """
        repita 10 vezes
            avancar 50;
        fim_repita;
        """
        tokens = tokenizar(codigo)
        esperado = [
            Token('REPITA', 'repita', 2),
            Token('NUMERO_INTEIRO', '10', 2),
            Token('VEZES', 'vezes', 2),
            Token('AVANCAR', 'avancar', 3),
            Token('NUMERO_INTEIRO', '50', 3),
            Token('PONTO_VIRGULA', ';', 3),
            Token('FIM_REPITA', 'fim_repita', 4),
            Token('PONTO_VIRGULA', ';', 4),
            Token('EOF', '', 5)
        ]
        self.assertEqual(tokens, esperado)

    def test_expressao_aritmetica(self):
        codigo = "lado = lado + 5;"
        tokens = tokenizar(codigo)
        esperado = [
            Token('ID', 'lado', 1),
            Token('ATRIBUICAO', '=', 1),
            Token('ID', 'lado', 1),
            Token('OP_ARITMETICO', '+', 1),
            Token('NUMERO_INTEIRO', '5', 1),
            Token('PONTO_VIRGULA', ';', 1),
            Token('EOF', '', 1)
        ]
        self.assertEqual(tokens, esperado)

    def test_comentarios_espacos_linhas(self):
        codigo = """
        // Primeira linha de comentario
        inicio       // Comentario no fim da linha
            var texto: t; // Declaração
        fim
        // Fim do arquivo
        """
        tokens = tokenizar(codigo)
        esperado = [
            Token('INICIO', 'inicio', 3),
            Token('VAR', 'var', 4),
            Token('TEXTO', 'texto', 4),
            Token('DOIS_PONTOS', ':', 4),
            Token('ID', 't', 4),
            Token('PONTO_VIRGULA', ';', 4),
            Token('FIM', 'fim', 5),
            Token('EOF', '', 7)
        ]
        self.assertEqual(tokens, esperado)
        # Verifica se o numero da linha do EOF está correto
        self.assertEqual(tokens[-1].linha, 7)


    def test_erro_lexico(self):
        codigo = "var inteiro: @variavel_invalida;"
        with self.assertRaises(SyntaxError) as cm:
            tokenizar(codigo)
        self.assertEqual(
            str(cm.exception),
            "Erro Léxico na linha 1: Caractere inválido '@' não reconhecido."
        )

    def test_codigo_completo_exemplo(self):
        codigo_exemplo = """
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
        tokens = tokenizar(codigo_exemplo)
        esperado = [
            Token('INICIO', 'inicio', 2),
            Token('VAR', 'var', 3),
            Token('INTEIRO', 'inteiro', 3),
            Token('DOIS_PONTOS', ':', 3),
            Token('ID', 'lado', 3),
            Token('PONTO_VIRGULA', ';', 3),
            Token('VAR', 'var', 4),
            Token('TEXTO', 'texto', 4),
            Token('DOIS_PONTOS', ':', 4),
            Token('ID', 'cor', 4),
            Token('PONTO_VIRGULA', ';', 4),
            Token('ID', 'lado', 6),
            Token('ATRIBUICAO', '=', 6),
            Token('NUMERO_INTEIRO', '5', 6),
            Token('PONTO_VIRGULA', ';', 6),
            Token('COR_DE_FUNDO', 'cor_de_fundo', 7),
            Token('TEXTO', '"black"', 7),
            Token('PONTO_VIRGULA', ';', 7),
            Token('DEFINIR_ESPESSURA', 'definir_espessura', 8),
            Token('NUMERO_INTEIRO', '2', 8),
            Token('PONTO_VIRGULA', ';', 8),
            Token('REPITA', 'repita', 10),
            Token('NUMERO_INTEIRO', '50', 10),
            Token('VEZES', 'vezes', 10),
            Token('DEFINIR_COR', 'definir_cor', 12),
            Token('TEXTO', '"cyan"', 12),
            Token('PONTO_VIRGULA', ';', 12),
            Token('AVANCAR', 'avancar', 15),
            Token('ID', 'lado', 15),
            Token('PONTO_VIRGULA', ';', 15),
            Token('GIRAR_DIREITA', 'girar_direita', 16),
            Token('NUMERO_INTEIRO', '90', 16),
            Token('PONTO_VIRGULA', ';', 16),
            Token('ID', 'lado', 17),
            Token('ATRIBUICAO', '=', 17),
            Token('ID', 'lado', 17),
            Token('OP_ARITMETICO', '+', 17),
            Token('NUMERO_INTEIRO', '5', 17),
            Token('PONTO_VIRGULA', ';', 17),
            Token('FIM_REPITA', 'fim_repita', 18),
            Token('PONTO_VIRGULA', ';', 18),
            Token('FIM', 'fim', 19),
            Token('EOF', '', 20)
        ]

        self.assertEqual(tokens, esperado)


if __name__ == '__main__':
    unittest.main(verbosity=2)