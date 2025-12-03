import json
from pathlib import Path

import pandas as pd

RAW_FILE = Path("data/raw/moves_raw.jsonl")
SILVER_DIR = Path("data/silver")
SILVER_DIR.mkdir(parents=True, exist_ok=True)


def load_raw_moves(path: Path):
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def build_moves_table(raw_moves):
    rows = []

    for m in raw_moves:
        mid = m["id"]
        name = m.get("name")
        move_type = m["type"]["name"] if m.get("type") else None

        damage_class = (
            m["damage_class"]["name"] if m.get("damage_class") else None
        )

        power = m.get("power")          # puede ser None
        accuracy = m.get("accuracy")    # puede ser None
        pp = m.get("pp")                # puntos de poder

        rows.append(
            {
                "id": mid,
                "name": name,
                "type": move_type,
                "damage_class": damage_class,
                "power": power,
                "accuracy": accuracy,
                "pp": pp,
            }
        )

    df_moves = pd.DataFrame(rows).sort_values("id").reset_index(drop=True)
    return df_moves


# ... funciones load_raw_pokemon, build_pokemon_tables, save_tables_csv ...

def run():
    print("==> Leyendo data RAW de movimientos...")
    raw_moves = load_raw_moves(RAW_FILE)
    print(f"   Registros cargados: {len(raw_moves)}")

    print("==> Construyendo tabla moves...")
    df_moves = build_moves_table(raw_moves)
    print("   moves:", df_moves.shape)

    out_path = SILVER_DIR / "moves.csv"
    print(f"==> Guardando CSV en {out_path} ...")
    df_moves.to_csv(out_path, index=False)
    print("==> OK. moves.csv generado.")


if __name__ == "__main__":
    run()