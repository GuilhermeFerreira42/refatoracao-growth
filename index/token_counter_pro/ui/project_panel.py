import wx
import os
import threading
from typing import Optional, Dict, Any, TYPE_CHECKING, List, Tuple
from core import natural_sort_key 
from core.scanner import TreeNode 

if TYPE_CHECKING:
    from .frame import TokenCounterFrame

# ----------------------------------------
# Classes de Abas (Visualização e Análise)
# ----------------------------------------

class ConsolidatedTreeTab(wx.Panel):
    """Aba 1: Resumo Hierárquico (Estilo ASCII tree /a /f)."""
    def __init__(self, parent, project_panel):
        super().__init__(parent)
        self.project_panel = project_panel
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # TextCtrl ReadOnly com fonte monoespaçada para garantir alinhamento ASCII
        self.text_output = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2 | wx.TE_DONTWRAP)
        
        # Configura fonte Courier New ou similar (monoespaçada)
        font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.text_output.SetFont(font)
        
        # Fundo escuro leve para contraste profissional (opcional, remova se preferir nativo)
        self.text_output.SetBackgroundColour(wx.Colour(30, 30, 30))
        self.text_output.SetForegroundColour(wx.Colour(220, 220, 220))
        
        sizer.Add(self.text_output, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(sizer)

    def update_data(self, root_node: Optional[TreeNode]):
        """Gera a árvore ASCII completa."""
        self.text_output.Clear()
        
        if not root_node:
            self.text_output.SetValue("Nenhum projeto carregado.")
            return

        # 1. Cabeçalho (Raiz)
        # Formata o total da raiz
        root_tokens_str = f"[ {root_node.total_recursive_tokens:>6,} tokens ]"
        
        # Cria a linha inicial: C:. ......... [ xxx tokens ]
        root_line = self._format_line(f"{os.path.basename(root_node.full_path)}:.", root_tokens_str)
        self.text_output.AppendText(root_line + "\n")

        # 2. Gera o corpo da árvore recursivamente
        self._write_ascii_tree(root_node, prefix="")

        # Rola para o topo
        self.text_output.ShowPosition(0)

    def _write_ascii_tree(self, node: TreeNode, prefix: str):
        """Função recursiva para desenhar linhas no estilo tree /f."""
        # Ordena: Pastas primeiro, depois arquivos
        children = sorted(node.children, key=lambda n: (not n.is_dir, natural_sort_key(n.name)))
        
        count = len(children)
        for i, child in enumerate(children):
            is_last = (i == count - 1)
            
            # --- Prepara a string de tokens ---
            t_val = child.total_recursive_tokens if child.is_dir else child.token_count
            token_str = f"[ {t_val:>6,} tokens ]"

            if child.is_dir:
                connector = "\\---" if is_last else "+---"
                tree_part = f"{prefix}{connector}{child.name}"
                
                # Escreve a linha da pasta
                line = self._format_line(tree_part, token_str)
                self.text_output.AppendText(line + "\n")
                
                # Calcula o prefixo para os filhos desta pasta
                child_prefix = prefix + ("    " if is_last else "|   ")
                self._write_ascii_tree(child, child_prefix)
                
            else:
                # Arquivos
                if node.parent is None: # Se filho direto da raiz
                    marker = "|   " if not is_last else "    "
                    tree_part = f"{marker}{child.name}"
                else:
                    # Dentro de subpastas, apenas o prefixo + indentação (4 espaços)
                    tree_part = f"{prefix}    {child.name}"

                line = self._format_line(tree_part, token_str)
                self.text_output.AppendText(line + "\n")
                
            # Adiciona linha vazia se for uma pasta não-vazia e não for o último item
            # Removido para simplificar o ASCII tree
            # if child.is_dir and child.children and not is_last:
            #     self.text_output.AppendText(f"{prefix}|\n")

    def _format_line(self, left_text: str, right_text: str) -> str:
        """Cria uma linha com padding de espaços para alinhar os tokens à direita."""
        # Largura alvo para o alinhamento dos tokens 
        TARGET_WIDTH = 100 
        
        len_left = len(left_text)
        len_right = len(right_text)
        
        # Garante pelo menos 2 espaços de separação
        padding_size = max(2, TARGET_WIDTH - len_left - len_right)
        
        padding = " " * padding_size
        
        return f"{left_text}{padding}{right_text}"

class SelectedFilesTab(wx.Panel):
    """Aba 2: Lista de Arquivos (Filtro e Detalhes) com ordenação por coluna."""
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

        # ListCtrl com colunas (apenas visualização)
        self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_HRULES | wx.LC_VRULES | wx.LC_SINGLE_SEL) 
        
        self.list_ctrl.InsertColumn(0, "Nome do Arquivo", width=250)
        self.list_ctrl.InsertColumn(1, "Extensão", width=80)
        self.list_ctrl.InsertColumn(2, "Tokens", width=100)
        self.list_ctrl.InsertColumn(3, "Caminho Completo", width=300)
        
        sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        
        self.lbl_total = wx.StaticText(self, label="Total Arquivos: 0 | Total Tokens do Projeto: 0")
        sizer.Add(self.lbl_total, 0, wx.ALL, 5)
        
        self.SetSizer(sizer)
        
        # Variáveis de estado de ordenação
        self.sort_column = 0 # Padrão: Nome do Arquivo
        self.sort_ascending = True # Padrão: Crescente
        self.all_nodes_cache: List[TreeNode] = []

        # Binding para clique na coluna e Prévia
        self.list_ctrl.Bind(wx.EVT_LIST_COL_CLICK, self.on_col_click)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected) 

    def on_col_click(self, event: wx.ListEvent):
        """Lida com o clique no cabeçalho da coluna para ordenar."""
        col = event.GetColumn()
        
        if col == self.sort_column:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_column = col
            self.sort_ascending = True # Volta para Crescente ao mudar de coluna
            
        self._refresh_list()


    def update_data(self, all_file_nodes: List[TreeNode], total_proj_tokens: int):
        """Atualiza a lista com base no filtro de busca."""
        # Apenas arquivos de texto devem ser exibidos
        self.all_nodes_cache = [n for n in all_file_nodes if n.is_text]
        self.total_proj_tokens = total_proj_tokens
        self._refresh_list()

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
            # Chave 0: Nome (usa natural_sort_key)
            1: lambda n: os.path.splitext(n.name)[1].lower(), # Extensão
            2: lambda n: n.token_count,                       # Tokens (Numérico)
            3: lambda n: n.full_path.lower(),                 # Caminho Completo
        }
        
        if self.sort_column == 0:
            # Ordenação natural para Nome do Arquivo
            displayed_nodes.sort(key=lambda n: natural_sort_key(n.name), reverse=not self.sort_ascending)
        else:
            sort_key_func = col_map.get(self.sort_column)
            if sort_key_func:
                displayed_nodes.sort(key=sort_key_func, reverse=not self.sort_ascending)
        # --- Fim da Lógica de Ordenação ---

        for i, node in enumerate(displayed_nodes):
            _, ext = os.path.splitext(node.name)

            idx = self.list_ctrl.InsertItem(i, node.name) # Coluna 0
            self.list_ctrl.SetItem(idx, 1, ext)
            self.list_ctrl.SetItem(idx, 2, f"{node.token_count:,}")
            self.list_ctrl.SetItem(idx, 3, node.full_path)
        
        self.current_map = {i: node.full_path for i, node in enumerate(displayed_nodes)}

        self.list_ctrl.Thaw()
        self.lbl_total.SetLabel(f"Total Arquivos: {len(self.all_nodes_cache):,} | Total Tokens do Projeto: {self.total_proj_tokens:,}")

    def on_search(self, event):
        self._refresh_list()

    def on_item_selected(self, event):
        """Dispara a prévia ao selecionar um item na lista."""
        idx = event.GetIndex()
        if idx in self.current_map:
            path = self.current_map[idx]
            self.project_panel.on_file_selected_for_preview(path)


