import os
import re
import threading
import traceback
from typing import Dict, List, Optional, Tuple, Set, Any, Callable

# Constante de segurança para evitar a leitura de arquivos gigantes
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def natural_sort_key(s: str) -> List[Any]:
    """
    Retorna uma chave para ordenação natural (ex: 'item2' antes de 'item10').
    Converte a string em uma lista de strings e números para ordenação.
    
    Args:
        s: A string a ser convertida em chave de ordenação natural.
        
    Returns:
        Uma lista com números inteiros e strings em minúsculas para ordenação natural.
        
    Exemplo:
        >>> natural_sort_key("file10.txt")
        ['file', 10, '.txt']
        >>> natural_sort_key("file2.txt")
        ['file', 2, '.txt']
    """
    return [int(text) if text.isdigit() else text.lower() 
            for text in re.split(r'(\d+)', s)]


class TreeNode:
    """
    Classe para representar nós da árvore de diretórios.
    Cada nó pode ser um arquivo ou diretório, com suporte a conteúdo e metadados.
    
    Attributes:
        name: Nome do arquivo ou diretório.
        full_path: Caminho completo (absoluto) do arquivo/diretório.
        children: Lista de nós filhos (TreeNode).
        is_dir: Booleano indicando se o nó é um diretório.
        size_bytes: Tamanho do arquivo em bytes (0 para diretórios).
        content: Conteúdo do arquivo como string (None se não lido ou diretório).
        token_count: Número de tokens do conteúdo (calculado posteriormente).
        extension: Extensão do arquivo (ex: '.py', '.txt').
        is_scanned: Booleano indicando se o arquivo foi processado.
        is_text: Booleano indicando se o arquivo foi lido como texto.
    """
    
    def __init__(self, name: str, full_path: str):
        """
        Inicializa um nó da árvore.
        
        Args:
            name: Nome do item (arquivo ou diretório).
            full_path: Caminho completo (absoluto) do item.
        """
        self.name: str = name
        self.full_path: str = full_path
        self.children: List['TreeNode'] = []
        self.is_dir: bool = os.path.isdir(full_path)
        self.size_bytes: int = 0
        self.content: Optional[str] = None
        self.token_count: Optional[int] = None
        self.extension: str = ''
        self.is_scanned: bool = False
        self.is_text: bool = False

    def add_child(self, child: 'TreeNode') -> None:
        """
        Adiciona um nó filho e mantém a lista de filhos ordenada naturalmente.
        Diretórios aparecem antes de arquivos na ordenação.
        
        Args:
            child: O nó filho a ser adicionado.
        """
        self.children.append(child)
        # depois ordenação natural por nome
        self.children.sort(key=lambda x: (not x.is_dir, natural_sort_key(x.name)))

    def get_file_paths(self) -> List[str]:
        """
        Retorna uma lista plana de todos os caminhos de arquivos neste nó e seus filhos.
        Ignora diretórios.
        
        Returns:
            Lista com caminhos absolutos de todos os arquivos no subárvore.
        """
        paths: List[str] = []
        if not self.is_dir:
            paths.append(self.full_path)
        for child in self.children:
            paths.extend(child.get_file_paths())
        return paths

    def __repr__(self) -> str:
        """Representação em string do nó para debug."""
        return f"TreeNode(name='{self.name}', is_dir={self.is_dir}, path='{self.full_path}')"


