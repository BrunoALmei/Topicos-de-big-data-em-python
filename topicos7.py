import sqlite3
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, messagebox
from tkinter import font, ttk
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def criar_banco_de_dados():
    conn = sqlite3.connect('carros_eletricos_brasil.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS evolucao_carros_eletricos_brasil (
        ano INTEGER PRIMARY KEY,
        quantidade INTEGER
    )
    ''')

    dados = [
        (2018, 3970),
        (2019, 11858),
        (2020, 19745),
        (2021, 34990),
        (2022, 49245),
        (2023, 78005),
        (2024, 79304)
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO evolucao_carros_eletricos_brasil (ano, quantidade) VALUES (?, ?)', dados)
    
    conn.commit()
    conn.close()


def consultar_por_ano(ano):
    conn = sqlite3.connect('carros_eletricos_brasil.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT quantidade FROM evolucao_carros_eletricos_brasil WHERE ano = ?', (ano,))
    
    dado = cursor.fetchone()
    conn.close()
    
    return dado


def consultar_ultimos_6_anos():
    conn = sqlite3.connect('carros_eletricos_brasil.db')
    cursor = conn.cursor()
    
    ano_atual = datetime.now().year
    cursor.execute('SELECT ano, quantidade FROM evolucao_carros_eletricos_brasil WHERE ano >= ?', (ano_atual - 6,))
    
    dados = cursor.fetchall()
    conn.close()
    
    return dados


def gerar_grafico(dados, canvas_frame):
    if not dados:
        messagebox.showwarning("Sem Dados", "Não há dados suficientes para mostrar no gráfico.")
        return

    # Dados para o gráfico
    anos = [d[0] for d in dados]
    quantidade = [d[1] for d in dados]
    
    # Criando o gráfico de barras (torres)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(anos, quantidade, color='dodgerblue')
    ax.set_title('Evolução de Carros Elétricos no Brasil', fontsize=16, fontweight='bold')
    ax.set_xlabel('Ano', fontsize=12)
    ax.set_ylabel('Quantidade de Carros Elétricos Fabricados', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)

    # Limpar o canvas anterior antes de desenhar o novo
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    # Adicionando o gráfico à interface do Tkinter
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


def on_combobox_select(event, canvas_frame):
    ano = combo_ano.get()
    if not ano:
        messagebox.showwarning("Erro", "Por favor, selecione um ano.")
        return
    
    # Consultar dados para o ano selecionado
    dado = consultar_por_ano(int(ano))
    if dado:
        dados = [(int(ano), dado[0])]
        gerar_grafico(dados, canvas_frame)
    else:
        messagebox.showwarning("Não Encontrado", f"Não há dados para o ano {ano}.")


def on_button_grafico_ultimos_6_anos_click(canvas_frame):
    dados = consultar_ultimos_6_anos()  
    gerar_grafico(dados, canvas_frame)


def criar_interface():
    root = Tk()
    root.title("Consulta Carros Elétricos no Brasil")
    
    title_font = font.Font(family="Helvetica", size=16, weight="bold")
    label_font = font.Font(family="Helvetica", size=12)
    button_font = font.Font(family="Helvetica", size=12, weight="bold")
    
    label = Label(root, text="Consulta Carros Elétricos no Brasil", font=title_font, fg="darkblue")
    label.grid(row=0, column=0, columnspan=2, pady=20)

    # Label e Combobox para selecionar o ano
    label_ano = Label(root, text="Selecione o ano para consulta:", font=label_font, anchor="w", fg="darkblue")
    label_ano.grid(row=1, column=0, padx=20, pady=5, sticky="w")

    global combo_ano
    combo_ano = ttk.Combobox(root, values=[2018, 2019, 2020, 2021, 2022, 2023, 2024], font=label_font, state="readonly")
    combo_ano.grid(row=1, column=1, padx=20, pady=5)
    combo_ano.bind("<<ComboboxSelected>>", lambda event: on_combobox_select(event, canvas_frame))
    
    # Botão para gerar gráfico dos últimos 6 anos
    button_grafico = Button(root, text="Gerar Gráfico (Últimos 6 Anos)", font=button_font, bg="seagreen", fg="white", command=lambda: on_button_grafico_ultimos_6_anos_click(canvas_frame))
    button_grafico.grid(row=2, column=0, columnspan=2, pady=15, padx=10, ipadx=10)
    
    # Frame para mostrar o gráfico
    global canvas_frame
    canvas_frame = ttk.Frame(root)
    canvas_frame.grid(row=3, column=0, columnspan=2, pady=20)

    root.geometry("600x400")
    root.config(bg="#f0f8ff")
    root.mainloop()


if __name__ == "__main__":
    criar_banco_de_dados()  
    criar_interface()