class ExtensionFilterTab(wx.Panel):
    """Aba 3: Resumo por Extensões (Visualização e Ordenação)."""
    def __init__(self, parent, project_panel):
        super().__init__(parent)
        self.project_panel = project_panel
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SINGLE_SEL)
        
        # Colunas puramente visuais
        self.list_ctrl.InsertColumn(0, "Extensão", width=100)
        self.list_ctrl.InsertColumn(1, "Arquivos (Contagem)", width=150)
        self.list_ctrl.InsertColumn(2, "Tokens Totais", width=150)
        
        sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)
        
        # Variáveis de estado de ordenação
        self.sort_column = 2 # Padrão: Tokens Totais
        self.sort_ascending = False # Padrão: Decrescente (Maior primeiro)
        self.cached_summary_list: List[Tuple[str, Dict[str, Any]]] = [] # Cache para ordenação

        # Binding para clique na coluna
        self.list_ctrl.Bind(wx.EVT_LIST_COL_CLICK, self.on_col_click)
        
    def on_col_click(self, event: wx.ListEvent):
        """Lida com o clique no cabeçalho da coluna para ordenar."""
        col = event.GetColumn()
        
        if col == self.sort_column:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_column = col
            # Padrão: Crescente para Extensão e Contagem, Decrescente para Tokens
            self.sort_ascending = (col != 2)
            
        self._refresh_list()

    def update_data(self, extension_summary: Dict[str, Dict[str, Any]]):
        """Recebe o resumo, armazena em cache e chama a atualização da lista."""
        # Converte o dicionário em uma lista para facilitar a ordenação
        self.cached_summary_list = list(extension_summary.items())
        
        self._refresh_list()

    def _refresh_list(self):
        """Aplica a ordenação e popula o ListCtrl."""
        self.list_ctrl.Freeze()
        self.list_ctrl.DeleteAllItems()

        # Define a chave de ordenação
        col_map = {
            0: lambda item: item[0],                 # Extensão (String)
            1: lambda item: item[1]['count'],        # Arquivos (Numérico)
            2: lambda item: item[1]['tokens'],       # Tokens Totais (Numérico)
        }
        
        sort_key_func = col_map.get(self.sort_column)

        if sort_key_func:
            sorted_exts = sorted(self.cached_summary_list, 
                                 key=sort_key_func, 
                                 reverse=not self.sort_ascending)
        else:
            sorted_exts = self.cached_summary_list # Fallback

        for i, (ext, data) in enumerate(sorted_exts):
            idx = self.list_ctrl.InsertItem(i, ext)
            self.list_ctrl.SetItem(idx, 1, f"{data['count']:,}")
            self.list_ctrl.SetItem(idx, 2, f"{data['tokens']:,}")
            
        self.list_ctrl.Thaw()


