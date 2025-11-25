# Tennis Performance Intelligence

This repository contains a data analysis and forecasting project for professional tennis players, focusing on match results, win percentages, and probabilistic forecasts for upcoming matches.

## Overview

The project analyzes match data for top ATP players, including Novak Djokovic, Carlos Alcaraz, and Jannik Sinner, for the 2024 season. Using historical match results, surface-specific models, and ELO ratings, the analysis provides insights into player performance, win probabilities, and tournament simulations.

---

## Data

The dataset includes:

- **Match information**: tournament, date, surface, players, and scores.
- **Player statistics**: win counts, win percentages, and match outcomes by surface.
- **Simulation outputs**: projected ELO ratings and tournament forecasts.

### Sample Data

| Year | Tournament | Date       | Surface | Winner         | Winner Country | Loser           | Loser Country | Score                |
|------|------------|------------|--------|----------------|----------------|-----------------|---------------|--------------------|
| 2024 | Dubai      | 20240221   | Hard   | Novak Djokovic | SRB            | Lorenzo Musetti | ITA           | 6-3 6-3            |
| 2024 | Monte Carlo| 20240411   | Clay   | Alejandro D. F.| ESP            | Novak Djokovic  | SRB           | 6-3 6-7(5) 6-1     |
| 2024 | Australian Open | 20240117 | Hard | Jannik Sinner | ITA           | Joao Sousa      | POR           | 6-4 7-5 6-1        |

---

## Key Insights

- **Top Player Win Percentages (2024 season)**:
  - Novak Djokovic: 85.1%
  - Carlos Alcaraz: 82.2%
  - Jannik Sinner: 81.7%
  - Rafael Nadal: 72.6%
  - Stefanos Tsitsipas: 69.0%

- **Surface Analysis**:
  - Hard: Novak Djokovic and Carlos Alcaraz dominate.
  - Clay: Djokovic shows nearly perfect performance against top competitors.
  - Grass: Performance more variable; probabilities differ across tournament levels.

- **Probabilistic Forecasts**:
  - Novak Djokovic vs Carlos Alcaraz on Hard: ~65% win probability for Djokovic.
  - Novak Djokovic vs Jannik Sinner on Hard: ~19% win probability for Djokovic.
  - Carlos Alcaraz vs Jannik Sinner on Hard: ~14% win probability for Alcaraz.

- **Tournament Simulations**:
  - Jannik Sinner consistently ranks high in simulated tournaments such as Brisbane, Hong Kong, and the Australian Open.
  - Surface-specific ELO ratings allow prediction of match outcomes with ~78-80% accuracy depending on the surface.

---

## Models & Methods

1. **Data Processing**
   - Match results cleaned and aggregated per player.
   - Win percentages computed per player and surface.

2. **Surface-Specific Models**
   - Hard, Clay, Grass models trained using historical outcomes.
   - Fallback all-surface model trained for missing data.

3. **ELO Ratings**
   - Surface-specific ELO ratings computed for all players.
   - Used in probabilistic forecasts and tournament simulations.

4. **Simulation**
   - Monte Carlo simulation of tournaments.
   - Top performers identified by match wins in simulations.

---

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/bellamartirosyan/tennis-performance-intelligence.git
   cd tennis-performance-intelligence
