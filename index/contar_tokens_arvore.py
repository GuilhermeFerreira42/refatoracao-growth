# contar_tokens_arvore.py – VERSÃO REFINADA (Tree /a /f Style)
import sys
from pathlib import Path
import tiktoken

# Força UTF-8 no Windows (100% funcional)
# Isso é crucial para que os caracteres de linha e a acentuação sejam exibidos corretamente
if sys.platform.startswith("win"):
    import _locale
    _locale._getdefaultlocale = (lambda *args: ['en_US', 'utf-8'])
sys.stdout.reconfigure(encoding='utf-8')

# --- CONFIGURAÇÃO ---
# Modelo usado para contagem
enc = tiktoken.encoding_for_model("gpt-4o")

# Extensões que queremos contar
EXTENSOES_VALIDAS = {
    ".html", ".htm", ".js", ".ts", ".jsx", ".tsx", ".css", ".scss", ".less",
    ".json", ".md", ".txt", ".svg", ".xml", ".py", ".vue", ".svelte",
    ".php", ".java", ".c", ".cpp", ".h", ".cs", ".go", ".rb", ".swift",
    ".kt", ".yaml", ".yml", ".ini", ".cfg", ".sh", ".bash", ".ps1", ".sql",
    ".log"
}

# --- CONSTANTES DE FORMATAÇÃO DA ÁRVORE (Padrão tree /a /f) ---
V_BAR = "│   "     # Conector de continuação de ramo
L_T = "├── "      # Conector de item intermediário
L_END = "└── "    # Conector de último item
INDENT = "    "   # Indentação para último item (continuação de ramo)
TOKEN_PLACEHOLDER = "<TOKENS:" # Placeholder temporário para tokens
TOKEN_DELIMITER = ">" 

# --- FUNÇÃO PRINCIPAL RECURSIVA ---

def contar_tokens_em_pasta(caminho: Path, prefixo: str = "") -> tuple[int, list[str]]:
    """
    Conta os tokens recursivamente e retorna o total e as linhas de saída.
    A impressão é adiada para garantir a ordem correta e o alinhamento.
    """
    total_tokens = 0
    linhas_de_saida = []

    # 1. Obter e ordenar itens: Pastas antes dos arquivos, depois alfabeticamente.
    try:
        itens = list(caminho.iterdir())
    except Exception:
        # Ignora pastas sem permissão
        return 0, []
        
    itens_filtrados = []
    for item in itens:
        # Filtra itens indesejados (ocultos, node_modules, .git etc.)
        nome_lower = item.name.lower()
        if item.name.startswith(".") or nome_lower in {"__pycache__", ".git", "node_modules", "vendor", "dist", "build"}:
            continue
        itens_filtrados.append(item)

    # Ordena os itens para ter o mesmo estilo do 'tree' nativo: Pastas primeiro
    itens_filtrados.sort(key=lambda x: (x.is_file(), x.name.lower()))


    for i, item in enumerate(itens_filtrados):
        eh_ultimo = (i == len(itens_filtrados) - 1)
        conector = L_END if eh_ultimo else L_T
        
        # O novo prefixo é a continuação do ramo atual:
        # Se for o último item da lista, o próximo nível é só indentação (sem a barra vertical)
        # Se não for o último, o próximo nível continua com a barra vertical
        novo_prefixo = prefixo + (INDENT if eh_ultimo else V_BAR)

        if item.is_dir():
            # 2. Chamada recursiva para pastas
            sub_total, sub_linhas = contar_tokens_em_pasta(item, novo_prefixo)
            
            if sub_total > 0:
                # Se a pasta não estiver vazia (após a filtragem), a incluímos
                
                # Linha da Pasta: Usa o placeholder para facilitar o alinhamento posterior
                folder_line = f"{prefixo}{conector}{item.name}/ {TOKEN_PLACEHOLDER}{sub_total}{TOKEN_DELIMITER}"
                linhas_de_saida.append(folder_line)
                
                # Adiciona o conteúdo da subpasta
                linhas_de_saida.extend(sub_linhas)
                total_tokens += sub_total
        
        elif item.is_file():
            # 3. Processamento de Arquivos
            if item.suffix.lower() in EXTENSOES_VALIDAS:
                try:
                    conteudo = item.read_text(encoding="utf-8", errors="ignore")
                    tokens = len(enc.encode(conteudo))
                    
                    # Linha do Arquivo: Usa o placeholder
                    file_line = f"{prefixo}{conector}{item.name} {TOKEN_PLACEHOLDER}{tokens}{TOKEN_DELIMITER}"
                    linhas_de_saida.append(file_line)
                    total_tokens += tokens
                except Exception:
                    # Ignora silenciosamente arquivos que não puderam ser lidos
                    pass
    
    return total_tokens, linhas_de_saida


# --- EXECUÇÃO E IMPRESSÃO FINAL (Alinhamento) ---

if __name__ == "__main__":
    
    # 1. Configuração do Path
    try:
        # Tenta usar o primeiro argumento da linha de comando.
        # Se não houver argumento, usa a pasta atual (Path('.')) como padrão.
        pasta = Path(sys.argv[1])
    except IndexError:
        pasta = Path(".") # <<< MUDANÇA AQUI: Define a pasta atual como padrão.

    if not pasta.is_dir():
        print(f"Erro: '{pasta}' não é um diretório válido.")
        # Se for a pasta atual e ela não existir, algo muito errado aconteceu.
        sys.exit(1)

    # 2. Construção da Árvore Lógica
    # A resolução do caminho completo ajuda a contextualizar a execução.
    print(f"Processando árvore de arquivos em: {pasta.resolve()}")
    print("-" * 50)
    total_geral, linhas = contar_tokens_em_pasta(pasta)
    
    # 3. Processamento Final para Alinhamento
    
    # a) Encontra o tamanho máximo da string de tokens formatada (ex: "123.456")
    max_token_str_len = 0
    for linha in linhas:
        if TOKEN_PLACEHOLDER in linha:
            _, parte_token = linha.split(TOKEN_PLACEHOLDER, 1)
            token_valor_str = parte_token.removesuffix(TOKEN_DELIMITER)
            
            try:
                tokens = int(token_valor_str)
                max_token_str_len = max(max_token_str_len, len(f"{tokens:,}"))
            except ValueError:
                pass

    # Define a largura mínima de alinhamento
    ALIGN_WIDTH = max(10, max_token_str_len)
    
    # b) Imprime a raiz da árvore 
    print(f"{pasta.name or pasta.resolve().name}/") # Usa o nome da pasta ou o último segmento do caminho resolvido
    
    # c) Imprime a árvore final, alinhando a contagem de tokens
    for linha in linhas:
        
        if TOKEN_PLACEHOLDER in linha:
            
            parte_nome, parte_token = linha.split(TOKEN_PLACEHOLDER, 1)
            tokens = int(parte_token.removesuffix(TOKEN_DELIMITER))
            
            tokens_formatado = f"{tokens:,}"
            padding = " " * (ALIGN_WIDTH - len(tokens_formatado))

            linha_final = f"{parte_nome}{padding} → {tokens_formatado} tokens"
            
            print(linha_final)
        
    # 4. Imprime o Total Geral
    print("-" * 50)
    print(f"Total Geral de Tokens (gpt-4o): {total_geral:,} tokens")