import os
from typing import List, Dict, Any, Optional

class TreeNode:
    """Representa um arquivo ou diretório na estrutura do projeto."""
    
    def __init__(self, name: str, full_path: str, is_dir: bool, size_bytes: int = 0):
        self.name: str = name
        # Caminho completo (chave única para o arquivo/conteúdo)
        self.full_path: str = full_path 
        self.is_dir: bool = is_dir
        self.size_bytes: int = size_bytes
        self.children: List['TreeNode'] = []
        self.parent: Optional['TreeNode'] = None
        
        # --- NOVOS ATRIBUTOS DE ESTADO (Para seleção na UI) ---
        # 0: Não selecionado, 1: Parcialmente selecionado, 2: Totalmente selecionado
        self.selection_state: int = 0 
        self.is_text: bool = False # Se o arquivo é texto ou binário/ignorado
        self.tokens: int = 0
        self.extension: str = ""

    def add_child(self, child: 'TreeNode'):
        self.children.append(child)
        child.parent = self

    def __repr__(self) -> str:
        return f"TreeNode(name='{self.name}', path='{self.full_path}', dir={self.is_dir}, state={self.selection_state})"