def read_file_content(file_path: str) -> Tuple[Optional[str], int]:
    """
    Lê o conteúdo de um arquivo de forma segura.
    Suporta múltiplas codificações com fallback e verifica tamanho máximo.
    
    Args:
        file_path: Caminho completo do arquivo a ser lido.
        
    Returns:
        Uma tupla (conteúdo, tamanho_bytes) onde:
        - conteúdo: String com o conteúdo do arquivo, ou None se falha na leitura/tamanho excedido.
        - tamanho_bytes: Tamanho do arquivo em bytes (sempre retornado).
        
    Raises:
        Nenhuma exceção é lançada; erros são impressos e None é retornado como conteúdo.
    """
    try:
        size_bytes = os.path.getsize(file_path)
    except OSError as e:
        print(f"ERRO ao obter tamanho do arquivo '{file_path}': {e}")
        return None, 0

    if size_bytes > MAX_FILE_SIZE_BYTES:
        print(f"AVISO: Arquivo muito grande ({size_bytes / (1024*1024):.2f} MB) "
              f"para leitura (máximo: {MAX_FILE_SIZE_MB} MB): {file_path}")
        return None, size_bytes

    # Tenta leitura com codificações mais comuns (por ordem de probabilidade)
    encodings = ['utf-8', 'iso-8859-1', 'cp1252', 'utf-16']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            return content, size_bytes
        except (UnicodeDecodeError, LookupError):
            continue  # Tenta próxima codificação
        except Exception as e:
            print(f"ERRO inesperado ao ler '{file_path}' com codificação {encoding}: {e}")
            continue

    # Se todas as codificações falharem
    print(f"ERRO: Não foi possível ler o arquivo '{file_path}' "
          f"com nenhuma das codificações testadas.")
    return None, size_bytes


