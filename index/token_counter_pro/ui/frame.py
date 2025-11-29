import wx
import threading
import sys
# AQUI: Importa os painéis reais, não placeholders
from .project_panel import ProjectPanel
from .text_panel import TextPanel
from core import scan_directory, get_encoder_info

class TokenCounterFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(1000, 700))
        self.scanner_thread = None
        self.cancel_flag = threading.Event()
        
        self.CreateStatusBar(2)
        self.SetStatusText(f"Encoder: {get_encoder_info()}", 1)

        notebook = wx.Notebook(self)
        
        # Instancia os painéis reais passando 'self' (o frame)
        self.project_panel = ProjectPanel(notebook, self)
        self.text_panel = TextPanel(notebook, self)
        
        notebook.AddPage(self.project_panel, "Arquivos")
        notebook.AddPage(self.text_panel, "Texto Direto")
        
        self.SetSizer(wx.BoxSizer(wx.VERTICAL))
        self.GetSizer().Add(notebook, 1, wx.EXPAND)
        self.Layout()
        self.Center()

    def start_new_scan(self, path):
        if self.scanner_thread and self.scanner_thread.is_alive():
            return
        
        self.cancel_flag.clear()
        self.SetStatusText("Escaneando...", 0)
        
        def run():
            res = scan_directory(path, cancel_flag=self.cancel_flag)
            res['root_path'] = path
            wx.CallAfter(self._finish_scan, res)
            
        self.scanner_thread = threading.Thread(target=run, daemon=True)
        self.scanner_thread.start()

    def _finish_scan(self, results):
        self.SetStatusText("Concluído.", 0)
        self.project_panel.handle_scan_result(results)

    def on_open_folder(self, event):
        dlg = wx.DirDialog(self, "Selecione pasta")
        if dlg.ShowModal() == wx.ID_OK:
            self.start_new_scan(dlg.GetPath())
        dlg.Destroy()

    def on_stop_scanning(self, event):
        if self.scanner_thread and self.scanner_thread.is_alive():
            self.cancel_flag.set()
            self.SetStatusText("Parando...", 0)

    def on_clear_all(self, event):
        # Reinicia a interface recriando ou limpando dados
        self.SetStatusText("Limpo.", 0)
        # Aqui você pode implementar a limpeza profunda se necessário