# Pokémon Advanced Analytics Challenge

ETL Pipeline · Feature Engineering · Power Score · Clustering · Type Analysis

Este repositorio contiene una solución completa al Pokémon Advanced Analytics Challenge, implementando un pipeline reproducible de obtención, procesamiento y análisis avanzado de datos provenientes de la PokéAPI. El objetivo es evaluar la fuerza relativa de cada Pokémon mediante un Power Score, analizar la efectividad de tipos y clasificar a las especies en roles estratégicos mediante clustering.

---
pokeapi-challenge/
│
├── data/
│   ├── raw/        # Datos extraídos directamente de la PokéAPI
│   ├── silver/     # Datos normalizados en CSV
│   └── gold/       # Features finales, power scores, clusters, exports
│
├── etl/
│   ├── run_etl_pipeline.py    # Orquestador: ejecuta todo el pipeline
│   ├── extract_raw.py         # Descarga datos desde PokéAPI
│   ├── transform_pokemon.py   # Normalización de Pokémon, stats, tipos y movimientos
│   ├── transform_moves.py     # Normalización de movimientos (moves.csv)
│   └── transform_types.py     # Construcción de matriz 18×18 de efectividad de tipos
│
├── notebooks/
│   ├── 01_eda_pokemon.ipynb           # Exploración y validación del dataset
│   ├── 02_build_features.ipynb        # Feature engineering y metrics avanzadas
│   ├── 03_power_score.ipynb           # Definición del Power Score final
│   ├── 04_type_effectiveness.ipynb    # Análisis de tipos (ofensivo/defensivo)
│   ├── 05_clustering_roles.ipynb      # Clustering + asignación de roles
│   └── 06_final_insights.ipynb        # Resultados finales para el informe
│
└── README.md     # Este documento

---

## 🧩 ¿Qué hace cada módulo del ETL?

1. extract_raw.py
	•	Llama a la PokéAPI.
	•	Extrae:
	•	Pokémon (stats, tipos, movimientos)
	•	Movimientos (power, accuracy, type)
	•	Tipos (efectividad ofensiva y defensiva)
	•	Guarda los resultados en data/raw/*.jsonl.

2. transform_pokemon.py
Transforma la data RAW en tablas limpias en formato CSV:
	•	pokemon.csv — Datos generales por Pokémon
	•	pokemon_stats.csv — 6 stats base por Pokémon
	•	pokemon_types.csv — Tipo 1 y Tipo 2
	•	pokemon_moves.csv — Tabla puente Pokémon ↔ movimientos

3. transform_moves.py
Genera moves.csv con columnas clave:
	•	id, name, type, damage_class,
	•	power, accuracy, pp

4. transform_types.py
Construye:
	•	type_effectiveness.csv
Una matriz completa tipo vs tipo (18×18) con los multiplicadores de daño.

5. run_etl_pipeline.py
Es el orquestador del pipeline completo.
Ejecuta en orden:
	1.	extract_raw.run()
	2.	transform_pokemon.run()
	3.	transform_moves.run()
	4.	transform_types.run()

Genera automáticamente todos los directorios y CSV necesarios en data/raw, data/silver y data/gold.

---

### ⚙️ Cómo correr el ETL completo

Asegúrate de estar en la raíz del proyecto y de tener el entorno virtual activo.
1. Instalar dependencias
    pip install -r requirements.txt
2. Ejecutar pipeline 
    python etl/run_etl_pipeline.py

---

## 🔍 ¿Qué obtengo al final del proyecto?
	•	Un Power Score reproducible por Pokémon.
	•	Rankings: ofensivo, defensivo y global.
	•	Pokémon “value picks” (poder relativo a experiencia).
	•	Matriz completa de efectividad de tipos + rankings ofensivos y defensivos.
	•	Segmentación funcional mediante clustering en 4 roles:
	•	Support / Utility
	•	Bruiser / All-Rounder
	•	Glass Cannon
	•	Powerhouse Tank
	•	Exportables listos para informe (data/gold/exports_for_report/).
