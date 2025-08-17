"""
Grid Competition Simulation

This script enforces strict per-run output versioning: all simulation output files (summaries, logs, population timecourses, GIFs, CSVs, etc.) are always written inside a uniquely named subfolder for each run, regardless of mode. This applies to demo mode, test mode, and persistent simulation mode. The policy sharply reduces accidental data loss, makes every result traceable, and guarantees outputs of different runs never collide.

**Output directory/versioning policy:**
- In demo mode: All outputs are placed in a uniquely named demo_run_<timestamp>_<uuid> directory (timestamp in ISO format with '-' instead of ':') under the current working directory.
- In test mode: All outputs go in test_run_<timestamp>_<uuid> under CWD.
- In persistent runs (default): Each run creates its own uniquely named <timestamp>_<uuid> output directory under either $HOME/simulation_runs, ./outputs, or an explicitly specified --output-dir; outputs are never mixed between runs.
- All output file writes are routed through an output_paths dictionary. All simulation/model logic for file I/O must use this dictionary.

**Traceability and safety improvements:**
- Every run's results—whether demo, test, or real—are isolated in their own folder.
- Accidental overwrites are impossible (unless the user deletes or renames a run folder).
- Reviewing, debugging, or comparing runs is simple: just examine the respective run directory.

"""

import os
import sys
import uuid
import datetime
import argparse

def is_writable_dir(path):
    try:
        os.makedirs(path, exist_ok=True)
        testfile = os.path.join(path, '.output_write_test')
        with open(testfile, 'w') as f:
            f.write('test')
        os.remove(testfile)
        return True
    except Exception:
        return False

def safe_exit(msg, code=1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)

def parse_args():
    parser = argparse.ArgumentParser(description="Grid Competition Simulation with Enforced Output Versioning/Directory Policy.\n\nEach run's outputs (logs, GIFs, summaries, etc.) are written into a uniquely named subfolder. Demo and test modes create demo_run_<timestamp>_<uuid> and test_run_<timestamp>_<uuid> subfolders in the current working directory; persistent runs use <timestamp>_<uuid> subdirectories under $HOME/simulation_runs, ./outputs, or as set via --output-dir. This improves safety, traceability, and reproducibility.")
    parser.add_argument('--output-dir',
                        type=str,
                        default=None,
                        help="Base directory for persistent runs. Ignored in demo/test (see docstring). Outputs always written to per-run versioned subfolder.")
    parser.add_argument('--demo', action='store_true', help='Run a short demo (outputs in a uniquely-versioned demo_run_… subfolder in CWD)')
    parser.add_argument('--test', action='store_true', help='Run an internal test (outputs in a uniquely-versioned test_run_… subfolder in CWD)')
    parser.add_argument('--steps', type=int, default=100, help='Number of simulation steps (default: 100)')
    parser.add_argument('--seed', type=int, default=42, help='Random seed (default: 42)')
    return parser.parse_args()

def setup_output_paths(args):
    cwd = os.getcwd()
    is_root = (os.geteuid() == 0)
    now = datetime.datetime.now().replace(microsecond=0)
    timestamp = now.isoformat().replace(':', '-')
    run_uuid = str(uuid.uuid4())
    if args.demo:
        mode = 'demo_run'
    elif args.test:
        mode = 'test_run'
    else:
        mode = 'run'
    if args.demo or args.test:
        if args.output_dir:
            print('WARNING: --output-dir is ignored in demo/test mode; outputs always go in CWD in versioned subfolder.', file=sys.stderr)
        output_dir = os.path.join(cwd, f"{mode}_{timestamp}_{run_uuid}")
    else:
        if args.output_dir:
            base_dir = os.path.abspath(args.output_dir)
        else:
            home = os.environ.get('HOME')
            if home and is_writable_dir(os.path.join(home, 'simulation_runs')):
                base_dir = os.path.join(home, 'simulation_runs')
            elif is_writable_dir(os.path.join(cwd, 'outputs')):
                base_dir = os.path.join(cwd, 'outputs')
            else:
                safe_exit('Could not find a writable default output directory. Use --output-dir to specify one.')
        if base_dir.startswith('/root') and not is_root:
            safe_exit('Refusing to write under /root as non-root. Use --output-dir or run as root.')
        output_dir = os.path.join(base_dir, f"{timestamp}_{run_uuid}")
    if not is_writable_dir(output_dir):
        safe_exit(f'Output directory "{output_dir}" cannot be created or is not writable.')
    def path(name):
        return os.path.join(output_dir, name)
    output_paths = {
        'base_output_dir': output_dir,
        'summary': path('grid_competition_summary.txt'),
        'population': path('grid_competition_population.txt'),
        'log': path('grid_competition.log'),
        'gif': path('grid_competition.gif'),
    }
    return output_paths

def main():
    args = parse_args()
    output_paths = setup_output_paths(args)
    with open(output_paths['summary'], 'w') as f:
        f.write('Simulation summary...\n')
    with open(output_paths['population'], 'w') as f:
        f.write('step, dolphins, humans\n')
        for step in range(args.steps):
            f.write(f"{step}, 42, 24\n")
    with open(output_paths['log'], 'w') as f:
        f.write('Log output for this run.\n')
    print(f"All outputs for this run: {output_paths['base_output_dir']}")

if __name__ == '__main__':
    main()
