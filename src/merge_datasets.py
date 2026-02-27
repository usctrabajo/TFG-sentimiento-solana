import pandas as pd
from pathlib import Path

def main():
    # Obtengo los directorios y establezco donde estan los inputs y donde vamos a duardar el output
    project_root=Path(__file__).resolve().parents[1]
    processed_dir=project_root / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    ohlcv_path=processed_dir / "sol_usd_market_vars.csv"
    tone_path=processed_dir / "gdelt_solana_tone_vars.csv"
    output_path=processed_dir / "merged_dataset.csv"

    # Cargamos los dos conjuntos de datos que ya obtuvimos antes
    ohlcv=pd.read_csv(ohlcv_path)
    tone=pd.read_csv(tone_path)

    # Pasamos las fechas a solo día
    ohlcv["date"]=pd.to_datetime(ohlcv["Date"]).dt.date
    tone["date"]=pd.to_datetime(tone["date"]).dt.date

    # Hacemos un merge (juntamos) ambos conjuntos de datos, juntando los días que tengan información en ambos conjuntos
    df=ohlcv.merge(tone,on="date",how="inner")

    # Las ordenamos por orden cronológico
    df=df.sort_values("date").reset_index(drop=True)

    # Quitamos columnas duplicadas si hay
    df=df.drop(columns=["Date"])

    # Eliminamos los primeros días debido a la naturaleza de varios indicadores
    df=df.dropna().reset_index(drop=True)

    # Lo guardamos en el CSV final
    df.to_csv(output_path,index=False)
    print(f"Guardado, con {len(df)} filas")


if __name__ == "__main__":
    main()