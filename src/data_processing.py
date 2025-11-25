import pandas as pd

def load_matches(path):
    df = pd.read_csv(path, low_memory=False)
    rename_map = {}
    for col, candidates in {
        'date': ['tourney_date','match_date','Date'],
        'winner_name': ['winner','winner_player','winner_fullname'],
        'loser_name': ['loser','loser_player','loser_fullname'],
        'surface': ['court','surface_type'],
        'tourney_name': ['tournament','tourney']
    }.items():
        if col not in df.columns:
            for cand in candidates:
                if cand in df.columns:
                    rename_map[cand] = col
                    break
    df = df.rename(columns=rename_map)
    required = ['date','tourney_name','surface','winner_name','loser_name']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns: {missing}")
    df = df[required + [c for c in df.columns if c not in required]]
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date','winner_name','loser_name'])
    df['surface'] = df['surface'].fillna('Unknown').astype(str).str.title().str.strip()
    df['tourney_name'] = df['tourney_name'].astype(str)
    df = df.sort_values('date').reset_index(drop=True)
    return df
