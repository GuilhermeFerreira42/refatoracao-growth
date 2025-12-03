import os
import threading
import re
from typing import Dict, Any, List, Optional, Set, Tuple

# Importar count_tokens do core corretamente
from .counter import count_tokens # Necessário para contar tokens APÓS o scan

# === CONSTANTES DE CONFIGURAÇÃO ===

# Lista de extensões de texto conhecidas (fast-path)
TEXT_EXTENSIONS: Set[str] = {
    '.py', '.txt', '.js', '.html', '.css', '.md', '.json', '.xml', '.c', '.h', 
    '.cpp', '.java', '.go', '.rs', '.ts', '.tsx', '.jsx', '.scss', '.sh', '.yaml', 
    '.ini', '.log', '.rst', '.vue', '.mts', '.mjs', '.cjs', '.tf', '.tfvars', '.toml',
    '.gitattributes', '.gitignore', '.editorconfig' # Adicionadas extensões comuns
}

# Lista de extensões que são quase sempre binárias (fast-path para ignorar)
IGNORED_BINARIES: Set[str] = {
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg', '.webp', # Imagens
    '.mp3', '.wav', '.ogg', # Áudio
    '.mp4', '.avi', '.mov', # Vídeo
    '.zip', '.rar', '.7z', '.tar', '.gz', # Arquivos comprimidos
    '.pdf', '.exe', '.dll', '.so', '.dylib', '.obj', '.bin', '.db', '.dat' # Outros binários
}

MAX_FILE_SIZE = 10 * 1024 * 1024 # 10MB
BINARY_CHECK_BYTES = 1024 # Quantos bytes ler para checagem heurística
NULL_BYTE_THRESHOLD = 5 # Se mais de 5 bytes nulos, assume binário

# === FUNÇÕES AUXILIARES ===

