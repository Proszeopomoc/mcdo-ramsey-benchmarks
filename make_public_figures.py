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
FIG.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://users.cecs.anu.edu.au/~bdm/data"

DPI = 300

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

def read_graph6_tokens(path):
    txt = Path(path).read_text(encoding="ascii", errors="replace")
    return [x.strip() for x in txt.split() if x.strip()]

def graph_from_g6_token(token):
    return nx.from_graph6_bytes(token.encode("ascii"))

def download_graphs(name, url):
    data_dir = FIG / "_source_graph6"
    data_dir.mkdir(parents=True, exist_ok=True)
    path = data_dir / name
    if not path.exists():
        urllib.request.urlretrieve(url, path)
    tokens = read_graph6_tokens(path)
    graphs = [graph_from_g6_token(tok) for tok in tokens]
    return path, graphs

def cyclic_graph(n, generators):
    gens = set(generators)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            d = (j - i) % n
            d = min(d, n - d)
            if d in gens:
                G.add_edge(i, j)
    return G

def paley_graph(p):
    residues = set((x * x) % p for x in range(1, p))
    G = nx.Graph()
    G.add_nodes_from(range(p))
    for i in range(p):
        for j in range(i + 1, p):
            d = (j - i) % p
            if d in residues:
                G.add_edge(i, j)
    return G

