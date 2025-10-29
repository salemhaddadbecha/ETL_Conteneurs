import pandas as pd
from pathlib import Path
from src.utils import parse_filename


def load_csv_auto(path):
    """
        Charge un fichier CSV hôtelier et détecte automatiquement le format PMS1 ou PMS2.

        Étapes :
        1. Parse le nom du fichier pour récupérer hotel_id, hotel_name, date_extraction.
        2. Charge le CSV en string.
        3. Détecte le type de PMS et applique le mapping correspondant (_map_pms1 ou _map_pms2).
        4. Si aucun format reconnu, crée des colonnes par défaut avec "UNKNOWN".

        Paramètres:
            path (str | Path): Chemin du fichier CSV.

        Retour:
            pd.DataFrame: DataFrame normalisé.
    """
    path = Path(path)
    meta = parse_filename(path.name)
    df = pd.read_csv(path, dtype=str)
    df.columns = [c.strip() for c in df.columns]

    # Détection du type de fichier
    if 'JOUR' in df.columns or 'SEGMENTATION' in df.columns:
        return _map_pms1(df, meta, 'PMS1')
    elif 'CHAR_BUSINESS_DATE' in df.columns or 'MASTER_VALUE' in df.columns or 'RESERVATION_DATE' in df.columns:
        pms_type = 'PMS2'
        return _map_pms2(df, meta, pms_type)
    else:
        df['date_parsed'] = pd.to_datetime(df.iloc[:, 0], errors='coerce')  # best effort
        df['hotel_id'] = meta['hotel_id']
        df['hotel_name'] = meta['hotel_name']
        df['date_extraction'] = meta['date_extraction']
        df['pms_type'] = 'UNKNOWN'
        return df


def _map_pms2(df, meta, pms_type):
    """
    Normalise les fichiers PMS2 (HMM), passé ou futur.

    Paramètres:
        df (pd.DataFrame): Données brutes PMS2.
        meta (dict): Métadonnées extraites du nom de fichier.
        pms_type (str): Type PMS ('PMS2').

    Retour:
        pd.DataFrame: DataFrame normalisé.
    """
    if 'CHAR_BUSINESS_DATE' in df.columns:
        file_type = 'past'
        df = df.rename(columns={
            'CHAR_BUSINESS_DATE': 'date_jour',
            'MASTER_VALUE': 'segment_code',
            'NO_DEFINITE_ROOMS': 'rooms',
            'IN_GUEST': 'guests',
            'REVENUE': 'revenue',
            'PER_DOUBLE_MKT': 'double_occ',
            'ARRIVAL_MKT': 'arrivals'
        })
    elif 'RESERVATION_DATE' in df.columns:
        file_type = 'future'
        df = df.rename(columns={
            'CHAR_RESERVATION_DATE': 'date_jour',
            'MARKET_CODE_SEQ': 'segment_code',
            'NO_DEFINITE_ROOMS': 'rooms',
            'NO_OF_GUESTS': 'guests',
            'TOTAL_REVENUE': 'revenue',
            'GUEST_MKT': 'guest_mkt',
            'DOUBLE_OCC_MKT': 'double_occ'
        })
    else:
        raise ValueError("Format inconnu pour PMS2 (ni past ni futur)")

    # Conversion types
    df['date_jour'] = pd.to_datetime(df['date_jour'], format='%d.%m.%y', errors='coerce')
    df['rooms'] = pd.to_numeric(df['rooms'], errors='coerce')
    df['guests'] = pd.to_numeric(df['guests'], errors='coerce')
    df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')

    # Ajout des métadonnées
    df['hotel_id'] = meta['hotel_id']
    df['hotel_name'] = meta['hotel_name']
    df['date_extraction'] = meta['date_extraction']
    df['pms_type'] = pms_type
    df['file_type'] = file_type

    return df


def _map_pms1(df, meta, pms_type):
    """
    Normalise les fichiers PMS1 (classique).

    Paramètres:
        df (pd.DataFrame): Données brutes PMS1.
        meta (dict): Métadonnées extraites du nom de fichier.
        pms_type (str): Type PMS ('PMS1').

    Retour:
        pd.DataFrame: DataFrame normalisé.
    """
    m = {
        'JOUR': 'date_jour',
        'SEGMENTATION': 'segment_code',
        'C.A. HBGT T.T.C.': 'ca_ttc',
        'OCCUP.': 'rooms_occupied',
        'PAX': 'pax',
        'ENF': 'enf',
        'ARRIVEES': 'arrivals',
        'NTES': 'ntes'
    }
    df = df.rename(columns=m)

    # Ajout métadonnées
    df['hotel_id'] = meta['hotel_id']
    df['hotel_name'] = meta['hotel_name']
    df['date_extraction'] = meta['date_extraction']
    df['pms_type'] = pms_type

    # Nettoyage numérique
    df['ca_ttc'] = (
        df['ca_ttc']
        .replace(r'Value\s*:\s*', '', regex=True)  # "Value : 9800" => "9800"
        .replace('"', '', regex=True)  # '"350"' => '350'
        .astype(str)
        .str.replace(',', '.')  # '1,23' => '1.23'
        .replace('', None)
    )

    # Conversion date
    df['date_jour'] = pd.to_datetime(df['date_jour'], errors='coerce',
                                     dayfirst=True)  # Assurer le bon ordre DD/MM/YYYY et mettre NAT pour les dates en erreurs
    return df