class FilePreviewTab(wx.Panel):
    """Aba 4: Prévia (Inalterada na função, apenas estilo)."""
    def __init__(self, parent, project_panel):
        super().__init__(parent)
        self.project_panel = project_panel
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.lbl_info = wx.StaticText(self, label="Selecione um arquivo para ver a prévia.")
        sizer.Add(self.lbl_info, 0, wx.EXPAND | wx.ALL, 5)
        
        self.preview_text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        # Mantendo o estilo visual escuro para parecer mais "profissional"
        self.preview_text.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.preview_text.SetBackgroundColour(wx.Colour(30, 30, 30))
        self.preview_text.SetForegroundColour(wx.Colour(220, 220, 220))
        
        sizer.Add(self.preview_text, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

    def update_preview(self, path: str, content: str, tokens: int):
        self.lbl_info.SetLabel(f"{os.path.basename(path)} | {tokens:,} Tokens")
        # Mantém o truncamento para evitar travamento da interface
        disp = content[:20000] + ("\n\n[... Conteúdo truncado para performance ...]" if len(content) > 20000 else "")
        self.preview_text.SetValue(disp)


class PathDropTarget(wx.FileDropTarget):
    def __init__(self, panel: 'ProjectPanel'): 
        super().__init__()
        self.panel = panel
    def OnDropFiles(self, x: int, y: int, filenames: list[str]) -> bool:
        if filenames: self.panel.on_drop_path(filenames[0]); return True
        return False


class ProjectPanel(wx.Panel):
    """Painel Principal: Orquestra a visualização e filtragem."""
    def __init__(self, parent: wx.Notebook, frame: 'TokenCounterFrame'):
        super().__init__(parent)
        self.frame = frame 
        
        # Estado (Model) - Simplificado drasticamente
        self.root_path: Optional[str] = None
        self.root_node: Optional[TreeNode] = None
        self.file_contents: Dict[str, str] = {}
        self.node_map: Dict[str, TreeNode] = {} 
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
        self.btn_open = wx.Button(left_panel, label="Abrir Pasta")
        self.btn_clear = wx.Button(left_panel, label="Limpar")
        btn_sizer.Add(self.btn_open, 1, wx.RIGHT, 2)
        btn_sizer.Add(self.btn_clear, 0)
        left_sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        # Árvore (Sem ImageList/Checkboxes)
        self.tree_ctrl = wx.TreeCtrl(left_panel, style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_BUTTONS | wx.TR_LINES_AT_ROOT) 
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
        self.notebook.AddPage(self.tab_files, "Lista de Arquivos (Filtro)") # Novo Nome
        self.notebook.AddPage(self.tab_exts, "Resumo por Extensões") # Novo Nome
        self.notebook.AddPage(self.tab_prev, "Prévia")
        
        right_sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)
        right_panel.SetSizer(right_sizer)

        self.splitter.SplitVertically(left_panel, right_panel, 300)
        self.splitter.SetMinimumPaneSize(200)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.splitter, 1, wx.EXPAND)
        self.SetSizer(main_sizer)

    def _setup_bindings(self):
        self.btn_open.Bind(wx.EVT_BUTTON, self.frame.on_open_folder)
        self.btn_clear.Bind(wx.EVT_BUTTON, self.frame.on_clear_all)
        
        # Árvore: Apenas clique simples para prévia
        self.tree_ctrl.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_tree_preview)

    def on_drop_path(self, path: str):
        if os.path.isdir(path): self.frame.start_initial_scan(path)

    # --- Lógica de Árvore (Visual) ---
    
    def on_tree_preview(self, event):
        """Lida com o clique simples para prévia do arquivo."""
        item = event.GetItem()
        if item.IsOk():
            path = self.tree_ctrl.GetItemData(item)
            # Apenas arquivos de texto podem ter prévia
            if path in self.node_map and self.node_map[path].is_text:
                self.on_file_selected_for_preview(path)

    def on_file_selected_for_preview(self, path: str):
        """Carrega o conteúdo do arquivo na aba de prévia."""
        node = self.node_map.get(path)
        if node and node.is_text and path in self.file_contents:
            self.tab_prev.update_preview(path, self.file_contents[path], node.token_count)
            self.notebook.SetSelection(3) # Vai para aba de prévia

    # --- Inicialização e Atualização de Dados ---

    def handle_scan_result(self, results: Dict[str, Any]):
        """Processa o resultado do scan e calcula os totais."""
        self.root_path = results['root_path']
        self.root_node = results['root_node']
        self.file_contents = results['file_contents']
        self.node_map = results['node_map']
        
        self.all_text_files = []
        self.extension_map = {}

        # Mapeia arquivos e extensões
        for path, node in self.node_map.items():
            if node.is_text:
                self.all_text_files.append(node)
                
                _, ext = os.path.splitext(node.name)
                ext = ext.lower()
                if ext not in self.extension_map: self.extension_map[ext] = []
                self.extension_map[ext].append(node)
        
        self.build_visual_tree()
        self.update_all_views()
        
        self.progress_bar.SetValue(0)
        self.status_text.SetLabel(f"Pronto. Projeto com {len(self.all_text_files):,} arquivos de texto.")

    def build_visual_tree(self):
        """Constrói a árvore lateral baseada no root_node."""
        self.tree_ctrl.DeleteAllItems()
        if not self.root_node: return
        
        root_item = self.tree_ctrl.AddRoot(os.path.basename(self.root_path))
        self.tree_ctrl.SetItemData(root_item, self.root_path)
        self._build_tree_recursive(root_item, self.root_node)
        self.tree_ctrl.Expand(root_item)

    def _build_tree_recursive(self, parent_item, node):
        sorted_children = sorted(node.children, key=lambda n: (not n.is_dir, natural_sort_key(n.name)))
        for child in sorted_children:
            new_item = self.tree_ctrl.AppendItem(parent_item, child.name)
            self.tree_ctrl.SetItemData(new_item, child.full_path)
            if child.is_dir:
                self._build_tree_recursive(new_item, child)

    def update_all_views(self):
        """Calcula a soma total e atualiza todas as abas."""
        if not self.root_node: return
        
        # Garante que os totais recursivos estejam somados (soma de todos os filhos)
        self.root_node.calculate_recursive_tokens() 
        total_proj_tokens = self.root_node.total_recursive_tokens

        # 1. Resumo extensões
        ext_summary = {}
        for ext, nodes in self.extension_map.items():
            tot = sum(n.token_count for n in nodes)
            ext_summary[ext] = {'count': len(nodes), 'tokens': tot}

        # 2. Atualizar Abas
        self.tab_tree.update_data(self.root_node)
        self.tab_files.update_data(self.all_text_files, total_proj_tokens)
        self.tab_exts.update_data(ext_summary)

    def clear_all_project_data(self):
        """Limpa todo o estado do projeto."""
        self.root_path = None
        self.root_node = None
        self.file_contents.clear()
        self.node_map.clear()
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