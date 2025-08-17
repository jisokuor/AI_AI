
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib import colors
import imageio
import random
from datetime import datetime

np.random.seed(42)
random.seed(42)

GRID_SIZE = 50
TIMESTEPS = 151
DOLPHIN_PAIRS = 375
HUMAN_PAIRS = 125
PAIR_SIZE = 2
DOLPHIN_SAFE = 15
ILLNESS_RATE_DOLPHIN = 0.01
ILLNESS_RATE_HUMAN = 0.02
HUMAN_PAIR_MINDIST = 6
DOLPHIN_REGION_START = (GRID_SIZE//2 - DOLPHIN_SAFE//2, GRID_SIZE//2 - DOLPHIN_SAFE//2)
DOLPHIN_REGION_END = (DOLPHIN_REGION_START[0] + DOLPHIN_SAFE, DOLPHIN_REGION_START[1] + DOLPHIN_SAFE)
EMPTY = 0
DOLPHIN = 1
HUMAN = 2

def position_in_dolphin_zone(r, c):
    return (DOLPHIN_REGION_START[0] <= r < DOLPHIN_REGION_END[0] and DOLPHIN_REGION_START[1] <= c < DOLPHIN_REGION_END[1])

def get_adjacent_cells(r, c, grid):
    adj = []
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0<=nr<GRID_SIZE and 0<=nc<GRID_SIZE:
            adj.append( (nr,nc) )
    return adj

def valid_pair_positions(grid, occupied_mask=None):
    mask = (grid==EMPTY) if occupied_mask is None else (grid==EMPTY) & (~occupied_mask)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE-1):
            if mask[r,c] and mask[r,c+1]:
                yield [(r,c),(r,c+1)]
    for r in range(GRID_SIZE-1):
        for c in range(GRID_SIZE):
            if mask[r,c] and mask[r+1,c]:
                yield [(r,c),(r+1,c)]

def place_dolphin_cluster(grid, pair_list, log_lines):
    region_r0, region_c0 = DOLPHIN_REGION_START
    region_r1, region_c1 = DOLPHIN_REGION_END
    used = np.zeros((GRID_SIZE,GRID_SIZE),bool)
    pair_ct = 0
    for orient in ['h','v']:
        for r in range(region_r0, region_r1):
            for c in range(region_c0, region_c1):
                if pair_ct>=DOLPHIN_PAIRS:
                    break
                if orient=='h' and c+1<region_c1:
                    if not used[r,c] and not used[r,c+1]:
                        grid[r,c]=DOLPHIN
                        grid[r,c+1]=DOLPHIN
                        used[r,c]=used[r,c+1]=True
                        pair_list.append( [(r,c),(r,c+1)] )
                        log_lines.append(f"{datetime.now().isoformat()} | Dolphin-Pair-{pair_ct:03d} placed H at ({r},{c})-({r},{c+1})")
                        pair_ct+=1
                if orient=='v' and r+1<region_r1:
                    if not used[r,c] and not used[r+1,c]:
                        grid[r,c]=DOLPHIN
                        grid[r+1,c]=DOLPHIN
                        used[r,c]=used[r+1,c]=True
                        pair_list.append( [(r,c),(r+1,c)] )
                        log_lines.append(f"{datetime.now().isoformat()} | Dolphin-Pair-{pair_ct:03d} placed V at ({r},{c})-({r+1},{c})")
                        pair_ct+=1
    if pair_ct<DOLPHIN_PAIRS:
        log_lines.append(f"WARNING: Only {pair_ct} dolphins placed in cluster!")
        raise RuntimeError("Failed to fill requested dolphin pairs in region!")
    return

