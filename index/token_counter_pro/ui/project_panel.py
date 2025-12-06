import wx
import os
import threading
from typing import Optional, Dict, Any, TYPE_CHECKING, List, Tuple
from core import natural_sort_key 
from core.scanner import TreeNode 

if TYPE_CHECKING:
    from .frame import TokenCounterFrame

# Constante para arquivos sem extensão (substitui o antigo IGNORED_EXT_KEY para esta função)
NO_EXT_KEY = "<sem_extensão>" 

# ----------------------------------------
# Classes de Abas (Visualização e Análise)
# ----------------------------------------

class ConsolidatedTreeTab(wx.Panel):
    """Aba 1: Resumo Hierárquico (Estilo ASCII tree /a /f)."""
    def __init__(self, parent, project_panel):
        super().__init__(parent)
        self.project_panel = project_panel
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.text_output = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.TE_DONTWRAP)
        
        font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.text_output.SetFont(font)
        
        self.DEFAULT_BG_COLOR = wx.Colour(30, 30, 30)
        self.DEFAULT_FG_COLOR = wx.Colour(220, 220, 220)
        self.HIGHLIGHT_BG_COLOR = wx.Colour(70, 70, 70) 
        
        self.text_output.SetBackgroundColour(self.DEFAULT_BG_COLOR)
        self.text_output.SetForegroundColour(self.DEFAULT_FG_COLOR)
        
        self.highlight_range = (0, 0) 
        
        sizer.Add(self.text_output, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(sizer)

    def update_data(self, root_node: Optional[TreeNode]):
        """Gera a árvore ASCII completa."""
        self.text_output.Clear()
        
        if not root_node:
            self.text_output.SetValue("Nenhum projeto carregado.")
            return

        # 1. Cabeçalho (Raiz)
        root_tokens_str = f"[ {root_node.total_recursive_tokens:>6,} tokens ]"
        root_line = self._format_line(f"{os.path.basename(root_node.full_path)}:.", root_tokens_str)
        self.text_output.AppendText(root_line + "\n")

        # 2. Gera o corpo da árvore recursivamente
        self._write_ascii_tree(root_node, prefix="")

        # Rola para o topo e reseta o destaque
        self.text_output.ShowPosition(0)
        self.highlight_range = (0, 0)

    def _write_ascii_tree(self, node: TreeNode, prefix: str):
        """Função recursiva para desenhar linhas no estilo tree /f."""
        children = sorted(node.children, key=lambda n: (not n.is_dir, natural_sort_key(n.name)))
        
        count = len(children)
        for i, child in enumerate(children):
            is_last = (i == count - 1)
            
            t_val = child.total_recursive_tokens if child.is_dir else child.token_count
            token_str = f"[ {t_val:>6,} tokens ]"

            if child.is_dir:
                connector = "\\---" if is_last else "+---"
                tree_part = f"{prefix}{connector}{child.name}"
                
                line = self._format_line(tree_part, token_str)
                self.text_output.AppendText(line + "\n")
                
                child_prefix = prefix + ("    " if is_last else "|   ")
                self._write_ascii_tree(child, child_prefix)
                
            else:
                # Arquivos
                if node.parent is None:
                    marker = "|   " if not is_last else "    "
                    tree_part = f"{marker}{child.name}"
                else:
                    tree_part = f"{prefix}    {child.name}"
                
                # ADIÇÃO: Marca arquivos que foram ignorados na visualização da árvore
                display_name = child.name
                if not child.is_text:
                    size_str = f"({child.size_bytes:,} bytes)"
                    display_name = f"{child.name} [IGNORADO {size_str}]"


                line = self._format_line(tree_part, token_str, name_override=display_name)
                self.text_output.AppendText(line + "\n")

    def _format_line(self, left_text: str, right_text: str, name_override: str = None) -> str:
        """Cria uma linha com padding de espaços para alinhar os tokens à direita."""
        TARGET_WIDTH = 100 
        
        if name_override:
            original_name = os.path.basename(left_text.split()[-1])
            temp_left_text = left_text.replace(original_name, name_override)
            left_text = temp_left_text

        len_left = len(left_text)
        len_right = len(right_text)
        
        padding_size = max(2, TARGET_WIDTH - len_left - len_right)
        
        padding = " " * padding_size
        
        return f"{left_text}{padding}{right_text}"
        
    def select_path_in_tree(self, path: str, node_map: Dict[str, TreeNode]):
        """Remove o destaque anterior e aplica um novo para o path fornecido."""
        node = node_map.get(path)
        if not node: return

        # 1. Remove o destaque anterior 
        if self.highlight_range[1] > self.highlight_range[0]:
            self.text_output.SetStyle(self.highlight_range[0], self.highlight_range[1], wx.TextAttr(self.DEFAULT_FG_COLOR, self.DEFAULT_BG_COLOR))
        
        # 2. Encontra o texto a ser procurado (Nome do item + Tag de Tokens)
        if node.is_dir:
            t_val = node.total_recursive_tokens
        else:
            t_val = node.token_count
            
        token_str = f"[ {t_val:>6,} tokens ]"
        
        # A busca precisa incluir a tag [IGNORADO] se o arquivo não for de texto
        search_name = node.name
        if not node.is_text and not node.is_dir:
            search_name = f"{node.name} [IGNORADO ({node.size_bytes:,} bytes)]"
        
        search_target = f"{search_name}{token_str}" 
        full_text = self.text_output.GetValue()
        
        # Encontra a posição do início da substring (nome+tokens)
        content_start_pos = full_text.find(search_name)
        
        if content_start_pos == -1:
            self.highlight_range = (0, 0) 
            return 

        # Encontra o início real da linha (depois do '\n' anterior)
        line_start = full_text.rfind('\n', 0, content_start_pos) + 1
        
        # Encontra o fim da linha (próximo '\n' ou fim do texto)
        line_end = full_text.find('\n', content_start_pos)
        if line_end == -1: 
            line_end = len(full_text)
            
        # 3. Aplica o novo destaque
        self.highlight_range = (line_start, line_end)
        
        attr = wx.TextAttr(self.DEFAULT_FG_COLOR, self.HIGHLIGHT_BG_COLOR)
        self.text_output.SetStyle(line_start, line_end, attr)
        
        # 4. Rola para a posição
        self.text_output.ShowPosition(line_start)


class SelectedFilesTab(wx.Panel):
    """Aba 2: Lista de Arquivos (Filtro e Detalhes) com ordenação por coluna. Inclui Ignorados por Extensão real."""
    def __init__(self, parent, project_panel):
        super().__init__(parent)
        self.project_panel = project_panel
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Busca
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        search_sizer.Add(wx.StaticText(self, label="Pesquisar:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.search_ctrl = wx.TextCtrl(self)
        self.search_ctrl.Bind(wx.EVT_TEXT, self.on_search)
        search_sizer.Add(self.search_ctrl, 1, wx.EXPAND)
        sizer.Add(search_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # ListCtrl com colunas 
        self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_HRULES | wx.LC_VRULES | wx.LC_SINGLE_SEL) 
        
        self.list_ctrl.InsertColumn(0, "Nome do Arquivo", width=250)
        self.list_ctrl.InsertColumn(1, "Extensão", width=120) # Aumenta a largura para caber <sem_extensão>
        self.list_ctrl.InsertColumn(2, "Tokens / Status", width=150) 
        self.list_ctrl.InsertColumn(3, "Caminho Completo", width=300)
        
        sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        
        self.lbl_total = wx.StaticText(self, label="Total Arquivos: 0 | Total Tokens do Projeto: 0")
        sizer.Add(self.lbl_total, 0, wx.ALL, 5)
        
        self.SetSizer(sizer)
        
        self.sort_column = 2 
        self.sort_ascending = False 
        self.all_nodes_cache: List[TreeNode] = []
        self.num_text_files = 0
        self.num_ignored_files = 0

        self.list_ctrl.Bind(wx.EVT_LIST_COL_CLICK, self.on_col_click)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_item_activated) 
        
    def on_col_click(self, event: wx.ListEvent):
        """Lida com o clique no cabeçalho da coluna para ordenar."""
        col = event.GetColumn()
        
        if col == self.sort_column:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_column = col
            self.sort_ascending = (col != 2)
            
        self._refresh_list()

    def on_item_activated(self, event):
        """Dispara a prévia ao dar duplo clique/Enter no item da lista."""
        idx = event.GetIndex()
        if idx >= 0 and idx < self.list_ctrl.GetItemCount():
            path = self.current_map[idx]
            self.project_panel.on_file_selected_for_preview(path)

    def update_data(self, all_file_nodes: List[TreeNode], total_proj_tokens: int):
        """Atualiza a lista com base no filtro de busca (Sincronização). Recebe todos os arquivos."""
        self.all_nodes_cache = all_file_nodes 
        self.total_proj_tokens = total_proj_tokens
        
        self.num_text_files = sum(1 for n in all_file_nodes if n.is_text)
        self.num_ignored_files = sum(1 for n in all_file_nodes if not n.is_text)
        
        self._refresh_list()

    def _get_ext_display(self, node: TreeNode) -> str:
        """Retorna a extensão ou a chave <sem_extensão>."""
        _, ext = os.path.splitext(node.name)
        return ext.lower() if ext else NO_EXT_KEY

    def _refresh_list(self):
        term = self.search_ctrl.GetValue().lower()
        self.list_ctrl.Freeze()
        self.list_ctrl.DeleteAllItems()
        
        displayed_nodes = []

        for node in self.all_nodes_cache:
            if term and term not in node.name.lower():
                continue
            displayed_nodes.append(node)

        # --- Lógica de Ordenação ---
        col_map = {
            0: lambda n: natural_sort_key(n.name),
            1: lambda n: self._get_ext_display(n), # Usa a extensão real
            # ORDENAÇÃO DE STATUS: Textos (contagem de tokens) primeiro, depois Ignorados (tamanho)
            2: lambda n: (0 if n.is_text else 1, n.token_count if n.is_text else n.size_bytes),                     
            3: lambda n: n.full_path.lower(),               
        }
        
        sort_key_func = col_map.get(self.sort_column)
        if sort_key_func:
            displayed_nodes.sort(key=sort_key_func, reverse=not self.sort_ascending)
        
        # --- Fim da Lógica de Ordenação ---

        self.current_map = {} 
        for i, node in enumerate(displayed_nodes):
            
            ext_display = self._get_ext_display(node)

            idx = self.list_ctrl.InsertItem(i, node.name) 
            self.list_ctrl.SetItem(idx, 1, ext_display) # Exibe a extensão real ou <sem_extensão>
            
            # MUDANÇA: Exibe tokens OU status de ignorado/binário
            if node.is_text:
                token_display = f"{node.token_count:,}"
                
            else:
                # Exibe o tamanho em bytes para arquivos ignorados/binários
                size_str = f"({node.size_bytes:,} bytes)"
                if node.size_bytes > 1024 * 1024:
                    size_str = f"({(node.size_bytes / (1024 * 1024)):.2f} MB)"
                token_display = f"IGNORADO {size_str}"
                
            self.list_ctrl.SetItem(idx, 2, token_display)
            self.list_ctrl.SetItem(idx, 3, node.full_path)
            self.current_map[i] = node.full_path

        self.list_ctrl.Thaw()
        
        # Atualiza o label com as contagens
        total_files = len(self.all_nodes_cache)
        total_tokens = self.total_proj_tokens
        self.lbl_total.SetLabel(f"Total Arquivos: {total_files:,} ({self.num_text_files:,} Texto + {self.num_ignored_files:,} Ignorados) | Total Tokens: {total_tokens:,}")

    def on_search(self, event):
        self._refresh_list()


class ExtensionFilterTab(wx.Panel):
    """Aba 3: Resumo por Extensões (Visualização e Ordenação). Cada extensão não lida individualmente."""
    def __init__(self, parent, project_panel):
        super().__init__(parent)
        self.project_panel = project_panel
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SINGLE_SEL)
        
        self.list_ctrl.InsertColumn(0, "Extensão / Status", width=150) 
        self.list_ctrl.InsertColumn(1, "Arquivos (Contagem)", width=150)
        self.list_ctrl.InsertColumn(2, "Tokens Totais", width=150)
        
        sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)
        
        self.sort_column = 2 
        self.sort_ascending = False 
        self.cached_summary_list: List[Tuple[str, Dict[str, Any]]] = []

        self.list_ctrl.Bind(wx.EVT_LIST_COL_CLICK, self.on_col_click)
        
    def on_col_click(self, event: wx.ListEvent):
        """Lida com o clique no cabeçalho da coluna para ordenar."""
        col = event.GetColumn()
        
        if col == self.sort_column:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_column = col
            self.sort_ascending = (col != 2) # Tokens: decrescente por padrão
            
        self._refresh_list()

    def update_data(self, extension_summary: Dict[str, Dict[str, Any]]):
        """Recebe o resumo, armazena em cache e chama a atualização da lista."""
        self.cached_summary_list = list(extension_summary.items())
        
        self._refresh_list()

    def _refresh_list(self):
        """Aplica a ordenação e popula o ListCtrl."""
        self.list_ctrl.Freeze()
        self.list_ctrl.DeleteAllItems()

        # Remove a lógica de tratamento especial do [IGNORADO]
        col_map = {
            0: lambda item: item[0],           
            1: lambda item: item[1]['count'],  
            2: lambda item: item[1]['tokens'], 
        }
        
        sort_key_func = col_map.get(self.sort_column)

        if sort_key_func:
            # Ordena todos os itens, incluindo <sem_extensão>
            sorted_exts = sorted(self.cached_summary_list, 
                                 key=sort_key_func, 
                                 reverse=not self.sort_ascending)
        else:
            sorted_exts = self.cached_summary_list

        for i, (ext, data) in enumerate(sorted_exts):
            idx = self.list_ctrl.InsertItem(i, ext)
            self.list_ctrl.SetItem(idx, 1, f"{data['count']:,}")
            
            token_display = f"{data['tokens']:,}"
            
            # Opção: colorir extensões com 0 tokens para destaque visual (opcional, mas útil)
            if data['tokens'] == 0:
                self.list_ctrl.SetItemTextColour(idx, wx.Colour(255, 100, 100)) # Vermelho suave
            else:
                self.list_ctrl.SetItemTextColour(idx, self.list_ctrl.GetForegroundColour())

            self.list_ctrl.SetItem(idx, 2, token_display)
            
        self.list_ctrl.Thaw()


