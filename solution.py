import pandas as pd
import re

def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    # 1. Walidacja nazwy nowej kolumny (tylko litery i podkreślenia)
    if not isinstance(new_column, str) or not re.match(r'^[a-zA-Z_]+$', new_column):
        return pd.DataFrame()
    
    if not isinstance(role, str):
        return pd.DataFrame()
        
    role_stripped = role.strip()
    
    # 2. Wykrywanie operatora (+, -, *)
    operators = ['+', '-', '*']
    op = None
    col1, col2 = None, None
    
    for o in operators:
        if o in role_stripped:
            parts = role_stripped.split(o)
            if len(parts) == 2:
                op = o
                col1, col2 = parts[0].strip(), parts[1].strip()
                break
                
    # Jeśli nie znaleziono operatora lub jest ich za dużo
    if op is None:
        return pd.DataFrame()
        
    # 3. Sprawdzenie czy kolumny wejściowe istnieją w DataFrame oraz czy składają się z liter i podkreśleń
    if col1 not in df.columns or col2 not in df.columns:
        return pd.DataFrame()
        
    if not re.match(r'^[a-zA-Z_]+$', col1) or not re.match(r'^[a-zA-Z_]+$', col2):
        return pd.DataFrame()
        
    # 4. Wykonanie operacji matematycznej i zwrócenie nowego DataFrame
    df_result = df.copy()
    try:
        if op == '+':
            df_result[new_column] = df_result[col1] + df_result[col2]
        elif op == '-':
            df_result[new_column] = df_result[col1] - df_result[col2]
        elif op == '*':
            df_result[new_column] = df_result[col1] * df_result[col2]
    except Exception:
        return pd.DataFrame()
        
    return df_result