def draw_graph(G, title, subtitle, out_stem, layout="circle", figsize=(16,16)):
    n = G.number_of_nodes()
    complete = nx.complete_graph(n)
    red_edges = normalize_edges(G.edges())
    red_set = set(red_edges)
    blue_edges = [e for e in normalize_edges(complete.edges()) if e not in red_set]

    if layout == "circle":
        pos = nx.circular_layout(G)
    else:
        pos = nx.spring_layout(G, seed=42, k=0.9, iterations=900)

    fig, ax = plt.subplots(figsize=figsize, dpi=DPI)
    ax.set_facecolor("white")

    nx.draw_networkx_edges(
        complete, pos,
        edgelist=blue_edges,
        edge_color="#6aaed6",
        width=0.7 if n > 20 else 1.2,
        alpha=0.18 if n > 20 else 0.28,
        ax=ax
    )

    nx.draw_networkx_edges(
        G, pos,
        edgelist=red_edges,
        edge_color="#cc2222",
        width=1.6 if n > 20 else 2.8,
        alpha=0.92,
        ax=ax
    )

    node_size = 900 if n > 20 else 1500
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
        fontsize=17,
        pad=18
    )
    ax.axis("off")
    plt.tight_layout()

    png = FIG / f"{out_stem}.png"
    pdf = FIG / f"{out_stem}.pdf"
    svg = FIG / f"{out_stem}.svg"

    plt.savefig(png, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.savefig(pdf, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.savefig(svg, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    return {
        "stem": out_stem,
        "png": str(png),
        "pdf": str(pdf),
        "svg": str(svg),
        "n": n,
        "red_edges": len(red_edges),
        "blue_edges": len(blue_edges)
    }

def draw_contact_sheet(graphs, title, subtitle, out_stem, cols=3):
    count = len(graphs)
    rows = math.ceil(count / cols)
    fig = plt.figure(figsize=(cols * 5.2, rows * 4.4 + 1.2), dpi=220)

    for idx, G in enumerate(graphs):
        ax = fig.add_subplot(rows, cols, idx + 1)
        n = G.number_of_nodes()
        complete = nx.complete_graph(n)
        red_edges = normalize_edges(G.edges())
        red_set = set(red_edges)
        blue_edges = [e for e in normalize_edges(complete.edges()) if e not in red_set]
        pos = nx.circular_layout(G) if n <= 20 else nx.spring_layout(G, seed=100 + idx, k=0.9, iterations=700)

        nx.draw_networkx_edges(complete, pos, edgelist=blue_edges, edge_color="#6aaed6", width=0.35, alpha=0.15, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color="#cc2222", width=0.9, alpha=0.9, ax=ax)
        nx.draw_networkx_nodes(G, pos, node_color="white", node_size=130 if n > 20 else 220, edgecolors="black", linewidths=0.55, ax=ax)
        nx.draw_networkx_labels(G, pos, labels={i: str(i) for i in G.nodes()}, font_size=3 if n > 20 else 5, ax=ax)
        ax.set_title(f"Graph {idx + 1}", fontsize=8)
        ax.axis("off")

    fig.suptitle(f"{title}\n{subtitle}", fontsize=18)
    plt.tight_layout(rect=[0, 0, 1, 0.94])

    png = FIG / f"{out_stem}.png"
    pdf = FIG / f"{out_stem}.pdf"
    svg = FIG / f"{out_stem}.svg"

    plt.savefig(png, dpi=220, bbox_inches="tight", facecolor="white")
    plt.savefig(pdf, bbox_inches="tight", facecolor="white")
    plt.savefig(svg, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    return {
        "stem": out_stem,
        "png": str(png),
        "pdf": str(pdf),
        "svg": str(svg),
        "count": count
    }

outputs = []

# R(3,3), K5 witness
G = nx.cycle_graph(5)
outputs.append(draw_graph(
    G,
    "R(3,3) lower-bound witness",
    "K5, one non-isomorphic counterexample",
    "R33_K5_counterexample",
    layout="circle"
))

# R(3,4), K8 sample from official catalogue
p, graphs = download_graphs("r34_8.g6", BASE_URL + "/r34_8.g6")
outputs.append(draw_graph(
    graphs[0],
    "R(3,4) lower-bound witness",
    "K8, first graph from official catalogue",
    "R34_K8_counterexample",
    layout="circle"
))

# R(3,5), K13 unique
p, graphs = download_graphs("r35_13.g6", BASE_URL + "/r35_13.g6")
outputs.append(draw_graph(
    graphs[0],
    "R(3,5) lower-bound witness",
    "K13, unique known graph",
    "R35_K13_unique_counterexample",
    layout="circle"
))

# R(3,6), K17 all 7
p, graphs = download_graphs("r36_17.g6", BASE_URL + "/r36_17.g6")
outputs.append(draw_contact_sheet(
    graphs,
    "All Ramsey(3,6,17) graphs",
    "7 known graphs",
    "R36_K17_all_7_graphs",
    cols=3
))
# also draw first graph
outputs.append(draw_graph(
    graphs[0],
    "R(3,6) lower-bound witness",
    "K17, graph 1 of 7 known graphs",
    "R36_K17_graph_1",
    layout="circle"
))

# R(4,4), Paley17 or official r44_17 if available
try:
    p, graphs = download_graphs("r44_17.g6", BASE_URL + "/r44_17.g6")
    G44 = graphs[0]
    subtitle44 = "K17, unique official graph"
except Exception:
    G44 = paley_graph(17)
    subtitle44 = "K17, Paley graph construction"
outputs.append(draw_graph(
    G44,
    "R(4,4) lower-bound witness",
    subtitle44,
    "R44_K17_unique_counterexample",
    layout="circle"
))

# R(3,9), K35 unique
p, graphs = download_graphs("r39_35.g6", BASE_URL + "/r39_35.g6")
outputs.append(draw_graph(
    graphs[0],
    "R(3,9) maximal graph",
    "K35, unique official graph",
    "R39_K35_unique_graph",
    layout="spring"
))

# R(5,5), K42 known reference sample
p, graphs = download_graphs("r55_42some.g6", BASE_URL + "/r55_42some.g6")
G55 = graphs[0]
outputs.append(draw_graph(
    G55,
    "R(5,5) known reference example",
    "K42, first source graph from r55_42some.g6",
    "R55_K42_reference_source_1",
    layout="spring"
))
outputs.append(draw_graph(
    nx.complement(G55),
    "R(5,5) known reference example",
    "K42, complement of first source graph",
    "R55_K42_reference_complement_1",
    layout="spring"
))

# Make combined PDF
packet = FIG / "RAMSEY_FIGURES_PACKET.pdf"
with PdfPages(packet) as pdf:
    for out in outputs:
        if "pdf" in out and Path(out["pdf"]).exists():
            # Put image into packet by reading png for consistent page size.
            png_path = out.get("png")
            if png_path and Path(png_path).exists():
                img = plt.imread(png_path)
                fig, ax = plt.subplots(figsize=(11.69, 8.27))
                ax.imshow(img)
                ax.axis("off")
                pdf.savefig(fig, bbox_inches="tight")
                plt.close(fig)

# CSV manifest of figures
fig_csv = FIG / "FIGURE_INDEX.csv"
with fig_csv.open("w", newline="", encoding="utf-8") as f:
    fields = sorted(set(k for row in outputs for k in row.keys()))
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for row in outputs:
        w.writerow(row)

# Update README figures section
readme = REPO / "README.md"
txt = readme.read_text(encoding="utf-8", errors="replace") if readme.exists() else ""
if "## Figures" not in txt:
    with readme.open("a", encoding="utf-8") as f:
        f.write("\n\n## Figures\n\n")
        f.write("Selected public Ramsey graph figures are available in the `figures/` directory.\n\n")
        f.write("Included figures:\n\n")
        f.write("- R(3,3), K5 lower-bound witness\n")
        f.write("- R(3,4), K8 lower-bound witness\n")
        f.write("- R(3,5), K13 unique lower-bound witness\n")
        f.write("- R(3,6), K17 all 7 known graphs\n")
        f.write("- R(4,4), K17 lower-bound witness\n")
        f.write("- R(3,9), K35 unique graph\n")
        f.write("- R(5,5), K42 known reference example and complement\n")
        f.write("\nThese figures are documentation artifacts. They do not disclose the private solver implementation.\n")

# SHA256 manifest for figures
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
    print(out.get("stem"), out.get("png", ""), out.get("pdf", ""))
