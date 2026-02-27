# TFG - Análisis de precios de Solana

Este es el repositorio para mi TFG de análisis de precios de Solana.

## Preparación

1. Descarga uv desde https://docs.astral.sh/uv/
2. Clona este repositorio y accede a la carpeta clonada
3. Ejecuta (desde la raíz del repo)

```bash
uv venv
uv sync
```

4. Prueba que funciona ejecutando `uv run python -m src.healthcheck`, deberia imprimir `OK`
5. Para ejecutar los scripts haz `uv run python -m src.nombre_sin_py`, por ejemplo `uv run python -m src.healthcheck`

## Orden de ejecución de scripts

Los hay que ejecutar con este formato: `uv run python -m src.filename`.

1. download_market_data (descarga los datos de Yahoo Finance) -> Devuelve `raw/sol_usd_ohlcv.csv`
2. download_gdelt_data (descarga el tone score) -> Devuelve `raw/gdelt_solana_tone.csv`
3. create_market_vars (crea las demás variables de mercado) -> Devuelve `processed/sol_usd_market_vars.csv`
4. create_tone_vars (crea las demás variables del tone score) -> Devuelve `processed/gdelt_solana_tone_vars.csv`
5. merge_datasets (junta ambos datasets) -> Devuelve `processed/merged_dataset.csv`
6. split_datasets (separa ambos datasets en train y test) -> Devuelve `processed/train.csv` y `processed/test.csv`
7. standarize_dataset (estandariza ambos datasets, dando resultado a los datasets finales) -> Devuelve `processed/final_test.csv` y `processed/final_train.csv`

> Los datos se separan cronológicamente, 80% para train y 20% para test
