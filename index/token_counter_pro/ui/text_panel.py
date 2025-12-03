import wx
import threading
from core import get_tokenization_details

class TextPanel(wx.Panel):
    """
    UI para Contagem de Tokens em Texto Direto (Aba 2 do Notebook principal).
    Implementa contagem automática com throttling (Timer).
    """
    def __init__(self, parent, frame):
        super().__init__(parent)
        self.frame = frame
        self.throttling_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._on_timer_tick, self.throttling_timer)
        
        self._setup_ui()
        self.text_area.Bind(wx.EVT_TEXT, self.on_text_change)

    def _setup_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 1. Área de Texto
        self.text_area = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_RICH2)
        main_sizer.Add(self.text_area, 1, wx.EXPAND | wx.ALL, 5)
        
        # 2. Painel de Resultados (Números Grandes)
        results_panel = wx.Panel(self, style=wx.SIMPLE_BORDER)
        results_sizer = wx.GridBagSizer(10, 5)
        
        # Tokens
        self.lbl_tokens_val = wx.StaticText(results_panel, label="0")
        self.lbl_tokens_val.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        results_sizer.Add(wx.StaticText(results_panel, label="TOTAL DE TOKENS:"), (0, 0), flag=wx.ALIGN_CENTER_VERTICAL)
        results_sizer.Add(self.lbl_tokens_val, (0, 1), flag=wx.EXPAND | wx.LEFT, border=10)
        
        # Palavras, Caracteres, Custo
        results_sizer.Add(wx.StaticText(results_panel, label="Palavras: 0"), (1, 0))
        results_sizer.Add(wx.StaticText(results_panel, label="Caracteres: 0"), (2, 0))
        self.lbl_cost_sim = wx.StaticText(results_panel, label="Custo Simulado: $0.00 (Estimativa)")
        results_sizer.Add(self.lbl_cost_sim, (3, 0), span=(1, 2), flag=wx.EXPAND)
        
        results_sizer.AddGrowableRow(0)
        results_sizer.AddGrowableCol(1)
        results_panel.SetSizer(results_sizer)
        
        main_sizer.Add(results_panel, 0, wx.EXPAND | wx.ALL, 5)
        
        # 3. Botão Limpar
        self.btn_clear = wx.Button(self, label="Limpar Texto")
        self.btn_clear.Bind(wx.EVT_BUTTON, self.on_clear)
        main_sizer.Add(self.btn_clear, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.SetSizer(main_sizer)

    def on_text_change(self, event):
        """Dispara o timer para realizar a contagem após um pequeno delay (throttling)."""
        if self.throttling_timer.IsRunning():
            self.throttling_timer.Stop()
        # Inicia a contagem após 500ms de inatividade
        self.throttling_timer.Start(500, oneShot=True)

    def _on_timer_tick(self, event):
        """Executa a contagem real na thread principal para evitar travamento da GUI."""
        text = self.text_area.GetValue()
        if not text:
            self._update_results(0, 0, 0, 0)
            return

        # Para manter a GUI responsiva, usamos threading, mas a contagem é rápida
        threading.Thread(target=self._run_calc, args=(text,), daemon=True).start()

    def _run_calc(self, text):
        res = get_tokenization_details(text)
        
        token_count = res['tokens']
        char_count = len(text)
        word_count = len(text.split())
        
        # Simulação de custo (ex: 0.50 USD por 1 milhão de tokens)
        cost = (token_count / 1_000_000) * 0.50 
        
        wx.CallAfter(self._update_results, token_count, char_count, word_count, cost)

    def _update_results(self, tokens: int, chars: int, words: int, cost: float):
        self.lbl_tokens_val.SetLabel(f"{tokens:,}")
        self.lbl_tokens_val.GetParent().FindWindowByLabel("Palavras: 0").SetLabel(f"Palavras: {words:,}")
        self.lbl_tokens_val.GetParent().FindWindowByLabel("Caracteres: 0").SetLabel(f"Caracteres: {chars:,}")
        self.lbl_cost_sim.SetLabel(f"Custo Simulado: ${cost:.6f} (Estimativa)")
        self.Layout()

    def on_clear(self, event):
        self.text_area.Clear()
        self._update_results(0, 0, 0, 0)