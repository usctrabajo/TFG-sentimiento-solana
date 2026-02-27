import pandas as pd
from pathlib import Path

def main():
    project_root=Path(__file__).resolve().parents[1]
    raw_dir=project_root / "data" / "raw"
    processed_dir=project_root / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    input_path=raw_dir / "gdelt_solana_tone.csv"
    output_path=processed_dir / "gdelt_solana_tone_vars.csv"

    # Cargamos los datos del tone score
    df=pd.read_csv(input_path)

    # Convertimos las fechas a formato datetime y las ordenamos

    df["date"]=pd.to_datetime(df["date"])
    df=df.sort_values("date").reset_index(drop=True)

    # Calculamos los lags del tone score (t-1,t-1 y t-3)
    df["tone_lag_1"]=df["tone_score"].shift(1)
    df["tone_lag_2"]=df["tone_score"].shift(2)
    df["tone_lag_3"]=df["tone_score"].shift(3)

    # Lo guardamos en el CSV de output
    df.to_csv(output_path, index=False)
    print(f"Guardado con {len(df)} lineas")

if __name__ == "__main__":
    main()