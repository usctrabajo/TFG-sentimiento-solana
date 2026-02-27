import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler

def main():
    # Cargo las rutas correctamente
    project_root=Path(__file__).resolve().parents[1]
    processed_dir=project_root / "data" / "processed"
    train_path=processed_dir / "train.csv"
    test_path=processed_dir / "test.csv"
    standarized_train=processed_dir / "final_train.csv"
    standarized_test=processed_dir / "final_test.csv"

    # Cargar los conjuntos de datos ya separados
    train=pd.read_csv(train_path)
    test=pd.read_csv(test_path)

    # Asegurar que las fechas esten en formato datetime (las fechas no se escalan)
    train["date"]=pd.to_datetime(train["date"])
    test["date"]=pd.to_datetime(test["date"])

    # Selecciono todas las columnas menos la fecha
    featured=[col for col in train.columns if col!="date"]

    # Me aseguro de que train y test tienen las mismas columnas
    missing=set(featured)-set(test.columns)
    if(missing):
        raise RuntimeError(f"En los datos de test faltan{missing}")
    
    # Aplicamos la estandarización, fit_transform calcula en train la media y desviación estándar y transform estandariza test con eso, asi evitamos que el test influya en el escalado
    scaler=StandardScaler()
    train_scaled=scaler.fit_transform(train[featured])
    test_scaled=scaler.transform(test[featured])

    # Reconstruyo los conjuntos de datos sin tocar las fechas
    final_train_scaled=pd.concat([train[["date"]].reset_index(drop=True),pd.DataFrame(train_scaled,columns=featured)],axis=1)
    final_test_scaled=pd.concat([test[["date"]].reset_index(drop=True),pd.DataFrame(test_scaled,columns=featured)],axis=1)

    # Guardamos los resultados en los CSV finales
    final_train_scaled.to_csv(standarized_train,index=False)
    final_test_scaled.to_csv(standarized_test,index=False)
    print(f"Train final tiene {len(final_train_scaled)} filas")
    print(f"Test final tiene {len(final_test_scaled)} filas")



if __name__ == "__main__":
    main()