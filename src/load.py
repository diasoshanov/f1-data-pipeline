import logging
import os
import json
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

COLUMNS = [
    'season', 'round', 'race_name', 'race_date', 'driver_id',
    'driver_name', 'constructor', 'grid', 'position', 'points', 'status',
]


def get_connection():
    """Подключение к Postgres, параметры из .env."""
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=5432,
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
    )


def load_results(rows):
    """Записать строки в raw.race_results (upsert)."""
    cols = ', '.join(COLUMNS)

    # колонки для обновления: все, кроме ключевых
    key_cols = ['season', 'round', 'driver_id']
    update_cols = [c for c in COLUMNS if c not in key_cols]
    set_clause = ', '.join(f'{c} = EXCLUDED.{c}' for c in update_cols)

    sql = f"""
        INSERT INTO raw.race_results ({cols})
        VALUES %s
        ON CONFLICT (season, round, driver_id)
        DO UPDATE SET {set_clause}
    """

    values = [tuple(r[c] for c in COLUMNS) for r in rows]

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            execute_values(cur, sql, values)
        conn.commit()
        logging.info('Записано строк: %s', len(values))
    finally:
        conn.close()

def load_from_file(path):
    """Прочитать JSON и записать строки в Postgres."""
    with open(path, 'r', encoding='utf-8') as file:
        rows = json.load(file)
    logging.info('Прочитано строк из файла: %s', len(rows))
    load_results(rows)


if __name__ == '__main__':
    from extract import fetch_results
    logging.basicConfig(level=logging.INFO)
    rows = fetch_results(2024)
    load_results(rows)