import json
from pathlib import Path

import pandas as pd

RAW_FILE = Path("data/raw/types_raw.jsonl")
SILVER_DIR = Path("data/silver")
SILVER_DIR.mkdir(parents=True, exist_ok=True)


def load_raw_types(path: Path):
    """Lee el JSONL crudo de tipos y devuelve una lista de dicts."""
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def build_type_effectiveness_table(raw_types):
    """
    Construye una tabla completa attacking_type x defending_type
    con el multiplicador de daño (0, 0.5, 1, 2...).

    Se basa en damage_relations de la PokéAPI:
      - double_damage_to      -> 2.0
      - half_damage_to        -> 0.5
      - no_damage_to          -> 0.0
      (Si no aparece en ninguna de esas listas => 1.0)
    """

    # 1) Indexar por nombre de tipo para acceso rápido
    type_by_name = {t["name"]: t for t in raw_types}

    # 2) Lista de todos los tipos (incluye "shadow", "unknown" si existen)
    type_names = sorted(type_by_name.keys())

    rows = []

    for attacking in type_names:
        t = type_by_name[attacking]
        dr = t.get("damage_relations", {})

        # Extraemos las listas de tipos objetivo para cada relación
        double_to = {x["name"] for x in dr.get("double_damage_to", [])}
        half_to = {x["name"] for x in dr.get("half_damage_to", [])}
        no_to = {x["name"] for x in dr.get("no_damage_to", [])}

        for defending in type_names:
            if defending in double_to:
                mult = 2.0
            elif defending in half_to:
                mult = 0.5
            elif defending in no_to:
                mult = 0.0
            else:
                mult = 1.0

            rows.append(
                {
                    "attacking_type": attacking,
                    "defending_type": defending,
                    "multiplier": mult,
                }
            )

    df = pd.DataFrame(rows).sort_values(
        ["attacking_type", "defending_type"]
    ).reset_index(drop=True)

    return df



def run():
    print("==> Leyendo data RAW de tipos...")
    raw_types = load_raw_types(RAW_FILE)
    print(f"   Registros cargados: {len(raw_types)}")

    print("==> Construyendo tabla type_effectiveness...")
    df_eff = build_type_effectiveness_table(raw_types)
    print("   type_effectiveness:", df_eff.shape)

    out_path = SILVER_DIR / "type_effectiveness.csv"
    print(f"==> Guardando CSV en {out_path} ...")
    df_eff.to_csv(out_path, index=False)
    print("==> OK. type_effectiveness.csv generado.")


if __name__ == "__main__":
    run()