def natural_sort_key(s: str) -> List[Any]:
    """Chave de ordenação natural."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def is_binary_by_content_check(file_path: str) -> bool:
    """
    Heurística: Lê os bytes iniciais e procura por alta densidade de bytes nulos (\x00),
    um forte indicador de arquivos binários (ex: imagens, executáveis).
    """
    try:
        if os.path.getsize(file_path) == 0:
            return False # Arquivo vazio não é binário (mas o token count será 0, o que é correto)
        
        # Abre o arquivo em modo binário
        with open(file_path, 'rb') as f:
            data = f.read(BINARY_CHECK_BYTES)
            
        # Contagem de bytes nulos
        null_byte_count = data.count(b'\x00')
        
        # Se a contagem de bytes nulos exceder o limite, considera binário
        if null_byte_count > NULL_BYTE_THRESHOLD:
            return True
        
        return False

    except IOError:
        # Arquivo inacessível ou outro erro de I/O, tratamos como não processável (binário)
        return True

# === TreeNode Definition (Mantida) ===
class TreeNode:
    # ... (A definição da classe TreeNode permanece inalterada) ...
    def __init__(self, name, full_path, is_dir, size_bytes=0, is_text=False, token_count=0, total_recursive_tokens=0, selection_state=0):
        self.name = name
        self.full_path = full_path
        self.is_dir = is_dir
        self.size_bytes = size_bytes
        self.is_text = is_text
        self.token_count = token_count
        self.total_recursive_tokens = total_recursive_tokens
        self.selection_state = selection_state
        self.children: List['TreeNode'] = []
        self.parent: Optional['TreeNode'] = None

    def add_child(self, child: 'TreeNode'):
        self.children.append(child)
        child.parent = self
        
    def calculate_recursive_tokens(self) -> int:
        """Calcula e atualiza o total de tokens do nó (soma dos filhos + próprio token_count se for arquivo)."""
        # A contagem agora considera o próprio token_count se o arquivo for classificado como texto (is_text=True)
        # O paradigma mudou: selecionamos tudo que é texto automaticamente (state=2)
        total_tokens = self.token_count if not self.is_dir and self.is_text else 0
        for child in self.children:
            total_tokens += child.calculate_recursive_tokens()
        self.total_recursive_tokens = total_tokens
        return total_tokens

# ===============================================

def scan_directory(root_path: str, cancel_flag: threading.Event, progress_callback: callable) -> Dict[str, Any]:
    """
    Escaneia o diretório, constrói a árvore, lê o conteúdo dos arquivos de texto e calcula a contagem inicial de tokens.
    """
    if not os.path.isdir(root_path):
        return {'root_node': None, 'file_contents': {}, 'text_file_paths': set(), 'all_extensions': set(), 'total_files': 0, 'root_path': root_path, 'node_map': {}}

    file_contents: Dict[str, str] = {}
    text_file_paths: List[str] = []
    all_extensions: Set[str] = set()
    total_files = 0
    
    # 1. Primeira Passagem: Coleta todos os arquivos e totaliza
    all_items = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Exclui pastas que são sempre irrelevantes (agora expandido para mais binários/dependências)
        dirnames[:] = [d for d in dirnames if not (d.startswith('.') or d in ('__pycache__', 'node_modules', 'dist', 'build', 'target', 'venv', 'env'))]
        for f in filenames:
            all_items.append(os.path.join(dirpath, f))
        total_files += len(filenames)
            
    root_node = TreeNode(os.path.basename(root_path), root_path, True, selection_state=2)
    node_map: Dict[str, TreeNode] = {root_path: root_node}

    # 2. Segunda Passagem: Criar a árvore, ler o conteúdo e preencher node_map
    current_scanned_count = 0
    
    for full_path in all_items:
        if cancel_flag.is_set(): break
            
        current_scanned_count += 1
        is_text_file = False
        
        try:
            size = os.path.getsize(full_path)
            item_name = os.path.basename(full_path)
            
            _, ext = os.path.splitext(item_name)
            ext = ext.lower()
            all_extensions.add(ext)
            
            # 1. Checagem de Extensão e Tamanho
            is_known_text = ext in TEXT_EXTENSIONS
            is_known_binary = ext in IGNORED_BINARIES or size > MAX_FILE_SIZE
            
            if not is_known_binary:
                
                # 2. Checagem de Conteúdo Binário (Heurística)
                # Se não for um binário conhecido, ou for de extensão desconhecida, faz a checagem por bytes nulos
                if is_known_text or not is_binary_by_content_check(full_path):
                    
                    # 3. Tenta Ler Estritamente como UTF-8
                    try:
                        # Tenta ler o arquivo. Se falhar no encoding, ele não é um texto limpo
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Sucesso: É um arquivo de texto limpo
                        is_text_file = True
                        file_contents[full_path] = content
                        text_file_paths.append(full_path)
                        # Atualiza o tamanho com o conteúdo lido (útil após decodificação)
                        child_node_size = len(content.encode('utf-8'))
                        
                    except UnicodeDecodeError:
                        # O arquivo falhou na decodificação UTF-8 (encoding diferente/malformado). Ignora.
                        is_text_file = False
                    
                    except Exception:
                        # Outros erros de I/O, ignora.
                        is_text_file = False
            
            # Cria o nó e atualiza o estado
            child_node = TreeNode(item_name, full_path, False, size_bytes=size if not is_text_file else child_node_size, 
                                  is_text=is_text_file, selection_state=2 if is_text_file else 0)
            
            # --- Criação da Hierarquia (Mesma Lógica Anterior) ---
            path_parts = os.path.relpath(full_path, root_path).split(os.path.sep)
            
            current_path_segment = root_path
            current_parent_node = root_node
            
            for part in path_parts[:-1]:
                current_path_segment = os.path.join(current_path_segment, part)
                if current_path_segment not in node_map:
                    new_dir_node = TreeNode(part, current_path_segment, True, selection_state=2)
                    current_parent_node.add_child(new_dir_node)
                    node_map[current_path_segment] = new_dir_node
                    current_parent_node = new_dir_node
                else:
                    current_parent_node = node_map[current_path_segment]
                    
            current_parent_node.add_child(child_node)
            node_map[full_path] = child_node

        except OSError:
            # Ignora arquivos inacessíveis
            pass
        finally:
            progress_callback(current_scanned_count, total_files, full_path)

    
    # 3. Contagem Inicial de Tokens e Totais Recursivos
    for path, content in file_contents.items():
        node = node_map.get(path)
        if node and node.is_text:
            tokens, _ = count_tokens(content)
            node.token_count = tokens
            
    # Remove a lógica de seleção de arquivos (state=2) e usa is_text
    text_file_paths_set = {path for path in file_contents.keys() if node_map.get(path) and node_map.get(path).is_text}
    
    # O total recursivo será recalculado no project_panel após a sincronização inicial
    
    return {
        'root_node': root_node,
        'file_contents': file_contents,
        'text_file_paths': text_file_paths_set,
        'all_extensions': all_extensions,
        'total_files': total_files,
        'root_path': root_path,
        'node_map': node_map
    }