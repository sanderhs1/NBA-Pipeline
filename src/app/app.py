from flask import Flask, request, render_template
import duckdb
import pandas as pd
from pathlib import Path
from nba_api.stats.static import players

app = Flask(__name__)
db_path = Path("db/nba_stats.duckdb")

all_players = players.get_players()
player_name_to_id = {p['full_name']: p['id'] for p in all_players}
player_names = sorted(player_name_to_id.keys())

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    error = None
    if request.method == "POST":
        player_name = request.form.get("player_name")

        player_id = player_name_to_id.get(player_name)
        if not player_id:
            error = f"Player '{player_name}' not found."
        else:
            query = f"""
                SELECT * FROM gamelog
                WHERE player_id = {player_id}
                ORDER BY game_date
            """
            try:
                con = duckdb.connect(str(db_path))
                results = con.execute(query).fetchdf()
                con.close()
            except Exception as e:
                error = str(e)

    return render_template("index.html", data=results, players=player_names, error=error)

if __name__ == "__main__":
    app.run(debug=True)

