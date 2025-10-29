from pathlib import Path
from datetime import datetime


def parse_filename(filename):
    """
       Parse le nom du fichier pour extraire l'ID de l'hôtel, le nom et la date d'extraction.

       Format attendu : {ID_HOTEL}_{NOM_HOTEL}_{DATE_EXTRACTION}.csv
       Exemple : 007_JamesBond_20251024.csv

       Paramètres:
           filename (str): Nom du fichier CSV.

       Retour:
           dict: {
               'hotel_id': str,
               'hotel_name': str,
               'date_extraction': datetime.date
           }
    """
    base = Path(filename).stem
    # allow names like HMM_past_MickeyMouse_20251024 or HMM_futur_MickeyMouse_20251024
    parts = base.split('_')
    # heuristique: last token is date, first token is id
    hotel_id = parts[0]
    try:
        date_extr = datetime.strptime(parts[-1], "%Y%m%d").date()
    except ValueError:
        date_extr = None
    # name is everything between first and last
    try:
        hotel_name = "_".join(parts[1:-1]) if len(parts) > 2 else None
    except ValueError:
        hotel_name = None
    return {"hotel_id": hotel_id, "hotel_name": hotel_name, "date_extraction": date_extr}
