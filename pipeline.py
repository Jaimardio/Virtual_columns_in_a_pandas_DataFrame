import pandas as pd
from solution import add_virtual_column

# 1. Wczytanie danych
df = pd.read_csv("sales.csv")

# 2. Usunięcie spacji z nagłówków i ujednolicenie nazw (zamiana spacji na podkreślenia, 
# żeby nazwy spełniały wymóg r'^[a-zA-Z_]+$' w naszej funkcji add_virtual_column)
df.columns = df.columns.str.strip()
df = df.rename(columns={
    "Unit Price": "Unit_Price",
    "Order ID": "Order_ID",
    "Order Date": "Order_Date"
})

# 3. Konwersja kolumn liczbowych na poprawne typy
df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")
df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").astype("Int64")

# 4. Obsługa braków i ujednolicanie tekstu
df["Discount"] = df["Discount"].fillna(0)
df["Region"] = df["Region"].fillna("Unknown").str.strip().str.title()
df["Product"] = df["Product"].str.strip()

# Odrzucenie wiersza-widmo (artefakt powtórzonego nagłówka odkryty podczas EDA)
df = df[df["Region"] != "Region"]

# 5. Ratowanie brakujących cen na podstawie średniej ceny tego samego produktu
df["Unit_Price"] = df["Unit_Price"].fillna(
    df.groupby("Product")["Unit_Price"].transform("mean")
)

# 6. Ostateczne usunięcie wierszy, których nie da się uratować
df = df.dropna(subset=["Unit_Price", "Quantity"])

# 7. OBLICZENIA Z UŻYCIEM FUNKCJI add_virtual_column

# Mnożymy Quantity * Unit_Price -> tworzymy kolumnę Subtotal
df = add_virtual_column(df, "Quantity * Unit_Price", "Subtotal")

# Odejmujemy Discount od Subtotal -> tworzymy ostateczną kolumnę Revenue
df = add_virtual_column(df, "Subtotal - Discount", "Revenue")

# Zaokrąglenie wyników do 2 miejsc po przecinku
df["Revenue"] = df["Revenue"].round(2)

# Zgrupowanie danych według regionów i zsumowanie przychodów
przychod_regiony = (
    df.groupby("Region")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)


# 8. ZAPIS WYNIKU i wyświetlenie wyników w konsoli
print("=" * 60)
print("       RAPORT Z PRZETWARZANIA DANYCH SPRZEDAŻOWYCH")
print("=" * 60)

print("\n--- Tabela z wyliczonym przychodem (pierwsze 5 wierszy) ---")
print(df[["Order_ID", "Region", "Product", "Quantity", "Unit_Price", "Discount", "Revenue"]].head())

print("\n--- Podsumowanie całkowitych przychodów według regionów ---")
print(przychod_regiony.to_string(index=False))

# Zapis do wymaganego pliku wynikowego
przychod_regiony.to_csv("revenue_by_region.csv", index=False)
print("\n" + "=" * 60)
print("[SUKCES] Plik 'revenue_by_region.csv' został pomyślnie wygenerowany!")
print("=" * 60)