class FilePreviewTab(wx.Panel):
    # ... (Sem alterações necessárias nesta classe, pois ela já lida com o status de binário/ignorado com base em node.is_text)
    # ... (Mantenha o conteúdo da classe FilePreviewTab do código anterior)
    
    """Aba 4: Prévia (Com suporte a carregamento assíncrono e binário)."""
    def __init__(self, parent, project_panel):
        super().__init__(parent)
        self.project_panel = project_panel
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.lbl_info = wx.StaticText(self, label="Selecione um arquivo para ver a prévia.")
        sizer.Add(self.lbl_info, 0, wx.EXPAND | wx.ALL, 5)
        
        self.preview_text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        
        self.preview_text.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.preview_text.SetBackgroundColour(wx.Colour(30, 30, 30))
        self.preview_text.SetForegroundColour(wx.Colour(220, 220, 220))
        
        sizer.Add(self.preview_text, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)
    
    def update_status_loading(self, path: str, tokens: int):
        """Mostra status de carregamento para arquivos de texto grandes."""
        file_name = os.path.basename(path)
        self.lbl_info.SetLabel(f"Carregando {file_name} ({tokens:,} Tokens)...")
        self.preview_text.SetValue("[ Carregando conteúdo em segundo plano... Por favor, aguarde. ]")
        
    def update_status_binary(self, path: str, size_bytes: int):
        """Mostra status para arquivos não-texto (binários ou ignorados)."""
        file_name = os.path.basename(path)
        
        size_str = f"{size_bytes:,} bytes"
        if size_bytes > 1024 * 1024:
             size_str = f"{(size_bytes / (1024 * 1024)):.2f} MB"
             
        self.lbl_info.SetLabel(f"{file_name} | Arquivo Binário/Ignorado (Tamanho: {size_str})")
        self.preview_text.SetValue("Este arquivo **não** é um arquivo de texto rastreável, foi ignorado (extensão/tamanho) ou o processo de leitura falhou.\n\n***O conteúdo não está disponível na prévia.***")

    def update_preview_content(self, path: str, content: str, tokens: int):
        """Recebe o resultado assíncrono e atualiza a prévia."""
        file_name = os.path.basename(path)
        self.lbl_info.SetLabel(f"{file_name} | {tokens:,} Tokens")
        
        TRUNCATE_LIMIT = 20000 
        disp = content[:TRUNCATE_LIMIT] + (f"\n\n[... Conteúdo truncado após {TRUNCATE_LIMIT} caracteres para performance e estabilidade da UI ...]" if len(content) > TRUNCATE_LIMIT else "")
        self.preview_text.SetValue(disp)

