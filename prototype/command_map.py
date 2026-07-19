"""
Explanatory diagram, not measured data.

Terminally-Addicted puts one curses window in front of six different
services. This script draws that shape directly: the terminal in the
center, a command out to each service, and the reply landing back in the
same window. No screenshot, no invented numbers — just the map of what
talks to what.

Run:
    MPLCONFIGDIR=/home/arya/projects/hackathons/.mplcache \
    /home/arya/projects/hackathons/.venv/bin/python prototype/command_map.py
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

plt.style.use("/home/arya/projects/hackathons/.style/garg-paper.mplstyle")

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

CENTER = np.array([6.0, 6.0])
RADIUS = 4.6

# (angle in degrees, node label, command, dry one-line caption, accent color)
SATELLITES = [
    (90, "Spotify API", "$sp", "search / queue / skip / play / pause", "#3b42db"),
    (30, "GitHub API", "$git", "create / close / comment / search issues", "#3b42db"),
    (-30, "Todoist API", "$todo", "add / list tasks", "#3b42db"),
    (-90, "OpenAI (GPT-4o-mini)", "$chat", "prompt in, reply back in-pane", "#e85b30"),
    (-150, "YouTube → ASCII renderer", "/yt", "search, download, render as terminal video", "#c2491d"),
    (150, "Vim", "$set env", "opens .env directly, no browser needed", "#6f2f96"),
]

INK = "#282215"
EDGE = "#c6b99f"

fig, ax = plt.subplots(figsize=(12, 12))
ax.set_xlim(0, 12)
ax.set_ylim(0, 12)
ax.set_aspect("equal")
ax.axis("off")

ax.set_title(
    "Terminally-Addicted: one curses window, six APIs\n"
    "concept sketch — what it does, drawn instead of screenshotted",
    loc="left",
)

# Center node: the curses terminal window.
center_box = FancyBboxPatch(
    CENTER - np.array([1.3, 0.6]), 2.6, 1.2,
    boxstyle="square,pad=0.05",
    facecolor="#eae4d6", edgecolor=INK, linewidth=1.4, zorder=3,
)
ax.add_patch(center_box)
ax.text(*CENTER, "curses terminal\n(command bar + panes)",
        ha="center", va="center", fontsize=10, fontweight="medium", zorder=4)

for angle_deg, label, command, caption, color in SATELLITES:
    theta = np.radians(angle_deg)
    direction = np.array([np.cos(theta), np.sin(theta)])
    pos = CENTER + RADIUS * direction

    box = FancyBboxPatch(
        pos - np.array([1.35, 0.45]), 2.7, 0.9,
        boxstyle="square,pad=0.05",
        facecolor="#eae4d6", edgecolor=EDGE, linewidth=1.2, zorder=3,
    )
    ax.add_patch(box)
    ax.text(pos[0], pos[1] + 0.13, label, ha="center", va="center",
            fontsize=9.5, zorder=4)
    ax.text(pos[0], pos[1] - 0.22, caption, ha="center", va="center",
            fontsize=7, color=INK, style="italic", zorder=4)

    # Arrow from center box edge to satellite box edge, so it doesn't
    # start/end buried inside either box.
    start = CENTER + direction * 1.3
    end = pos - direction * 1.35

    arrow = FancyArrowPatch(
        start, end,
        arrowstyle="<->", mutation_scale=14,
        color=color, linewidth=1.6, zorder=2,
    )
    ax.add_patch(arrow)

    # Command label sits just off the arrow's midpoint, offset
    # perpendicular to the arrow so it never overlaps the line itself.
    mid = (start + end) / 2
    perp = np.array([-direction[1], direction[0]])
    label_pos = mid + perp * 0.4
    ax.text(*label_pos, command, ha="center", va="center",
            fontsize=9.5, fontweight="medium", color=color, zorder=4)

fig.savefig(os.path.join(FIGURES_DIR, "command_map.png"), dpi=200)
plt.close(fig)

print(f"Wrote {FIGURES_DIR}/command_map.png")
