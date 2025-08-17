# Grid Competition Simulation Output Versioning Policy

**Every run (demo, test, or live) of grid_competition.py writes all outputs to a _uniquely named subfolder_ in the current working directory or an appropriate base directory.** This directory is always named with both the run mode, the timestamp (YYYY-MM-DDTHH-MM-SS), and a UUID, e.g.:

demo_run_2025-08-17T19-45-43_1ecb4f12-d61c-4ae8-98bf-abc123def456/
test_run_2025-08-17T19-45-43_b282193c-7ea3-44a0-a833-def789fed000/
2025-08-17T19-45-43_797bbfa2-b5a6-4dae-9113-dc4e6d271234/

**Policy highlights:**
- **All summary, population, log, GIF, and other output files are strictly isolated in a _per-run_ folder.**
- **Demo mode**: outputs go into `demo_run_<timestamp>_<uuid>/` in the current working directory.
- **Test mode**: outputs go into `test_run_<timestamp>_<uuid>/` under CWD.
- **Persistent/real simulations**: outputs go under `<timestamp>_<uuid>/` subfolder of `$HOME/simulation_runs` (if writable), else `./outputs` in CWD, else user-set `--output-dir`.
- **Output folder is always new and never reused across runs.**
- All file creation and output logic is centralized via the `output_paths` mapping.
- Writing to `/root` is refused unless running as root.

**Rationale:**
- Guarantees results are not inadvertently overwritten, even across multiple users or parallel runs.
- Makes it trivial to find, compare, or archive specific runs—each is a self-contained folder.
- Enables simple reproducibility studies, debugging, postmortem investigation.

**Example output folder (demo mode):**

demo_run_2025-08-17T19-45-43_1ecb4f12-d61c-4ae8-98bf-abc123def456/
    grid_competition_summary.txt
    grid_competition_population.txt
    grid_competition.log
    grid_competition.gif

**How to use:**
- Run demo: `python grid_competition.py --demo`
- Run test: `python grid_competition.py --test`
- Run persistent simulation: `python grid_competition.py --steps 200`
- Use a custom base directory (for persistent runs only): `python grid_competition.py --output-dir /my/results`

See the script top-level docstring or --help for detailed logic and enforced rules.
