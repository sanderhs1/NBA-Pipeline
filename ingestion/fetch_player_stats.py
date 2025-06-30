import os
from datetime import datetime
import pandas as pd
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
from nba_api.stats.library.http import NBAStatsHTTP

def get_player_id(player_name):
    results = players.find_players_by_full_name(player_name)
    if not results:
        raise ValueError(f"Player '{player_name}' not found.")
    return results[0]['id']

def fetch_player_stats(player_id: int, season: str) -> pd.DataFrame:
    gamelog = playergamelog.PlayerGameLog(player_id=player_id, season=season, season_type_all_star='Regular Season')
    df = gamelog.get_data_frames()[0]
    return df

def save_to_csv(df: pd.DataFrame, player_name: str, output_dir: str = "data/raw"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{player_name.replace(' ', '_')}_gamelog_{timestamp}.csv"
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)
    print(f"✅ Saved {len(df)} records to {filepath}")

def main():
    player_name = "LeBron James"
    season = "2023"

    print(f"📥 Fetching game logs for {player_name} ({season})")
    player_id = get_player_id(player_name)
    df = fetch_player_stats(player_id, season)
    save_to_csv(df, player_name)

if __name__ == "__main__":
    main()