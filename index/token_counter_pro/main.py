import argparse
import sys
import wx
import os

# Verifica e importa os módulos locais
try:
    from core import TIKTOKEN_AVAILABLE
    from cli.interface import cli_scan_only # Função do CLI que será implementada
    from ui.app import TokenCounterApp # Classe principal da GUI que será implementada
except ImportError as e:
    print("--------------------------------------------------------------------------------", file=sys.stderr)
    print("ERRO FATAL: Falha ao importar módulos internos do Token Counter Pro.", file=sys.stderr)
    print("Verifique se você está executando 'main.py' a partir do diretório raiz do projeto 'token_counter_pro'.", file=sys.stderr)
    print(f"Detalhe do Erro: {e}", file=sys.stderr)
    sys.exit(1)

def main():
    """
    Função principal para lidar com o modo CLI ou GUI.
    """
    parser = argparse.ArgumentParser(description="Token Counter Pro: Contagem de tokens em código-fonte e texto.")
    parser.add_argument(
        '--scan-only', 
        type=str, 
        help="Modo CLI: Escaneia o diretório especificado e imprime o resumo da estrutura no console."
    )
    args = parser.parse_args()

    # Exibe informações de ambiente
    wxpython_version = wx.version() if 'wx' in sys.modules else "Não instalado (Modo CLI)"
    tiktoken_status = "disponível" if TIKTOKEN_AVAILABLE else "ausente"
    
    print(f"Ambiente: wxpython_version={wxpython_version}, tiktoken={tiktoken_status}")

    if args.scan_only:
        # Modo CLI
        print("Iniciando no Modo CLI...")
        # A função cli_scan_only está sendo importada, mas a implementação virá em cli/interface.py
        try:
            cli_scan_only(args.scan_only)
        except Exception as e:
            print(f"Erro no modo CLI: {e}", file=sys.stderr)
    else:
        # Modo GUI
        print("Iniciando no Modo GUI...")
        try:
            # Garante que wx.App e MainLoop sejam chamados apenas no modo GUI
            app = TokenCounterApp(0)
            app.MainLoop()
        except Exception as e:
            # Captura erros comuns de inicialização do wxPython
            if not 'wx' in sys.modules or not hasattr(wx, 'App'):
                print("--------------------------------------------------------------------------------", file=sys.stderr)
                print("Erro ao iniciar a aplicação wxPython.", file=sys.stderr)
                print("A biblioteca 'wxPython' pode estar ausente ou incompatível.", file=sys.stderr)
                print("Instale-a usando: pip install wxPython", file=sys.stderr)
                print(f"Detalhes do Erro: {e}", file=sys.stderr)
            else:
                 print(f"Erro inesperado na GUI: {e}", file=sys.stderr)


if __name__ == '__main__':
    # Verifica se o diretório de trabalho é o 'token_counter_pro' para garantir as importações relativas
    if os.path.basename(os.getcwd()) != "token_counter_pro":
        # Se main.py for chamado de fora do diretório do projeto, ajusta o path
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
    main()