# -*- coding: utf-8 -*-
# teste_final_encoding.py

import tkinter as tk
import sys

print("--- Teste de Encoding Isolado ---")
print("Este script não lê nenhum outro arquivo do projeto.")
print(f"Encoding padrão do sistema: {sys.getdefaultencoding()}")
print(f"Encoding do sistema de arquivos: {sys.getfilesystemencoding()}")


# A string abaixo é criada diretamente aqui. Se houver erro, é na leitura deste próprio arquivo.
texto_com_acento = "Teste de Acentuação: Alimentação, Transações, Ações ~ ^ ç"

print(f"Texto dentro do Python: {texto_com_acento}")

try:
    root = tk.Tk()
    root.title("Teste Final de Codificação")
    
    # Vamos exibir o texto na janela.
    label = tk.Label(root, text=f"Texto exibido na Janela:\n\n{texto_com_acento}", font=("Arial", 14))
    label.pack(padx=40, pady=40)
    
    root.mainloop()

except Exception as e:
    print(f"Ocorreu um erro ao criar a interface: {e}")