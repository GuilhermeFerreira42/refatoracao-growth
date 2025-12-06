import os
import threading
import re
from typing import Dict, Any, List, Optional, Set, Tuple

# Importar count_tokens do core corretamente
from .counter import count_tokens 

# === CONSTANTES DE CONFIGURAÇÃO ===
# ... (CONSTANTES DE CONFIGURAÇÃO MANTIDAS) ...

TEXT_EXTENSIONS: Set[str] = {
    '.py', '.txt', '.js', '.html', '.css', '.md', '.json', '.xml', '.c', '.h', 
    '.cpp', '.java', '.go', '.rs', '.ts', '.tsx', '.jsx', '.scss', '.sh', '.yaml', 
    '.ini', '.log', '.rst', '.vue', '.mts', '.mjs', '.cjs', '.tf', '.tfvars', '.toml',
    '.gitattributes', '.gitignore', '.editorconfig' 
}

IGNORED_BINARIES: Set[str] = {
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg', '.webp', 
    '.mp3', '.wav', '.ogg', 
    '.mp4', '.avi', '.mov', 
    '.zip', '.rar', '.7z', '.tar', '.gz', 
    '.pdf', '.exe', '.dll', '.so', '.dylib', '.obj', '.bin', '.db', '.dat'
}

MAX_FILE_SIZE = 10 * 1024 * 1024 
BINARY_CHECK_BYTES = 1024 
NULL_BYTE_THRESHOLD = 5 

# === FUNÇÕES AUXILIARES ===

