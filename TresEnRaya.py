import tkinter as tk
import math
import random

board = [" " for _ in range(9)]
modo = "minimax"
modo_juego = "IA"
turno = None
juego_terminado = False

def check_winner(b, p):
    combos = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    return any(b[c[0]] == b[c[1]] == b[c[2]] == p for c in combos)

def is_draw(b):
    return " " not in b


def minimax(b, is_max, alpha, beta):
    if check_winner(b, "O"):
        return 1
    if check_winner(b, "X"):
        return -1
    if is_draw(b):
        return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "O"
                val = minimax(b, False, alpha, beta)
                b[i] = " "
                best = max(best, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "X"
                val = minimax(b, True, alpha, beta)
                b[i] = " "
                best = min(best, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break
        return best

def mejor_minimax():
    mejores = []
    best_val = -math.inf

    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            val = minimax(board, False, -math.inf, math.inf)
            board[i] = " "

            if val > best_val:
                best_val = val
                mejores = [i]
            elif val == best_val:
                mejores.append(i)

    return random.choice(mejores)

def constructivo():
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            if check_winner(board, "O"):
                board[i] = " "
                return i
            board[i] = " "

    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            if check_winner(board, "X"):
                board[i] = " "
                return i
            board[i] = " "

    if board[4] == " ":
        return 4

    esquinas = [i for i in [0, 2, 6, 8] if board[i] == " "]
    if esquinas:
        return random.choice(esquinas)

    libres = [i for i in range(9) if board[i] == " "]
    return random.choice(libres)

root = tk.Tk()
root.title("Tres en Raya")
root.config(bg="#1e1e2f")

buttons = []
status = tk.StringVar()
status.set("Elige quién empieza")

modo_label = tk.StringVar()
modo_label.set("Modo: Minimax")

mensaje_final = tk.StringVar()
mensaje_final.set("")

def actualizar():
    for i in range(9):
        if board[i] == "X":
            buttons[i].config(text="X", bg="#2ecc71")
        elif board[i] == "O":
            buttons[i].config(text="O", bg="#e74c3c")
        else:
            buttons[i].config(text=" ", bg="#34495e")

def terminar_juego(mensaje):
    global juego_terminado
    juego_terminado = True

    status.set("")
    mensaje_final.set(mensaje)

    for btn in buttons:
        btn.config(state="disabled")


def turno_ia():
    global turno

    if modo_juego == "2J" or juego_terminado:
        return

    if board.count(" ") == 9:
        mov = random.choice(range(9))
    else:
        if modo == "minimax":
            mov = mejor_minimax()
        else:
            mov = constructivo()

    board[mov] = "O"
    actualizar()

    if check_winner(board, "O"):
        terminar_juego("🤖 IA Gana")
        return

    if is_draw(board):
        terminar_juego("🤝 Empate")
        return

    turno = "X"
    status.set("Tu turno")

def click(i):
    global turno

    if juego_terminado:
        return

    if board[i] != " ":
        return

    if modo_juego == "2J":
        board[i] = turno
        actualizar()

        if check_winner(board, turno):
            terminar_juego(f"🏆 Gana {turno}")
            return

        if is_draw(board):
            terminar_juego("🤝 Empate")
            return

        turno = "O" if turno == "X" else "X"
        status.set(f"Turno de: {turno}")
        return

    if turno != "X":
        return

    board[i] = "X"
    actualizar()

    if check_winner(board, "X"):
        terminar_juego("🏆 Ganaste")
        return

    if is_draw(board):
        terminar_juego("🤝 Empate")
        return

    turno = "O"
    status.set("Turno de la IA")
    root.after(400, turno_ia)


def cambiar_modo():
    global modo
    if modo == "minimax":
        modo = "constructivo"
        modo_label.set("Modo: Constructivo")
    else:
        modo = "minimax"
        modo_label.set("Modo: Minimax")

def cambiar_juego():
    global modo_juego
    if modo_juego == "IA":
        modo_juego = "2J"
        status.set("Modo: 2 Jugadores")
    else:
        modo_juego = "IA"
        status.set("Modo: IA")

def reiniciar():
    global board, turno, juego_terminado
    board = [" " for _ in range(9)]
    turno = None
    juego_terminado = False

    for btn in buttons:
        btn.config(state="normal")

    mensaje_final.set("")
    actualizar()
    status.set("Elige quién empieza")

def empieza_jugador():
    global turno
    reiniciar()
    turno = "X"

    if modo_juego == "2J":
        status.set("Turno de: X")
    else:
        status.set("Tu turno")

def empieza_ia():
    global turno
    reiniciar()
    turno = "O"

    if modo_juego == "2J":
        status.set("Turno de: O")
    else:
        status.set("Turno de la IA")
        root.after(400, turno_ia)


for i in range(9):
    btn = tk.Button(
        root,
        text=" ",
        font=("Arial", 24, "bold"),
        width=5,
        height=2,
        bg="#34495e",
        fg="white",
        command=lambda i=i: click(i)
    )
    btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
    buttons.append(btn)

tk.Button(
    root,
    text="Cambiar modo",
    command=cambiar_modo,
    bg="#f1c40f"
).grid(row=3, column=0)

tk.Button(
    root,
    text="Reiniciar",
    command=reiniciar,
    bg="#3498db"
).grid(row=3, column=1)

tk.Label(
    root,
    textvariable=modo_label,
    fg="white",
    bg="#1e1e2f"
).grid(row=3, column=2)

tk.Button(
    root,
    text="Empiezo yo",
    command=empieza_jugador,
    bg="#2ecc71"
).grid(row=4, column=0)

tk.Button(
    root,
    text="Empieza IA",
    command=empieza_ia,
    bg="#e74c3c"
).grid(row=4, column=1)

tk.Button(
    root,
    text="Modo 2 Jugadores",
    command=cambiar_juego,
    bg="#9b59b6"
).grid(row=4, column=2)

tk.Label(
    root,
    textvariable=mensaje_final,
    font=("Arial", 20, "bold"),
    fg="#f1c40f",
    bg="#1e1e2f"
).grid(row=6, column=0, columnspan=3, pady=15)

tk.Label(
    root,
    textvariable=status,
    fg="white",
    bg="#1e1e2f",
    font=("Arial", 11, "bold")
).grid(row=5, column=0, columnspan=3, pady=5)

root.mainloop()