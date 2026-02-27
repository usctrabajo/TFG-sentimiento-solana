import yfinance as yf
import pandas as pd
from pathlib import Path

def main():
    # Establecer correctamente la ruta de descarga
    project_root=Path(__file__).resolve().parents[1]
    raw_dir=project_root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    output_path=raw_dir / "sol_usd_ohlcv.csv"
    
    # Obtener datos de SOL-USD con Yahoo Finance desde el 1 de febrero de 2021 a intervalos de 1 día
    df = yf.download("SOL-USD", start="2021-02-01", interval="1d", progress=False)


    # Asegurarnos de que no nos devuelve un DataFrame vacío
    if df.empty:
        raise RuntimeError("Se ha obtenido un DataFrame vacío.")
    
    # Convertir el índice (Date) en una columna
    df=df.reset_index()

    # Aplanar las columnas porque Yahoo Finance las da como MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns=df.columns.get_level_values(0)


    # Quitar Price como nombre de las columnas
    df.columns.name=None

    # Reordenadar columnas para Date, OHLCV
    df=df[["Date", "Open", "High", "Low", "Close", "Volume"]]

        
    print(df.head())
    
    # Guardar el DataFrame en un CSV
    df.to_csv(output_path, index=False)

    # Imprimir resultado exitoso
    print("Datos descargados en : "+str(output_path))
    print("Hay "+str(len(df))+" filas")

if __name__ == "__main__":
    main()