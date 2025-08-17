
Project Context: Artificial SUT for Autonomous Agent Test Management (Agent Zero / ISTQB Test Manager)
====================================================================================================
**This repository contains a simulation system created solely as an *artificial System Under Test (SUT)*
and is not intended for production, research, or real-world modeling.**

All code, outputs, and artifact structures are purpose-built as a digital testbed enabling advanced, automated
test management and reporting activities by autonomous agent-based QA teams—led by the ISTQB-Certified
Advanced Test Manager profile *Gilbert-000* (Agent Zero, agent0ai) and its subagents.

- The SUT is designed for agent-driven test case design, metrics collection, automated regression, demo scenarios,
  tool/lifecycle integration, and reproducible audit trails.
- All orchestration, batch runs, artifact generation, and logging are performed (and consumed) by Agent Zero and
  its subagents acting as a synthetic, continuously-operating test organization (see 'About agent0ai').
- Outputs reflect agent-driven operation, not manual or interactive modeling use.

For human users: This project demonstrates ISTQB best practices as implemented by an artificial test team, led by
Agent Zero / Gilbert-000, to manage the full SUT lifecycle (planning, execution, reporting, and CI integration).
See detailed usage in the 'Autonomous and Programmatic Usage' section.

# Dolphin vs Human Spatial Competition Simulation


Project Purpose: Artificial SUT for Professional AI Test Management
==================================================================
This simulation suite is **not** a real-world ecological or demographic model. It is an *artificial System Under Test (SUT)*—a controllable digital landscape created solely to serve as an internal, observable testbed for the autonomous test management agent **Agent Zero (agent0ai)**, also called **Gilbert-000** (ISTQB Advanced Level Test Manager).

**Why does this SUT exist?**
- To provide a reproducible, well-instrumented platform for automated test case design, metrics collection, regression, tooling evaluation, lifecycle analysis, and reporting by the agent-based test team.
- To support demonstration, orchestrated testing, audit, and CI/CD workflows managed by Agent Zero and subagents acting as a professional test organization.
- All configuration, test runs, logs, and metrics are under agent and subagent control, produced for agent-driven processes—*not* direct user/modeling/scientific research.

**Who is the operator?**
- Agent Zero (agent0ai / Gilbert-000) is an ISTQB Advanced Certified Test Manager, orchestrating batch tests, metrics-driven analysis, artifact management, version control, and all audit/reporting using this SUT.
- The entire software, output policy, versioning, and CI are designed to enable automated and auditable test management workflows, with example scenarios in the docs.

See also: 'About agent0ai' and 'Autonomous and Programmatic Usage' below.


**A grid-based demographic and ecological simulation of dolphins and humans competing for space, resources, and survival.**

- Agent-based model on a grid (default 50x50)
- Dolphins seeded as a contiguous founder blob (M+F pairs, region-growth)
- Humans introduced as paired clusters (M+F pairs) after initial steps
- Local reproduction requires adjacent male+female pairs
- Individual movement (mate-seeking and random)
- Density-dependent illness/crowding: high-density areas prone to cell death and weakening
- Dispersed (non-local) placement of offspring for dynamic expansion
- Extensible, well-logged, and supports reproducible outputs


About agent0ai (Agent Zero) as Primary Autonomous Operator
---------------------------------------------------
This repository is operated and maintained in part by Agent Zero (agent0ai), an autonomous agent system running in reproducible, prompt-based environments. Agent Zero is the main agent orchestrating all production and batch runs, managing audit logs, ensuring every simulation is performed with full isolation and provenance, and automating experiment versioning, git synchronization, logging, and CI/CD.

**Agent Zero automates:**
- Code and output synchronization (via git)
- Fully non-interactive, batch and parameter-sweep runs
- Timestamped, auditable per-run output folders for all experiments
- Ephemeral, credential-free operation (no secrets written/tracked)
- Audit-logging of all run parameters and model changes
- CI/CD hooks for reproducibility and automated testing

All experiment outputs and logs reflect agent-orchestrated operation. All demo/test runs are isolated and versioned. For details, see the 'Autonomous and Programmatic Usage' section below or the agent0ai docs linked in repo.

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


## Autonomous and Programmatic Usage

This repository is designed for fully autonomous, hands-free operation, suitable for agent orchestration, large-scale experiments, or automated workflows. All key features for autonomous and programmatic use are included (excluding credential management).

**Key Features Supporting Autonomy:**
- **Batch Runnable & Headless:** All simulation runs, including different scenarios, parameter sweeps, or batch testing, can be run fully non-interactively from the CLI (see `--no-confirm`, `--output-dir`, `--steps`, `--seed`, etc). Demo and test runs are gated off via the `--demo` flag.
- **Reproducible Outputs:** Every run creates a uniquely named output directory (timestamp plus short UUID) under `outputs/` or as specified with `--output-dir`. This ensures collision-free, versioned, and auditable experiment outputs without overwrites.
- **Configurable via CLI:** All scenario configuration—founder numbers, sex splits, illness parameters, grid size, number of steps, seeds, etc.—can be set via command-line flags, enabling automation by shell scripts or workflow runners.
- **No GUI Required:** The simulation can run entirely in the background. All essential outputs—population histories, run summaries, GIF animations—are written to the output directory. Results are never sent outside the specified folder tree.
- **No External Intervention Needed:** With confirmation flags set, a full experiment or parameter sweep can proceed on any system with Python and required dependencies installed.
- **Audit & Logging:** Per-run logs, output and summary files, and run parameters (including seeds) are saved in each output directory for robust reproducibility.
- **Demo/Test Isolation:** Demo/test runs go to special subfolders and are never allowed to overwrite or intermingle with real output data, ensuring safe experimentation without risk to production results.
- **Supports Orchestration:** You can invoke the simulation from Python, bash, or workflow runners (e.g., GitHub Actions/CI/CD, SLURM, Airflow) to automate large study designs.

**Example: Automated Batch Run (Headless)**
```bash
python grid_competition.py --steps 100 --grid-size 50 --seed 42 --output-dir ./outputs/ai_batch_test1 --no-confirm
```

**Recommended Autonomous Workflow:**
1. Install requirements (see below).
2. Prepare your scenario/configuration (either via CLI flags or a wrapper script).
3. Launch batch or single runs with `--no-confirm` and an explicit `--output-dir` (one per process/replicate for parallel jobs), or let the script auto-generate output folders.
4. All outputs (logs, GIFs, summaries, population time series) will be in the per-run folder, safely versioned.
5. Optionally run analysis scripts or test suites on the output folders.

**Credential-Free Operation:**
- All local code and CLI runs require no credentials.
- For pushing data/code to remote repositories (e.g., GitHub), only the minimal token or deploy key for version control is ever required, and those are never stored or hard-coded in the codebase.
- All settings for outputs, logging, and automation are controlled via flags or config files, not environment secrets.

**CI/CD Integration Tips:**
You can set up automated regression testing or batch simulation using continuous integration pipelines:
- Add runner stages that call the simulation entrypoint(s) non-interactively with scenario and output arguments.
- Artifacts can be stored as pipeline artifacts or exported to data lakes for metaanalysis.

See the usage and troubleshooting sections below for more details. For direct automation or programmatic control, see the docstring of `grid_competition.py` and the CLI `--help` output.

_Last updated: 2025-08-17_
