import pandas as pd
import pandera as pa
import os
import logging

# Configurar logs
logging.basicConfig(filename='logs/pipeline.log', level=logging.INFO, 
                    format='%(asctime)s | %(levelname)s | %(message)s')

def ejecutar_validacion():
    try:
        print("--- INICIANDO ETAPA 3: VALIDACIÓN ---")
        
        # Crear carpetas de destino por si acaso
        os.makedirs(os.path.join('data', 'validated'), exist_ok=True)
        os.makedirs(os.path.join('data', 'errors'), exist_ok=True)
        
        # Cargar los datos limpios de la etapa 2
        df = pd.read_csv('data/clean/netflix_limpio.csv')
        
        # --- A. VALIDACIÓN ESTRUCTURAL (Con Pandera - Mínimo 3) ---
        # 1. release_year debe ser un año razonable (1900-2030)
        # 2. type debe ser exactamente MOVIE o TV SHOW
        # 3. show_id debe empezar con la letra 's'
        esquema = pa.DataFrameSchema({
            "release_year": pa.Column(int, pa.Check.in_range(1900, 2030), nullable=True),
            "type": pa.Column(str, pa.Check.isin(["MOVIE", "TV SHOW"]), nullable=True),
            "show_id": pa.Column(str, pa.Check.str_startswith("s"), nullable=True)
        })
        
        errores_indices = set()
        
        try:
            esquema.validate(df, lazy=True)
            print("[1/3] Validación Estructural con Pandera: OK")
        except pa.errors.SchemaErrors as err:
            print("[1/3] Pandera detectó errores estructurales que serán separados.")
            if 'index' in err.failure_cases.columns:
                errores_indices.update(err.failure_cases['index'].dropna().tolist())

        # --- B. VALIDACIÓN SEMÁNTICA (Reglas de Negocio - Mínimo 2) ---
        print("[2/3] Aplicando Validaciones Semánticas (Reglas lógicas)...")
        for idx, row in df.iterrows():
            # Regla 1: Una película no puede agregarse a Netflix ANTES de su año de lanzamiento
            if pd.notna(row['año_agregado']) and pd.notna(row['release_year']):
                if row['año_agregado'] < row['release_year']:
                    errores_indices.add(idx)
            
            # Regla 2: Si es una Película ('MOVIE'), su duración debe contener la palabra 'min'
            if row['type'] == 'MOVIE' and pd.notna(row['duration']):
                if 'min' not in str(row['duration']):
                    errores_indices.add(idx)

        # --- C. SEPARAR Y GUARDAR ---
        # Separamos los buenos de los malos
        df_errores = df.loc[list(errores_indices)]
        df_validos = df.drop(index=list(errores_indices))
        
        # Rutas
        ruta_validos = 'data/validated/netflix_validos.csv'
        ruta_errores = 'data/errors/netflix_errores.csv'
        
        # Guardar
        df_validos.to_csv(ruta_validos, index=False)
        df_errores.to_csv(ruta_errores, index=False)
        
        logging.info(f"VALIDACIÓN OK: {len(df_validos)} registros válidos y {len(df_errores)} errores separados.")
        print(f"[3/3] Separación lista -> Válidos: {len(df_validos)} | Con Errores: {len(df_errores)}")
        print(f"\n[ÉXITO] Etapa 3 completada. Archivos en data/validated/ y data/errors/")
        
    except Exception as e:
        logging.error(f"ERROR EN VALIDACIÓN: {e}")
        print(f"[ERROR] Ocurrió un problema: {e}")

if __name__ == "__main__":
    ejecutar_validacion()