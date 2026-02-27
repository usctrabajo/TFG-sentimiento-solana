import pandas as pd
import requests
from pathlib import Path
from datetime import datetime
import time
import random



# Para descargar el Average Tone diario
def get_gdelt_data(session:requests.Session, start_date:pd.Timestamp, end_date:pd.Timestamp):
    # La URL de la API de GDELT (docs en https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)
    endpoint_url="https://api.gdeltproject.org/api/v2/doc/doc"
    

    # Headers para evitar tantas limitaciones de la API
    headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/145.0.0.0 Safari/537.36",
    "Accept": "application/json",
    }
    # Para que cuadren los días
    start_dt=pd.to_datetime(start_date).replace(hour=0, minute=0,second=0)
    end_dt=pd.to_datetime(end_date).replace(hour=23, minute=59,second=59)

    # Los parámetros que enviaremos para la consulta
    params={
        "query": "Solana", # Palabra clave e idioma
        "mode": "TimelineTone", # Average Tone
        "startdatetime": start_dt.strftime("%Y%m%d%H%M%S"), # Formato de fecha que exige GDELT
        "enddatetime": end_dt.strftime("%Y%m%d%H%M%S"),
        "format": "json", # Formato de la respuesta
    }

    for attempt in range(8): # Intentos por si hay errores
        try:
            response=session.get(endpoint_url, params=params,headers=headers, timeout=50) # Hacemos la petición
        except requests.RequestException as e:
            # Manejamos errores y esperamos, vamos a esperar para no sobrepasar los limites de la API
            wait=min(60*(2**attempt), 600)+random.uniform(1,3)
            print(f"Error: {e} . Espera {wait} segundos")
            time.sleep(wait)
            continue
            

        # Si nos lo devueelve en formato JSON obtenemos la serie
        if response.status_code==200:
            if("application/json") in response.headers.get("Content-Type",""):
                # Obtener la respuesta en formato JSON
                data=response.json()
                # Average Tone
                series=data["timeline"][0]["data"]
                # Para agregar las filas
                rows=[]
                for item in series:
                    dt=pd.to_datetime(item["date"], format="%Y%m%dT%H%M%SZ", utc=True).date()
                    rows.append({"date": dt, "tone_score": float(item["value"])})
                return rows
            else:
                print("No se ha devuelto un JSON")
                # Imprimir lo que nos devolvio en vez de JSON
                print(response.text)
                return []
            
        # Si obtenemos una respuesta de demasiadas peticiones
        if response.status_code==429:
            # Vemos si la respuesta nos dice cuanto tenemos que esperar, si no lo decidimos nosotros
            retry_after=response.headers.get("Retry-After")
            if retry_after is not None:
                try:
                    wait=int(retry_after)
                except ValueError:
                    wait=60*(attempt+1) # Espera 60 segundos, si falla 120 y si vuelve a fallar 180, etc...
            else:
                wait=min(60*(2**attempt), 900) # Duplica el tiempo de espera hasta alcanzar 15 mins
            wait=wait+random.uniform(0,3)
            print(f"Demasiadas requests, espera {wait} segundos")
            time.sleep(wait)
            continue
        
        print("ERROR")
        print(response.text)
        raise RuntimeError(f"Código de error: {response.status_code}")
    raise RuntimeError("Falló varias veces")



def main():
    # Establecemos la ruta de descarga
    project_root=Path(__file__).resolve().parents[1]
    raw_dir=project_root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    output_path=raw_dir / "gdelt_solana_tone.csv"

    # Definimos las fechas del período de los que vamos a obtener los datos
    start_date="2021-02-01"
    end_date=datetime.today().strftime("%Y-%m-%d")


    # Las obtenemos con una misma sesión
    with requests.Session() as session:
        rows=get_gdelt_data(session, start_date, end_date)

    
    # Creamos el DataFrame final
    df=pd.DataFrame(rows)

    # Lanzamos error si está vacío
    if df.empty:
        raise RuntimeError("No se descargó correctamente")
    
    # Ordenamos por fecha
    df = df.sort_values("date").reset_index(drop=True)
    
    # Lo guardamos en un CSV
    df.to_csv(output_path, index=False)

    print("Se guardó correctamente")
    print(f"Hay {len(df)} días")

if __name__ == "__main__":
    main()
