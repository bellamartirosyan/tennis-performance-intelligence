import numpy as np
from collections import defaultdict

def elo_win_prob(elo_a, elo_b):
    return 1 / (1 + 10 ** ((elo_b - elo_a) / 400))

def build_draw(top_players_df, draw_size=128):
    players = top_players_df.sort_values('final_projected_elo', ascending=False)['player'].tolist()
    if len(players) < draw_size:
        players += [None]*(draw_size - len(players))
    return players[:draw_size]

def simulate_single_tournament(draw_players, surface, projected_df, n_simulations=4000):
    elos = {p: projected_df.set_index('player')[f'proj_elo_{surface}'].to_dict() for p in projected_df['player']}
    draw_size = len(draw_players)
    winners = defaultdict(int)

    # Vectorized Monte Carlo
    for _ in range(n_simulations):
        current_round = draw_players.copy()
        while len(current_round) > 1:
            next_round = []
            for i in range(0, len(current_round), 2):
                a = current_round[i]
                b = current_round[i+1] if i+1 < len(current_round) else None
                if a is None: next_round.append(b); continue
                if b is None: next_round.append(a); continue
                elo_a, elo_b = elos.get(a, 1500), elos.get(b, 1500)
                prob_a = elo_win_prob(elo_a, elo_b)
                next_round.append(a if np.random.rand() < prob_a else b)
            current_round = next_round
        winners[current_round[0]] += 1
    return winners
