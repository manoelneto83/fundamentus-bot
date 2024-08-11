import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re

def validar_input(valor):
    if re.match(r'^\d{0,4}(\,\d{0,2})?$', valor):  # Aceita até 4 dígitos antes da vírgula e até 2 dígitos depois da vírgula
        return True
    return False

def formatar_input(event):
    valor = event.widget.get()
    novo_valor = re.sub(r'\D', '', valor)  # Remove todos os caracteres não numéricos
    if len(novo_valor) > 2:
        novo_valor = f"{novo_valor[:-2]},{novo_valor[-2:]}"  # Formata como '0,00'
    event.widget.delete(0, tk.END)
    event.widget.insert(0, novo_valor)

def verificar_inputs():
    liquidez_valor = entrada_liquidez.get()
    dy_valor = entrada_dy.get()

    if validar_input(liquidez_valor) and validar_input(dy_valor):
        messagebox.showinfo("Sucesso", "Inputs válidos: Liquidez = " + liquidez_valor + ", DY = " + dy_valor)
    else:
        messagebox.showerror("Erro", "Inputs inválidos. Insira valores em reais.")

janela = tk.Tk()
janela.title("Inputs em Reais")
janela.geometry('300x200')  # Define o tamanho da janela

estilo = ttk.Style()
estilo.configure('Estilo.TFrame', background='lightblue')
estilo.configure('Estilo.TLabel', background='lightblue')
estilo.configure('Estilo.TEntry', foreground='black', background='white', fieldbackground='lightgray')

frame = ttk.Frame(janela, style='Estilo.TFrame')
frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)  # Adiciona espaço interno

rotulo_liquidez = ttk.Label(frame, text="Liquidez (R$): ", style='Estilo.TLabel')
rotulo_liquidez.pack(pady=(10, 0))  # Adiciona espaço acima

entrada_liquidez = ttk.Entry(frame, style='Estilo.TEntry')
entrada_liquidez.pack(pady=(0, 10))  # Adiciona espaço abaixo
entrada_liquidez.insert(0, "0,00")  # Insere o valor padrão
entrada_liquidez.bind('<KeyRelease>', formatar_input)  # Aplica a formatação do input
entrada_liquidez.configure(justify='right')  # Alinha o texto à direita

rotulo_dy = ttk.Label(frame, text="DY (R$): ", style='Estilo.TLabel')
rotulo_dy.pack(pady=(10, 0))  # Adiciona espaço acima

entrada_dy = ttk.Entry(frame, style='Estilo.TEntry')
entrada_dy.pack(pady=(0, 10))  # Adiciona espaço abaixo
entrada_dy.insert(0, "0,00")  # Insere o valor padrão
entrada_dy.bind('<KeyRelease>', formatar_input)  # Aplica a formatação do input
entrada_dy.configure(justify='right')  # Alinha o texto à direita

botao_verificar = ttk.Button(frame, text="Verificar", command=verificar_inputs)
botao_verificar.pack(pady=(10, 0))  # Adiciona espaço acima

janela.mainloop()
