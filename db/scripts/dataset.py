import duckdb
from pathlib import Path

def load_csv_to_duckdb(csv_path, db_path="db/nba_stats.duckdb", table_name="gamelog"):
    conn = duckdb.connect(db_path)
    csv_path = Path(csv_path)

    conn.execute(f"""
        CREATE OR REPLACE TABLE {table_name} AS 
        SELECT * FROM read_csv_auto('{csv_path.as_posix()}');
    """)

    print(f"Loaded {csv_path.name} into {table_name} table in {db_path}")
    conn.close()

if __name__ == "__main__":
    csv_file = ""
    load_csv_to_duckdb(csv_file)