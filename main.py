import sys
import os

diretorio_src = os.path.join(os.path.dirname(__file__), 'src')
sys.path.append(diretorio_src)

from tokenizer import tokenizar
from parser import Parser
from semantico import AnalisadorSemantico
from gerador import GeradorDeCodigo

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 main.py <caminho_para_o_arquivo.txt>")
        sys.exit(1)

    caminho_arquivo_entrada = sys.argv[1]

    nome_base = os.path.splitext(os.path.basename(caminho_arquivo_entrada))[0]
    caminho_arquivo_saida = os.path.join('examples', 'output', f'{nome_base}.py')

    try:
        with open(caminho_arquivo_entrada, 'r', encoding='utf-8') as arquivo:
            codigo_fonte = arquivo.read()
        print(f"--- Compilando o arquivo: {caminho_arquivo_entrada} ---")

        # Fases de Análise
        tokens = tokenizar(codigo_fonte)
        parser = Parser(tokens)
        arvore_sintatica = parser.parse()
        analisador_semantico = AnalisadorSemantico()
        analisador_semantico.visit(arvore_sintatica)
        print("Análise Léxica, Sintática e Semântica concluídas com sucesso!")

        # Geração do Código
        gerador = GeradorDeCodigo()
        codigo_python = gerador.gerar(arvore_sintatica, nome_base)

        os.makedirs(os.path.dirname(caminho_arquivo_saida), exist_ok=True)
        with open(caminho_arquivo_saida, 'w', encoding='utf-8') as arquivo_saida:
            arquivo_saida.write(codigo_python)

        print("\n--- Compilação finalizada com sucesso! ---")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo_entrada}' não foi encontrado.")
    except (SyntaxError, NameError, TypeError) as e:
        print(f"\nERRO: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
