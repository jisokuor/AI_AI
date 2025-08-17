# grid_competition.py
"""
Spatial Competition Simulation: Dolphins vs Humans
-------------------------------------------------
Implements a 50x50 grid simulation of spatial expansion, sex-ratio, and density dependence for two species.

Outputs:
    - /root/grid_competition.gif
    - /root/grid_competition_population.txt
    - /root/grid_competition_summary.txt

Dependencies: numpy, matplotlib, pillow
"""
# ===========================
# USER PARAMETERS
# ===========================
GRID_SIZE = 50               # 40 or 50 (default: 50 for speed)
DOLPHIN_BLOB_FRAC = 0.3      # initial fraction of map for dolphin blob
DOLPHIN_SEED_POS = (GRID_SIZE//2, GRID_SIZE//2)   # Center seed (can randomize)
HUMAN_N = 4                  # always 4 humans
MAX_STEPS = 150
ILLNESS_ENABLED = True       # set False to disable density-dependent illness
ILLNESS_FACTOR = 0.8         # relative risk; per neighbor occupied fraction * this constant
GIF_FRAME_INTERVAL = 1       # Render every N steps
RANDOM_SEED = 137            # For reproducibility

# ===========================
# IMPORTS
# ===========================
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Headless
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import random
import os

# ===========================
# GLOBALS & SETUP
# ===========================
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)
OUTPUT_DIR = '/root'
GIF_PATH = OUTPUT_DIR + '/grid_competition.gif'
POP_TABLE_PATH = OUTPUT_DIR + '/grid_competition_population.txt'
SUMMARY_PATH = OUTPUT_DIR + '/grid_competition_summary.txt'

SPECIES = {'empty':0, 'dolphin':1, 'human':2}
SEX = {'none':0, 'male':1, 'female':2}
COLORS = {
    (1,1): (90,180,250),    # Dolphin male: blue
    (1,2): (220,110,190),   # Dolphin female: magenta
    (2,1): (60,180,90),     # Human male: green
    (2,2): (255,180,60),    # Human female: orange
    (0,0): (255,255,255),   # Empty: white
}
ANNOT_FONT = None
try:
    ANNOT_FONT = ImageFont.truetype("DejaVuSans-Bold.ttf", 14)
except:
    ANNOT_FONT = None

# ... [truncated for brevity; will untruncate full code in next cell if not successful] ...
