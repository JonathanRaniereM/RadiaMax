from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import (
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPolygonF,
    QRadialGradient,
)
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

# =========================================================
# RADIA MAX - TELA DE GRÁFICOS
# Salve este arquivo como: pages/graphs.py
# No main.py:
#   from pages.graphs import GraphsPage
#   "graphs": GraphsPage(),
# =========================================================

BG = "#020b16"
PANEL = "#07182b"
PANEL_2 = "#0a2038"
PANEL_3 = "#17304b"
LINE = "#1b344f"
LINE_SOFT = "#2a5374"
TEXT = "#f7fbff"
MUTED = "#aeb9ca"
CYAN = "#05e6ff"
BLUE = "#057fe8"
GREEN = "#20e377"
YELLOW = "#ffc20e"
ORANGE = "#ff9700"
RED = "#ff5d73"


def qcolor(hex_color: str, alpha: int | None = None) -> QColor:
    c = QColor(hex_color)
    if alpha is not None:
        c.setAlpha(alpha)
    return c


def rgba(hex_color: str, alpha: int) -> QColor:
    return qcolor(hex_color, alpha)


def app_font(size: int, weight: int = QFont.Normal) -> QFont:
    f = QFont("Segoe UI")
    f.setPointSize(size)
    f.setWeight(weight)
    return f


def set_font(widget: QWidget, size: int, weight: int = QFont.Normal) -> None:
    widget.setFont(app_font(size, weight))


