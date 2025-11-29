import wx
import sys
import os

# Importa o Frame principal
try:
    from ui.frame import TokenCounterFrame
    from core import TIKTOKEN_AVAILABLE
except ImportError:
    print("FATAL: Não foi possível importar TokenCounterFrame ou módulos do core.", file=sys.stderr)
    sys.exit(1)

class TokenCounterApp(wx.App):
    """
    Classe principal da aplicação wxPython, responsável pela inicialização
    do Frame e pela configuração inicial do ambiente.
    """
    def OnInit(self) -> bool:
        """
        Rotina de inicialização.
        """
        # 1. Configuração de Debug/Info
        wxpython_version = wx.version()
        tiktoken_status = "disponível" if TIKTOKEN_AVAILABLE else "ausente"
        
        print(f"Ambiente da GUI: wxpython_version={wxpython_version}, tiktoken={tiktoken_status}")
        
        # 2. Inicialização da UI
        # O frame será o 'top window'
        frame = TokenCounterFrame(None, "Token Counter Pro - Análise e Contagem de Tokens")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True