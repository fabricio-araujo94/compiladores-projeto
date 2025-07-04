#!/bin/bash

echo "Iniciando a execução dos scripts Python..."
echo "---"

echo "Desenhando uma estrela."
python main.py examples/input/entrada1.txt
python examples/output/saida_entrada1.py

echo "Desenhando uma flor."
python main.py examples/input/entrada2.txt
python examples/output/saida_entrada2.py

echo "Desenhando quadrados coloridos separados."
python main.py examples/input/entrada3.txt
python examples/output/saida_entrada3.py


echo "---"
echo "Todos os scripts Python foram executados."