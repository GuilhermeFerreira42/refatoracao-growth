import wx
import sys
import os

# Adiciona o diretório raiz do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.frame import TokenCounterFrame
from core import TIKTOKEN_AVAILABLE

class TokenCounterApp(wx.App):
    def OnInit(self):
        # Informações de ambiente no console
        print(f"Ambiente: wxpython_version={wx.version()} tiktoken={'disponível' if TIKTOKEN_AVAILABLE else 'ausente'}")
        
        # Cria a janela principal
        frame = TokenCounterFrame(None, title="Token Counter Pro (v2)")
        self.SetTopWindow(frame)
        return True

if __name__ == '__main__':
    app = TokenCounterApp(False)
    print("Iniciando no Modo GUI...")
    app.MainLoop()