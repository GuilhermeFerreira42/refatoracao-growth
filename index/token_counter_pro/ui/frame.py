import wx
import threading
import sys
import os 
from typing import Optional
from .project_panel import ProjectPanel
from .text_panel import TextPanel
from core import scan_directory, get_encoder_info, count_tokens

class TokenCounterFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(1200, 800))
        self.scanner_thread: Optional[threading.Thread] = None
        self.cancel_flag = threading.Event()
        
        self.CreateStatusBar(2)
        self.SetStatusText(f"Encoder: {get_encoder_info()}", 1)

        main_notebook = wx.Notebook(self)
        
        self.project_panel = ProjectPanel(main_notebook, self)
        self.text_panel = TextPanel(main_notebook, self)
        
        main_notebook.AddPage(self.project_panel, "1. Análise de Arquivos e Projetos")
        main_notebook.AddPage(self.text_panel, "2. Contagem de Tokens em Texto Direto")
        
        self.SetSizer(wx.BoxSizer(wx.VERTICAL))
        self.GetSizer().Add(main_notebook, 1, wx.EXPAND)
        self.Layout()
        self.Center()
        self.Show(True)

    # --- Lógica de Scan (1ª Fase: Estrutura) ---
    def start_initial_scan(self, path):
        if self.scanner_thread and self.scanner_thread.is_alive():
            return
        
        self.cancel_flag.clear()
        self.SetStatusText("Escaneando estrutura...", 0)
        self.project_panel.progress_bar.SetValue(0)
        self.project_panel.status_text.SetLabel("Iniciando varredura...")
        
        def run():
            results = scan_directory(path, self.cancel_flag, self._update_scan_progress)
            wx.CallAfter(self._finish_scan, results)
            
        self.scanner_thread = threading.Thread(target=run, daemon=True)
        self.scanner_thread.start()

    def _update_scan_progress(self, scanned: int, total: int, current_path: str):
        """Atualiza a barra de progresso de forma thread-safe."""
        if self.cancel_flag.is_set():
            return
            
        if total > 0:
            percent = int((scanned / total) * 100)
            wx.CallAfter(self.project_panel.progress_bar.SetValue, percent)
            wx.CallAfter(self.project_panel.status_text.SetLabel, 
                         f"Estrutura: {scanned}/{total} arquivos lidos. Atual: {os.path.basename(current_path)}")

    def _finish_scan(self, results):
        self.SetStatusText("Estrutura carregada e contagem inicial concluída.", 0)
        self.project_panel.handle_scan_result(results)

    # --- Lógica de Contagem (2ª Fase: Processamento/Atualização) ---
    # CORREÇÃO: Adicionado o argumento 'event'
    def start_token_counting(self, event):
        """
        Dispara a atualização de totais após uma mudança de seleção.
        O botão "Recalcular Totais" é o ponto central de sincronização após qualquer seleção.
        """
        if not self.project_panel.root_node:
            self.project_panel.status_text.SetLabel("Erro: Nenhuma pasta carregada.")
            return

        self.SetStatusText("Recalculando totais de tokens selecionados...", 0)
        self.project_panel.status_text.SetLabel("Recalculando e sincronizando painéis...")
        
        self.project_panel.recalculate_selected_totals()
        
        self.SetStatusText("Totais de Tokens Selecionados atualizados.", 0)
        self.project_panel.status_text.SetLabel("Pronto para usar.")


    def on_open_folder(self, event):
        dlg = wx.DirDialog(self, "Selecione a Pasta do Projeto")
        if dlg.ShowModal() == wx.ID_OK:
            self.start_initial_scan(dlg.GetPath())
        dlg.Destroy()

    def on_stop_scanning(self, event):
        if self.scanner_thread and self.scanner_thread.is_alive():
            self.cancel_flag.set()
            self.SetStatusText("Cancelando...", 0)
            self.project_panel.status_text.SetLabel("Processo Cancelado.")
        
    def on_clear_all(self, event):
        self.SetStatusText("Projeto Limpo.", 0)
        self.project_panel.clear_all_project_data()