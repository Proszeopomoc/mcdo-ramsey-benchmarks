from pathlib import Path
from itertools import combinations
import urllib.request
import hashlib
import csv
import json
import math

import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

REPO = Path(r"C:\github\mcdo-ramsey-benchmarks")
FIG = REPO / "figures"
SRC = FIG / "_source_graph6"
SRC.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://users.cecs.anu.edu.au/~bdm/data"
DPI = 220

def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def normalize_edges(edges):
    out = set()
    for a, b in edges:
        a = int(a)
        b = int(b)
        if a == b:
            continue
        if a > b:
            a, b = b, a
        out.add((a, b))
    return sorted(out)

def graph6_tokens(path):
    txt = Path(path).read_text(encoding="ascii", errors="replace")
    return [x.strip() for x in txt.split() if x.strip()]

def get_graphs(filename, url):
    path = SRC / filename
    if not path.exists():
        urllib.request.urlretrieve(url, path)
    return path, [nx.from_graph6_bytes(x.encode("ascii")) for x in graph6_tokens(path)]

def cycle_graph_5():
    return nx.cycle_graph(5)

def draw_single(G, title, subtitle, stem, layout="circle"):
    n = G.number_of_nodes()
    K = nx.complete_graph(n)
    red_edges = normalize_edges(G.edges())
    red_set = set(red_edges)
    blue_edges = [e for e in normalize_edges(K.edges()) if e not in red_set]

    if layout == "circle":
        pos = nx.circular_layout(G)
    else:
        pos = nx.spring_layout(G, seed=42, k=0.85, iterations=900)

    fig, ax = plt.subplots(figsize=(14, 14), dpi=DPI)
    ax.set_facecolor("white")

    nx.draw_networkx_edges(
        K, pos,
        edgelist=blue_edges,
        edge_color="#6aaed6",
        width=0.7 if n > 20 else 1.1,
        alpha=0.18 if n > 20 else 0.30,
        ax=ax
    )

    nx.draw_networkx_edges(
        G, pos,
        edgelist=red_edges,
        edge_color="#cc2222",
        width=1.7 if n > 20 else 2.8,
        alpha=0.92,
        ax=ax
    )

    node_size = 750 if n > 20 else 1450
    font_size = 7 if n > 20 else 11

    nx.draw_networkx_nodes(
        G, pos,
        node_color="white",
        node_size=node_size,
        edgecolors="black",
        linewidths=1.4,
        ax=ax
    )

    nx.draw_networkx_labels(
        G, pos,
        labels={i: str(i) for i in G.nodes()},
        font_size=font_size,
        font_weight="bold",
        ax=ax
    )

    ax.set_title(
        f"{title}\n{subtitle}\nN={n}, red_edges={len(red_edges)}, blue_edges={len(blue_edges)}",
        fontsize=15,
        pad=16
    )
    ax.axis("off")
    plt.tight_layout()

    png = FIG / f"{stem}.png"
    pdf = FIG / f"{stem}.pdf"

    plt.savefig(png, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.savefig(pdf, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    return {
        "stem": stem,
        "title": title,
        "n": n,
        "red_edges": len(red_edges),
        "blue_edges": len(blue_edges),
        "png": str(png.relative_to(REPO)),
        "pdf": str(pdf.relative_to(REPO))
    }

def draw_contact_sheet(graphs, title, subtitle, stem, cols=3):
    count = len(graphs)
    rows = math.ceil(count / cols)

    fig = plt.figure(figsize=(cols * 5.2, rows * 4.4 + 1.2), dpi=200)

    for idx, G in enumerate(graphs):
        ax = fig.add_subplot(rows, cols, idx + 1)
        n = G.number_of_nodes()
        K = nx.complete_graph(n)
        red_edges = normalize_edges(G.edges())
        red_set = set(red_edges)
        blue_edges = [e for e in normalize_edges(K.edges()) if e not in red_set]

        if n <= 20:
            pos = nx.circular_layout(G)
        else:
            pos = nx.spring_layout(G, seed=100 + idx, k=0.85, iterations=700)

        nx.draw_networkx_edges(
            K, pos,
            edgelist=blue_edges,
            edge_color="#6aaed6",
            width=0.35,
            alpha=0.15,
            ax=ax
        )

        nx.draw_networkx_edges(
            G, pos,
            edgelist=red_edges,
            edge_color="#cc2222",
            width=0.9,
            alpha=0.9,
            ax=ax
        )

        nx.draw_networkx_nodes(
            G, pos,
            node_color="white",
            node_size=130 if n > 20 else 220,
            edgecolors="black",
            linewidths=0.55,
            ax=ax
        )

        nx.draw_networkx_labels(
            G, pos,
            labels={i: str(i) for i in G.nodes()},
            font_size=3 if n > 20 else 5,
            ax=ax
        )

        ax.set_title(f"Graph {idx + 1}", fontsize=8)
        ax.axis("off")

    fig.suptitle(f"{title}\n{subtitle}", fontsize=18)
    plt.tight_layout(rect=[0, 0, 1, 0.94])

    png = FIG / f"{stem}.png"
    pdf = FIG / f"{stem}.pdf"

    plt.savefig(png, dpi=200, bbox_inches="tight", facecolor="white")
    plt.savefig(pdf, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    return {
        "stem": stem,
        "title": title,
        "count": count,
        "png": str(png.relative_to(REPO)),
        "pdf": str(pdf.relative_to(REPO))
    }

outputs = []

# R(3,3), K5
outputs.append(draw_single(
    cycle_graph_5(),
    "R(3,3) lower-bound witness",
    "K5 counterexample",
    "R33_K5_counterexample",
    "circle"
))

# R(3,4), K8
_, graphs = get_graphs("r34_8.g6", BASE_URL + "/r34_8.g6")
outputs.append(draw_single(
    graphs[0],
    "R(3,4) lower-bound witness",
    "K8 graph from the official catalogue",
    "R34_K8_counterexample",
    "circle"
))

# R(3,5), K13
_, graphs = get_graphs("r35_13.g6", BASE_URL + "/r35_13.g6")
outputs.append(draw_single(
    graphs[0],
    "R(3,5) lower-bound witness",
    "K13 unique graph from the official catalogue",
    "R35_K13_unique_counterexample",
    "circle"
))

# R(3,6), K17, all 7
_, graphs = get_graphs("r36_17.g6", BASE_URL + "/r36_17.g6")
outputs.append(draw_contact_sheet(
    graphs,
    "All Ramsey(3,6,17) graphs",
    "7 official graphs",
    "R36_K17_all_7_graphs",
    cols=3
))
outputs.append(draw_single(
    graphs[0],
    "R(3,6) lower-bound witness",
    "K17 graph 1 of 7 official graphs",
    "R36_K17_graph_1",
    "circle"
))

# R(4,4), K17
try:
    _, graphs = get_graphs("r44_17.g6", BASE_URL + "/r44_17.g6")
    G44 = graphs[0]
    sub44 = "K17 unique official graph"
except Exception:
    p = 17
    residues = set((x * x) % p for x in range(1, p))
    G44 = nx.Graph()
    G44.add_nodes_from(range(p))
    for i in range(p):
        for j in range(i + 1, p):
            if ((j - i) % p) in residues:
                G44.add_edge(i, j)
    sub44 = "K17 Paley graph construction"

outputs.append(draw_single(
    G44,
    "R(4,4) lower-bound witness",
    sub44,
    "R44_K17_unique_counterexample",
    "circle"
))

# R(3,9), K35
_, graphs = get_graphs("r39_35.g6", BASE_URL + "/r39_35.g6")
outputs.append(draw_single(
    graphs[0],
    "R(3,9) maximal graph",
    "K35 unique official graph",
    "R39_K35_unique_graph",
    "spring"
))

# R(4,6), K35, 37 known graphs
_, graphs = get_graphs("r46_35some.g6", BASE_URL + "/r46_35some.g6")
outputs.append(draw_contact_sheet(
    graphs,
    "Largest known Ramsey(4,6,35) graphs",
    "37 known graphs, contact sheet",
    "R46_K35_all_37_known_graphs",
    cols=5
))
outputs.append(draw_single(
    graphs[0],
    "Largest known Ramsey(4,6,35) graph",
    "Representative graph 1 of 37 known graphs",
    "R46_K35_representative_graph_1",
    "spring"
))

# R(5,5), K42 known reference sample
_, graphs = get_graphs("r55_42some.g6", BASE_URL + "/r55_42some.g6")
G55 = graphs[0]

outputs.append(draw_single(
    G55,
    "R(5,5) known reference example",
    "K42 first source graph from r55_42some.g6",
    "R55_K42_reference_source_1",
    "spring"
))

outputs.append(draw_single(
    nx.complement(G55),
    "R(5,5) known reference example",
    "K42 complement of first source graph",
    "R55_K42_reference_complement_1",
    "spring"
))

# Combined PDF
packet = FIG / "RAMSEY_FIGURES_PACKET.pdf"
with PdfPages(packet) as pdf:
    for out in outputs:
        png_path = REPO / out["png"]
        if png_path.exists():
            img = plt.imread(png_path)
            fig, ax = plt.subplots(figsize=(11.69, 8.27))
            ax.imshow(img)
            ax.axis("off")
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)

# Figure index
fig_csv = FIG / "FIGURE_INDEX.csv"
fields = sorted(set(k for row in outputs for k in row.keys()))
with fig_csv.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for row in outputs:
        w.writerow(row)

# Figures README
fig_readme = FIG / "README.md"
fig_readme.write_text(
"""# Public Ramsey graph figures

This directory contains selected public Ramsey graph figures.

Included:

- R(3,3), K5 lower-bound witness
- R(3,4), K8 lower-bound witness
- R(3,5), K13 unique lower-bound witness
- R(3,6), K17 all 7 official graphs
- R(4,4), K17 lower-bound witness
- R(3,9), K35 unique official graph
- R(4,6), K35 known sample of 37 graphs
- R(5,5), K42 known reference example and complement

These figures are documentation artifacts. They do not disclose the private solver implementation.
""",
encoding="utf-8"
)

# Update main README
readme = REPO / "README.md"
txt = readme.read_text(encoding="utf-8", errors="replace") if readme.exists() else ""
if "## Figures" not in txt:
    with readme.open("a", encoding="utf-8") as f:
        f.write("\n\n## Figures\n\n")
        f.write("Selected public Ramsey graph figures are available in the `figures/` directory.\n\n")
        f.write("See `figures/RAMSEY_FIGURES_PACKET.pdf` for a combined PDF.\n")
        f.write("\nThese figures are documentation artifacts. They do not disclose the private solver implementation.\n")

# Figure manifest
manifest = FIG / "SHA256_FIGURES_MANIFEST.txt"
lines = []
for p in sorted(FIG.rglob("*")):
    if p.is_file() and p.name != "SHA256_FIGURES_MANIFEST.txt":
        lines.append(f"{p.relative_to(FIG).as_posix()}  {sha256_file(p)}")
manifest.write_text("\n".join(lines), encoding="utf-8")

print("")
print("=== RESULT ===")
print("FINAL_STATUS: FIGURES_CREATED")
print("FIG_DIR:", FIG)
print("PACKET:", packet)
print("FIGURE_INDEX:", fig_csv)
print("MANIFEST:", manifest)
print("")
for out in outputs:
    print(out.get("stem"), out.get("png"), out.get("pdf"))
