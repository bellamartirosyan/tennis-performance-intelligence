#!/usr/bin/env python3
# run_season_simulator.py
"""
Tennis Season Simulator
- Computes surface-specific ELOs
- Simulates tournaments using Monte Carlo
- Saves simulation results
"""

import pandas as pd
import numpy as np
import os

# -----------------------------
# Configuration
# -----------------------------
MATCHES_FILE = "atp_matches_2024.csv"
N_MONTE_CARLO = 2000  # number of simulations per tournament
SURFACES = ['Hard', 'Clay', 'Grass']
K_FACTOR = 32  # standard ELO K-factor

TOURNAMENTS = [
    "Brisbane", "Hong Kong", "United Cup", "Auckland", "Adelaide",
    "Australian Open", "Montpellier",
    "Davis Cup QLS R1: UKR vs USA",
    "Davis Cup QLS R1: SRB vs SVK",
    "Davis Cup WG1 PO: COL vs LUX",
    "Davis Cup QLS R1: SWE vs BRA",
    "Davis Cup QLS R1: HUN vs GER"
]

# -----------------------------
# Load matches
# -----------------------------
if os.path.exists(MATCHES_FILE):
    matches = pd.read_csv(MATCHES_FILE)
else:
    print(f"{MATCHES_FILE} not found, generating dummy matches...")
    # Dummy dataset: 3000 matches, random players, surfaces, and scores
    players = ['Carlos Alcaraz', 'Casper Ruud', 'Grigor Dimitrov', 'Holger Rune', 'Alexander Zverev']
    matches = pd.DataFrame({
        'player1': np.random.choice(players, 3000),
        'player2': np.random.choice(players, 3000),
        'score1': np.random.randint(0, 3, 3000),
        'score2': np.random.randint(0, 3, 3000),
        'surface': np.random.choice(SURFACES, 3000),
        'tournament': np.random.choice(TOURNAMENTS, 3000)
    })

print(f"Loaded matches: {matches.shape}")

# -----------------------------
# Compute Surface-Specific ELOs
# -----------------------------
players = pd.unique(matches[['player1', 'player2']].values.ravel())
elos = pd.DataFrame(index=players, columns=SURFACES, dtype=float).fillna(1500.0)

for idx, row in matches.iterrows():
    p1, p2, s1, s2, surface = row['player1'], row['player2'], row['score1'], row['score2'], row['surface']
    
    # Expected score
    E1 = 1 / (1 + 10 ** ((elos.loc[p2, surface] - elos.loc[p1, surface]) / 400))
    E2 = 1 - E1
    
    # Actual score (win = 1, loss = 0)
    S1 = 1 if s1 > s2 else 0
    S2 = 1 - S1
    
    # Update ELOs
    elos.loc[p1, surface] += K_FACTOR * (S1 - E1)
    elos.loc[p2, surface] += K_FACTOR * (S2 - E2)

# Player base table with final projected ELO
player_base = []
for p in elos.index:
    surface_dict = elos.loc[p].to_dict()
    player_base.append({
        'player': p,
        'surface_elos': surface_dict,
        'final_projected_elo': np.mean(list(surface_dict.values()))
    })
player_base_df = pd.DataFrame(player_base)
print(f"Built player base table: {player_base_df.shape}")

# -----------------------------
# Monte Carlo Tournament Simulation
# -----------------------------
np.random.seed(42)  # for reproducibility

def simulate_tournament(players_df, tournament_name):
    """Simulate tournament using Monte Carlo bracket approach"""
    top_results = []
    players_list = players_df['player'].tolist()
    final_elos = players_df.set_index('player')['final_projected_elo'].to_dict()
    
    for _ in range(N_MONTE_CARLO):
        # Randomly pair players and simulate matches
        shuffled = np.random.permutation(players_list)
        winners = []
        for i in range(0, len(shuffled), 2):
            if i+1 >= len(shuffled):
                winners.append(shuffled[i])
                continue
            p1, p2 = shuffled[i], shuffled[i+1]
            prob_p1 = final_elos[p1] / (final_elos[p1] + final_elos[p2])
            winner = p1 if np.random.rand() < prob_p1 else p2
            winners.append(winner)
        players_list = winners
    # Count appearances in final
    counts = pd.Series(winners).value_counts().sort_values(ascending=False)
    for player, count in counts.head(3).items():
        top_results.append((player, int(count)))
    return top_results

# Run all tournaments
simulations = []
for t in TOURNAMENTS:
    top = simulate_tournament(player_base_df, t)
    print(f"Simulated {t}: top sample -> {top}")
    simulations.append({'tournament': t, 'top3': top})

# Save results
sim_df = pd.DataFrame(simulations)
sim_df.to_csv("tournament_simulations.csv", index=False)
print(f"Saved simulations: {sim_df.shape}")
print("Done.")
