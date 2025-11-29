import wx
import os
import threading
from typing import Optional, Set, Dict, Any, TYPE_CHECKING
from core import TreeNode, count_tokens

# Evita ciclo de importação apenas para tipagem
if TYPE_CHECKING:
    from .frame import TokenCounterFrame

# --- Classe auxiliar para Drag & Drop ---
class PathDropTarget(wx.FileDropTarget):
    def __init__(self, panel: 'ProjectPanel'): 
        super().__init__()
        self.panel = panel

    def OnDropFiles(self, x: int, y: int, filenames: list[str]) -> bool:
        if filenames:
            self.panel.on_drop_path(filenames[0])
            return True
        return False

class ProjectPanel(wx.Panel):
    def __init__(self, parent: wx.Notebook, frame: 'TokenCounterFrame'):
        super().__init__(parent)
        self.frame = frame 
        
        # --- Estado ---
        self.root_path: Optional[str] = None
        self.root_node: Optional[TreeNode] = None
        self.file_contents: Dict[str, str] = {}
        self.selected_file_paths: Set[str] = set()
        self.total_tokens_in_project = 0
        self.total_scanned_files = 0

        self._setup_ui()
        self._setup_bindings()
        self._setup_drag_and_drop()

    def _setup_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 1. Painel de Controle
        control_panel = wx.Panel(self, style=wx.RAISED_BORDER)
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.open_folder_btn = wx.Button(control_panel, label="Abrir Pasta (&O)...")
        self.stop_btn = wx.Button(control_panel, label="Parar Scan")
        self.clear_btn = wx.Button(control_panel, label="Limpar Tudo")
        
        control_sizer.Add(self.open_folder_btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        control_sizer.Add(self.stop_btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        control_sizer.Add(self.clear_btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        control_sizer.AddStretchSpacer(1)
        
        self.scan_status_label = wx.StaticText(control_panel, label="Status: Aguardando pasta...")
        control_sizer.Add(self.scan_status_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 10)
        control_panel.SetSizer(control_sizer)
        
        main_sizer.Add(control_panel, 0, wx.EXPAND | wx.ALL, 5)

        # 2. Splitter (Árvore e Preview)
        self.splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE | wx.SP_3DSASH)
        
        # Árvore
        tree_panel = wx.Panel(self.splitter)
        tree_sizer = wx.BoxSizer(wx.VERTICAL)
        self.tree_ctrl = wx.TreeCtrl(tree_panel, style=wx.TR_DEFAULT_STYLE | wx.TR_SINGLE | wx.TR_HAS_BUTTONS)
        tree_sizer.Add(self.tree_ctrl, 1, wx.EXPAND)
        tree_panel.SetSizer(tree_sizer)
        
        # Preview
        preview_panel = wx.Panel(self.splitter)
        preview_sizer = wx.BoxSizer(wx.VERTICAL)
        preview_sizer.Add(wx.StaticText(preview_panel, label="Prévia:"), 0, wx.LEFT | wx.TOP, 5)
        self.preview_text = wx.TextCtrl(preview_panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        preview_sizer.Add(self.preview_text, 1, wx.EXPAND | wx.ALL, 5)
        preview_panel.SetSizer(preview_sizer)
        
        self.splitter.SplitHorizontally(tree_panel, preview_panel, sashPosition=400)
        main_sizer.Add(self.splitter, 1, wx.EXPAND | wx.ALL, 5)

        # 3. Resultados
        results_panel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        results_sizer = wx.GridBagSizer(5, 5)
        
        results_sizer.Add(wx.StaticText(results_panel, label="Arquivos:"), (0, 0))
        results_sizer.Add(wx.StaticText(results_panel, label="Tokens:"), (1, 0))
        results_sizer.Add(wx.StaticText(results_panel, label="Bytes:"), (2, 0))

        self.selected_files_label = wx.StaticText(results_panel, label="0")
        self.total_tokens_label = wx.StaticText(results_panel, label="0")
        self.total_bytes_label = wx.StaticText(results_panel, label="0")
        
        results_sizer.Add(self.selected_files_label, (0, 1))
        results_sizer.Add(self.total_tokens_label, (1, 1))
        results_sizer.Add(self.total_bytes_label, (2, 1))
        results_sizer.AddGrowableCol(1)
        
        results_panel.SetSizer(results_sizer)
        main_sizer.Add(results_panel, 0, wx.EXPAND | wx.ALL, 5)
        
        self.SetSizer(main_sizer)

    def _setup_bindings(self):
        self.open_folder_btn.Bind(wx.EVT_BUTTON, self.frame.on_open_folder)
        self.clear_btn.Bind(wx.EVT_BUTTON, self.frame.on_clear_all)
        self.stop_btn.Bind(wx.EVT_BUTTON, self.frame.on_stop_scanning)
        self.tree_ctrl.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_tree_selection_changed)
        
    def _setup_drag_and_drop(self):
        dt = PathDropTarget(self)
        self.SetDropTarget(dt)

    def on_drop_path(self, path: str):
        if os.path.isdir(path):
            self.scan_status_label.SetLabel(f"Iniciando: {os.path.basename(path)}")
            self.frame.start_new_scan(path)
        else:
            wx.MessageBox("Apenas pastas são aceitas.", "Erro", wx.OK | wx.ICON_ERROR)

    def on_tree_selection_changed(self, event):
        item = event.GetItem()
        if not item or not item.IsOk(): 
            return
        
        # CORREÇÃO: GetItemData retorna o objeto Python direto (str) no Phoenix
        file_path = self.tree_ctrl.GetItemData(item)
        
        if file_path and isinstance(file_path, str) and file_path in self.file_contents:
            content = self.file_contents[file_path]
            # Limita a prévia
            disp = content[:10000] + ("\n\n[... Truncado ...]" if len(content) > 10000 else "")
            self.preview_text.SetValue(disp)
        else:
            self.preview_text.Clear()

    def handle_scan_result(self, results: Dict[str, Any]):
        self.root_path = results['root_path']
        self.root_node = results['root_node']
        self.file_contents = results['file_contents']
        self.selected_file_paths = set(results['text_file_paths'])
        
        self.update_tree_view()
        self._recalculate_totals()
        self.scan_status_label.SetLabel("Pronto.")

    def update_tree_view(self):
        self.tree_ctrl.DeleteAllItems()
        self.preview_text.Clear()
        if self.root_node:
            root = self.tree_ctrl.AddRoot(f"ROOT: {self.root_node.name}")
            # CORREÇÃO: Passar o objeto diretamente (sem wx.TreeItemData)
            self.tree_ctrl.SetItemData(root, self.root_path)
            self._add_children(root, self.root_node)
            self.tree_ctrl.Expand(root)

    def _add_children(self, parent_item, node):
        # Ordenação simples
        children = sorted(node.children, key=lambda x: (not x.is_dir, x.name.lower()))
        
        for child in children:
            txt = child.name
            # CORREÇÃO: Usar .full_path que existe na classe TreeNode
            path = child.full_path
            
            if not child.is_dir:
                if child.is_text and path in self.file_contents:
                    # Contagem rápida sob demanda
                    from core import count_tokens 
                    t, _ = count_tokens(self.file_contents[path])
                    txt += f" ({t} tokens)"
                else:
                    txt += f" ({child.size_bytes} B)"
            
            new_item = self.tree_ctrl.AppendItem(parent_item, txt)
            # CORREÇÃO: Passar a string path diretamente
            self.tree_ctrl.SetItemData(new_item, path)
            
            if child.is_dir:
                self._add_children(new_item, child)

    def _recalculate_totals(self):
        total_tokens = 0
        from core import count_tokens
        
        for path in self.selected_file_paths:
            c = self.file_contents.get(path)
            if c:
                t, _ = count_tokens(c)
                total_tokens += t
        
        self.total_tokens_in_project = total_tokens
        self.total_scanned_files = len(self.selected_file_paths)
        self.selected_files_label.SetLabel(str(self.total_scanned_files))
        self.total_tokens_label.SetLabel(f"{total_tokens:,}")