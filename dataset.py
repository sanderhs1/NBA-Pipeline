import duckdb

conn = duckdb.connect('nba_stats.duckdb')

tables = conn.execute("SHOW TABLES").fetchall()
print("Tables:", tables)

rows = conn.execute("SELECT * FROM player_stats LIMIT 5").fetchall()
for row in rows:
    print(row)

conn.close()