import turtle
import math

# --- Configuração da Tela e Tartaruga ---
screen = turtle.Screen()
screen.title("entrada3")
t = turtle.Turtle()
t.speed(0)
pilha_posicao = []

# --- Código Gerado pelo Compilador ---
# Inicialização de variáveis
lado = 0

lado = 80
if (50 > 30):
    t.pencolor("blue")
else:
    t.pencolor("green")
for _ in range(4):
    t.backward(lado)
    t.left(90)
t.penup()
t.goto(120, -50)
t.pendown()
if (50 < 30):
    t.pencolor("blue")
else:
    t.pencolor("green")
for _ in range(4):
    t.forward(lado)
    t.right(90)

# --- Finalização ---
turtle.done()