import pandas as pd
from pathlib import Path

def main():
    # Cargo las rutas del proyecto
    project_root=Path(__file__).resolve().parents[1]
    processed_dir=project_root / "data" / "processed"
    input_path=processed_dir / "merged_dataset.csv"
    train_path=processed_dir / "train.csv"
    test_path=processed_dir / "test.csv"

    # Cargar el conjunto de datos ya mergueado
    df=pd.read_csv(input_path)

    # Asegurar el formato datetime de la columna de las fechas y ordenarlas
    df["date"]=pd.to_datetime(df["date"])
    df=df.sort_values("date").reset_index(drop=True)

    # Separar los datos sin mezclarlos (porque el orden importa), 80% 20%
    split_index=int(len(df)*0.8)
    train_data=df.iloc[:split_index].copy()
    test_data=df.iloc[split_index:].copy()

    # Guardarlos en los CSV
    train_data.to_csv(train_path,index=False)
    test_data.to_csv(test_path,index=False)

    print(f"Train con {len(train_data)} filas")
    print(f"Test con {len(test_data)} filas")

    
if __name__ == "__main__":
    main()