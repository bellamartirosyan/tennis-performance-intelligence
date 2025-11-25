# test_project.py
# This script tests imports and basic function calls in your src package

# Import functions from your src modules
from src.data_processing import load_matches
from src.elo_model import compute_elo

from src.monte_carlo_sim import simulate_tournament
from src.forecast import forecast_matches

def main():
    print("Testing project setup...")

    # Test data_processing
    try:
        test_df = load_matches("data/raw/atp_matches_2024.csv")
        print("✅ load_matches works. Data shape:", test_df.shape)
    except Exception as e:
        print("❌ load_matches failed:", e)

    # Test elo_model (dummy test)
    try:
        elo = compute_elo(1500, 1400)
        print("✅ compute_elo works. Sample output:", elo)
    except Exception as e:
        print("❌ compute_elo failed:", e)

    # Test monte_carlo_sim (dummy test)
    try:
        winner = simulate_tournament(["Player1", "Player2", "Player3"])
        print("✅ simulate_tournament works. Winner sample:", winner)
    except Exception as e:
        print("❌ simulate_tournament failed:", e)

    # Test forecast (dummy test)
    try:
        top_players = [{"name":"Player1","rank":1}, {"name":"Player2","rank":2}]
        forecast = forecast_matches(top_players)
        print("✅ forecast_matches works. Sample output:\n", forecast.head())
    except Exception as e:
        print("❌ forecast_matches failed:", e)

if __name__ == "__main__":
    main()
