"""Silkscreen artwork of the Christmas bell board -> SVG files in this folder (edakit places them, edakit.toml
[[boards.main.silk.art]]).

    uv run --project <edakit> python hardware/art/make_art.py

Everything is drawn in mm as filled shapes (strokes are buffered here), so what edakit prints is what the SVG shows.
JLCPCB prints silkscreen lines from 0.15 mm; nothing here is thinner than 0.2 mm.
"""

import math
from pathlib import Path

import numpy as np
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath
from scipy.interpolate import splev, splprep
from shapely.affinity import rotate, scale, translate
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
SCRIPT_FONT = "/usr/share/fonts/opentype/urw-base35/Z003-MediumItalic.otf"  # URW Z003, a Zapf Chancery clone
LINE = 0.25  # stroke width of lines and arcs


def smooth(points, n=200, closed=False):
    pts = np.array(points + points[:1] if closed else points, dtype=float)
    tck, _ = splprep([pts[:, 0], pts[:, 1]], s=0, per=closed, k=min(3, len(pts) - 1))
    x, y = splev(np.linspace(0, 1, n), tck)
    return list(zip(x, y))


def stroke(points, width=LINE):
    return LineString(points).buffer(width / 2, cap_style="round", join_style="round")


def arc(cx, cy, r, a0, a1, width=LINE, n=40):
    a = np.radians(np.linspace(a0, a1, n))
    return stroke(list(zip(cx + r * np.cos(a), cy + r * np.sin(a))), width)


def bell_body(w, h):
    """Bell silhouette, rim at y = 0, crown at y = h."""
    half = [(0.50, 0.00), (0.47, 0.08), (0.40, 0.20), (0.35, 0.38), (0.32, 0.58), (0.28, 0.76), (0.20, 0.90),
            (0.08, 0.985), (0.0, 1.0)]
    right = smooth([(x * w, y * h) for x, y in half], 120)
    left = [(-x, y) for x, y in reversed(right)]
    body = Polygon(right + left[1:]).buffer(0)
    lip = box(-0.54 * w, -0.06 * h, 0.54 * w, 0.06 * h).buffer(0.04 * w)
    return body.union(lip)


def holly_leaf(length, width):
    """Pointed leaf with three spikes per side, along +x, base at the origin."""
    top, bottom = [], []
    for i in range(7):
        t = i / 6
        y = width / 2 * math.sin(math.pi * t) * (1.15 if i % 2 else 0.8)
        top.append((t * length, y))
        bottom.append((t * length, -y))
    leaf = Polygon(top + list(reversed(bottom))[1:-1]).buffer(0)
    vein = stroke([(0.1 * length, 0), (0.85 * length, 0)], 0.22)
    return leaf.difference(vein)


def big_bell():
    w, h = 10.0, 11.0
    body = bell_body(w, h)
    shine = stroke(smooth([(-0.28 * w, 0.25 * h), (-0.24 * w, 0.5 * h), (-0.17 * w, 0.75 * h)], 60), 0.55)
    band = stroke(smooth([(-0.42 * w, 0.18 * h), (0, 0.13 * h), (0.42 * w, 0.18 * h)], 60), 0.3)
    body = body.difference(shine).difference(band)
    clapper = Point(0, -0.14 * h).buffer(0.11 * w)
    crown = Point(0, 1.03 * h).buffer(0.1 * w).difference(Point(0, 1.03 * h).buffer(0.05 * w))
    leaves = [translate(rotate(holly_leaf(4.2, 1.9), a, origin=(0, 0)), 0.3, 0.98 * h) for a in (25, 155, 100)]
    berries = [Point(x, 0.97 * h + y).buffer(0.55) for x, y in ((-0.5, 0.1), (0.55, 0.15), (0.0, -0.45))]
    holly = unary_union(leaves).difference(unary_union([b.buffer(0.25) for b in berries])).union(unary_union(berries))
    ring = unary_union([arc(0, 0.55 * h, r, a0, a1) for r in (6.8, 8.0, 9.2) for a0, a1 in ((-28, 28), (152, 208))])
    return unary_union([body, clapper, crown.difference(holly.buffer(0.25)), holly, ring])


def small_bell():
    w, h = 3.0, 3.2
    return unary_union([bell_body(w, h), Point(0, -0.16 * h).buffer(0.14 * w),
                        arc(0, 0.5 * h, 2.4, -30, 30, 0.22), arc(0, 0.5 * h, 2.4, 150, 210, 0.22)])


def chevron(size=1.6):
    return stroke([(-size / 3, size / 2), (size / 3, 0), (-size / 3, -size / 2)], 0.3)


def star(r=1.0, points=5, inner=0.45):
    pts = [((r if i % 2 == 0 else r * inner) * math.cos(math.pi / 2 + i * math.pi / points),
            (r if i % 2 == 0 else r * inner) * math.sin(math.pi / 2 + i * math.pi / points)) for i in range(2 * points)]
    return Polygon(pts)


def snowflake(r=1.6):
    arms = []
    for k in range(6):
        a = math.radians(60 * k)
        c, s = math.cos(a), math.sin(a)
        arms.append(stroke([(0, 0), (r * c, r * s)], 0.22))
        for t in (0.55,):
            bx, by = t * r * c, t * r * s
            for da in (40, -40):
                b = math.radians(60 * k + da)
                arms.append(stroke([(bx, by), (bx + 0.35 * r * math.cos(b), by + 0.35 * r * math.sin(b))], 0.22))
    return unary_union(arms)


def lettering(text, height):
    """Text in the script font as filled outlines, emboldened so the hairlines print."""
    path = TextPath((0, 0), text, size=10, prop=FontProperties(fname=SCRIPT_FONT))
    shape = None
    for ring in path.to_polygons():
        if len(ring) >= 3:
            p = Polygon(ring).buffer(0)
            shape = p if shape is None else shape.symmetric_difference(p)
    x0, y0, x1, y1 = shape.bounds
    f = height / (y1 - y0)
    return scale(translate(shape, -x0, -y0), f, f, origin=(0, 0)).buffer(0.09)


def write_svg(name, geom):
    x0, y0, x1, y1 = geom.bounds
    d = []
    for p in getattr(geom, "geoms", [geom]):
        if p.geom_type != "Polygon" or p.is_empty:
            continue
        for ring in (p.exterior, *p.interiors):
            c = list(ring.coords)
            d.append("M " + " L ".join(f"{x - x0:.3f},{y1 - y:.3f}" for x, y in c) + " Z")
    w, h = x1 - x0, y1 - y0
    (HERE / name).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.2f}mm" height="{h:.2f}mm" viewBox="0 0 {w:.3f} {h:.3f}">\n'
        f'  <path fill="#000" fill-rule="evenodd" d="{" ".join(d)}"/>\n</svg>\n')
    print(f"{name}: {w:.1f} x {h:.1f} mm")


if __name__ == "__main__":
    write_svg("bell.svg", big_bell())
    write_svg("small_bell.svg", small_bell())
    write_svg("greeting.svg", lettering("Frohe Weihnachten", 4.0))
    write_svg("chevron.svg", chevron())
    write_svg("star.svg", star())
    write_svg("snowflake.svg", snowflake())