# MUDANÇA: PathDropTarget para aceitar MÚLTIPLOS caminhos (arquivos e pastas)
class PathDropTarget(wx.FileDropTarget):
    def __init__(self, panel: 'ProjectPanel'): 
        super().__init__()
        self.panel = panel
    def OnDropFiles(self, x: int, y: int, filenames: list[str]) -> bool:
        if filenames: 
            self.panel.on_drop_path(filenames) # Passa a lista completa
            return True
        return False


class ProjectPanel(wx.Panel):
    """Painel Principal: Orquestra a visualização e filtragem."""
    def __init__(self, parent: wx.Notebook, frame: 'TokenCounterFrame'):
        super().__init__(parent)
        self.frame = frame 
        
        self.root_path: Optional[str] = None
        self.root_node: Optional[TreeNode] = None
        self.file_contents: Dict[str, str] = {} 
        self.node_map: Dict[str, TreeNode] = {} 
        self.all_files: List[TreeNode] = [] 
        self.all_text_files: List[TreeNode] = [] 
        self.extension_map: Dict[str, List[TreeNode]] = {} 
        
        self._setup_ui()
        self._setup_bindings()
        self.SetDropTarget(PathDropTarget(self))

    def _setup_ui(self):
        self.splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE | wx.SP_3DSASH)
        
        # --- PAINEL LATERAL (EXPLORER) ---
        left_panel = wx.Panel(self.splitter)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Área de Ação Superior
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # O botão agora deve disparar um diálogo que suporta MULTI-SELEÇÃO de arquivos/pastas (a ser implementado em frame.py)
        self.btn_open = wx.Button(left_panel, label="Abrir Arquivo(s)/Pasta") 
        self.btn_clear = wx.Button(left_panel, label="Limpar")
        btn_sizer.Add(self.btn_open, 1, wx.RIGHT, 2)
        btn_sizer.Add(self.btn_clear, 0)
        left_sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        self.tree_ctrl = wx.TreeCtrl(left_panel, style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_BUTTONS | wx.TR_LINES_AT_ROOT) 
        self.tree_ctrl.SetBackgroundColour(wx.Colour(30, 30, 30))
        self.tree_ctrl.SetForegroundColour(wx.Colour(220, 220, 220))
        
        left_sizer.Add(self.tree_ctrl, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        
        # Status
        self.progress_bar = wx.Gauge(left_panel, range=100, style=wx.GA_HORIZONTAL)
        left_sizer.Add(self.progress_bar, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        self.status_text = wx.StaticText(left_panel, label="Aguardando...")
        left_sizer.Add(self.status_text, 0, wx.EXPAND | wx.ALL, 5)
        
        left_panel.SetSizer(left_sizer)

        # --- PAINEL DIREITO (ABAS) ---
        right_panel = wx.Panel(self.splitter)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.notebook = wx.Notebook(right_panel)
        self.tab_tree = ConsolidatedTreeTab(self.notebook, self)
        self.tab_files = SelectedFilesTab(self.notebook, self)
        self.tab_exts = ExtensionFilterTab(self.notebook, self)
        self.tab_prev = FilePreviewTab(self.notebook, self)
        
        self.notebook.AddPage(self.tab_tree, "Resumo da Árvore")
        self.notebook.AddPage(self.tab_files, "Lista de Arquivos (Filtro)")
        self.notebook.AddPage(self.tab_exts, "Resumo por Extensões")
        self.notebook.AddPage(self.tab_prev, "Prévia")
        
        right_sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)
        right_panel.SetSizer(right_sizer)

        self.splitter.SplitVertically(left_panel, right_panel, 300)
        self.splitter.SetMinimumPaneSize(200)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.splitter, 1, wx.EXPAND)
        self.SetSizer(main_sizer)

    def _setup_bindings(self):
        # self.frame.on_open_folder (frame.py) agora deve lidar com a abertura multi-seleção
        self.btn_open.Bind(wx.EVT_BUTTON, self.frame.on_open_folder) 
        self.btn_clear.Bind(wx.EVT_BUTTON, self.frame.on_clear_all)
        
        self.tree_ctrl.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_tree_selection_changed)

    def on_drop_path(self, paths: List[str]):
        """Lida com a entrada de caminhos múltiplos (arquivos e/ou pastas) por drag and drop."""
        if paths: 
            # Chama a função de scan com a lista completa de caminhos
            self.frame.start_initial_scan(paths) 
        
    def on_tree_selection_changed(self, event):
        """
        Lida com o clique simples na árvore lateral.
        Ação: Mudar para a aba Resumo da Árvore e destacar o item selecionado.
        """
        item = event.GetItem()
        if item.IsOk():
            path = self.tree_ctrl.GetItemData(item)
            
            self.notebook.SetSelection(0) 
            
            if path in self.node_map:
                self.tab_tree.select_path_in_tree(path, self.node_map)

    def on_file_selected_for_preview(self, path: str):
        """Orquestra o carregamento assíncrono do conteúdo do arquivo na aba de prévia (acessado por duplo-clique)."""
        node = self.node_map.get(path)
        if not node: return

        self.notebook.SetSelection(3) 
        
        if not node.is_text:
            self.tab_prev.update_status_binary(path, node.size_bytes)
            return

        self.tab_prev.update_status_loading(path, node.token_count)

        threading.Thread(target=self._load_preview_async, args=(path, node.token_count), daemon=True).start()

    def _load_preview_async(self, path: str, tokens: int):
        """Função rodando em thread para carregar e truncar o preview de arquivos grandes."""
        content = self.file_contents.get(path, "") 
        
        wx.CallAfter(self.tab_prev.update_preview_content, path, content, tokens)

    # --- Inicialização e Atualização de Dados ---

    def handle_scan_result(self, results: Dict[str, Any]):
        """
        Processa o resultado do scan e calcula os totais (Sincronização).
        MUDANÇA: Usa a extensão real ou NO_EXT_KEY para agrupamento, sem o [IGNORADO] global.
        """
        self.root_path = results['root_path']
        self.root_node = results['root_node']
        self.file_contents = results['file_contents']
        self.node_map = results['node_map']
        
        self.all_files = [] 
        self.all_text_files = [] 
        self.extension_map = {}
        
        # Mapeia arquivos e extensões
        for path, node in self.node_map.items():
            if node.is_dir: continue 

            self.all_files.append(node)
            
            file_name, ext = os.path.splitext(node.name)
            ext = ext.lower()
            
            # NOVO: Usa a extensão real, ou <sem_extensão>
            map_key = ext if ext else NO_EXT_KEY 

            if map_key not in self.extension_map: self.extension_map[map_key] = []
            self.extension_map[map_key].append(node)

            if node.is_text: 
                self.all_text_files.append(node)
        
        self.build_visual_tree()
        self.update_all_views()
        
        self.progress_bar.SetValue(0)
        self.status_text.SetLabel(f"Pronto. Projeto com {len(self.all_files):,} arquivos ({len(self.all_text_files):,} de texto).")

    def build_visual_tree(self):
        """Constrói a árvore lateral baseada no root_node."""
        self.tree_ctrl.DeleteAllItems()
        if not self.root_node: return
        
        # MUDANÇA: Se o root_node for um diretório raiz virtual (quando há múltiplos inputs), 
        # a exibição pode ser ajustada para "Múltiplos Itens Selecionados" ou o nome do diretório raiz.
        
        root_item = self.tree_ctrl.AddRoot(os.path.basename(self.root_path))
        self.tree_ctrl.SetItemData(root_item, self.root_path)
        self._build_tree_recursive(root_item, self.root_node)
        self.tree_ctrl.Expand(root_item)

    def _build_tree_recursive(self, parent_item, node):
        sorted_children = sorted(node.children, key=lambda n: (not n.is_dir, natural_sort_key(n.name)))
        for child in sorted_children:
            display_name = child.name
            
            if not child.is_dir and not child.is_text:
                size_str = f"({(child.size_bytes / (1024 * 1024)):.2f}MB)" if child.size_bytes > 1024*1024 else f"({child.size_bytes:,}B)"
                display_name = f"{child.name} [IGNORADO {size_str}]"
            
            new_item = self.tree_ctrl.AppendItem(parent_item, display_name)
            self.tree_ctrl.SetItemData(new_item, child.full_path)
            
            if child.is_dir:
                self._build_tree_recursive(new_item, child)

    def update_all_views(self):
        """Calcula a soma total e atualiza todas as abas."""
        if not self.root_node: return
        
        self.root_node.calculate_recursive_tokens() 
        total_proj_tokens = self.root_node.total_recursive_tokens

        # 1. Resumo extensões
        ext_summary = {}
        for ext, nodes in self.extension_map.items():
            # A soma de tokens é calculada apenas para arquivos de texto (token_count > 0).
            tot = sum(n.token_count for n in nodes) 
            ext_summary[ext] = {'count': len(nodes), 'tokens': tot}

        # 2. Atualizar Abas
        self.tab_tree.update_data(self.root_node)
        self.tab_files.update_data(self.all_files, total_proj_tokens) 
        self.tab_exts.update_data(ext_summary)

    def clear_all_project_data(self):
        """Limpa todo o estado do projeto."""
        self.root_path = None
        self.root_node = None
        self.file_contents.clear()
        self.node_map.clear()
        self.all_files.clear() 
        self.all_text_files.clear()
        self.extension_map.clear()
        
        self.tree_ctrl.DeleteAllItems()
        self.tab_tree.update_data(None)
        self.tab_files.update_data([], 0)
        self.tab_exts.update_data({})
        self.tab_prev.preview_text.Clear()
        self.tab_prev.lbl_info.SetLabel("Selecione um arquivo para ver a prévia.")
        self.progress_bar.SetValue(0)
        self.status_text.SetLabel("Aguardando...")