from pathlib import Path
import sys

# 1) Asegurar que la raíz del proyecto esté en sys.path
#    (un nivel por encima de esta carpeta "etl")
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from src.extract_raw import run as run_extract_raw
from src.transform_pokemon import run as run_transform_pokemon
from src.transform_moves import run as run_transform_moves
from src.transform_types import run as run_transform_types


def run_etl_pipeline():
    print("========== INICIO ETL POKÉMON ==========")

    print("\n[1/4] EXTRACT RAW ...")
    run_extract_raw()

    print("\n[2/4] TRANSFORM POKÉMON ...")
    run_transform_pokemon()

    print("\n[3/4] TRANSFORM MOVES ...")
    run_transform_moves()

    print("\n[4/4] TRANSFORM TYPES ...")
    run_transform_types()

    print("\n========== FIN ETL POKÉMON ==========")


if __name__ == "__main__":
    run_etl_pipeline()