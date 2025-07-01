import duckdb
db_path = "db/nba_stats.duckdb"

con = duckdb.connect(db_path)
seasons = con.execute("SELECT DISTINCT season_id FROM gamelog ORDER BY season_id").fetchall()
con.close()

print("Seasons in DB:")
for s in seasons:
    print(s[0])