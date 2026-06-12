import sqlite3
import pandas as pd
import logging
import os

# Configurar logs
logging.basicConfig(filename='logs/pipeline.log', level=logging.INFO, 
                    format='%(asctime)s | %(levelname)s | %(message)s')

def ejecutar_carga():
    try:
        print("--- INICIANDO ETAPA 4: CARGA A BASE DE DATOS ---")
        
        # 1. Cargar los datos validados de la etapa 3
        df_validos = pd.read_csv('data/validated/netflix_validos.csv')
        
        # 2. Conectarse a SQLite (creará el archivo pipeline.db automáticamente)
        ruta_bd = 'pipeline.db'
        conn = sqlite3.connect(ruta_bd)
        print("[1/3] Conectado a la base de datos SQLite 'pipeline.db'.")
        
        # 3. Cargar los datos usando Transacciones ACID (COMMIT/ROLLBACK)
        try:
            # El bloque 'with' en sqlite3 maneja la transacción automáticamente [cite: 209]
            with conn:
                df_validos.to_sql('netflix_catalogo', conn, if_exists='replace', index=False)
                logging.info(f"CARGA OK: {len(df_validos)} registros insertados en BD.")
                print(f"[2/3] Transacción exitosa. {len(df_validos)} registros cargados.")
                
        except Exception as e:
            # Si algo falla, se revierte todo (ROLLBACK) [cite: 213, 215]
            logging.error(f"CARGA FALLIDA, EJECUTANDO ROLLBACK: {e}")
            print(f"[ERROR] Falló la transacción. Se ejecutó ROLLBACK. Detalles: {e}")
            conn.rollback()
            raise
            
        # 4. Verificación SQL exigida por la rúbrica [cite: 320]
        print("\n[3/3] Verificando los datos en la Base de Datos con SQL:")
        consulta = "SELECT type, COUNT(*) as cantidad FROM netflix_catalogo GROUP BY type;"
        resultado = pd.read_sql_query(consulta, conn)
        print(resultado)
        
        print("\n[ÉXITO] ¡PIPELINE 100% COMPLETADO! Todo listo para subir a GitHub.")
        
    except Exception as e:
        print(f"[ERROR GENERAL]: {e}")
    finally:
        # Siempre cerrar la conexión [cite: 218]
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    ejecutar_carga()