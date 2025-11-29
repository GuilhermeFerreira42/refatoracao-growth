import tiktoken
from typing import Optional, Tuple, Dict, Any

# --- TIKTOKEN e Configurações Globais ---
# Tentativa de inicialização do tiktoken (para ser usada pelo scanner/counter)
try:
    # Usar o modelo padrão para a contagem de tokens
    TOKEN_ENCODER = tiktoken.encoding_for_model("gpt-4o")
    TIKTOKEN_AVAILABLE = True
    MODEL_NAME = "gpt-4o"
    # 1.28M context é uma informação do modelo, mas vamos manter a simplicidade na string
    CONTEXT_INFO = f"{MODEL_NAME} (Tokenização real)"
except ImportError:
    # Fallback caso tiktoken não esteja instalado
    TOKEN_ENCODER = None
    TIKTOKEN_AVAILABLE = False
    MODEL_NAME = "N/A"
    CONTEXT_INFO = "gpt-4o (tiktoken AUSENTE, usando bytes/4 como FALLBACK)"

def count_tokens(text: str) -> Tuple[int, str]:
    """
    Conta o número de tokens no texto fornecido.
    
    Se tiktoken estiver disponível, usa a contagem real.
    Caso contrário, usa um fallback simples (bytes / 4) para estimativa.

    Args:
        text: A string de texto a ser tokenizada.

    Returns:
        Uma tupla contendo: (total_tokens, nome_do_encoder_ou_fallback)
    """
    if not text:
        return 0, CONTEXT_INFO
    
    try:
        if TIKTOKEN_AVAILABLE and TOKEN_ENCODER:
            # Contagem real usando tiktoken
            tokens = TOKEN_ENCODER.encode(text)
            return len(tokens), MODEL_NAME
        else:
            # Contagem de fallback: 1 token para cada 4 bytes (regra empírica)
            byte_size = len(text.encode('utf-8'))
            estimated_tokens = max(1, byte_size // 4)
            return estimated_tokens, CONTEXT_INFO
            
    except Exception as e:
        print(f"ERRO ao contar tokens: {e}. Usando fallback.")
        # Garante que sempre retornamos um resultado (o fallback)
        byte_size = len(text.encode('utf-8'))
        estimated_tokens = max(1, byte_size // 4)
        return estimated_tokens, CONTEXT_INFO

def get_encoder_info() -> str:
    """
    Retorna a string de informação sobre o encoder em uso.
    """
    return CONTEXT_INFO

def get_tokenization_details(text: str) -> Dict[str, Any]:
    """
    Calcula o total de tokens e bytes, e fornece detalhes adicionais.

    Args:
        text: A string de texto a ser analisada.

    Returns:
        Um dicionário com 'tokens', 'byte_size', 'encoder_info', 'token_list' (opcional).
    """
    token_count, encoder_info = count_tokens(text)
    
    byte_size = len(text.encode('utf-8'))
    
    details = {
        'tokens': token_count,
        'byte_size': byte_size,
        'encoder_info': encoder_info,
        'token_list': None # Não é eficiente retornar a lista completa por padrão
    }
    
    # Se tiktoken estiver disponível, podemos adicionar mais detalhes
    if TIKTOKEN_AVAILABLE and TOKEN_ENCODER:
        try:
            # Retorna os tokens como strings, útil para preview na Aba 2
            # decode_single_token_bytes retorna bytes, precisamos decodificar para string
            tokens = [TOKEN_ENCODER.decode_single_token_bytes(t).decode('utf-8', errors='ignore') 
                      for t in TOKEN_ENCODER.encode(text)]
            details['token_list'] = tokens
        except Exception as e:
            print(f"Aviso: Não foi possível decodificar a lista de tokens. {e}")

    return details


if __name__ == '__main__':
    # Teste rápido de funcionalidade
    print("--- Teste do Módulo Counter ---")
    
    test_text_pt = "Olá mundo! Este é um teste com tiktoken."
    test_text_en = "Hello world! This is a test with tiktoken."
    
    print(f"Texto (PT): '{test_text_pt}'")
    pt_details = get_tokenization_details(test_text_pt)
    print(f"  Tokens: {pt_details['tokens']} | Bytes: {pt_details['byte_size']} | Encoder: {pt_details['encoder_info']}")
    
    print(f"Texto (EN): '{test_text_en}'")
    en_details = get_tokenization_details(test_text_en)
    print(f"  Tokens: {en_details['tokens']} | Bytes: {en_details['byte_size']} | Encoder: {en_details['encoder_info']}")
    
    if not TIKTOKEN_AVAILABLE:
        print("\nAVISO: O tiktoken NÃO está instalado. As contagens acima são estimativas.")