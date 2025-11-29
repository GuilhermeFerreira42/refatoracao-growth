import wx
import threading
from core import get_tokenization_details, TIKTOKEN_AVAILABLE

class TextPanel(wx.Panel):
    def __init__(self, parent, frame):
        super().__init__(parent)
        self.frame = frame
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.text_area = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        sizer.Add(self.text_area, 1, wx.EXPAND | wx.ALL, 5)
        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_calc = wx.Button(self, label="Calcular Tokens")
        self.lbl_result = wx.StaticText(self, label="Tokens: 0")
        
        btn_sizer.Add(self.btn_calc, 0, wx.ALL, 5)
        btn_sizer.Add(self.lbl_result, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer.Add(btn_sizer, 0, wx.EXPAND)
        
        self.SetSizer(sizer)
        self.btn_calc.Bind(wx.EVT_BUTTON, self.on_calc)

    def on_calc(self, event):
        text = self.text_area.GetValue()
        # Processamento simples em thread
        threading.Thread(target=self._run_calc, args=(text,), daemon=True).start()

    def _run_calc(self, text):
        res = get_tokenization_details(text)
        wx.CallAfter(self.lbl_result.SetLabel, f"Tokens: {res['tokens']:,}")