import sys
import os
from typing import List, Any
# Importa as funcionalidades do core
try:
    from core import scan_directory, TreeNode, count_tokens
    # natural_sort_key e TreeNode também são importados via core/__init__.py
except ImportError as e:
    print(f"Erro ao importar módulos do core: {e}", file=sys.stderr)
    sys.exit(1)

# A função de ordenação natural para consistência na árvore
def _natural_sort_key(s: str) -> List[Any]:
    """Retorna uma chave para ordenação natural (copiada do scanner)."""
    import re
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def _print_node(node: TreeNode, prefix: str = "", is_root: bool = True):
    """
    Imprime um nó da árvore de diretórios em formato hierárquico para o console.
    """
    if not is_root:
        # Imprime o nó atual (diretório ou arquivo)
        line = f"{prefix}├── {node.name}"
        if not node.is_dir and node.is_text:
            # Conta tokens (usando a função do core)
            if node.content is not None:
                token_count, _ = count_tokens(node.content)
                line += f" (Tokens: {token_count:,} | Tamanho: {node.size_bytes:,} bytes)"
                
            # Adiciona a contagem de tokens ao nó para referência (o scanner não fazia isso)
            node.token_count = token_count
        elif not node.is_dir and node.is_scanned and not node.is_text:
             line += f" (Ignorado/Binário: {node.size_bytes:,} bytes)"

        print(line)
        
        # Ajusta o prefixo para os filhos
        new_prefix = prefix + ("│   " if not prefix.endswith("└── ") and not prefix.endswith("    ") else "    ")
    else:
        # Raiz
        print(f"\n{node.name}/")
        new_prefix = ""
        
    num_children = len(node.children)
    for i, child in enumerate(node.children):
        is_last = (i == num_children - 1)
        
        child_line_prefix = new_prefix
        if not is_root:
            child_line_prefix = prefix + ("└── " if is_last else "├── ")

        if child.is_dir:
            print(f"{child_line_prefix}{'└──' if is_last and is_root else '├──'} {child.name}/")
            # Recursão
            _print_node(child, prefix + ('    ' if is_last else '│   '), is_root=False)
        else:
            line = f"{child_line_prefix}{'└──' if is_last and is_root else '├──'} {child.name}"
            
            if child.is_text and child.content is not None:
                 token_count, _ = count_tokens(child.content)
                 line += f" (Tokens: {token_count:,} | Tamanho: {child.size_bytes:,} bytes)"
                 
            print(line)

def cli_scan_only(root_path: str):
    """
    Executa o escaneamento do diretório e imprime o resumo no console (Modo CLI).
    """
    root_path = os.path.abspath(root_path)
    print(f"\n=== Token Counter Pro - Modo CLI ===\n")
    print(f"Escaneando diretório: {root_path}")
    
    # 1. Escaneamento
    try:
        # Usa um callback simples para mostrar o progresso no console
        def cli_progress_callback(file_name, current, total):
            sys.stdout.write(f"\rProcessando... {file_name} ({current}/{total})")
            sys.stdout.flush()

        results = scan_directory(
            root_path, 
            extensions_filter=None, # Sem filtro no CLI por padrão
            progress_callback=cli_progress_callback
        )
        sys.stdout.write("\r" + " " * 80 + "\r") # Limpa a linha de progresso
        sys.stdout.flush()

        root_node: TreeNode = results['root_node']
        
        # 2. Contagem Total (Agregação)
        total_tokens = 0
        total_bytes = 0
        for path, content in results['file_contents'].items():
            tokens, _ = count_tokens(content)
            total_tokens += tokens
            total_bytes += os.path.getsize(path) # Usa o tamanho real
            
        text_files_count = len(results['text_file_paths'])
        total_extensions = len(results['all_extensions'])

        # 3. Impressão da Estrutura
        print("\n--- Estrutura de Diretórios & Tokens ---")
        
        # Inicia a impressão da árvore
        _print_node(root_node)

        # 4. Impressão do Resumo
        print("\n--- Resumo Global ---")
        print(f"Diretório Raiz: {root_path}")
        print(f"Arquivos de Texto Encontrados: {text_files_count:,}")
        print(f"Total de Tokens (Estimativa Real): {total_tokens:,}")
        print(f"Tamanho Total do Conteúdo Lido: {total_bytes:,} bytes")
        print(f"Total de Extensões Únicas Descobertas: {total_extensions}")
        print(f"Lista de Extensões: {sorted(list(results['all_extensions']))}")
        
    except FileNotFoundError as e:
        print(f"\nERRO: {e}", file=sys.stderr)
    except Exception as e:
        print(f"\nERRO FATAL: {e}", file=sys.stderr)

# A função de teste __main__ foi removida daqui, pois o main.py a chama.