def scan_directory(
    root_path: str,
    extensions_filter: Optional[Set[str]] = None,
    cancel_flag: Optional[threading.Event] = None,
    progress_callback: Optional[Callable[[str, int, int], None]] = None
) -> Dict[str, Any]:
    """
    Escaneia o diretório raiz, constrói a árvore de nós, lê o conteúdo
    dos arquivos de texto e descobre todas as extensões.
    
    Suporta cancelamento via threading.Event e feedback de progresso via callback.
    
    Args:
        root_path: O caminho do diretório a ser escaneado (deve existir e ser diretório).
        extensions_filter: Conjunto de extensões (ex: {'.py', '.js'}) a processar.
                          Se None, todas as extensões são consideradas.
        cancel_flag: Evento de threading (threading.Event) para interromper o escaneamento.
                    Se None, um novo Event() é criado (sem cancelamento externo).
        progress_callback: Função chamada com (nome_arquivo, arquivos_processados, total_arquivos)
                          para feedback visual do progresso. Se None, sem callback.

    Returns:
        Um dicionário contendo:
        - 'root_node': Nó raiz da árvore de diretórios (TreeNode).
        - 'text_file_paths': Lista de caminhos absolutos dos arquivos de texto lidos.
        - 'file_contents': Mapeamento {caminho_absoluto: conteúdo_string}.
        - 'all_extensions': Conjunto (set) de todas as extensões encontradas.
        - 'cancelled': Booleano indicando se o escaneamento foi cancelado.
        
    Raises:
        FileNotFoundError: Se root_path não existe ou não é um diretório.
        
    Example:
        >>> results = scan_directory('/path/to/project', 
        ...                          extensions_filter={'.py', '.js'},
        ...                          progress_callback=lambda f, c, t: print(f"{c}/{t}: {f}"))
        >>> print(results['all_extensions'])
        {'.py', '.js', '.json', ...}
    """
    # Validações iniciais
    if not os.path.isdir(root_path):
        raise FileNotFoundError(f"O caminho não é um diretório válido: {root_path}")

    # Inicializa cancel_flag se não fornecido
    if cancel_flag is None:
        cancel_flag = threading.Event()

    # Inicialização dos coletores de resultados
    all_extensions: Set[str] = set()
    text_file_paths: List[str] = []
    file_contents: Dict[str, str] = {}

    # Cria nó raiz da árvore
    root_node = TreeNode(
        os.path.basename(root_path) or root_path,
        os.path.abspath(root_path)
    )

    # Fila de diretórios para processar (BFS - breadth-first search)
    # Cada item: (caminho_do_diretorio, nó_pai)
    queue: List[Tuple[str, TreeNode]] = [(os.path.abspath(root_path), root_node)]

    # Primeira passagem: Contar total de arquivos para a barra de progresso
    total_files = 0
    try:
        for _, _, filenames in os.walk(root_path):
            total_files += len(filenames)
    except Exception as e:
        print(f"AVISO: Erro ao contar arquivos para progresso: {e}")
        total_files = 0  # Se falhar, continua sem progress bar precisa

    files_processed = 0

    # Segunda passagem: Escaneamento real e construção da árvore/leitura de conteúdo
    try:
        while queue:  # Processa enquanto houver diretórios na fila
            if cancel_flag.is_set():
                print("Escaneamento cancelado pelo usuário.")
                break

            current_dir, parent_node = queue.pop(0)  # Remove primeiro (FIFO)

            try:
                # Ordena o conteúdo do diretório para garantir a ordenação natural
                dir_content = sorted(os.listdir(current_dir), key=natural_sort_key)
            except PermissionError as e:
                print(f"AVISO: Permissão negada ao acessar '{current_dir}': {e}")
                continue
            except Exception as e:
                print(f"AVISO: Erro ao listar diretório '{current_dir}': {e}")
                continue

            for item_name in dir_content:
                if cancel_flag.is_set():
                    print("Escaneamento cancelado durante iteração.")
                    break

                full_path = os.path.join(current_dir, item_name)

                # Ignorar links simbólicos para evitar loops infinitos
                if os.path.islink(full_path):
                    continue

                try:
                    if os.path.isdir(full_path):
                        # Cria nó de diretório e adiciona à fila para processamento posterior
                        new_dir_node = TreeNode(item_name, full_path)
                        parent_node.add_child(new_dir_node)
                        queue.append((full_path, new_dir_node))

                    elif os.path.isfile(full_path):
                        files_processed += 1

                        # Extrai e normaliza a extensão
                        _, ext = os.path.splitext(item_name)
                        ext = ext.lower()

                        # Registra a extensão encontrada
                        all_extensions.add(ext)

                        # Verifica se deve processar este arquivo com base no filtro
                        is_allowed_extension = (extensions_filter is None or 
                                               ext in extensions_filter)

                        # Cria nó do arquivo
                        file_node = TreeNode(item_name, full_path)
                        file_node.extension = ext
                        file_node.is_scanned = True

                        if is_allowed_extension:
                            # Lê o conteúdo do arquivo
                            content, size_bytes = read_file_content(full_path)
                            file_node.size_bytes = size_bytes

                            if content is not None:
                                file_node.content = content
                                file_node.is_text = True
                                file_contents[full_path] = content
                                text_file_paths.append(full_path)
                        else:
                            # Arquivo ignorado pelo filtro - ainda registra tamanho
                            try:
                                file_node.size_bytes = os.path.getsize(full_path)
                            except OSError:
                                file_node.size_bytes = 0

                        parent_node.add_child(file_node)

                        # Chama callback para feedback visual de progresso
                        if progress_callback:
                            try:
                                progress_callback(item_name, files_processed, total_files)
                            except Exception as e:
                                print(f"AVISO: Erro no callback de progresso: {e}")

                except Exception as e:
                    print(f"ERRO ao processar item '{full_path}': {e}")
                    continue

            if cancel_flag.is_set():
                break  # Sai do loop se cancelamento foi solicitado

    except Exception as e:
        print(f"ERRO FATAL no escaneamento do diretório: {e}")
        traceback.print_exc()

    return {
        'root_node': root_node,
        'text_file_paths': text_file_paths,
        'file_contents': file_contents,
        'all_extensions': all_extensions,
        'cancelled': cancel_flag.is_set()
    }


if __name__ == '__main__':
    # --- Teste Simples do Módulo Scanner ---
    print("=== Teste do Módulo Scanner ===\n")

    # Teste com diretório atual (substituir por um diretório de teste)
    test_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        results = scan_directory(
            test_dir,
            extensions_filter={'.py'},
            progress_callback=lambda f, c, t: print(f"  {c}/{t}: {f}")
        )

        print(f"\n✓ Escaneamento concluído com sucesso!")
        print(f"  Arquivos de texto encontrados: {len(results['text_file_paths'])}")
        print(f"  Extensões descobertas: {sorted(results['all_extensions'])}")
        print(f"  Cancelado: {results['cancelled']}")

    except FileNotFoundError as e:
        print(f"✗ Erro: {e}")
    except Exception as e:
        print(f"✗ Erro inesperado: {e}")
        traceback.print_exc()
