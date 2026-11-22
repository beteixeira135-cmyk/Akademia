"""Render the first three TCC flowcharts as readable PNG and SVG assets."""
from html import escape
from pathlib import Path
from math import atan2, cos, sin, pi

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
GREEN = "#1F4D3D"
GOLD = "#B88932"
INK = "#26332D"
PALE = "#F2F6F3"
PALE_GOLD = "#FBF6E9"
WHITE = "#FFFFFF"


def font(size, bold=False):
    candidates = [
        Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"),
        Path(r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf"),
    ]
    for path in candidates:
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


class Diagram:
    def __init__(self, filename, width, height):
        self.filename = filename
        self.width = width
        self.height = height
        self.nodes = []
        self.edges = []

    def node(self, key, label, x, y, w, h, fill=PALE, shape="box"):
        item = dict(key=key, label=label, x=x, y=y, w=w, h=h, fill=fill, shape=shape)
        self.nodes.append(item)
        return item

    def edge(self, points, label=None, label_at=None, dashed=False):
        self.edges.append(dict(points=points, label=label, label_at=label_at, dashed=dashed))

    def _line(self, draw, points, dashed=False):
        for start, end in zip(points, points[1:]):
            x1, y1 = start
            x2, y2 = end
            if not dashed:
                draw.line((x1, y1, x2, y2), fill=GREEN, width=7)
                continue
            length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            if not length:
                continue
            ux, uy = (x2 - x1) / length, (y2 - y1) / length
            offset = 0
            while offset < length:
                stop = min(offset + 20, length)
                draw.line(
                    (x1 + ux * offset, y1 + uy * offset, x1 + ux * stop, y1 + uy * stop),
                    fill=GOLD,
                    width=6,
                )
                offset += 34
        x1, y1 = points[-2]
        x2, y2 = points[-1]
        angle = atan2(y2 - y1, x2 - x1)
        length = 25
        wing = 13
        base = (x2 - length * cos(angle), y2 - length * sin(angle))
        draw.polygon(
            [
                (x2, y2),
                (base[0] + wing * cos(angle + pi / 2), base[1] + wing * sin(angle + pi / 2)),
                (base[0] + wing * cos(angle - pi / 2), base[1] + wing * sin(angle - pi / 2)),
            ],
            fill=GOLD if dashed else GREEN,
        )

    def _text(self, draw, label, x, y, font_obj, fill=INK):
        draw.multiline_text(
            (x, y),
            label,
            font=font_obj,
            fill=fill,
            anchor="mm",
            align="center",
            spacing=9,
        )

    def render_png(self):
        image = Image.new("RGB", (self.width, self.height), WHITE)
        draw = ImageDraw.Draw(image)
        regular = font(42)
        bold = font(42, True)
        edge_font = font(30, True)

        for edge in self.edges:
            self._line(draw, edge["points"], edge["dashed"])
            if edge["label"]:
                x, y = edge["label_at"]
                draw.rounded_rectangle((x - 55, y - 25, x + 55, y + 25), radius=16, fill=WHITE)
                self._text(draw, edge["label"], x, y, edge_font, GREEN)

        for item in self.nodes:
            x, y, w, h = item["x"], item["y"], item["w"], item["h"]
            if item["shape"] == "diamond":
                draw.polygon(
                    [(x + w / 2, y), (x + w, y + h / 2), (x + w / 2, y + h), (x, y + h / 2)],
                    fill=item["fill"],
                    outline=GREEN,
                    width=6,
                )
            else:
                draw.rounded_rectangle(
                    (x, y, x + w, y + h),
                    radius=28,
                    fill=item["fill"],
                    outline=GREEN,
                    width=6,
                )
            numbered = item["label"].splitlines()[0].split(".", 1)[0].isdigit()
            self._text(draw, item["label"], x + w / 2, y + h / 2, bold if numbered else regular)

        image.save(ROOT / f"{self.filename}.png", dpi=(300, 300), optimize=True)
        self.render_svg()

    def render_svg(self):
        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">',
            f'<rect width="100%" height="100%" fill="{WHITE}"/>',
            f'<defs><marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L12,6 L0,12 z" fill="{GREEN}"/></marker>',
            f'<marker id="arrow-dashed" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L12,6 L0,12 z" fill="{GOLD}"/></marker></defs>',
        ]
        for edge in self.edges:
            points = " ".join(f"{x},{y}" for x, y in edge["points"])
            dash = ' stroke-dasharray="14 12"' if edge["dashed"] else ""
            marker = "arrow-dashed" if edge["dashed"] else "arrow"
            parts.append(
                f'<polyline points="{points}" fill="none" stroke="{GOLD if edge["dashed"] else GREEN}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#{marker})"{dash}/>'
            )
            if edge["label"]:
                x, y = edge["label_at"]
                parts.append(f'<rect x="{x - 55}" y="{y - 25}" width="110" height="50" rx="14" fill="{WHITE}"/>')
                parts.append(f'<text x="{x}" y="{y + 10}" text-anchor="middle" font-family="Arial,sans-serif" font-size="30" font-weight="bold" fill="{GREEN}">{escape(edge["label"])}</text>')
        for item in self.nodes:
            x, y, w, h = item["x"], item["y"], item["w"], item["h"]
            if item["shape"] == "diamond":
                points = f"{x + w / 2},{y} {x + w},{y + h / 2} {x + w / 2},{y + h} {x},{y + h / 2}"
                parts.append(f'<polygon points="{points}" fill="{item["fill"]}" stroke="{GREEN}" stroke-width="6"/>')
            else:
                parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" fill="{item["fill"]}" stroke="{GREEN}" stroke-width="6"/>')
            lines = item["label"].splitlines()
            center_y = y + h / 2
            line_height = 54
            start_y = center_y - (len(lines) - 1) * line_height / 2 + 14
            weight = "bold" if lines[0].split(".", 1)[0].isdigit() else "normal"
            for index, line in enumerate(lines):
                parts.append(
                    f'<text x="{x + w / 2}" y="{start_y + index * line_height}" text-anchor="middle" font-family="Arial,sans-serif" font-size="42" font-weight="{weight}" fill="{INK}">{escape(line)}</text>'
                )
        parts.append("</svg>")
        (ROOT / f"{self.filename}.svg").write_text("\n".join(parts), encoding="utf-8")


