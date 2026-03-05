import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(figsize=(15, 7))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')
ax.axis('off')
ax.set_xlim(0, 15)
ax.set_ylim(0, 7)

BOX_BG = "#d4d4d4"
BOX_EC = "#888888"
CONTAINER_EC = "#333333"
TEXT_COLOR = "#111111"
TITLE_COLOR = "#111111"

def draw_box(ax, x, y, w, h, label, title=None, fontsize=9.5):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                         facecolor=BOX_BG, edgecolor=BOX_EC, linewidth=1.5, zorder=3)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, label, ha='center', va='center',
            fontsize=fontsize, fontweight='bold', color=TEXT_COLOR, zorder=4)
    if title:
        ax.text(x + w/2, y + h + 0.23, title, ha='center', va='bottom',
                fontsize=9.5, fontweight='bold', color=TITLE_COLOR, zorder=4)

def draw_container(ax, x, y, w, h, label=None):
    rect = patches.Rectangle((x, y), w, h, facecolor='none',
                              edgecolor=CONTAINER_EC, linewidth=1.5, zorder=2)
    ax.add_patch(rect)
    if label:
        ax.text(x + w/2, y + h + 0.15, label, ha='center', va='bottom',
                fontsize=10, fontweight='bold', color=TITLE_COLOR, zorder=4)

def draw_cloud(ax, cx, cy, label, title=None):
    """Draw a cloud shape centred at (cx, cy)."""
    radii = [0.65, 0.50, 0.60, 0.50, 0.70, 0.55]
    offsets = [(-0.7, 0.25), (-0.1, 0.55), (0.5, 0.4), (0.85, -0.1), (0.15, -0.4), (-0.55, -0.3)]
    for (dx, dy), r in zip(offsets, radii):
        c = plt.Circle((cx + dx, cy + dy), r, facecolor=BOX_BG, edgecolor=BOX_EC, linewidth=1, zorder=3)
        ax.add_artist(c)
    ax.text(cx, cy + 0.1, label, ha='center', va='center',
            fontsize=8.5, fontweight='bold', color=TEXT_COLOR, zorder=5, multialignment='center')
    if title:
        ax.text(cx, cy + 1.05, title, ha='center', va='bottom',
                fontsize=9.5, fontweight='bold', color=TITLE_COLOR, zorder=5)

def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.3), zorder=5)

def line(ax, xs, ys):
    ax.plot(xs, ys, color='black', lw=1.3, zorder=5)


# ─── 1. User Interface box (left) ───────────────────────────────────────────
draw_box(ax, 0.3, 2.8, 2.2, 1.6, "User\nInput / Response", title="User\nInterface")

# ─── 2. Big container (Information + Storage + NLP sub zone) ────────────────
draw_container(ax, 3.2, 0.8, 7.8, 5.4)

# ─── 3. Information Unit ────────────────────────────────────────────────────
draw_box(ax, 3.7, 3.5, 2.4, 1.5, "Agent A:\nGemini Parser", title="Information\nUnit")

# ─── 4. Storage Unit ────────────────────────────────────────────────────────
draw_box(ax, 7.3, 3.5, 2.4, 1.5, "Predefined\nPrompts &\nContext", title="Storage\nUnit")

# ─── 5. NLP / Multi-Agent sub-container ─────────────────────────────────────
draw_container(ax, 5.5, 1.0, 4.5, 1.9)
ax.text(5.5 + 4.5/2, 3.0, "NLP Models", ha='center', va='bottom',
        fontsize=9.5, fontweight='bold', color=TITLE_COLOR, zorder=4)

draw_box(ax, 5.75, 1.2, 1.8, 1.4, "Agent B\n(Scout)", fontsize=9)
draw_box(ax, 7.95, 1.2, 1.8, 1.4, "Agent C\n(Auditor)", fontsize=9)

# ─── 6. Integration Unit (cloud, right) ─────────────────────────────────────
draw_cloud(ax, 13.0, 3.65,
           "GitHub Report\nWeb Search\nSlack / Email\n2026 Ready",
           title="Integration\nUnit")

# ─── ARROWS ──────────────────────────────────────────────────────────────────
# Input: User → Information Unit
arrow(ax, 2.55, 3.6, 3.68, 4.1)
ax.text(3.05, 3.9, "Input", fontsize=8.5, fontweight='bold', ha='center')

# Information Unit → Storage Unit
arrow(ax, 6.12, 4.25, 7.28, 4.25)

# Storage Unit → NLP sub-container
arrow(ax, 8.5, 3.48, 8.5, 2.92)

# NLP sub-container → Integration Unit
line(ax, [11.02, 12.0], [1.95, 1.95])
arrow(ax, 12.0, 1.95, 12.0, 3.0)

# Response: bottom of NLP sub → bottom of User box
line(ax,  [5.5, 1.4], [1.0, 1.0])
arrow(ax, 1.4, 1.0, 1.4, 2.78)
ax.text(3.3, 0.75, "Response", fontsize=8.5, fontweight='bold', ha='center')

# Storage → Integration
arrow(ax, 11.02, 4.25, 12.05, 4.25)

plt.tight_layout(pad=0.2)
plt.savefig("v:/PROJECTS/ai+agent/workflow_demo.png", dpi=200, bbox_inches='tight', facecolor='white')
print("Saved!")
