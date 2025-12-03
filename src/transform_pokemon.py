import json
from pathlib import Path

import pandas as pd

RAW_FILE = Path("data/raw/pokemon_raw.jsonl")
SILVER_DIR = Path("data/silver")
SILVER_DIR.mkdir(parents=True, exist_ok=True)


def load_raw_pokemon(path: Path):
    """Lee el JSONL crudo de Pokémon y devuelve una lista de dicts."""
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def build_pokemon_tables(raw_pokemon):
    """
    A partir del JSON bruto de /pokemon crea:
      - pokemon
      - pokemon_stats
      - pokemon_types
      - pokemon_moves
    """

    pokemon_rows = []
    stats_rows = []
    types_rows = []
    moves_rows = []

    for p in raw_pokemon:
        pid = p["id"]

        # ---- Tabla pokemon ----
        total_base_stats = sum(s["base_stat"] for s in p.get("stats", []))

        pokemon_rows.append(
            {
                "id": pid,
                "name": p.get("name"),
                "height": p.get("height"),
                "weight": p.get("weight"),
                "base_experience": p.get("base_experience"),
                "total_base_stats": total_base_stats,
            }
        )

        # ---- Tabla pokemon_stats ----
        for s in p.get("stats", []):
            stats_rows.append(
                {
                    "pokemon_id": pid,
                    "stat_name": s["stat"]["name"],   # hp, attack, defense, ...
                    "stat_value": s["base_stat"],
                    "effort": s.get("effort", None),
                }
            )

        # ---- Tabla pokemon_types ----
        for t in p.get("types", []):
            types_rows.append(
                {
                    "pokemon_id": pid,
                    "slot": t.get("slot"),            # 1, 2...
                    "type": t["type"]["name"],        # fire, water, etc.
                }
            )

        # ---- Tabla pokemon_moves ----
        for m in p.get("moves", []):
            move_url = m["move"]["url"]
            # URL típica: https://pokeapi.co/api/v2/move/13/
            move_id = int(move_url.rstrip("/").split("/")[-1])

            moves_rows.append(
                {
                    "pokemon_id": pid,
                    "move_id": move_id,
                    "move_name": m["move"]["name"],
                }
            )

    # Convertir a DataFrames
    df_pokemon = pd.DataFrame(pokemon_rows).sort_values("id").reset_index(drop=True)
    df_stats = pd.DataFrame(stats_rows).sort_values(["pokemon_id", "stat_name"]).reset_index(drop=True)
    df_types = pd.DataFrame(types_rows).sort_values(["pokemon_id", "slot"]).reset_index(drop=True)
    df_moves = pd.DataFrame(moves_rows).sort_values(["pokemon_id", "move_id"]).reset_index(drop=True)

    return df_pokemon, df_stats, df_types, df_moves


def save_tables_csv(df_pokemon, df_stats, df_types, df_moves, out_dir: Path):
    """
    Guarda las tablas en capa SILVER en formato CSV.
    """
    df_pokemon.to_csv(out_dir / "pokemon.csv", index=False)
    df_stats.to_csv(out_dir / "pokemon_stats.csv", index=False)
    df_types.to_csv(out_dir / "pokemon_types.csv", index=False)
    df_moves.to_csv(out_dir / "pokemon_moves.csv", index=False)



def run():
    print("==> Leyendo data RAW de Pokémon...")
    raw_pokemon = load_raw_pokemon(RAW_FILE)
    print(f"   Registros cargados: {len(raw_pokemon)}")

    print("==> Construyendo tablas normalizadas...")
    df_pokemon, df_stats, df_types, df_moves = build_pokemon_tables(raw_pokemon)

    print("   pokemon:", df_pokemon.shape)
    print("   pokemon_stats:", df_stats.shape)
    print("   pokemon_types:", df_types.shape)
    print("   pokemon_moves:", df_moves.shape)

    print("==> Guardando CSV en data/silver ...")
    save_tables_csv(df_pokemon, df_stats, df_types, df_moves, SILVER_DIR)
    print("==> OK. Tablas SILVER (CSV) generadas.")


if __name__ == "__main__":
    run()