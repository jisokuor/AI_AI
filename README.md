# Dolphin vs Human Spatial Competition Simulation

**A grid-based demographic and ecological simulation of dolphins and humans competing for space, resources, and survival.**

- Agent-based model on a grid (default 50x50)
- Dolphins seeded as a contiguous founder blob (M+F pairs, region-growth)
- Humans introduced as paired clusters (M+F pairs) after initial steps
- Local reproduction requires adjacent male+female pairs
- Individual movement (mate-seeking and random)
- Density-dependent illness/crowding: high-density areas prone to cell death and weakening
- Dispersed (non-local) placement of offspring for dynamic expansion
- Extensible, well-logged, and supports reproducible outputs

## Quick Start

1. **Clone the repository:**
   ```
   git clone https://github.com/jisokuor/AI_AI.git
   cd AI_AI
   ```
2. **Set up dependencies (Python 3.7+ recommended):**
   ```
   pip install numpy matplotlib pillow
   ```
3. **Run a simulation:**
   ```
   python grid_competition.py  # Prompts for settings and confirmation
   ```
   - For a demo/test run:
   ```
   python grid_competition.py --demo
   python grid_competition.py --test
   ```
   - To use custom number of steps or a specific seed:
   ```
   python grid_competition.py --steps 150 --seed 137
   ```
   - To specify output directory (for persistent runs):
   ```
   python grid_competition.py --output-dir ./outputs
   ```

4. **See results:**
    - Every run creates a timestamped, unique output folder containing:
      * `grid_competition_population.txt`: Per-step counts of dolphins/humans (with sex and pairing if enabled)
      * `grid_competition_summary.txt`: Summary of final population, extinction events, key milestones
      * `grid_competition.gif`: Animation of the grid and competition dynamics (**if enabled/successful**)
      * `grid_competition.log`: Structured event log (optional)

## Features
- **Spatial agent-based dynamics:** Dolphins and humans occupy and colonize cells on the grid.
- **Sexed reproduction:** Only adjacent M+F pairs of same species can reproduce.
- **Individual movement:** Each agent may move one step per cycle, prioritizing mate proximity.
- **Density-dependent illness:** Clusters with ≥6 same-type neighbors may die or become weakened (configurable probabilities)
- **Dynamic per-run output:** All artifacts are saved in a unique folder per run for traceability and comparison.

## Output Versioning Policy
_Every simulation run creates its own, timestamped, UUID-suffixed subfolder (e.g., `simulation_runs/2025-08-17T19-45-43_f00baa`). All logs, CSVs, summaries, GIFs, and data files for a run are isolated and never overwritten._
- By default, demo/test outputs go under `demo_run_...` or `test_run_...`
- Production runs go under `simulation_runs/` or a user-supplied output dir
- Outputs are deliberately .gitignored by default for reproducibility (exception: you may add demo/example folders manually)

## Interpreting Outputs
- **grid_competition.gif**: Shows the spatial spread, extinction/coexistence, and illness events frame by frame
- **grid_competition_population.txt**: CSV of populations per step
- **grid_competition_summary.txt**: Final counts and key events
- **grid_competition.log**: Optional; detailed events, parameter records

## Troubleshooting
- If you see no .gif in outputs, check PIL and matplotlib setup, or rerun locally with GUI support.
- For reproducibility, use the same seed (--seed).
- Never run as root unless explicitly intended (the script blocks privileged output unwisely).
- Use forced git add `git add -f simulation_runs/...` if you wish to commit example outputs for sharing.

## How to Contribute / Contact
- Open issues or PRs in this repository.
- Suggestions, new ecological rules, or code improvements are welcome!

---

_Last updated: 2025-08-17_
