import yfinance as yf
import pandas as pd
from rich.console import Console
from rich.table import Table
from datetime import datetime

empreses = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META",
    "JPM", "V", "MA", "UNH", "JNJ", "PG", "HD", "BAC",
    "KO", "PEP", "COST", "WMT", "DIS", "NFLX", "ADBE", "CRM",
    "ORCL", "INTC", "CSCO", "IBM", "QCOM", "TXN", "AMD",
    "PFE", "MRK", "ABBV", "BMY", "AMGN", "CVX", "XOM", "COP",
    "GS", "MS", "BLK", "AXP", "USB", "WFC", "C",
    "MCD", "SBUX", "NKE", "TGT"
]

MAX_PE = float(input("Quin P/E màxim vols? "))
MIN_MARGE = float(input("Quin marge mínim vols (en %): ")) / 100

console = Console()
resultats = []

for empresa in empreses:
    try:
        accio = yf.Ticker(empresa)
        info = accio.info
        pe = info.get("trailingPE", 0) or 0
        marge = info.get("profitMargins", 0) or 0
        dividend = info.get("dividendYield", 0) or 0
        if pe < MAX_PE and pe > 0 and marge > MIN_MARGE:
            resultats.append({
                "Empresa": empresa,
                "Preu": round(info.get("currentPrice", 0) or 0, 2),
                "P/E": round(pe, 1),
                "Marge": str(round(marge * 100, 1)) + "%",
                "Dividend": str(round(dividend, 2)) + "%",
                "Deute": round(info.get("debtToEquity", 0) or 0, 1),
            })
    except:
        console.print(f"[red]Error amb {empresa}, saltant...[/red]")

df = pd.DataFrame(resultats)
df = df.sort_values("P/E")
df = df.reset_index(drop=True)

taula = Table(title="Screener d'Accions")
for columna in df.columns:
    taula.add_column(columna)
for _, fila in df.iterrows():
    color = "green" if fila["P/E"] < 20 else "yellow"
    taula.add_row(*[str(x) for x in fila], style=color)

console.print(taula)
console.print(f"\nEmpreses analitzades: {len(empreses)}")
console.print(f"Empreses que passen el filtre: {len(df)}")
if len(df) > 0:
    console.print(f"Millor oportunitat (P/E més baix): {df.iloc[0]['Empresa']}")

data_avui = datetime.now().strftime("%Y-%m-%d")
nom_fitxer = f"screener_{data_avui}.xlsx"
df.to_excel(nom_fitxer, index=False)
console.print(f"\nResultats guardats a: {nom_fitxer}")