def random_far_apart_pairs(grid, N_pairs, avoid_mask, min_dist, log_lines, species_name="Human"):
    free_mask = (grid==EMPTY) & (~avoid_mask)
    cand_coords = [(r,c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if free_mask[r,c]]
    pairs = []
    placed_cells = set()
    for i in range(N_pairs):
        succ=False
        random.shuffle(cand_coords)
        for r,c in cand_coords:
            for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r+dr, c+dc
                if 0<=nr<GRID_SIZE and 0<=nc<GRID_SIZE and grid[nr,nc]==EMPTY:
                    pair_pos = [(r,c),(nr,nc)]
                    # check min-dist from all already placed pairs
                    minpair_dist = min([abs(r-rr)+abs(c-cc) for (rr,cc) in placed_cells] + [min_dist])
                    if len(placed_cells)==0 or minpair_dist>=min_dist:
                        grid[r,c]=HUMAN
                        grid[nr,nc]=HUMAN
                        pairs.append(pair_pos)
                        placed_cells.update(pair_pos)
                        nowt = datetime.now().isoformat()
                        log_lines.append(f"{nowt} | {species_name}-Pair-{i:03d} placed at ({r},{c})-({nr},{nc})")
                        succ=True
                        break
            if succ: break
        # Relax if too crowded
        if not succ:
            for r,c in cand_coords:
                for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr, nc = r+dr, c+dc
                    if 0<=nr<GRID_SIZE and 0<=nc<GRID_SIZE and grid[nr,nc]==EMPTY:
                        pair_pos = [(r,c),(nr,nc)]
                        minpair_dist = min([abs(r-rr)+abs(c-cc) for (rr,cc) in placed_cells] + [2])
                        if (len(placed_cells)==0 or minpair_dist>=2):
                            grid[r,c]=HUMAN
                            grid[nr,nc]=HUMAN
                            pairs.append(pair_pos)
                            placed_cells.update(pair_pos)
                            nowt = datetime.now().isoformat()
                            log_lines.append(f"{nowt} | {species_name}-Pair-{i:03d} placed (relaxed-dist) at ({r},{c})-({nr},{nc})")
                            succ=True
                            break
                if succ: break
        if not succ:
            log_lines.append(f"ERROR: Could not fit all {species_name} pairs on grid!")
            raise RuntimeError("Grid too full for all pairs!")
    return pairs

def render_grid(grid, step, annotate=None):
    cmap = colors.ListedColormap(["white", "#2699c6", "#f17664"])
    norm = colors.BoundaryNorm([0,1,2,3], cmap.N)
    fig,ax = plt.subplots(figsize=(5,5))
    ax.imshow(grid, cmap=cmap, norm=norm, vmin=0, vmax=2)
    ax.set_xticks([])
    ax.set_yticks([])
    text = f"Step {step}"
    if annotate:
        ax.text(0.7,1.03, annotate, fontsize=10, color='black', transform=ax.transAxes, bbox=dict(facecolor='yellow',alpha=0.6))
    ax.text(0.01,1.03, text, fontsize=12, color='k', fontweight='bold', transform=ax.transAxes)
    if step==0 or annotate:
        dr0, dc0 = DOLPHIN_REGION_START
        size = DOLPHIN_SAFE
        rect = patches.Rectangle( (dc0-0.5,dr0-0.5), size, size, linewidth=2,edgecolor='navy',facecolor='none',ls='dashed')
        ax.add_patch(rect)
    fig.tight_layout(pad=0)
    fig.canvas.draw()
    img_arr = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    img_arr = img_arr.reshape(fig.canvas.get_width_height()[::-1]+(3,))
    plt.close(fig)
    return img_arr

def validate_pairs(grid, dolphin_pairs, human_pairs):
    ok = True
    problems=[]
    occ = np.zeros_like(grid)
    for p in dolphin_pairs:
        for cell in p:
            if occ[cell]>0:
                problems.append(f"Dolphin overlap at {cell}")
                ok = False
            occ[cell]=1
            if not (0<=cell[0]<GRID_SIZE and 0<=cell[1]<GRID_SIZE and grid[cell]==DOLPHIN):
                problems.append(f"Dolphin pair at {cell} is off-grid or wrong species")
                ok=False
    for p in human_pairs:
        for cell in p:
            if occ[cell]>0:
                problems.append(f"Human overlap at {cell}")
                ok = False
            occ[cell]=1
            if not (0<=cell[0]<GRID_SIZE and 0<=cell[1]<GRID_SIZE and grid[cell]==HUMAN):
                problems.append(f"Human pair at {cell} is off-grid or wrong species")
                ok=False
    allhuman = [tuple(cell) for p in human_pairs for cell in p]
    for i,p1 in enumerate(human_pairs):
        for j,p2 in enumerate(human_pairs):
            if i>=j: continue
            for c1 in p1:
                for c2 in p2:
                    d = abs(c1[0]-c2[0])+abs(c1[1]-c2[1])
                    if d<2:
                        problems.append(f"Human pairs too close at {c1},{c2}: dist {d}")
                        ok=False
    return ok, problems

def fix_pair_overlaps(grid, dolphin_pairs, human_pairs, log_path):
    with open(log_path,'a') as f:
        f.write('*** Attempting auto-fix of invalid pair grid ***\n')
    grid[:]=EMPTY
    i=0
    for p in dolphin_pairs:
        for cell in p:
            if grid[cell]==EMPTY:
                grid[cell]=DOLPHIN
            else:
                with open(log_path,'a') as f:
                    f.write(f"Dolphin fix overlapping at {cell}\n")
    for p in human_pairs:
        for cell in p:
            if grid[cell]==EMPTY:
                grid[cell]=HUMAN
            else:
                with open(log_path,'a') as f:
                    f.write(f"Human fix overlapping at {cell}\n")

def simulate():
    log_lines = []
    birth_events = []
    illness_events = []
    pop_stats = []
    frames = []
    grid = np.zeros((GRID_SIZE,GRID_SIZE), dtype=np.int8)
    dolphin_pairs = []
    human_pairs = []
    # Step 0: Founding dolphins
    place_dolphin_cluster(grid, dolphin_pairs, log_lines)
    pop_stats.append( (0, len(dolphin_pairs)*PAIR_SIZE, 0) )
    img = render_grid(grid, 0, annotate="Founding dolphin cluster (750)")
    frames.append(img)
    log_lines.append(f"{datetime.now().isoformat()} | Step 0: {len(dolphin_pairs)*PAIR_SIZE} dolphins placed in cluster.")
    for step in range(1, TIMESTEPS):
        if step==15:
            avoid_mask = (grid==DOLPHIN)
            new_pairs = random_far_apart_pairs(grid, HUMAN_PAIRS, avoid_mask, HUMAN_PAIR_MINDIST, log_lines)
            human_pairs = new_pairs.copy()
            log_lines.append(f"{datetime.now().isoformat()} | Step 15: {len(human_pairs)*2} humans introduced.")
        added_dolphin_pairs = []
        added_human_pairs = []
        # Dolphins reproduce
        for pair in dolphin_pairs:
            for anchor in pair:
                r,c = anchor
                for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr,nc = r+dr,c+dc
                    if 0<=nr<GRID_SIZE and 0<=nc<GRID_SIZE and grid[nr,nc]==EMPTY:
                        for sdr,sdc in [(-1,0),(1,0),(0,-1),(0,1)]:
                            nnr, nnc = nr+sdr, nc+sdc
                            if 0<=nnr<GRID_SIZE and 0<=nnc<GRID_SIZE and grid[nnr,nnc]==EMPTY and (nnr,nnc)!=(r,c):
                                grid[nr,nc]=DOLPHIN
                                grid[nnr,nnc]=DOLPHIN
                                added_dolphin_pairs.append( [(nr,nc),(nnr,nnc)] )
                                birth_events.append( (step, 'DOLPHIN', nr, nc, nnr, nnc) )
                                break
                        break
        # Humans reproduce
        for pair in human_pairs:
            for anchor in pair:
                r,c = anchor
                for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr,nc = r+dr,c+dc
                    if 0<=nr<GRID_SIZE and 0<=nc<GRID_SIZE and grid[nr,nc]==EMPTY:
                        for sdr,sdc in [(-1,0),(1,0),(0,-1),(0,1)]:
                            nnr, nnc = nr+sdr, nc+sdc
                            if 0<=nnr<GRID_SIZE and 0<=nnc<GRID_SIZE and grid[nnr,nnc]==EMPTY and (nnr,nnc)!=(r,c):
                                grid[nr,nc]=HUMAN
                                grid[nnr,nnc]=HUMAN
                                added_human_pairs.append( [(nr,nc),(nnr,nnc)] )
                                birth_events.append( (step, 'HUMAN', nr, nc, nnr, nnc) )
                                break
                        break
        dolphin_pairs.extend(added_dolphin_pairs)
        human_pairs.extend(added_human_pairs)
        # Illness random removal
        if step>0:
            for species, pairs, code, ill_rate in [ ('DOLPHIN',dolphin_pairs,DOLPHIN,ILLNESS_RATE_DOLPHIN), ('HUMAN',human_pairs,HUMAN,ILLNESS_RATE_HUMAN) ]:
                if len(pairs)==0:
                    continue
                N_die = int(len(pairs)*ill_rate)
                if N_die>0:
                    to_kill = np.random.choice( len(pairs), N_die, replace=False )
                    kill_idx_sorted = sorted(to_kill, reverse=True)
                    for idx in kill_idx_sorted:
                        for cell in pairs[idx]:
                            grid[cell[0],cell[1]] = EMPTY
                        illness_events.append( (step, species, pairs[idx][0], pairs[idx][1]) )
                        del pairs[idx]
        N_d = len(dolphin_pairs)*PAIR_SIZE
        N_h = len(human_pairs)*PAIR_SIZE
        pop_stats.append( (step, N_d, N_h) )
        if step == 15:
            img = render_grid(grid, step, annotate="Humans introduced (250)")
        else:
            img = render_grid(grid, step)
        frames.append(img)
        # Log step stats
        log_lines.append(f"{datetime.now().isoformat()} | Step {step}: {N_d} dolphins, {N_h} humans. Births: {len(added_dolphin_pairs)+len(added_human_pairs)}. Deaths: {len(illness_events)}")
    # Write GIF
    gif_path = '/root/human_dolphin_competition_cluster50x50.gif'
    imageio.mimsave(gif_path, frames, duration=0.18)
    # Write log
    log_path = '/root/human_dolphin_competition_cluster50x50_log.txt'
    with open(log_path,'w') as f:
        for l in log_lines:
            f.write(l+'\n')
        f.write('--- Major births ---\n')
        for b in birth_events:
            f.write(f"{b}\n")
        f.write('--- Major illness events ---\n')
        for ie in illness_events:
            f.write(f"{ie}\n")
    ok, problems = validate_pairs(grid, dolphin_pairs, human_pairs)
    if not ok:
        with open(log_path,'a') as f:
            f.write('*** Pair placement validation: problems found!\n')
            for pl in problems:
                f.write(pl+'\n')
        fix_pair_overlaps(grid, dolphin_pairs, human_pairs, log_path)
    final_d = len(dolphin_pairs)*PAIR_SIZE
    final_h = len(human_pairs)*PAIR_SIZE
    summary = [
        f"Simulation completed. Step={TIMESTEPS-1}, Grid {GRID_SIZE}x{GRID_SIZE}",
        f"Final dolphins: {final_d}\nFinal humans: {final_h}",
        f"Major events:",
        f"* {DOLPHIN_PAIRS} dolphin pairs founded in central 15x15 cluster (step 0)",
        f"* {HUMAN_PAIRS} human pairs introduced at step 15, outside cluster if possible",
        f"* Random death per step: dolphins {ILLNESS_RATE_DOLPHIN*100:.1f}%, humans {ILLNESS_RATE_HUMAN*100:.1f}%",
        f"* Copulation: each pair may reproduce if local free space available",
        f"* Humans placed at min Manhattan dist={HUMAN_PAIR_MINDIST} (or relaxed to 2 if grid too full)",
        f"Outcome: {'Humans survived' if final_h>0 else 'Humans eliminated'}, {'Dolphins survived' if final_d>0 else 'Dolphins eliminated' if final_d==0 else ''}",
        f"Total steps: {TIMESTEPS-1}",
        f"Check log for detailed event and placement audit."
    ]
    summary_path = '/root/human_dolphin_competition_cluster50x50_summary.txt'
    with open(summary_path,'w') as f:
        for line in summary:
            f.write(line+'\n')
    print(f"---- Finished simulation ----\nSee: {gif_path}\nLog: {log_path}\nSummary: {summary_path}")

if __name__ == "__main__":
    simulate()
