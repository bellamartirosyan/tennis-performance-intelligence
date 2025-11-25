import numpy as np
from collections import defaultdict

INITIAL_ELO = 1500
K_BASE = 24

def compute_surface_elos(matches_df, initial_elo=INITIAL_ELO, k_base=K_BASE):
    players = defaultdict(lambda: defaultdict(lambda: initial_elo))
    winner_pre, loser_pre = [], []

    for _, r in matches_df.iterrows():
        surf = r['surface'] if r['surface'] else 'Unknown'
        w, l = r['winner_name'], r['loser_name']
        elo_w, elo_l = players[surf][w], players[surf][l]
        winner_pre.append(elo_w)
        loser_pre.append(elo_l)
        expected_w = 1 / (1 + 10 ** ((elo_l - elo_w) / 400))
        players[surf][w] = elo_w + k_base * (1 - expected_w)
        players[surf][l] = elo_l + k_base * (0 - (1 - expected_w))
    
    matches_df = matches_df.copy()
    matches_df['winner_elo_pre'] = winner_pre
    matches_df['loser_elo_pre'] = loser_pre

    final_elos = {p: dict(surf_dict) for surf_dict in players.values() for p in surf_dict.keys()}
    return matches_df, players
