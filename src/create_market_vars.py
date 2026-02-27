import numpy as np
import pandas as pd
from pathlib import Path

def create_rsi(close:pd.Series, window:int=14)->pd.Series: # Calculamos el RSI, +70% suele ser sobrecompra y menos de 30% sobreventa
    # Primero se calculan los cambios diarios del precio (delta), se separan subidas y bajadas, se calculan las medias suavizadas de ganancias/pérdidas (RS) y se aplica la fórmula del RSI que es RSI=100-(100/(1+RS)), de todo esto hay muchísima información en Internet
    # Cambios diarios del precio
    delta=close.diff()
    
    # Se separan pérdidas y ganancias
    gain=delta.clip(lower=0)
    loss=-delta.clip(upper=0)

    # Medias suavizadas

    avg_gain=gain.ewm(alpha=1/window, adjust=False).mean()
    avg_loss=loss.ewm(alpha=1/window, adjust=False).mean()

    # Se calcula RS (fuerza relativa)
    rs=avg_gain/avg_loss

    # Fórmula final del RSI

    rsi=100-(100/(1+rs))
    return rsi

def main():
    # Carga correcta de los datos y especificación de donde guardaremos el output
    project_root=Path(__file__).resolve().parents[1]
    raw_dir=project_root / "data" / "raw"
    processed_dir=project_root / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    input_path=raw_dir / "sol_usd_ohlcv.csv"
    output_path=processed_dir / "sol_usd_market_vars.csv"

    # Cargo datos
    df=pd.read_csv(input_path)
    # Pasamos la fecha a formato datetime
    df["Date"]=pd.to_datetime(df["Date"])

    # Lo ordenamos por orden cronológico ascendente
    df=df.sort_values("Date").reset_index(drop=True)

    # Eliminamos las filas con valores nulos
    df=df.dropna(subset=["Open", "High", "Low", "Close", "Volume"]).reset_index(drop=True)

    # Logs del precio de cierre ( para calcular log retornos)
    df["log_close"]=np.log(df["Close"])

    # Calcular log returnos diarios
    df["log_return"]=df["log_close"].diff()

    # Rango diario (high-low)
    df["range"]=df["High"]-df["Low"]

    # Rango relativo (high-low)/close
    df["range_rel"]=df["range"]/df["Close"]

    # Retorno simple diario
    df["return"]=df["Close"].pct_change()

    # Calculo SMA (media móvil simple, el promedio de los últimos x días)
    df["sma_7"]=df["Close"].rolling(7).mean()
    df["sma_14"]=df["Close"].rolling(14).mean()
    df["sma_30"]=df["Close"].rolling(30).mean()

    # Calculamos EMA (media móvil exponencial)
    df["ema_12"]=df["Close"].ewm(span=12, adjust=False).mean()
    df["ema_26"]=df["Close"].ewm(span=26, adjust=False).mean()

    # RSI de los últimos 14 días
    df["rsi_14"]=create_rsi(df["Close"],window=14)

    # Calculo MACD (EMA12-EMA26), signal(EMA9 del MACD) y la intensidad del cruce (MACD-signal)
    df["macd"]=df["ema_12"]-df["ema_26"]
    df["macd_signal"]=df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_hist"]=df["macd"]-df["macd_signal"]

    # Calculo desviación estándar rolling de los log-retornos (volatilidad)
    df["vol_7"]=df["log_return"].rolling(7).std()
    df["vol_14"]=df["log_return"].rolling(14).std()
    df["vol_30"]=df["log_return"].rolling(30).std()

    # Retorno acumulado semanal (mediante log-retornos)
    df["log_return_7d"]=df["log_return"].rolling(7).sum()

    # Guardamos las columnas que queremos para el conjunto de datos de salida
    output=df[[
        "Date", "Open", "High", "Low", "Close", "Volume",
        "log_return", "return",
        "range", "range_rel",
        "sma_7", "sma_14", "sma_30",
        "ema_12", "ema_26",
        "rsi_14",
        "macd", "macd_signal", "macd_hist",
        "vol_7", "vol_14", "vol_30",
        "log_return_7d",]].copy()
    

    # Ordenamos por fecha
    output = output.sort_values("Date").reset_index(drop=True)

    # Lo guardamos en el CSV
    output.to_csv(output_path, index=False)
    print(f"Guardadas {len(output)} filas")


if __name__ == "__main__":
    main()
