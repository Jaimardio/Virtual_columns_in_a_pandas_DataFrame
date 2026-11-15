import os
import pandas as pd
import pytest
from solution import add_virtual_column

# 1. TESTY DLA CZĘŚCI 1 (Funkcja add_virtual_column)

def test_my_custom_virtual_column_addition():
  """test Part 1: Sprawdza poprawne działanie dodawania dwóch kolumn."""
  df = pd.DataFrame({"kolumna_a": [10, 20], "kolumna_b": [5, 15]})
  result = df = add_virtual_column(
      df, "kolumna_a + kolumna_b", "kolumna_wynikowa"
  )

  assert "kolumna_wynikowa" in result.columns
  assert list(result["kolumna_wynikowa"]) == [15, 35]


def test_my_custom_virtual_column_invalid_target_name():
  """test Part 1: Sprawdza, czy funkcja odrzuca (zwraca pusty DataFrame)
  nazwę nowej kolumny zawierającą cyfry lub niedozwolone znaki.
  """
  df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
  result = add_virtual_column(df, "x * y", "z1")  # 'z1' zawiera cyfrę
  assert isinstance(result, pd.DataFrame)
  assert result.empty

# 2. TESTY DLA CZĘŚCI 2 (Pipeline i plik wynikowy)

def test_my_custom_pipeline_output_structure():
  """test Part 2: Weryfikuje, czy plik revenue_by_region.csv
  został poprawnie wygenerowany, ma dokładnie dwie kolumny oraz poprawny format.
  """
  file_path = "revenue_by_region.csv"
  assert os.path.exists(file_path), (
      f"Brak pliku wynikowego {file_path}! Uruchom najpierw pipeline.py."
  )

  df_res = pd.read_csv(file_path)

  # Sprawdzenie nagłówków wymaganych w zadaniu
  expected_cols = ["Region", "Revenue"]
  assert list(df_res.columns) == expected_cols, (
      f"Oczekiwano kolumn {expected_cols}, a są {list(df_res.columns)}"
  )

  # Sprawdzenie czy wartości przychodów są liczbami zmiennoprzecinkowymi
  assert pd.api.types.is_numeric_dtype(df_res["Revenue"]), (
      "Kolumna Revenue nie zawiera danych liczbowych!"
  )