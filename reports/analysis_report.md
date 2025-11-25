ATP 2024 Season Analysis Report
1. Overview

This report presents an analytical deep-dive into the 2024 ATP season, focusing on match outcomes, player performance metrics, ELO-based strength estimates, and Monte Carlo tournament simulations.
The analysis combines historical match data from atp_matches_2024.csv, custom ELO modeling, and result visualizations created in the accompanying Jupyter notebook.

2. Dataset Summary

The dataset includes all ATP-level matches from the 2024 season.

Columns:

tourney_name

tourney_date

surface

winner_name / loser_name

winner_country / loser_country

score

The notebook performs:

date cleaning

win–loss aggregation

country-level win distribution

top player performance extraction

3. Key Statistical Findings
3.1 Win Percentages of Top Players (2024 Season)

Based on the aggregated results:

Player	Wins	Matches	Win %
Novak Djokovic	137	161	85.09%
Carlos Alcaraz	176	214	82.24%
Jannik Sinner	187	229	81.66%
Rafael Nadal	53	73	72.60%
Stefanos Tsitsipas	156	226	69.03%

Djokovic maintains the highest win rate, but Sinner and Alcaraz remain extremely close in performance metrics, confirming the tight competition among the current top tier.

3.2 Player-Specific Match Insights
Novak Djokovic – 2024 Snapshot

The sample results show:

Strong early-season hard-court performances

A tougher stretch on clay, including losses to Davidovich Fokina and Alcaraz

Wins against Hurkacz, Khachanov, Kecmanovic, Djere

Djokovic’s season demonstrates resilience and depth despite competitive pressure from younger players.

Jannik Sinner – 2024 Snapshot

Sinner’s sample:

Clean wins in early hard-court tournaments

Solid run in the Australian Open until losing to Tsitsipas

Continued consistency against mid-ranking opponents

His rising form aligns with his high win percentage.

4. Country-Level Insights

A bar chart in the notebook highlights win counts by player nationality.
(Warning suppressed: palette without hue deprecated.)

Spain, Italy, Serbia, and the USA dominate total wins — reflecting where current ATP depth lies.

5. Simulation Results (Monte Carlo Model)

Simulations were run for key early-season tournaments (Brisbane, Adelaide, United Cup, Australian Open, etc.).

Example outcomes:

Brisbane:

Carlos Alcaraz

Grigor Dimitrov

Casper Ruud

Australian Open:

Alexander Zverev

Grigor Dimitrov

Casper Ruud

Across simulations, Dimitrov shows surprisingly high consistency, benefiting from ELO-based matchup modeling.

6. Modeling Approach

The project uses:

ELO System

Base ELO from previous seasons

Surface-specific adjustments

Match-to-match updates

K-factor tuned for ATP variability

Monte Carlo Simulation

Each tournament:

loads a player field

runs N simulated brackets (commonly 1,000–10,000)

logs win probability distributions

7. How to Reproduce the Results

See the notebook:

notebooks/analysis_2024.ipynb


And run:

python src/run_season_simulator.py


Requirements are listed in requirements.txt.

8. Conclusion

The 2024 season data confirms a highly competitive environment at the top, with Djokovic, Alcaraz, and Sinner maintaining extremely strong win rates.
Simulations suggest a shifting landscape where Dimitrov and Zverev emerge as dark-horse threats in early tournaments.
The combined ELO + simulation pipeline provides a realistic, data-driven way to forecast tournament outcomes.

9. Files Referenced

data/atp_matches_2024.csv

notebooks/analysis_2024.ipynb

src/run_season_simulator.py

src/elo_utils.py

src/simulation_engine.py