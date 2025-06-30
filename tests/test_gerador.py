import unittest
import textwrap
from src.gerador import GeradorDeCodigo
from src.ast_nodes import *
from src.tokenizer import Token

class TestGeradorDeCodigo(unittest.TestCase):

    def setUp(self):
        """Prepara uma nova instância do gerador para cada teste."""
        self.gerador = GeradorDeCodigo()

    def _criar_token_dummy(self, tipo, valor, linha=1):
        """Cria um token simples para os nós da AST."""
        return Token(tipo, valor, linha)

    def _comparar_codigo(self, gerado, esperado):
        """
        Compara duas strings de código, ignorando espaços extras e
        quebras de linha no início/fim para evitar testes frágeis.
        """
        # textwrap.dedent remove a indentação comum do bloco de string
        esperado_limpo = textwrap.dedent(esperado).strip()
        gerado_limpo = gerado.strip()
        self.assertEqual(gerado_limpo, esperado_limpo)

    def test_geracao_declaracao_e_atribuicao(self):
        # AST para: var inteiro: x; x = 10;
        decl = VarDecl(
            Tipo(self._criar_token_dummy('INTEIRO', 'inteiro')),
            [Variavel(self._criar_token_dummy('ID', 'x'))]
        )
        atrib = Atribuicao(
            Variavel(self._criar_token_dummy('ID', 'x')),
            Literal(self._criar_token_dummy('NUMERO_INTEIRO', '10'))
        )
        arvore = Programa(bloco=Bloco(declaracoes=[decl], comandos=[atrib]))
        
        codigo_gerado = self.gerador.gerar(arvore)

        codigo_esperado = """
        import turtle
        import math

        # --- Configuração da Tela e Tartaruga ---
        screen = turtle.Screen()
        screen.title("Resultado")
        t = turtle.Turtle()
        t.speed(0)
        pilha_posicao = []

        # --- Código Gerado pelo Compilador ---
        # Inicialização de variáveis
        x = 0

        x = 10

        # --- Finalização ---
        turtle.done()
        """
        self._comparar_codigo(codigo_gerado, codigo_esperado)

    def test_geracao_comando_simples(self):
        # AST para: avancar 100;
        comando = ComandoSimples(
            self._criar_token_dummy('AVANCAR', 'avancar'),
            Literal(self._criar_token_dummy('NUMERO_INTEIRO', '100'))
        )
        arvore = Programa(bloco=Bloco(declaracoes=[], comandos=[comando]))

        codigo_gerado = self.gerador.gerar(arvore)
        
        # Verifica apenas a linha do comando gerado
        self.assertIn("t.forward(100)", codigo_gerado)

    def test_geracao_repita(self):
        # AST para: repita 2 vezes avancar 50; fim_repita;
        comando_interno = ComandoSimples(
            self._criar_token_dummy('AVANCAR', 'avancar'),
            Literal(self._criar_token_dummy('NUMERO_INTEIRO', '50'))
        )
        repita = Repita(
            vezes=Literal(self._criar_token_dummy('NUMERO_INTEIRO', '2')),
            bloco=Bloco(declaracoes=[], comandos=[comando_interno])
        )
        arvore = Programa(bloco=Bloco(declaracoes=[], comandos=[repita]))
        
        codigo_gerado = self.gerador.gerar(arvore)
        
        # Verifica a estrutura do laço for
        self.assertIn("for _ in range(2):", codigo_gerado)
        self.assertIn("    t.forward(50)", codigo_gerado)

    def test_geracao_se_senao(self):
        # AST para: se verdadeiro entao avancar 10; senao recuar 10; fim_se;
        condicao = Literal(self._criar_token_dummy('VERDADEIRO', 'verdadeiro'))
        comando_se = ComandoSimples(self._criar_token_dummy('AVANCAR', 'avancar'), 
                                    Literal(self._criar_token_dummy('NUMERO_INTEIRO', '10')))
        comando_senao = ComandoSimples(self._criar_token_dummy('RECUAR', 'recuar'), 
                                       Literal(self._criar_token_dummy('NUMERO_INTEIRO', '10')))
        
        estrutura_se = Se(
            condicao=condicao,
            bloco_se=Bloco([], [comando_se]),
            bloco_senao=Bloco([], [comando_senao])
        )
        arvore = Programa(bloco=Bloco(declaracoes=[], comandos=[estrutura_se]))
        
        codigo_gerado = self.gerador.gerar(arvore)

        self.assertIn("if True:", codigo_gerado)
        self.assertIn("    t.forward(10)", codigo_gerado)
        self.assertIn("else:", codigo_gerado)
        self.assertIn("    t.backward(10)", codigo_gerado)

    def test_geracao_expressao_binaria(self):
        # AST para: x = (5 + 3) * 2;
        op_soma = BinOp(
            Literal(self._criar_token_dummy('NUMERO_INTEIRO', '5')),
            self._criar_token_dummy('OP_ARITMETICO', '+'),
            Literal(self._criar_token_dummy('NUMERO_INTEIRO', '3'))
        )
        op_mult = BinOp(
            op_soma,
            self._criar_token_dummy('OP_ARITMETICO', '*'),
            Literal(self._criar_token_dummy('NUMERO_INTEIRO', '2'))
        )
        atribuicao = Atribuicao(Variavel(self._criar_token_dummy('ID', 'x')), op_mult)
        declaracao = VarDecl(Tipo(self._criar_token_dummy('INTEIRO', 'inteiro')), 
                             [Variavel(self._criar_token_dummy('ID', 'x'))])
        arvore = Programa(bloco=Bloco(declaracoes=[declaracao], comandos=[atribuicao]))

        codigo_gerado = self.gerador.gerar(arvore)

        self.assertIn("x = ((5 + 3) * 2)", codigo_gerado)
        
if __name__ == '__main__':
    unittest.main(verbosity=2)