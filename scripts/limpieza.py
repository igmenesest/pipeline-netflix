import pandas as pd
import os
import logging

# Configurar el log
logging.basicConfig(filename='logs/pipeline.log', level=logging.INFO, 
                    format='%(asctime)s | %(levelname)s | %(message)s')

def ejecutar_limpieza():
    try:
        print("--- INICIANDO ETAPA 2: LIMPIEZA Y TRANSFORMACIÓN ---")
        
        # Truco antibugs: si Windows se marea con la ruta, lee el original
        ruta_raw = 'data/raw/netflix_titles.csv'
        if not os.path.exists(ruta_raw):
            ruta_raw = 'netflix_titles.csv'
            
        df = pd.read_csv(ruta_raw)
        
        # 1. Tratar Duplicados
        duplicados_antes = df.duplicated().sum()
        df = df.drop_duplicates()
        print(f"\n[1/4] Duplicados eliminados: {duplicados_antes}")
        
        # 2. Tratar Nulos
        df['director'] = df['director'].fillna('Sin Director')
        df['country'] = df['country'].fillna('Desconocido')
        df = df.dropna(subset=['date_added']) 
        print("[2/4] Valores nulos tratados (imputados y eliminados).")
        
        # 3. Transformaciones (Las 3 exigidas por la pauta)
        df['type'] = df['type'].str.upper()
        df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
        df['año_agregado'] = df['date_added'].dt.year
        print("[3/4] 3 Transformaciones aplicadas (Mayúsculas, Formato Fecha, Columna Nueva).")
        
        # 4. Guardar dataset limpio asegurando que la carpeta exista
        os.makedirs('data/clean', exist_ok=True)
        ruta_clean = 'data/clean/netflix_limpio.csv'
        df.to_csv(ruta_clean, index=False)
        
        logging.info(f"LIMPIEZA OK: Datos guardados en {ruta_clean}")
        print(f"\n[4/4] [ÉXITO] Etapa 2 completada. Archivo guardado en: {ruta_clean}")
        
    except Exception as e:
        logging.error(f"ERROR EN LIMPIEZA: {e}")
        print(f"[ERROR] Ocurrió un problema: {e}")

if __name__ == "__main__":
    ejecutar_limpieza()
