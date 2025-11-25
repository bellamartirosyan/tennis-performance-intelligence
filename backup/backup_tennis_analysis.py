import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Step 0: Paths (updated for 2024)
# -----------------------------
raw_path = "data/raw/"
matches_file = os.path.join(raw_path, "atp_matches_qual_chall_2024.csv")  # 2024 data
players_file = os.path.join(raw_path, "atp_players.csv")  # player info stays the same

# Ensure results folder exists
results_path = "results"
os.makedirs(results_path, exist_ok=True)

# -----------------------------
# Step 1: Load CSVs
# -----------------------------
matches_df = pd.read_csv(matches_file)
players_df = pd.read_csv(players_file)

print("Matches shape:", matches_df.shape)
print("Players shape:", players_df.shape)

# -----------------------------
# Step 3: Basic Exploration (EDA)
# -----------------------------
print("First 5 rows of matches data:")
print(matches_df.head())
print("\nFirst 5 rows of players data:")
print(players_df.head())

print("\nMatches columns:", matches_df.columns.tolist())
print("Players columns:", players_df.columns.tolist())

print("\nMissing values in matches data:")
print(matches_df.isnull().sum())
print("\nMissing values in players data:")
print(players_df.isnull().sum())

print("\nSummary statistics for matches data:")
print(matches_df.describe())

print("\nNumber of matches per surface:")
print(matches_df['surface'].value_counts())

# -----------------------------
# Step 4: Visualizations
# -----------------------------
# 4.1 Matches by Surface
plt.figure(figsize=(8,5))
sns.countplot(data=matches_df, x='surface', order=matches_df['surface'].value_counts().index)
plt.title("Number of Matches by Surface")
plt.xlabel("Surface")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(os.path.join(results_path, "matches_by_surface.png"))
plt.show()

# 4.2 Top 10 Winners
top_winners = matches_df['winner_name'].value_counts().head(10)
plt.figure(figsize=(10,5))
sns.barplot(x=top_winners.index, y=top_winners.values)
plt.title("Top 10 Winners")
plt.xticks(rotation=45, ha='right')
plt.ylabel("Number of Wins")
plt.tight_layout()
plt.savefig(os.path.join(results_path, "top_10_winners.png"))
plt.show()

# 4.3 Top 10 Tournaments
top_tournaments = matches_df['tourney_name'].value_counts().head(10)
plt.figure(figsize=(12,5))
sns.barplot(x=top_tournaments.index, y=top_tournaments.values)
plt.title("Top 10 Tournaments by Matches")
plt.xticks(rotation=45, ha='right')
plt.ylabel("Number of Matches")
plt.tight_layout()
plt.savefig(os.path.join(results_path, "top_10_tournaments.png"))
plt.show()

# 4.4 Matches per Year
if 'tourney_date' in matches_df.columns:
    matches_df['year'] = pd.to_datetime(matches_df['tourney_date'], errors='coerce').dt.year
    matches_per_year = matches_df['year'].value_counts().sort_index()
    plt.figure(figsize=(10,5))
    sns.lineplot(x=matches_per_year.index, y=matches_per_year.values, marker='o')
    plt.title("Matches per Year")
    plt.xlabel("Year")
    plt.ylabel("Number of Matches")
    plt.tight_layout()
    plt.savefig(os.path.join(results_path, "matches_per_year.png"))
    plt.show()

# -----------------------------
# Step 5: Merge Player Info & Analyze Nationality
# -----------------------------
# Merge winner and loser countries
matches_df = matches_df.merge(players_df[['player_id','country']], left_on='winner_id', right_on='player_id', how='left').rename(columns={'country':'winner_country'})
matches_df = matches_df.merge(players_df[['player_id','country']], left_on='loser_id', right_on='player_id', how='left').rename(columns={'country':'loser_country'})

# Quick check
print("\nSample merged data with winner/loser countries:")
print(matches_df[['winner_name','winner_country','loser_name','loser_country']].head(10))

# Top 10 countries by wins
top_countries = matches_df['winner_country'].value_counts().head(10)
print("\nTop 10 Countries by Wins:")
print(top_countries)

plt.figure(figsize=(10,5))
sns.barplot(x=top_countries.index, y=top_countries.values)
plt.title("Top 10 Countries by Wins")
plt.xticks(rotation=45, ha='right')
plt.ylabel("Number of Wins")
plt.tight_layout()
plt.savefig(os.path.join(results_path, "top_10_countries.png"))
plt.show()

# Pivot table: wins per country per surface
wins_surface = matches_df.pivot_table(index='winner_country', columns='surface', values='winner_id', aggfunc='count', fill_value=0)

print("\nWins by Country and Surface:")
pd.set_option('display.max_rows', None)  # Show all rows in Terminal
print(wins_surface)

