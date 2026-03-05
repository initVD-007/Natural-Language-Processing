import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(12, 6))
ax.axis('off')
ax.set_xlim(0, 15)
ax.set_ylim(0, 7)

# Colors matching the requested visual style
BOX_BG = "#cccccc"
BOX_EC = "#aaaaaa"
TEXT_COLOR = "black"

def draw_round_box(x, y, w, h, text, title=""):
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2", ec=BOX_EC, fc=BOX_BG, zorder=3)
    ax.add_patch(box)
    if title:
        ax.text(x + w/2, y + h + 0.35, title, ha='center', va='center', fontsize=11, fontweight='bold', color=TEXT_COLOR)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=10, fontweight='bold', color=TEXT_COLOR)

def draw_container(x, y, w, h):
    rect = patches.Rectangle((x, y), w, h, fill=False, edgecolor='black', linewidth=1.2, zorder=2)
    ax.add_patch(rect)

def draw_cloud(x, y, w, h, text, title=""):
    c1 = patches.Circle((x+0.5, y+0.5), 0.6, ec="none", fc=BOX_BG, zorder=3)
    c2 = patches.Circle((x+1.2, y+1.0), 0.8, ec="none", fc=BOX_BG, zorder=3)
    c3 = patches.Circle((x+1.8, y+0.6), 0.7, ec="none", fc=BOX_BG, zorder=3)
    c4 = patches.Circle((x+1.0, y+0.2), 0.6, ec="none", fc=BOX_BG, zorder=3)
    c5 = patches.Circle((x+2.0, y-0.1), 0.6, ec="none", fc=BOX_BG, zorder=3)
    c6 = patches.Circle((x+0.5, y-0.2), 0.5, ec="none", fc=BOX_BG, zorder=3)
    c7 = patches.Circle((x+1.2, y-0.5), 0.7, ec="none", fc=BOX_BG, zorder=3)
    for c in [c1, c2, c3, c4, c5, c6, c7]:
        ax.add_patch(c)
    
    if title:
        ax.text(x + w/2, y + 1.2 + 0.4, title, ha='center', va='center', fontsize=11, fontweight='bold', color=TEXT_COLOR)
    ax.text(x + w/2, y + h/2 - 0.2, text, ha='center', va='center', fontsize=10, fontweight='bold', color=TEXT_COLOR)

def draw_arrow(x1, y1, x2, y2, text="", arrowstyle="-|>", connectionstyle="arc3"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), 
                arrowprops=dict(arrowstyle=arrowstyle, facecolor='black', edgecolor='black', lw=1.2, connectionstyle=connectionstyle), zorder=1)
    if text:
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.3, text, ha='center', va='center', fontsize=10, fontweight='bold')

# Architecture Elements
# Left
draw_round_box(0.5, 3.5, 2.5, 1.5, "Streamlit\nApp Output", title="User\nInterface")

# Middle Container Box
draw_container(4.5, 0.5, 7.5, 6)

# Middle inner items
draw_round_box(5.0, 4.5, 2.5, 1.2, "Agent A:\nParser", title="Information\nUnit")
draw_round_box(8.5, 4.5, 2.5, 1.2, "Semantic\nEngine", title="Storage\nUnit")

# NLP Models replacement (Multi-Agents)
# White container for the sub list
rect = patches.Rectangle((7.0, 1.5), 4.5, 1.8, fill=True, facecolor='white', edgecolor='black', linewidth=1, zorder=4)
ax.add_patch(rect)
ax.text(7.0 + 4.5/2, 1.5 + 1.8 - 0.3, "Multi-Agent Query generation", ha='center', va='center', fontsize=10, fontweight='bold', zorder=5)
draw_round_box(7.5, 1.7, 1.5, 0.6, "Agent B\n(Scout)")
draw_round_box(9.5, 1.7, 1.5, 0.6, "Agent C\n(Auditor)")

# Right
draw_cloud(13.5, 3.5, 2.5, 1.5, "PDF Export\nWeb Search\n2026 Ready", title="Integration\nUnit")

# Arrows
draw_arrow(3.2, 4.25, 4.8, 4.25, "Input")
draw_arrow(7.7, 5.1, 8.3, 5.1, "")
draw_arrow(9.75, 4.3, 9.75, 3.5, "")

# Return response arrow (from NLP box back to User UI)
draw_arrow(7.0, 1.8, 1.75, 1.8, "", arrowstyle="-", connectionstyle="arc3")
draw_arrow(1.75, 1.8, 1.75, 3.2, "", arrowstyle="-|>", connectionstyle="arc3")
ax.text(3.5, 2.0, "Response", ha='center', va='center', fontsize=10, fontweight='bold')

# Arrow to integration
draw_arrow(12.0, 4.25, 12.8, 4.25, "")

plt.tight_layout()
plt.savefig("v:/PROJECTS/ai+agent/workflow_demo.png", dpi=300, bbox_inches='tight')