def draw_icon(painter: QPainter, name: str, rect: QRectF, color: QColor | str, line_width: float | None = None):
    painter.save()
    c = QColor(color) if isinstance(color, str) else QColor(color)
    w, h = rect.width(), rect.height()
    lw = line_width or max(1.8, min(w, h) * 0.065)
    painter.translate(rect.left(), rect.top())
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setPen(QPen(c, lw, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
    painter.setBrush(Qt.NoBrush)

    def p(x, y):
        return QPointF(x * w, y * h)

    if name == "chart":
        painter.drawLine(p(0.16, 0.82), p(0.16, 0.18))
        painter.drawLine(p(0.16, 0.82), p(0.88, 0.82))
        painter.drawPolyline(QPolygonF([p(0.25, 0.68), p(0.42, 0.52), p(0.56, 0.60), p(0.80, 0.30)]))
        painter.drawLine(p(0.80, 0.30), p(0.80, 0.46))
        painter.drawLine(p(0.80, 0.30), p(0.64, 0.31))

    elif name == "target":
        painter.drawEllipse(QRectF(w * 0.18, h * 0.18, w * 0.64, h * 0.64))
        painter.drawEllipse(QRectF(w * 0.34, h * 0.34, w * 0.32, h * 0.32))
        painter.drawLine(p(0.50, 0.06), p(0.50, 0.25))
        painter.drawLine(p(0.50, 0.75), p(0.50, 0.94))
        painter.drawLine(p(0.06, 0.50), p(0.25, 0.50))
        painter.drawLine(p(0.75, 0.50), p(0.94, 0.50))

    elif name == "check":
        painter.drawEllipse(QRectF(w * 0.18, h * 0.18, w * 0.64, h * 0.64))
        painter.drawPolyline(QPolygonF([p(0.34, 0.52), p(0.46, 0.64), p(0.69, 0.39)]))

    elif name == "grid":
        painter.drawRoundedRect(QRectF(w * 0.14, h * 0.18, w * 0.72, h * 0.64), 2.5, 2.5)
        for y in (0.39, 0.61):
            painter.drawLine(p(0.14, y), p(0.86, y))
        for x in (0.38, 0.62):
            painter.drawLine(p(x, 0.18), p(x, 0.82))

    elif name == "layers":
        painter.drawRoundedRect(QRectF(w * 0.18, h * 0.18, w * 0.64, h * 0.18), 4, 4)
        painter.drawRoundedRect(QRectF(w * 0.25, h * 0.41, w * 0.64, h * 0.18), 4, 4)
        painter.drawRoundedRect(QRectF(w * 0.12, h * 0.64, w * 0.64, h * 0.18), 4, 4)

    elif name == "download":
        painter.drawLine(p(0.50, 0.15), p(0.50, 0.62))
        painter.drawLine(p(0.32, 0.46), p(0.50, 0.64))
        painter.drawLine(p(0.68, 0.46), p(0.50, 0.64))
        painter.drawRoundedRect(QRectF(w * 0.20, h * 0.70, w * 0.60, h * 0.16), 3, 3)

    painter.restore()


class GlassPanel(QFrame):
    def __init__(
        self,
        radius: int = 16,
        fill: str = PANEL,
        fill_alpha: int = 120,
        border: str = LINE_SOFT,
        border_alpha: int = 150,
        parent=None,
    ):
        super().__init__(parent)
        self.radius = radius
        self.fill = fill
        self.fill_alpha = fill_alpha
        self.border = border
        self.border_alpha = border_alpha
        self.setAttribute(Qt.WA_StyledBackground, False)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(self.rect().adjusted(1, 1, -1, -1))
        path = QPainterPath()
        path.addRoundedRect(rect, self.radius, self.radius)

        base = QColor(self.fill)
        grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
        grad.setColorAt(0.00, QColor(base.red(), base.green(), base.blue(), min(255, self.fill_alpha + 20)))
        grad.setColorAt(0.55, QColor(base.red(), base.green(), base.blue(), self.fill_alpha))
        grad.setColorAt(1.00, QColor(base.red(), base.green(), base.blue(), max(55, self.fill_alpha - 32)))
        painter.fillPath(path, grad)

        top_glow = QLinearGradient(rect.left(), rect.top(), rect.right(), rect.top())
        top_glow.setColorAt(0, QColor(255, 255, 255, 0))
        top_glow.setColorAt(0.5, rgba("#b8eaff", 35))
        top_glow.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setPen(QPen(top_glow, 1))
        painter.drawLine(QPointF(rect.left() + 18, rect.top() + 1), QPointF(rect.right() - 18, rect.top() + 1))

        painter.setPen(QPen(rgba(self.border, self.border_alpha), 1.0))
        painter.drawPath(path)

        super().paintEvent(event)


class StyledButton(QPushButton):
    def __init__(self, text: str, primary: bool = False, height: int = 40):
        super().__init__(text)
        self.setFixedHeight(height)
        self.setCursor(Qt.PointingHandCursor)

        if primary:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: #14c9e8;
                    color: white;
                    border: none;
                    border-radius: 13px;
                    padding: 0 16px;
                    font: 800 10px "Segoe UI";
                }}
                QPushButton:hover {{ background: #25def7; }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: rgba(8, 28, 49, 0.55);
                    color: {TEXT};
                    border: 1px solid #2a5677;
                    border-radius: 13px;
                    padding: 0 16px;
                    font: 800 10px "Segoe UI";
                }}
                QPushButton:hover {{
                    color: {CYAN};
                    border-color: {CYAN};
                    background: rgba(9, 38, 64, 0.72);
                }}
            """)


class TopChip(QPushButton):
    def __init__(self, text: str, color: str, selected: bool = False):
        super().__init__(text)
        self.color = color
        self.setCheckable(True)
        self.setChecked(selected)
        self.setFixedHeight(34)
        self.setMinimumWidth(138)
        self.setCursor(Qt.PointingHandCursor)
        self.toggled.connect(self._sync)
        self._sync()

    def _sync(self):
        if self.isChecked():
            self.setStyleSheet(f"""
                QPushButton {{
                    background: rgba({QColor(self.color).red()}, {QColor(self.color).green()}, {QColor(self.color).blue()}, 0.15);
                    color: {self.color};
                    border: 1px solid {self.color};
                    border-radius: 15px;
                    padding: 0 16px;
                    font: 800 10px "Segoe UI";
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: rgba(8, 28, 49, 0.68);
                    color: {MUTED};
                    border: 1px solid #2a5677;
                    border-radius: 15px;
                    padding: 0 16px;
                    font: 800 10px "Segoe UI";
                }}
                QPushButton:hover {{
                    color: {self.color};
                    border-color: {self.color};
                }}
            """)


class SectionHeader(QWidget):
    def __init__(self, title: str, subtitle: str = "", accent: str | None = None):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        t = QLabel(title)
        t.setStyleSheet(f"color: {accent or TEXT};")
        set_font(t, 18, QFont.Black)
        layout.addWidget(t)

        if subtitle:
            s = QLabel(subtitle)
            s.setWordWrap(True)
            s.setStyleSheet(f"color: {MUTED};")
            set_font(s, 10)
            layout.addWidget(s)


class LegendItem(QWidget):
    def __init__(self, color: str, label: str, dashed: bool = True, filled: bool = False, marker: bool = False):
        super().__init__()
        self.color = color
        self.label = label
        self.dashed = dashed
        self.filled = filled
        self.marker = marker
        self.setFixedHeight(31)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        y = self.height() / 2

        if self.filled:
            painter.setBrush(rgba(BLUE, 96))
            painter.setPen(QPen(QColor(BLUE), 1.2))
            painter.drawRoundedRect(QRectF(0, y - 6, 34, 12), 4, 4)
        elif self.marker:
            painter.setBrush(QColor(TEXT))
            painter.setPen(QPen(QColor(self.color), 2.3))
            painter.drawEllipse(QPointF(17, y), 6, 6)
        else:
            pen = QPen(QColor(self.color), 2.2)
            if self.dashed:
                pen.setDashPattern([6, 5])
            painter.setPen(pen)
            painter.drawLine(QPointF(0, y), QPointF(34, y))

        painter.setPen(QColor(MUTED))
        painter.setFont(app_font(10))
        painter.drawText(QRectF(50, 0, self.width() - 50, self.height()), Qt.AlignVCenter | Qt.AlignLeft, self.label)


class IconBox(QWidget):
    def __init__(self, icon: str, color: str, size: int = 58, radius: int = 13):
        super().__init__()
        self.icon = icon
        self.color = QColor(color)
        self.radius = radius
        self.setFixedSize(size, size)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(self.rect().adjusted(1, 1, -1, -1))
        path = QPainterPath()
        path.addRoundedRect(rect, self.radius, self.radius)

        grad = QRadialGradient(rect.center(), rect.width() * 0.92)
        c = QColor(self.color)
        c.setAlpha(80)
        grad.setColorAt(0, c)
        c2 = QColor(self.color)
        c2.setAlpha(22)
        grad.setColorAt(1, c2)
        painter.fillPath(path, grad)

        painter.setPen(QPen(self.color, 1.25))
        painter.drawPath(path)

        draw_icon(painter, self.icon, rect.adjusted(13, 13, -13, -13), self.color, 2.2)


class GraphCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(410)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(self.rect().adjusted(2, 2, -2, -2))

        bg = QLinearGradient(rect.topLeft(), rect.bottomRight())
        bg.setColorAt(0, QColor(6, 20, 38, 218))
        bg.setColorAt(1, QColor(2, 9, 20, 235))
        painter.fillRect(rect, bg)

        left = rect.left() + 56
        top = rect.top() + 32
        right = rect.right() - 28
        bottom = rect.bottom() - 36
        plot_w = right - left
        plot_h = bottom - top

        def m(x: float, y: float) -> QPointF:
            return QPointF(left + (x / 11) * plot_w, bottom - (y / 12) * plot_h)

        # grid mais próximo da referência
        painter.setPen(QPen(rgba("#ffffff", 23), 1))
        for i in range(12):
            x = left + i * plot_w / 11
            painter.drawLine(QPointF(x, top), QPointF(x, bottom))
        for i in range(7):
            y = bottom - i * plot_h / 6
            painter.drawLine(QPointF(left, y), QPointF(right, y))

        # região viável sombreada
        region_points = [m(0, 0), m(0, 6), m(4, 4), m(8.0, 0)]
        region = QPainterPath(region_points[0])
        for pt in region_points[1:]:
            region.lineTo(pt)
        region.closeSubpath()

        painter.fillPath(region, rgba(CYAN, 44))
        painter.fillPath(region, rgba(BLUE, 74))
        painter.setPen(QPen(QColor(CYAN), 2.3))
        painter.drawPath(region)

        # restrição 1: x1 + 2x2 <= 12
        p1 = QPen(QColor(CYAN), 2.4)
        p1.setDashPattern([8, 6])
        painter.setPen(p1)
        painter.drawLine(m(0, 6), m(11, 0.5))

        # restrição 2: 2x1 + x2 <= 18
        p2 = QPen(QColor(GREEN), 2.4)
        p2.setDashPattern([8, 6])
        painter.setPen(p2)
        painter.drawLine(m(3.2, 11.6), m(9, 0))

        # curvas de nível / objetivo
        pz = QPen(QColor(YELLOW), 2.25)
        pz.setDashPattern([5, 5])
        painter.setPen(pz)
        painter.drawLine(m(1.0, 3.4), m(7.5, 8.6))
        painter.drawLine(m(1.7, 3.8), m(8.1, 9.4))
        painter.drawLine(m(2.3, 4.2), m(8.7, 10.0))

        # eixos acima da região
        painter.setPen(QPen(QColor("#dbe7f4"), 1.8))
        painter.drawLine(QPointF(left, bottom), QPointF(right, bottom))
        painter.drawLine(QPointF(left, bottom), QPointF(left, top))

        # setas dos eixos
        painter.drawLine(QPointF(right, bottom), QPointF(right - 10, bottom - 6))
        painter.drawLine(QPointF(right, bottom), QPointF(right - 10, bottom + 6))
        painter.drawLine(QPointF(left, top), QPointF(left - 6, top + 10))
        painter.drawLine(QPointF(left, top), QPointF(left + 6, top + 10))

        # ponto ótimo
        optimal = m(4, 4)
        painter.setBrush(QColor(TEXT))
        painter.setPen(QPen(QColor(CYAN), 4))
        painter.drawEllipse(optimal, 9, 9)

        painter.setBrush(rgba(YELLOW, 55))
        painter.setPen(QPen(QColor(YELLOW), 1.5))
        painter.drawEllipse(optimal, 18, 18)

        # tooltip do ponto ótimo
        tip = QRectF(optimal.x() + 58, optimal.y() - 72, 148, 54)
        tip_path = QPainterPath()
        tip_path.addRoundedRect(tip, 9, 9)
        painter.fillPath(tip_path, rgba("#08253f", 236))
        painter.setPen(QPen(QColor(CYAN), 1.2))
        painter.drawPath(tip_path)
        painter.setPen(QColor(TEXT))
        painter.setFont(app_font(9, QFont.Bold))
        painter.drawText(tip.adjusted(12, 7, -8, -7), Qt.AlignLeft | Qt.AlignVCenter, "Ponto ótimo (4, 4)\nZ = 32")

        # rótulos das linhas
        painter.setFont(app_font(8, QFont.Bold))
        painter.setPen(QColor(CYAN))
        painter.drawText(QPointF(m(7.7, 8.6).x(), m(7.7, 8.6).y()), "x₁ + 2x₂ ≤ 12")
        painter.setPen(QColor(GREEN))
        painter.drawText(QPointF(m(6.7, 3.2).x(), m(6.7, 3.2).y()), "2x₁ + x₂ ≤ 18")
        painter.setPen(QColor(YELLOW))
        painter.drawText(QPointF(m(8.0, 9.5).x(), m(8.0, 9.5).y()), "Z = 3x₁ + 5x₂")

        # rótulos numéricos
        painter.setPen(QColor("#dbe3ef"))
        painter.setFont(app_font(9))
        for y in (0, 2, 4, 6, 8, 10):
            painter.drawText(QRectF(left - 34, m(0, y).y() - 8, 24, 16), Qt.AlignRight | Qt.AlignVCenter, str(y))
        for x in (0, 2, 4, 6, 8, 10):
            painter.drawText(QRectF(m(x, 0).x() - 10, bottom + 10, 24, 18), Qt.AlignCenter, str(x))

        painter.setFont(app_font(10, QFont.Bold))
        painter.drawText(QPointF(left - 34, top + 6), "x₂")
        painter.drawText(QPointF(right + 8, bottom + 8), "x₁")


class CartesianPanel(GlassPanel):
    def __init__(self):
        super().__init__(radius=18, fill=PANEL_3, fill_alpha=212, border="#285474", border_alpha=178)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(22)

        left = QVBoxLayout()
        left.setSpacing(13)

        title = QLabel("Plano cartesiano")
        title.setStyleSheet(f"color: {CYAN};")
        set_font(title, 19, QFont.Black)

        sub = QLabel("Análise gráfica habilitada apenas para problemas com duas variáveis.")
        sub.setWordWrap(True)
        sub.setStyleSheet(f"color: {MUTED};")
        set_font(sub, 10)

        legend_title = QLabel("Legenda")
        legend_title.setStyleSheet(f"color: {TEXT};")
        set_font(legend_title, 12, QFont.Bold)

        left.addWidget(title)
        left.addWidget(sub)
        left.addSpacing(8)
        left.addWidget(legend_title)
        left.addWidget(LegendItem(CYAN, "Restrição 1"))
        left.addWidget(LegendItem(GREEN, "Restrição 2"))
        left.addWidget(LegendItem(YELLOW, "Curvas de nível"))
        left.addWidget(LegendItem(BLUE, "Região viável", dashed=False, filled=True))
        left.addWidget(LegendItem(CYAN, "Solução ótima", dashed=False, marker=True))
        left.addStretch(1)

        layout.addLayout(left, 0)
        graph_box = GlassPanel(radius=13, fill="#081d33", fill_alpha=172, border="#27506f", border_alpha=145)
        graph_layout = QVBoxLayout(graph_box)
        graph_layout.setContentsMargins(10, 10, 10, 10)
        graph_layout.addWidget(GraphCanvas())
        layout.addWidget(graph_box, 1)


class SummaryGraphicPanel(GlassPanel):
    def __init__(self):
        super().__init__(radius=18, fill=PANEL_3, fill_alpha=218, border="#2b5677", border_alpha=175)
        self.setMinimumHeight(220)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        title = QLabel("Resumo gráfico")
        title.setStyleSheet(f"color: {CYAN};")
        set_font(title, 18, QFont.Black)
        layout.addWidget(title)

        grid = QHBoxLayout()
        grid.setSpacing(18)

        left_col = QVBoxLayout()
        left_col.setSpacing(14)
        left_col.addWidget(SummaryMetric("2", "Variáveis\nx₁ e x₂", CYAN))
        left_col.addWidget(SummaryMetric("✓", "Região viável\nSombreada", GREEN, icon_like=True))

        right_col = QVBoxLayout()
        right_col.setSpacing(14)
        right_col.addWidget(SummaryMetric("2", "Restrições\nRetas", CYAN))
        right_col.addWidget(SummaryMetric("↗", "Curvas de nível\nObjetivo", YELLOW, icon_like=True))

        grid.addLayout(left_col, 1)
        grid.addLayout(right_col, 1)
        layout.addLayout(grid, 1)


class SummaryMetric(QWidget):
    def __init__(self, value: str, label: str, color: str, icon_like: bool = False):
        super().__init__()
        self.value = value
        self.label = label
        self.color = QColor(color)
        self.icon_like = icon_like
        self.setMinimumHeight(70)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        box = QRectF(0, 5, 62, 62)
        path = QPainterPath()
        path.addRoundedRect(box, 12, 12)
        painter.fillPath(path, rgba(self.color.name(), 28))
        painter.setPen(QPen(self.color, 1.1))
        painter.drawPath(path)

        painter.setPen(self.color)
        painter.setFont(app_font(25 if self.icon_like else 20, QFont.Black))
        painter.drawText(box, Qt.AlignCenter, self.value)

        painter.setPen(QColor(MUTED))
        painter.setFont(app_font(10))
        lines = self.label.split("\n")
        painter.drawText(QRectF(82, 12, self.width() - 84, 22), Qt.AlignLeft | Qt.AlignVCenter, lines[0])
        painter.setPen(QColor(TEXT))
        painter.setFont(app_font(12, QFont.Normal))
        painter.drawText(QRectF(82, 38, self.width() - 84, 22), Qt.AlignLeft | Qt.AlignVCenter, lines[1])


class OptimalSolutionPanel(GlassPanel):
    def __init__(self):
        super().__init__(radius=18, fill="#102338", fill_alpha=218, border=GREEN, border_alpha=205)
        self.setMinimumHeight(260)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(26)

        icon = BigCheck()
        layout.addWidget(icon, 0, Qt.AlignCenter)

        col = QVBoxLayout()
        col.setSpacing(8)

        title = QLabel("Solução ótima")
        title.setStyleSheet(f"color: {GREEN};")
        set_font(title, 18, QFont.Black)

        subtitle = QLabel("Coordenadas")
        subtitle.setStyleSheet(f"color: {MUTED};")
        set_font(subtitle, 11)

        x1 = QLabel("x₁ = 4")
        x2 = QLabel("x₂ = 4")
        for lbl in (x1, x2):
            lbl.setStyleSheet(f"color: {TEXT};")
            set_font(lbl, 17, QFont.Bold)

        line = QFrame()
        line.setFixedHeight(1)
        line.setStyleSheet("background: rgba(130, 160, 190, 0.24);")

        z = QLabel("Z = 32")
        z.setStyleSheet(f"color: {TEXT};")
        set_font(z, 24, QFont.Black)

        col.addWidget(title)
        col.addSpacing(10)
        col.addWidget(subtitle)
        col.addWidget(x1)
        col.addWidget(x2)
        col.addWidget(line)
        col.addWidget(z)
        col.addStretch(1)

        layout.addLayout(col, 1)


class BigCheck(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(118, 118)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(self.rect().adjusted(4, 4, -4, -4))
        painter.setBrush(rgba(GREEN, 30))
        painter.setPen(QPen(QColor(GREEN), 2.4))
        painter.drawEllipse(rect)

        painter.setPen(QPen(QColor(GREEN), 8, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawPolyline(QPolygonF([
            QPointF(rect.left() + rect.width() * 0.30, rect.top() + rect.height() * 0.54),
            QPointF(rect.left() + rect.width() * 0.45, rect.top() + rect.height() * 0.68),
            QPointF(rect.left() + rect.width() * 0.73, rect.top() + rect.height() * 0.36),
        ]))


class ResultCard(GlassPanel):
    def __init__(self, icon: str, title: str, value: str, subtitle: str, color: str):
        super().__init__(radius=15, fill="#0d2237", fill_alpha=218, border="#235171", border_alpha=145)
        self.setMinimumHeight(98)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(13)

        layout.addWidget(IconBox(icon, color, 50))

        col = QVBoxLayout()
        col.setSpacing(2)

        t = QLabel(title)
        t.setStyleSheet(f"color: {MUTED};")
        set_font(t, 10, QFont.Bold)

        v = QLabel(value)
        v.setStyleSheet(f"color: {TEXT};")
        set_font(v, 17, QFont.Black)

        s = QLabel(subtitle)
        s.setStyleSheet(f"color: {MUTED};")
        set_font(s, 9)

        col.addWidget(t)
        col.addWidget(v)
        col.addWidget(s)
        layout.addLayout(col, 1)


class FooterNote(GlassPanel):
    def __init__(self):
        super().__init__(radius=12, fill="#0d2237", fill_alpha=168, border="#27506f", border_alpha=145)
        self.setFixedHeight(54)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)

        txt = QLabel("Eixos x₁ e x₂ • Restrições como retas • Região viável sombreada • Curvas de nível • Ponto ótimo destacado")
        txt.setStyleSheet(f"color: {MUTED};")
        set_font(txt, 12)
        layout.addWidget(txt)


class GraphsPage(QWidget):
    request_navigate = Signal(str)

    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(22, 14, 22, 18)
        root.setSpacing(14)

        top = QHBoxLayout()
        top.setSpacing(14)

        title_col = QVBoxLayout()
        title_col.setSpacing(6)

        title = QLabel("Tela gráfica")
        title.setStyleSheet(f"color: {TEXT};")
        set_font(title, 30, QFont.Black)

        subtitle = QLabel("Região viável, curvas de nível e solução ótima para problemas com duas variáveis")
        subtitle.setStyleSheet(f"color: {MUTED};")
        set_font(subtitle, 13)

        underline = QFrame()
        underline.setFixedSize(70, 4)
        underline.setStyleSheet(f"background: {CYAN}; border-radius: 2px;")

        title_col.addWidget(title)
        title_col.addWidget(subtitle)
        title_col.addWidget(underline, 0, Qt.AlignLeft)

        top.addLayout(title_col, 1)
        top.addWidget(TopChip("Região viável", CYAN, True), 0, Qt.AlignTop)
        top.addWidget(TopChip("Curvas de nível", YELLOW, True), 0, Qt.AlignTop)
        top.addWidget(TopChip("Ponto ótimo", GREEN, True), 0, Qt.AlignTop)
        root.addLayout(top)

        body = QHBoxLayout()
        body.setSpacing(18)

        left = QVBoxLayout()
        left.setSpacing(14)
        left.addWidget(CartesianPanel(), 1)

        result_cards = QHBoxLayout()
        result_cards.setSpacing(14)
        result_cards.addWidget(ResultCard("target", "Solução ótima", "Z = 32", "Ponto ótimo = (4, 4)", CYAN))
        result_cards.addWidget(ResultCard("chart", "Plano", "2D", "Análise para x₁ e x₂", GREEN))
        result_cards.addWidget(ResultCard("check", "Viabilidade", "OK", "Região viável sombreada", YELLOW))
        result_cards.addWidget(ResultCard("download", "Exportação", "PNG/PDF", "Pronto para relatório", BLUE))
        left.addLayout(result_cards)

        body.addLayout(left, 1)

        right_host = QWidget()
        right_host.setMinimumWidth(390)
        right_host.setMaximumWidth(430)
        right = QVBoxLayout(right_host)
        right.setContentsMargins(0, 0, 0, 0)
        right.setSpacing(18)

        # Dois cards grandes, como na referência.
        # Isso elimina a sobreposição que existia com 3 cards espremidos na coluna.
        right.addWidget(SummaryGraphicPanel(), 0)
        right.addWidget(OptimalSolutionPanel(), 1)

        body.addWidget(right_host)
        root.addLayout(body, 1)

        root.addWidget(FooterNote())