def natural_sort_key(s: str) -> List[Any]:
    """Chave de ordenação natural."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def is_binary_by_content_check(file_path: str) -> bool:
    """Heurística: Checa por bytes nulos."""
    try:
        if os.path.getsize(file_path) == 0:
            return False 
        
        with open(file_path, 'rb') as f:
            data = f.read(BINARY_CHECK_BYTES)
            
        null_byte_count = data.count(b'\x00')
        
        if null_byte_count > NULL_BYTE_THRESHOLD:
            return True
        
        return False

    except IOError:
        return True
    

def _get_common_root(paths: List[str]) -> str:
    """
    Encontra o diretório pai mais comum entre todos os caminhos de entrada (LCA).
    Corrigido para reconstruir caminhos absolutos corretamente em Windows.
    """
    if not paths:
        return ""
    
    # 1. Normaliza e filtra caminhos existentes
    normalized_paths = [os.path.abspath(p) for p in paths]
    valid_paths = [p for p in normalized_paths if os.path.exists(p)]
    
    if not valid_paths:
        return ""
        
    # 2. Divide em componentes
    # Ex: 'C:\Users\Foo' -> ['C:', 'Users', 'Foo'] no Windows
    components = [p.split(os.path.sep) for p in valid_paths]

    if not components:
        return ""
        
    # 3. Encontra o prefixo comum
    common_prefix_list = os.path.commonprefix(components)
    
    # 4. Reconstrói o caminho raiz CORRETAMENTE
    if not common_prefix_list:
        # Se for absoluto, retorna a raiz do SO (ex: '/' ou 'C:\')
        if os.path.isabs(valid_paths[0]):
            return os.path.abspath(os.path.sep)
        return ""

    if common_prefix_list[0].endswith(':') and os.name == 'nt': 
        # CORREÇÃO PARA WINDOWS: Reconstrói a partir do drive letter garantindo a barra de separação (Ex: 'C:' + '\' + 'Users')
        if len(common_prefix_list) == 1:
            root_path = common_prefix_list[0] + os.path.sep
        else:
            root_path = common_prefix_list[0] + os.path.sep + os.path.join(*common_prefix_list[1:])
    else:
        # Unix/Linux ou outros caminhos que os.path.join trata corretamente
        root_path = os.path.join(*common_prefix_list)

    # Garante que o root_path seja o diretório pai se o LCA for um arquivo
    if os.path.isfile(root_path):
        root_path = os.path.dirname(root_path)
    
    # Normaliza (remove barras duplas, barras finais, etc.)
    root_path = os.path.normpath(root_path)

    return root_path

# === TreeNode Definition ===
class TreeNode:
    """Classe para representar um nó na estrutura de diretórios do projeto."""
    def __init__(self, name, full_path, is_dir, size_bytes=0, is_text=False, token_count=0, total_recursive_tokens=0, selection_state=0):
        self.name = name
        self.full_path = full_path
        self.is_dir = is_dir
        self.size_bytes = size_bytes
        self.is_text = is_text
        self.token_count = token_count
        self.total_recursive_tokens = total_recursive_tokens
        self.selection_state = selection_state # 0: ignorado, 1: parcial, 2: selecionado
        self.children: List['TreeNode'] = []
        self.parent: Optional['TreeNode'] = None

    def add_child(self, child: 'TreeNode'):
        self.children.append(child)
        child.parent = self
        
    def calculate_recursive_tokens(self) -> int:
        """Calcula e atualiza o total de tokens do nó e seus filhos."""
        total_tokens = self.token_count if not self.is_dir and self.is_text else 0
        for child in self.children:
            total_tokens += child.calculate_recursive_tokens()
        self.total_recursive_tokens = total_tokens
        return total_tokens

# ===============================================

def scan_directory(paths: List[str], cancel_flag: threading.Event, progress_callback: callable) -> Dict[str, Any]:
    """
    Escaneia múltiplos arquivos e diretórios (suporte a D&D e seleção múltipla),
    tratando-os como um projeto composto.
    """
    if not paths:
        return {'root_node': None, 'file_contents': {}, 'text_file_paths': set(), 'all_extensions': set(), 'total_files': 0, 'root_path': "", 'node_map': {}}

    file_contents: Dict[str, str] = {}
    text_file_paths: List[str] = []
    all_extensions: Set[str] = set()
    
    # 1. Determina a Raiz do Projeto Composto (LCA)
    root_path = _get_common_root(paths)
    
    # Define o nome da raiz. 
    # Se root_path for a raiz do SO (ex: '/' ou 'C:\'), usa um nome descritivo.
    if root_path == os.path.abspath(os.path.sep) or (os.name == 'nt' and len(root_path) == 3 and root_path[1] == ':'):
        root_node_name = "Projeto Composto (Raiz)"
    else:
        root_node_name = os.path.basename(root_path) 
        
    root_node = TreeNode(root_node_name, root_path, True, selection_state=2)
    node_map: Dict[str, TreeNode] = {root_path: root_node}
    
    # 2. Coleta todos os arquivos recursivamente
    all_items: List[str] = []
    
    for input_path in paths:
        input_path = os.path.abspath(input_path)
        
        if not os.path.exists(input_path):
            continue

        if os.path.isdir(input_path):
            # Escaneia pastas recursivamente
            for dirpath, dirnames, filenames in os.walk(input_path):
                # Exclui pastas irrelevantes
                dirnames[:] = [d for d in dirnames if not (d.startswith('.') or d in ('__pycache__', 'node_modules', 'dist', 'build', 'target', 'venv', 'env'))]
                for f in filenames:
                    all_items.append(os.path.join(dirpath, f))
        
        elif os.path.isfile(input_path):
            # Adiciona arquivos diretamente
            all_items.append(input_path)

    total_files = len(all_items)
    
    # 3. Segunda Passagem: Criar a árvore, ler o conteúdo e preencher node_map
    current_scanned_count = 0
    
    for full_path in all_items:
        if cancel_flag.is_set(): break
            
        current_scanned_count += 1
        is_text_file = False
        size = 0 
        child_node_size = 0 
        
        try:
            size = os.path.getsize(full_path)
            item_name = os.path.basename(full_path)
            
            _, ext = os.path.splitext(item_name)
            ext = ext.lower()
            all_extensions.add(ext)
            
            # Checagens de Binário e Leitura de Conteúdo (Lógica mantida)
            is_known_text = ext in TEXT_EXTENSIONS
            is_known_binary = ext in IGNORED_BINARIES or size > MAX_FILE_SIZE
            
            if not is_known_binary:
                if is_known_text or not is_binary_by_content_check(full_path):
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        is_text_file = True
                        file_contents[full_path] = content
                        text_file_paths.append(full_path)
                        child_node_size = len(content.encode('utf-8'))
                        
                    except UnicodeDecodeError:
                        is_text_file = False 
                    except Exception:
                        is_text_file = False 

            # Cria o nó do arquivo
            child_node = TreeNode(item_name, full_path, False, 
                                  size_bytes=size if not is_text_file else child_node_size, 
                                  is_text=is_text_file, 
                                  selection_state=2 if is_text_file else 0)
            
            # --- Criação da Hierarquia (Relativa à nova root_path) ---
            # Determina o caminho relativo a partir da raiz comum
            if full_path == root_path:
                path_parts = [item_name]
            elif root_path == os.path.dirname(full_path):
                path_parts = [item_name]
            else:
                # Usa relpath para obter a lista de diretórios intermediários
                path_parts = os.path.relpath(full_path, root_path).split(os.path.sep)
                
            # Filtra componentes indesejados (como '.') que relpath pode gerar
            path_parts = [p for p in path_parts if p and p != '.']
            
            current_path_segment = root_path
            current_parent_node = root_node
            
            # Navega pelos diretórios intermediários e os cria se necessário
            for part in path_parts[:-1]:
                current_path_segment = os.path.join(current_path_segment, part)
                # Garante que o path para o nó de diretório não é o path da raiz em si
                if current_path_segment == root_path: 
                    continue
                    
                if current_path_segment not in node_map:
                    # Cria nó de diretório intermediário
                    new_dir_node = TreeNode(part, current_path_segment, True, selection_state=2)
                    current_parent_node.add_child(new_dir_node)
                    node_map[current_path_segment] = new_dir_node
                    current_parent_node = new_dir_node
                else:
                    current_parent_node = node_map[current_path_segment]
                    
            # Adiciona o nó do arquivo final
            current_parent_node.add_child(child_node)
            node_map[full_path] = child_node

        except OSError:
            pass 
        finally:
            progress_callback(current_scanned_count, total_files, full_path)

    # 4. Contagem Inicial de Tokens
    for path, content in file_contents.items():
        node = node_map.get(path)
        if node and node.is_text:
            tokens, _ = count_tokens(content)
            node.token_count = tokens
            
    text_file_paths_set = {path for path in file_contents.keys() if node_map.get(path) and node_map.get(path).is_text}
    
    return {
        'root_node': root_node,
        'file_contents': file_contents,
        'text_file_paths': text_file_paths_set,
        'all_extensions': all_extensions,
        'total_files': total_files,
        'root_path': root_path, 
        'node_map': node_map
    }