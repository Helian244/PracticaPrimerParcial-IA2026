import tkinter as tk
import time
from collections import deque
from PIL import Image, ImageTk

filas = 10
columnas = 10
tam = 50

color_fondo = "#1e1e2f"
color_camino = "#ecf0f1"
color_pared = "#2c3e50"
color_visitado = "#ff6b6b"
color_final = "#51cf66"

inicio = (0, 0)
meta = (filas-1, columnas-1)

movimientos = [(0,-1),(0,1),(-1,0),(1,0)]

laberinto = []

def cargar_imagenes():
    global raton_img, queso_img

    raton = Image.open("assets/raton.png").resize((tam, tam))
    queso = Image.open("assets/queso.png").resize((tam, tam))

    raton_img = ImageTk.PhotoImage(raton)
    queso_img = ImageTk.PhotoImage(queso)

laberintos = [
    [
    [0,0,0,1,0,0,0,0,0,0],
    [1,1,0,1,0,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,0,1,0],
    [0,0,0,0,0,0,1,0,1,0],
    [0,1,1,1,1,0,1,0,0,0],
    [0,0,0,0,1,0,1,1,1,0],
    [1,1,1,0,1,0,0,0,1,0],
    [0,0,0,0,0,0,1,0,0,0],
    [0,1,1,1,1,0,0,0,1,0],
    ],
    [
    [0,1,0,0,0,0,1,0,0,0],
    [0,1,0,1,1,0,1,0,1,0],
    [0,0,0,1,0,0,0,0,1,0],
    [1,1,0,1,0,1,1,0,1,0],
    [0,0,0,0,0,1,0,0,0,0],
    [0,1,1,1,0,1,0,1,1,0],
    [0,0,0,1,0,0,0,1,0,0],
    [1,1,0,1,1,1,0,1,0,1],
    [0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,0],
    ],
    [
    [0,0,1,0,0,0,0,1,0,0],
    [1,0,1,0,1,1,0,1,0,1],
    [1,0,0,0,0,1,0,0,0,1],
    [1,1,1,1,0,1,1,1,0,0],
    [0,0,0,1,0,0,0,1,1,0],
    [0,1,0,1,1,1,0,0,0,0],
    [0,1,0,0,0,1,0,1,1,0],
    [0,1,1,1,0,0,0,1,0,0],
    [0,0,0,1,0,1,0,0,0,1],
    [1,1,0,0,0,1,1,1,0,0],
    ],
    [
    [0,0,0,0,1,0,0,0,0,0],
    [1,1,1,0,1,0,1,1,1,0],
    [0,0,0,0,0,0,1,0,0,0],
    [0,1,1,1,1,0,1,0,1,1],
    [0,0,0,0,1,0,0,0,0,0],
    [1,1,1,0,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,0,1,0],
    [0,0,0,0,0,0,1,0,0,0],
    [0,1,1,1,1,0,0,0,1,0],
    ],
    [
    [0,0,0,1,0,0,0,0,0,0],
    [0,1,0,1,0,1,1,1,1,0],
    [0,1,0,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,1,0,1,0],
    [0,0,0,0,0,0,1,0,0,0],
    [0,1,1,1,1,0,1,1,1,0],
    [0,0,0,0,1,0,0,0,0,0],
    [1,1,1,0,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,0],
    ]
]

def cargar_laberinto():
    global laberinto
    import random
    laberinto = [fila[:] for fila in random.choice(laberintos)]
    dibujar()
    texto.set("laberinto cargado")

def dibujar():
    canvas.delete("all")

    if not laberinto:
        return

    for i in range(filas):
        for j in range(columnas):
            color = color_camino if laberinto[i][j] == 0 else color_pared
            canvas.create_rectangle(j*tam, i*tam, (j+1)*tam, (i+1)*tam, fill=color, outline="")

    canvas.create_image(meta[1]*tam, meta[0]*tam, anchor="nw", image=queso_img)
    canvas.create_image(inicio[1]*tam, inicio[0]*tam, anchor="nw", image=raton_img)

def limpiar():
    dibujar()
    texto.set("listo")

def ejecutar(tipo):
    if not laberinto:
        texto.set("carga un laberinto primero")
        return
    limpiar()
    t0 = time.time()
    estructura = deque([(inicio, [inicio])]) if tipo == "bfs" else [(inicio, [inicio])]
    visitados = set()
    explorados = []
    while estructura:
        (x,y), camino = estructura.popleft() if tipo == "bfs" else estructura.pop()
        if (x,y) == meta:
            tiempo = time.time() - t0
            animar(explorados, camino)
            texto.set(f"{tipo.upper()} | tiempo: {tiempo:.4f}s | nodos: {len(explorados)} | pasos: {len(camino)}")
            return
        if (x,y) in visitados:
            continue
        visitados.add((x,y))
        explorados.append((x,y))
        for dx, dy in movimientos:
            nx, ny = x+dx, y+dy
            if 0 <= nx < filas and 0 <= ny < columnas:
                if laberinto[nx][ny] == 0:
                    estructura.append(((nx,ny), camino + [(nx,ny)]))

def animar(explorados, camino):

    # dibujar explorados (rojo)
    for (x,y) in explorados:
        canvas.create_rectangle(y*tam, x*tam, (y+1)*tam, (x+1)*tam,
                                fill=color_visitado, outline="")

        # volver a dibujar queso y raton encima
        canvas.create_image(meta[1]*tam, meta[0]*tam, anchor="nw", image=queso_img)
        canvas.create_image(inicio[1]*tam, inicio[0]*tam, anchor="nw", image=raton_img)

        root.update()
        time.sleep(0.01)

    # dibujar camino final (verde)
    for (x,y) in camino:
        canvas.create_rectangle(y*tam, x*tam, (y+1)*tam, (x+1)*tam,
                                fill=color_final, outline="")

        # raton se mueve
        canvas.create_image(meta[1]*tam, meta[0]*tam, anchor="nw", image=queso_img)
        canvas.create_image(y*tam, x*tam, anchor="nw", image=raton_img)

        root.update()
        time.sleep(0.06)

root = tk.Tk()
root.title("laberinto ia")
root.config(bg=color_fondo)

frame = tk.Frame(root, bg=color_fondo, padx=20, pady=20)
frame.pack()

canvas = tk.Canvas(frame, width=columnas*tam, height=filas*tam, bg="black")
canvas.grid(row=0, column=0, columnspan=5, pady=10)

texto = tk.StringVar()
texto.set("carga un laberinto")

tk.Label(frame, textvariable=texto, bg=color_fondo, fg="white", font=("Arial", 11, "bold")).grid(row=1, column=0, columnspan=5, pady=10)

tk.Button(frame, text="cargar laberinto", command=cargar_laberinto, bg="#3498db").grid(row=2, column=1, pady=5)
tk.Button(frame, text="bfs", command=lambda: ejecutar("bfs"), bg="#2ecc71").grid(row=2, column=2)
tk.Button(frame, text="dfs", command=lambda: ejecutar("dfs"), bg="#e74c3c").grid(row=2, column=3)
tk.Button(frame, text="limpiar", command=limpiar, bg="#f1c40f").grid(row=2, column=4)

# inicio
cargar_imagenes()

root.mainloop()