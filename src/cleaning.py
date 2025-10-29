import pandas as pd
import numpy as np


def basic_validation(df, ref_hotel, ref_seg):
    """
        Nettoie et enrichit un DataFrame hôtelier.

        Étapes principales :
        1. Supprime les lignes sans date_jour.
        2. Convertit les colonnes numériques en float/int et gère les valeurs négatives.
        3. Marque les valeurs irréalistes (ex:rooms_occupied > 5000) comme NaN.
        4. Mappe les codes de segment vers des labels via ref_seg.
        5. Enrichit les métadonnées de l'hôtel via ref_hotel (ville, pays, devise, type_contrat).

        Paramètres:
            df (pd.DataFrame): Données brutes du fichier hôtelier.
            ref_hotel (pd.DataFrame): Table de référence des hôtels.
            ref_seg (pd.DataFrame): Table de référence des segments.

        Retour:
            pd.DataFrame: DataFrame nettoyé et enrichi.
        """
    # Supprimer les lignes sans date_jour
    df = df[~df['date_jour'].isna()].copy()

    # Cast numérique sécurisé
    num_cols = ['ca_ttc', 'rooms_occupied', 'pax', 'enf', 'arrivals']
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

    # Remplacer les valeurs négatives par NaN
    for c in ['ca_ttc', 'rooms_occupied', 'pax', 'arrivals']:
        if c in df.columns:
            df.loc[df[c] < 0, c] = np.nan

    # Limite réaliste pour rooms_occupied
    if 'rooms_occupied' in df.columns:
        df.loc[df['rooms_occupied'] > 5000, 'rooms_occupied'] = pd.NA  # A adapter la limite de chambres occupées

    # Map segment_code -> segment_label
    if 'segment_code' in df.columns:
        seg_map = dict(zip(ref_seg['Code Segment'], ref_seg['Segment']))  # Dict with Segment: Code Segment
        df['segment_label'] = df['segment_code'].map(seg_map).fillna(df['segment_code'])
    df['segment_code'] = df['segment_code'].fillna('AUTRES')
    df['segment_label'] = df['segment_label'].fillna('AUTRES')

    # Enrichir les métadonnées hôtel
    if 'hotel_id' in df.columns:
        hmap = ref_hotel.set_index('ID hotel').to_dict('index')

        def get_meta(hid, field):
            try:
                return hmap.get(hid, {}).get(field)
            except Exception:
                return None

        df['ville'] = df['hotel_id'].apply(lambda x: get_meta(x, 'Ville'))
        df['pays'] = df['hotel_id'].apply(lambda x: get_meta(x, 'Pays'))
        df['devise'] = df['hotel_id'].apply(lambda x: get_meta(x, 'Devise'))
        df['type_contrat'] = df['hotel_id'].apply(lambda x: get_meta(x, 'Type de contrat'))
    return df


def deduplicate(df):
    """
       Supprime les doublons dans le DataFrame.

       Étapes :
       1. Supprime les doublons exacts.
       2. Pour les mêmes combinaisons (hotel_id, date_jour, segment_code, date_extraction),
          garde la dernière ligne basée sur date_extraction.
       Retour:
           pd.DataFrame: DataFrame sans doublons.
    """
    df = df.drop_duplicates()
    subset = ['hotel_id', 'date_jour', 'segment_code', 'date_extraction']
    if all(c in df.columns for c in subset):
        df = df.sort_values(by=['date_extraction']).drop_duplicates(subset=subset,
                                                                    keep='last')  # Keep last based on date_extraction
    return df
