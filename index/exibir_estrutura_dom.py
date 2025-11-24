# arvore_html_completa.py  ← versão que FUNCIONA NO WINDOWS

import os
import sys

# FORÇA UTF-8 no Windows (resolve o erro de acentos de uma vez por todas)
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from bs4 import BeautifulSoup

# === MUDE AQUI SE O NOME DO ARQUIVO FOR DIFERENTE ===
arquivo_html = "Suplementos_ comprar suplementos alimentares é na Growth!.html"

def imprimir_arvore(tag, nivel=0):
    indent = "  " * nivel
    nome = tag.name or "[texto]"
    classe = tag.get("class", [])
    classe_str = "." + " ".join(classe) if classe else ""
    id_tag = "#" + tag.get("id", "") if tag.get("id") else ""
    
    linha = f"{indent}└─ <{nome}{id_tag}{classe_str}>"
    print(linha)

    # Todos os filhos diretos
    for filho in tag.find_all(recursive=False):
        if filho.name:  # só tags
            imprimir_arvore(filho, nivel + 1)

# =================== EXECUÇÃO =====================
print("Montando árvore COMPLETA do HTML... Aguenta aí!\n")

try:
    soup = BeautifulSoup(open(arquivo_html, "r", encoding="utf-8"), "lxml")
except:
    soup = BeautifulSoup(open(arquivo_html, "r", encoding="utf-8"), "html.parser")

body = soup.find("body")
if body:
    print("<body>")
    imprimir_arvore(body)
else:
    print("<html inteiro>")
    imprimir_arvore(soup.html or soup)

print("\nPRONTO! Árvore completa salva em arvore_completa.txt")