def center_top(node):
    return (node["x"] + node["w"] / 2, node["y"])


def center_bottom(node):
    return (node["x"] + node["w"] / 2, node["y"] + node["h"])


def center_left(node):
    return (node["x"], node["y"] + node["h"] / 2)


def center_right(node):
    return (node["x"] + node["w"], node["y"] + node["h"] / 2)


def architecture():
    d = Diagram("01-arquitetura-geral", 1800, 1840)
    labels = [
        "1. Objetivo\nAvaliar perdas por desfolha",
        "2. Entradas secundárias\nClima, solo e materiais",
        "3. Modelagem mensal\n3-PG-PJS",
        "4. Danos à copa\nDesfolha e outros fatores",
        "5. Cenários\nIntensidade, época e frequência",
        "6. Calibração\nBertulio et al. (2008)",
        "7. Simulações\nVersões original e calibrada",
        "8. Metamodelo\nRandom Forest",
        "9. Indicadores\nFolhagem, crescimento e madeira",
        "10. Interpretação\nAlcance e limites",
    ]
    nodes = []
    for index, label in enumerate(labels):
        row, side = divmod(index, 2)
        left_to_right = row % 2 == 0
        column = side if left_to_right else 1 - side
        nodes.append(d.node(f"N{index + 1}", label, 120 + column * 820, 100 + row * 350, 740, 210, PALE if index % 2 == 0 else PALE_GOLD))
    for row in range(5):
        first, second = nodes[row * 2], nodes[row * 2 + 1]
        if row % 2 == 0:
            d.edge([center_right(first), center_left(second)])
        else:
            d.edge([center_left(first), center_right(second)])
        if row < 4:
            d.edge([center_bottom(second), center_top(nodes[(row + 1) * 2])])
    d.render_png()


