import turtle
import math

# --- Configuração da Tela e Tartaruga ---
screen = turtle.Screen()
screen.title("entrada1")
t = turtle.Turtle()
t.speed(0)
pilha_posicao = []

# --- Código Gerado pelo Compilador ---
# Inicialização de variáveis
lado = 0
angulo_ponta = 0
angulo_interno = 0
cor = ""
i = 0

lado = 100
angulo_ponta = 144
angulo_interno = 72
cor = "blue"
t.pencolor(cor)
t.pensize(3)
i = 0
while (i < 5):
    t.forward(lado)
    t.right(angulo_ponta)
    t.forward(lado)
    t.left(angulo_interno)
    i = (i + 1)

# --- Finalização ---
turtle.done()