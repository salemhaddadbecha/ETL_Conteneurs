import pandas as pd
from pathlib import Path
from src.ingestion import load_csv_auto
from src.cleaning import basic_validation, deduplicate
from src.modeling import build_final_model
from src.db import upsert_dataframe

# --- Définition des chemins ---
input_file = "data/input/007_JamesBond_20251024.csv"
# input_file = "data/input/HMM_past_MickeyMouse_20251024.csv"
ref_hotel_path = "data/refs/ref_hotel.csv"
ref_seg_path = "data/refs/ref_segmentation.csv"
output_folder = "data/output"

#  Étape 1 : Chargement des données
df_raw = load_csv_auto(input_file)
ref_hotel = pd.read_csv(ref_hotel_path, dtype=str)
ref_seg = pd.read_csv(ref_seg_path, dtype=str)

# --- Étape 2 : Nettoyage et validation ---
df_clean = basic_validation(df_raw, ref_hotel, ref_seg)
df_nodup = deduplicate(df_clean)

# --- Étape 3 : Construction du modèle final ---
df_final = build_final_model(df_nodup)
print(df_final)

# --- Étape 4 : Sauvegarde des résultats en parquet ---
out_path = Path(output_folder) / (Path(input_file).stem + ".parquet")
df_final.to_parquet(out_path, index=False)

# --- Étape 5 : Mise à jour / insertion dans PostgreSQL ---
upsert_dataframe(df_final)

print(f"Données insérées/mises à jour dans PostgreSQL: {len(df_final)} lignes")