def monthly_cycle():
    d = Diagram("02-ciclo-mensal", 1800, 1930)
    w, h, left, right, center = 700, 140, 80, 1020, 550
    climate = d.node("climate", "Clima, solo e\nágua disponível", left, 80, w, h)
    canopy = d.node("canopy", "Copa e área foliar", right, 80, w, h)
    light = d.node("light", "Luz captada pela copa", center, 300, w, h)
    growth = d.node("growth", "Crescimento\n3-PG-PJS", center, 510, w, h, PALE_GOLD)
    decision = d.node("decision", "Ataque\nno mês?", center + 140, 720, 420, 160, PALE_GOLD, "diamond")
    usual = d.node("usual", "Alocação usual", left, 990, w, h)
    removal = d.node("removal", "Retirada foliar", right, 990, w, h, PALE_GOLD)
    compensation = d.node("compensation", "Compensação calibrada", right, 1190, w, h, PALE_GOLD)
    update = d.node("update", "Estoques e IAF atualizados", center, 1390, w, h)
    output = d.node("output", "Folhagem, crescimento e volume", center, 1590, w, h)
    next_month = d.node("next", "Próximo mês", center, 1770, w, 120)
    d.edge([center_bottom(climate), (center_bottom(climate)[0], 255), (center_top(light)[0] - 100, 255), center_top(light)])
    d.edge([center_bottom(canopy), (center_bottom(canopy)[0], 255), (center_top(light)[0] + 100, 255), center_top(light)])
    d.edge([center_bottom(light), center_top(growth)])
    d.edge([center_bottom(growth), center_top(decision)])
    d.edge([center_left(decision), (center_left(decision)[0] - 120, 940), center_top(usual)], "Não", (center_left(decision)[0] - 180, 930))
    d.edge([center_right(decision), (center_right(decision)[0] + 120, 940), center_top(removal)], "Sim", (center_right(decision)[0] + 180, 930))
    d.edge([center_bottom(removal), center_top(compensation)])
    d.edge([center_bottom(usual), (center_bottom(usual)[0], 1350), (center_top(update)[0] - 100, 1350), center_top(update)])
    d.edge([center_bottom(compensation), (center_bottom(compensation)[0], 1350), (center_top(update)[0] + 100, 1350), center_top(update)])
    d.edge([center_bottom(update), center_top(output)])
    d.edge([center_bottom(output), center_top(next_month)])
    d.edge([center_left(next_month), (35, center_left(next_month)[1]), (35, 150), (left, 150)], dashed=True)
    d.render_png()


def scenario_matrix():
    d = Diagram("03-cenarios", 1800, 1700)
    matrix = d.node("matrix", "Matriz de condições", 550, 70, 700, 140)
    intensity = d.node("intensity", "Intensidade\ndo ataque", 60, 300, 500, 150)
    season = d.node("season", "Época\ndo ataque", 650, 300, 500, 150)
    frequency = d.node("frequency", "Frequência\ndos ataques", 1240, 300, 500, 150)
    combine = d.node("combine", "Combinar os fatores", 550, 560, 700, 150, PALE_GOLD)
    isolated = d.node("isolated", "Ataque isolado", 60, 820, 500, 150)
    twice = d.node("twice", "Dois ataques", 650, 820, 500, 150)
    annual = d.node("annual", "Ataques anuais", 1240, 820, 500, 150)
    simulation = d.node("simulation", "Executar cada cenário", 550, 1080, 700, 150, PALE_GOLD)
    original = d.node("original", "Versão original", 240, 1330, 550, 150)
    calibrated = d.node("calibrated", "Versão calibrada", 1010, 1330, 550, 150, PALE_GOLD)
    result = d.node("result", "Comparar com o controle pareado", 550, 1550, 700, 120)
    d.edge([center_bottom(matrix), (center_bottom(matrix)[0], 255), (center_top(intensity)[0], 255), center_top(intensity)])
    d.edge([center_bottom(matrix), center_top(season)])
    d.edge([center_bottom(matrix), (center_bottom(matrix)[0], 255), (center_top(frequency)[0], 255), center_top(frequency)])
    for node in (intensity, season, frequency):
        d.edge([center_bottom(node), (center_top(combine)[0], 500), center_top(combine)])
    d.edge([center_bottom(combine), (center_bottom(combine)[0], 770), center_top(isolated)])
    d.edge([center_bottom(combine), center_top(twice)])
    d.edge([center_bottom(combine), (center_bottom(combine)[0], 770), center_top(annual)])
    for node in (isolated, twice, annual):
        d.edge([center_bottom(node), (center_top(simulation)[0], 1040), center_top(simulation)])
    d.edge([center_bottom(simulation), (center_bottom(simulation)[0], 1300), center_top(original)])
    d.edge([center_bottom(simulation), (center_bottom(simulation)[0], 1300), center_top(calibrated)])
    d.edge([center_bottom(original), (center_bottom(original)[0], 1520), (center_top(result)[0] - 100, 1520), center_top(result)])
    d.edge([center_bottom(calibrated), (center_bottom(calibrated)[0], 1520), (center_top(result)[0] + 100, 1520), center_top(result)])
    d.render_png()


if __name__ == "__main__":
    architecture()
    monthly_cycle()
    scenario_matrix()
