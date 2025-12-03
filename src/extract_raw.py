import os
import json
import time
from pathlib import Path

import requests

BASE_URL = "https://pokeapi.co/api/v2"
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def _save_jsonl(path: Path, records):
    """Guarda una lista de dicts en JSONL."""
    with path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")


def _get_json(url: str):
    """Wrapper simple con pequeño retry/backoff."""
    for attempt in range(3):
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        time.sleep(1 + attempt)
    resp.raise_for_status()


# -------------------------
# 1) POKÉMON RAW
# -------------------------

def extract_pokemon_raw(limit: int = 2000):
    """
    Descarga el detalle completo de todos los Pokémon.
    Guarda cada respuesta de /pokemon/{id} como una línea en pokemon_raw.jsonl.
    """
    print("==> Extrayendo listado de Pokémon...")
    url = f"{BASE_URL}/pokemon?limit={limit}&offset=0"
    data = _get_json(url)
    results = data["results"]  # [{name, url}, ...]

    print(f"   Encontrados {len(results)} Pokémon. Descargando detalle...")
    pokemon_records = []
    for i, p in enumerate(results, start=1):
        detail = _get_json(p["url"])
        pokemon_records.append(detail)

        if i % 100 == 0:
            print(f"   Pokémon descargados: {i}")

    out_path = RAW_DIR / "pokemon_raw.jsonl"
    _save_jsonl(out_path, pokemon_records)
    print(f"==> pokemon_raw.jsonl guardado en {out_path} ({len(pokemon_records)} registros)")


# -------------------------
# 2) MOVES RAW
# -------------------------

def extract_moves_raw(limit: int = 2000):
    """
    Descarga el detalle de todos los movimientos de la API.
    Guarda cada respuesta de /move/{id} como una línea en moves_raw.jsonl.
    """
    print("==> Extrayendo listado de movimientos...")
    url = f"{BASE_URL}/move?limit={limit}&offset=0"
    data = _get_json(url)
    results = data["results"]  # [{name, url}, ...]

    print(f"   Encontrados {len(results)} movimientos. Descargando detalle...")
    move_records = []
    for i, m in enumerate(results, start=1):
        detail = _get_json(m["url"])
        move_records.append(detail)

        if i % 100 == 0:
            print(f"   Movimientos descargados: {i}")

    out_path = RAW_DIR / "moves_raw.jsonl"
    _save_jsonl(out_path, move_records)
    print(f"==> moves_raw.jsonl guardado en {out_path} ({len(move_records)} registros)")


# -------------------------
# 3) TYPES RAW
# -------------------------

def extract_types_raw():
    """
    Descarga el detalle de todos los tipos.
    Guarda cada respuesta de /type/{id} como una línea en types_raw.jsonl.
    """
    print("==> Extrayendo listado de tipos...")
    url = f"{BASE_URL}/type?limit=200&offset=0"
    data = _get_json(url)
    results = data["results"]  # [{name, url}, ...]

    print(f"   Encontrados {len(results)} tipos. Descargando detalle...")
    type_records = []
    for i, t in enumerate(results, start=1):
        detail = _get_json(t["url"])
        type_records.append(detail)

    out_path = RAW_DIR / "types_raw.jsonl"
    _save_jsonl(out_path, type_records)
    print(f"==> types_raw.jsonl guardado en {out_path} ({len(type_records)} registros)")


# -------------------------
# MAIN
# -------------------------

def run():
    extract_pokemon_raw(limit=2000)
    extract_moves_raw(limit=2000)
    extract_types_raw()


if __name__ == "__main__":
    run()