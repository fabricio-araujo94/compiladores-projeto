import turtle
import math

# --- Configuração da Tela e Tartaruga ---
screen = turtle.Screen()
screen.title("entrada2")
t = turtle.Turtle()
t.speed(0)
pilha_posicao = []

# --- Código Gerado pelo Compilador ---
# Inicialização de variáveis
angulo = 0

screen.bgcolor("black")
t.pencolor("magenta")
t.pensize(2)
angulo = 30
for _ in range(12):
    pilha_posicao.append({'pos': t.pos(), 'heading': t.heading()})
    t.right(90)
    t.circle(100)
    if pilha_posicao:
        estado = pilha_posicao.pop()
        t.penup()
        t.setpos(estado['pos'])
        t.setheading(estado['heading'])
        t.pendown()
    t.right(angulo)
t.pencolor("yellow")
t.circle(10)

# --- Finalização ---
turtle.done()