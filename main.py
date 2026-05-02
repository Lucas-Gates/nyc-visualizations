import time
from vis_code.clean_data import load_and_clean_data
from vis_code.Dist_1 import dist1
from vis_code.Dist_2 import dist2
from vis_code.relationships import relPlot
from vis_code.Agg import agg
from vis_code.Parallel import parallel

# ── Constants ────────────────────────────────────────────────────────────────

TITLE = [
    "  ██████╗ ███████╗    ██████╗ ██████╗   █████╗   █████╗ ",
    " ██╔════╝ ██╔════╝    ╚════██╗╚════██╗ ██╔═████╗██╔═████╗",
    " ██║      ███████╗     █████╔╝ █████╔╝ ██║██╔██║██║██╔██║",
    " ██║      ╚════██║    ██╔═══╝  ╚═══██╗ ████╔╝██║████╔╝██║",
    " ╚██████╗ ███████║    ███████╗██████╔╝ ╚██████╔╝╚██████╔╝",
    "  ╚═════╝ ╚══════╝    ╚══════╝╚═════╝   ╚═════╝  ╚═════╝ ",
]

SUBTITLE = [
    "┌────────────────────────────────────────────────────────┐",
    "│          NYC Motor Vehicle Collision Analysis          │",
    "│                     Final Project                      │",
    "│                                                        │",
    "│        Kyle Zink  —  Zen Mitchell  —  Lucas Gate       │",
    "└────────────────────────────────────────────────────────┘",
]

OUTRO = [
    "┌─────────────────────────────────────────────────────────────┐",
    "│                     End of Program                          │",
    "│              Thank you for running our project!             │",
    "│          Kyle Zink  —  Zen Mitchell  —  Lucas Gates         │",
    "└─────────────────────────────────────────────────────────────┘",
]

MENU = """
══════════════════════════════════════════
             CONTROL PANEL               
══════════════════════════════════════════
  1  ►  Severity Distribution
  2  ►  Crashes by Hour Distribution
  3  ►  Relationship Visualization
  4  ►  Aggregated Crashes by Borough
  5  ►  Parallel Coordinates
  6  ►  Run All Visualizations
──────────────────────────────────────────
  0  ►  Quit
══════════════════════════════════════════"""


# ── Helpers ──────────────────────────────────────────────────────────────────

def typewrite(text, delay=0.4, dots=3):
    """Prints text followed by animated dots."""
    print(text, end="")
    for _ in range(dots):
        time.sleep(delay)
        print(".", end="", flush=True)
    print()

def print_animated(lines, delay):
    """Prints a list of lines with a delay between each."""
    for line in lines:
        print(line)
        time.sleep(delay)


# ── Main ─────────────────────────────────────────────────────────────────────

# Header
print()
print_animated(TITLE, delay=0.07)
print()
print_animated(SUBTITLE, delay=0.06)
print()

# Load & clean data
df_clean = load_and_clean_data()

# Map each menu choice to its function(s)
ACTIONS = {
    "1": lambda: dist1(df_clean),
    "2": lambda: dist2(df_clean),
    "3": lambda: relPlot(df_clean),
    "4": lambda: agg(df_clean),
    "5": lambda: parallel(df_clean),
    "6": lambda: [dist1(df_clean), dist2(df_clean), relPlot(df_clean), agg(df_clean), parallel(df_clean)],
}

# Control loop
while True:
    print(MENU)
    choice = input("\n    Enter your choice: ").strip()

    if choice == "0":
        print()
        print_animated(OUTRO, delay=0.04)
        print()
        typewrite("Goodbye", delay=0.4, dots=3)
        print()
        break

    elif choice in ACTIONS:
        ACTIONS[choice]()

    else:
        print("\n    Invalid choice. Please try again.")