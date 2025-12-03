import tiktoken
from typing import Optional, Tuple, Dict, Any, List

# --- TIKTOKEN e Configurações Globais ---
try:
    TOKEN_ENCODER = tiktoken.encoding_for_model("gpt-4o")
    TIKTOKEN_AVAILABLE = True
    MODEL_NAME = "gpt-4o"
    CONTEXT_INFO = f"{MODEL_NAME} (Tokenização real)"
except ImportError:
    TOKEN_ENCODER = None
    TIKTOKEN_AVAILABLE = False
    MODEL_NAME = "N/A"
    CONTEXT_INFO = "gpt-4o (tiktoken AUSENTE, usando bytes/4 como FALLBACK)"

def count_tokens(text: str) -> Tuple[int, str]:
    if not text: return 0, CONTEXT_INFO
    
    try:
        if TIKTOKEN_AVAILABLE and TOKEN_ENCODER:
            tokens = TOKEN_ENCODER.encode(text)
            return len(tokens), MODEL_NAME
        else:
            byte_size = len(text.encode('utf-8'))
            estimated_tokens = max(1, byte_size // 4)
            return estimated_tokens, CONTEXT_INFO
            
    except Exception:
        byte_size = len(text.encode('utf-8'))
        estimated_tokens = max(1, byte_size // 4)
        return estimated_tokens, CONTEXT_INFO

def get_encoder_info() -> str:
    return CONTEXT_INFO

def get_tokenization_details(text: str) -> Dict[str, Any]:
    token_count, encoder_info = count_tokens(text)
    byte_size = len(text.encode('utf-8'))
    
    details = {
        'tokens': token_count,
        'byte_size': byte_size,
        'encoder_info': encoder_info,
        'token_list': None
    }
    
    if TIKTOKEN_AVAILABLE and TOKEN_ENCODER:
        try:
            tokens = [TOKEN_ENCODER.decode_single_token_bytes(t).decode('utf-8', errors='ignore') 
                      for t in TOKEN_ENCODER.encode(text)]
            details['token_list'] = tokens
        except Exception:
            pass

    return details