# Heatmap
plt.figure(figsize=(12,8))
sns.heatmap(wins_surface, annot=True, fmt='d', cmap='YlGnBu')
plt.title("Wins by Country and Surface")
plt.tight_layout()
plt.savefig(os.path.join(results_path, "wins_by_country_surface.png"))
plt.show()



# Total wins per player
wins = matches_df.groupby('winner_name').size().rename('wins')

# Total losses per player
losses = matches_df.groupby('loser_name').size().rename('losses')

# Combine into one DataFrame
player_stats = pd.concat([wins, losses], axis=1).fillna(0)

# Win rate
player_stats['win_rate'] = player_stats['wins'] / (player_stats['wins'] + player_stats['losses'])

# Sort by wins
player_stats_sorted = player_stats.sort_values(by='wins', ascending=False)

print("\nTop 10 Players by Wins:")
print(player_stats_sorted.head(10))


top_10_players = player_stats_sorted.head(10)
plt.figure(figsize=(12,6))
sns.barplot(x=top_10_players.index, y=top_10_players['wins'])
plt.title("Top 10 Players by Wins (2024)")
plt.xticks(rotation=45, ha='right')
plt.ylabel("Wins")
plt.tight_layout()
plt.savefig(os.path.join(results_path, "top_10_players.png"))
plt.show()


# Pivot: wins per player per surface
wins_surface_player = matches_df.pivot_table(
    index='winner_name',
    columns='surface',
    values='winner_id',
    aggfunc='count',
    fill_value=0
)

print("\nWins per Player by Surface (sample top 10):")
print(wins_surface_player.sort_values(by='hard', ascending=False).head(10))

# Heatmap: top 15 players by wins
top_players_surface = wins_surface_player.loc[top_10_players.index]
plt.figure(figsize=(12,8))
sns.heatmap(top_players_surface, annot=True, fmt='d', cmap='YlOrRd')
plt.title("Top Players Wins by Surface (2024)")
plt.tight_layout()
plt.savefig(os.path.join(results_path, "top_players_surface.png"))
plt.show()



# Sort matches by date
matches_df['tourney_date'] = pd.to_datetime(matches_df['tourney_date'], errors='coerce')
matches_df = matches_df.sort_values(['winner_name','tourney_date'])

# Initialize streak dictionary
streaks = {}

for player in matches_df['winner_name'].unique():
    player_matches = matches_df[(matches_df['winner_name']==player) | (matches_df['loser_name']==player)]
    player_matches = player_matches.sort_values('tourney_date')
    current_streak = 0
    max_streak = 0
    for _, row in player_matches.iterrows():
        if row['winner_name'] == player:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    streaks[player] = max_streak

# Convert to DataFrame
streaks_df = pd.DataFrame.from_dict(streaks, orient='index', columns=['max_win_streak']).sort_values('max_win_streak', ascending=False)

print("\nTop 10 Players by Win Streaks (2024):")
print(streaks_df.head(10))

# Start with all players at a base Elo rating of 1500
players = pd.concat([matches_df['winner_name'], matches_df['loser_name']]).unique()
elo_ratings = {player: 1500 for player in players}

# Elo parameters
K = 32  # sensitivity factor


def expected_score(rating_a, rating_b):
    """Compute expected score of player A vs B."""
    return 1 / (1 + 10**((rating_b - rating_a)/400))

def update_elo(rating_winner, rating_loser, K=32):
    """Update Elo ratings after a match."""
    expected_win = expected_score(rating_winner, rating_loser)
    expected_loss = expected_score(rating_loser, rating_winner)
    
    rating_winner_new = rating_winner + K * (1 - expected_win)
    rating_loser_new = rating_loser + K * (0 - expected_loss)
    
    return rating_winner_new, rating_loser_new


# Sort matches by date
matches_df = matches_df.sort_values('tourney_date')

# Apply Elo updates for each match
for _, row in matches_df.iterrows():
    winner = row['winner_name']
    loser = row['loser_name']
    elo_winner, elo_loser = update_elo(elo_ratings[winner], elo_ratings[loser], K)
    elo_ratings[winner] = elo_winner
    elo_ratings[loser] = elo_loser


elo_df = pd.DataFrame.from_dict(elo_ratings, orient='index', columns=['elo_2024'])
elo_df = elo_df.sort_values('elo_2024', ascending=False)
print("\nTop 10 Players by Elo Rating (2024):")
print(elo_df.head(10))


# Top 10 Elo players chart
top_elo = elo_df.head(10)
plt.figure(figsize=(12,6))
sns.barplot(x=top_elo.index, y=top_elo['elo_2024'])
plt.title("Top 10 Players by Elo Rating (2024)")
plt.xticks(rotation=45, ha='right')
plt.ylabel("Elo Rating")
plt.tight_layout()
plt.savefig(os.path.join(results_path, "top_10_players_elo.png"))
plt.show()
