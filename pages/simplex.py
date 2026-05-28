from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QFont, QLinearGradient, QPainter, QPainterPath, QPen, QRadialGradient, QPolygonF
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

# =========================================================
# RADIA MAX - SIMPLEX TABULAR
# Salve este arquivo como: pages/simplex.py
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


def css_rgba(hex_color: str, alpha: int) -> str:
    c = QColor(hex_color)
    return f"rgba({c.red()}, {c.green()}, {c.blue()}, {alpha / 255:.3f})"


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
    lw = line_width or max(1.7, min(w, h) * 0.07)
    painter.translate(rect.left(), rect.top())
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setPen(QPen(c, lw, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
    painter.setBrush(Qt.NoBrush)

    def p(x, y):
        return QPointF(x * w, y * h)

    if name == "refresh":
        painter.drawArc(QRectF(w * 0.18, h * 0.18, w * 0.64, h * 0.64), 45 * 16, 265 * 16)
        painter.drawLine(p(0.76, 0.22), p(0.76, 0.42))
        painter.drawLine(p(0.76, 0.22), p(0.57, 0.23))
    elif name == "pivot":
        painter.drawEllipse(QRectF(w * 0.18, h * 0.18, w * 0.64, h * 0.64))
        painter.drawEllipse(QRectF(w * 0.38, h * 0.38, w * 0.24, h * 0.24))
    elif name == "check":
        painter.drawEllipse(QRectF(w * 0.16, h * 0.16, w * 0.68, h * 0.68))
        painter.drawPolyline(QPolygonF([p(0.32, 0.53), p(0.46, 0.66), p(0.72, 0.36)]))
    elif name == "clock":
        painter.drawEllipse(QRectF(w * 0.18, h * 0.18, w * 0.64, h * 0.64))
        painter.drawLine(p(0.50, 0.31), p(0.50, 0.53))
        painter.drawLine(p(0.50, 0.53), p(0.65, 0.62))
    elif name == "target":
        painter.drawEllipse(QRectF(w * 0.18, h * 0.18, w * 0.64, h * 0.64))
        painter.drawEllipse(QRectF(w * 0.36, h * 0.36, w * 0.28, h * 0.28))
        painter.drawLine(p(0.50, 0.06), p(0.50, 0.24))
        painter.drawLine(p(0.50, 0.76), p(0.50, 0.94))
        painter.drawLine(p(0.06, 0.50), p(0.24, 0.50))
        painter.drawLine(p(0.76, 0.50), p(0.94, 0.50))
    elif name == "table":
        painter.drawRoundedRect(QRectF(w * 0.14, h * 0.18, w * 0.72, h * 0.64), 2.5, 2.5)
        for y in (0.39, 0.61):
            painter.drawLine(p(0.14, y), p(0.86, y))
        for x in (0.38, 0.62):
            painter.drawLine(p(x, 0.18), p(x, 0.82))
    elif name == "download":
        painter.drawLine(p(0.50, 0.15), p(0.50, 0.62))
        painter.drawLine(p(0.32, 0.46), p(0.50, 0.64))
        painter.drawLine(p(0.68, 0.46), p(0.50, 0.64))
        painter.drawRoundedRect(QRectF(w * 0.20, h * 0.72, w * 0.60, h * 0.15), 3, 3)
    elif name == "arrow-right":
        painter.drawLine(p(0.22, 0.50), p(0.75, 0.50))
        painter.drawLine(p(0.58, 0.34), p(0.75, 0.50))
        painter.drawLine(p(0.58, 0.66), p(0.75, 0.50))
    elif name == "reset":
        painter.drawArc(QRectF(w * 0.18, h * 0.18, w * 0.64, h * 0.64), 70 * 16, 270 * 16)
        painter.drawLine(p(0.27, 0.30), p(0.22, 0.12))
        painter.drawLine(p(0.27, 0.30), p(0.45, 0.28))
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
        grad.setColorAt(0.0, QColor(base.red(), base.green(), base.blue(), min(255, self.fill_alpha + 18)))
        grad.setColorAt(0.55, QColor(base.red(), base.green(), base.blue(), self.fill_alpha))
        grad.setColorAt(1.0, QColor(base.red(), base.green(), base.blue(), max(55, self.fill_alpha - 28)))
        painter.fillPath(path, grad)

        top_glow = QLinearGradient(rect.left(), rect.top(), rect.right(), rect.top())
        top_glow.setColorAt(0, QColor(255, 255, 255, 0))
        top_glow.setColorAt(0.5, rgba("#b8eaff", 34))
        top_glow.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setPen(QPen(top_glow, 1))
        painter.drawLine(QPointF(rect.left() + 18, rect.top() + 1), QPointF(rect.right() - 18, rect.top() + 1))

        painter.setPen(QPen(rgba(self.border, self.border_alpha), 1.0))
        painter.drawPath(path)
        super().paintEvent(event)


class SectionHeader(QWidget):
    def __init__(self, title: str, subtitle: str = ""):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        t = QLabel(title)
        t.setStyleSheet(f"color: {TEXT};")
        set_font(t, 17, QFont.Black)
        layout.addWidget(t)
        if subtitle:
            s = QLabel(subtitle)
            s.setStyleSheet(f"color: {MUTED};")
            set_font(s, 10)
            layout.addWidget(s)


class StyledButton(QPushButton):
    def __init__(self, text: str, primary: bool = False, height: int = 38):
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
                    padding: 0 14px;
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
                    padding: 0 14px;
                    font: 800 10px "Segoe UI";
                }}
                QPushButton:hover {{
                    color: {CYAN};
                    border-color: {CYAN};
                    background: rgba(9, 38, 64, 0.72);
                }}
            """)


class StepChip(QLabel):
    def __init__(self, text: str, active: bool = False):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(28)
        self.setMinimumWidth(78)
        self.setStyleSheet(f"""
            QLabel {{
                color: {TEXT if active else MUTED};
                background: {css_rgba(CYAN, 36) if active else '#0c2238'};
                border: 1px solid {CYAN if active else '#255173'};
                border-radius: 11px;
                padding: 0 10px;
                font: 800 9px "Segoe UI";
            }}
        """)


class IconBox(QWidget):
    def __init__(self, icon: str, color: str, size: int = 48):
        super().__init__()
        self.icon = icon
        self.color = QColor(color)
        self.setFixedSize(size, size)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(self.rect().adjusted(1, 1, -1, -1))
        path = QPainterPath()
        path.addRoundedRect(rect, 12, 12)
        grad = QRadialGradient(rect.center(), rect.width() * 0.85)
        c = QColor(self.color)
        c.setAlpha(78)
        grad.setColorAt(0, c)
        c2 = QColor(self.color)
        c2.setAlpha(22)
        grad.setColorAt(1, c2)
        painter.fillPath(path, grad)
        painter.setPen(QPen(self.color, 1.2))
        painter.drawPath(path)
        draw_icon(painter, self.icon, rect.adjusted(12, 12, -12, -12), self.color, 2.1)


class TableCell(QLabel):
    def __init__(self, text: str, header: bool = False, base: bool = False, highlight: bool = False, muted: bool = False):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumHeight(38 if not header else 36)
        color = "#b8c7d9" if header else (MUTED if muted else TEXT)
        bg = "transparent"
        border = "rgba(70, 120, 160, 0.25)"
        if base:
            bg = "rgba(16, 45, 72, 0.62)"
        if highlight:
            bg = "rgba(5, 230, 255, 0.24)"
            border = "rgba(5, 230, 255, 0.82)"
        self.setStyleSheet(f"""
            QLabel {{
                color: {color};
                background: {bg};
                border: 1px solid {border};
                padding: 2px 6px;
                font: {'800' if header or base or highlight else '600'} 11px "Segoe UI";
            }}
        """)


class TableauWidget(GlassPanel):
    def __init__(self, headers: list[str], rows: list[list[str]], highlight: tuple[int, int] | None = None):
        super().__init__(radius=10, fill="#0a2038", fill_alpha=118, border="#235171", border_alpha=130)
        self.headers = headers
        self.rows = rows
        self.highlight = highlight
        self._build()

    def _build(self):
        grid = QGridLayout(self)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)

        for c, h in enumerate(self.headers):
            grid.addWidget(TableCell(h, header=True), 0, c)
            grid.setColumnStretch(c, 1)

        for r, row in enumerate(self.rows, start=1):
            for c, value in enumerate(row):
                is_base = c == 0
                is_high = self.highlight == (r - 1, c)
                grid.addWidget(TableCell(value, base=is_base, highlight=is_high), r, c)


class PivotMarker(QWidget):
    def __init__(self, label: str = "Elemento pivô"):
        super().__init__()
        self.label = label
        self.setFixedHeight(44)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        cx = self.width() / 2
        painter.setPen(QPen(QColor(CYAN), 1.4, Qt.DashLine))
        painter.drawLine(QPointF(cx, 0), QPointF(cx, 14))
        badge = QRectF(cx - 58, 13, 116, 28)
        path = QPainterPath()
        path.addRoundedRect(badge, 10, 10)
        painter.fillPath(path, rgba("#062237", 230))
        painter.setPen(QPen(QColor(CYAN), 1.0))
        painter.drawPath(path)
        painter.setPen(QColor(CYAN))
        painter.setFont(app_font(9, QFont.Bold))
        painter.drawText(badge, Qt.AlignCenter, self.label)


class TableauPanel(GlassPanel):
    def __init__(self, title: str, headers: list[str], rows: list[list[str]], highlight: tuple[int, int] | None = None, pivot: bool = False):
        super().__init__(radius=15, fill=PANEL_3, fill_alpha=214, border="#285474", border_alpha=168)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 15, 18, 15)
        layout.setSpacing(10)
        t = QLabel(title)
        t.setStyleSheet(f"color: {CYAN};")
        set_font(t, 16, QFont.Black)
        layout.addWidget(t)
        table = TableauWidget(headers, rows, highlight)
        layout.addWidget(table, 1)
        if pivot:
            layout.addWidget(PivotMarker(), 0, Qt.AlignCenter)


class RatioPanel(GlassPanel):
    def __init__(self):
        super().__init__(radius=15, fill=PANEL_3, fill_alpha=214, border="#285474", border_alpha=168)
        self.setMinimumWidth(175)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 15, 16, 15)
        layout.setSpacing(10)

        t1 = QLabel("Variável que entra")
        t1.setStyleSheet(f"color: {CYAN};")
        set_font(t1, 14, QFont.Black)
        layout.addWidget(t1)
        layout.addWidget(StepChip("x₂", True), 0, Qt.AlignLeft)

        line1 = QFrame()
        line1.setFixedHeight(1)
        line1.setStyleSheet("background: rgba(120,160,200,0.22);")
        layout.addWidget(line1)

        t2 = QLabel("Variável que sai")
        t2.setStyleSheet(f"color: {CYAN};")
        set_font(t2, 14, QFont.Black)
        layout.addWidget(t2)
        out = StepChip("s₂", True)
        out.setStyleSheet(f"""
            QLabel {{
                color: {GREEN};
                background: {css_rgba(GREEN, 45)};
                border: 1px solid {GREEN};
                border-radius: 11px;
                padding: 0 10px;
                font: 800 9px "Segoe UI";
            }}
        """)
        layout.addWidget(out, 0, Qt.AlignLeft)

        line2 = QFrame()
        line2.setFixedHeight(1)
        line2.setStyleSheet("background: rgba(120,160,200,0.22);")
        layout.addWidget(line2)

        lbl = QLabel("Teste da razão (b / x₂)")
        lbl.setStyleSheet(f"color: {MUTED};")
        set_font(lbl, 9)
        layout.addWidget(lbl)
        layout.addWidget(RatioBox("10 / 1 = 10", False))
        layout.addWidget(RatioBox("14 / 2 = 7    ← mínimo", True))
        layout.addStretch(1)


class RatioBox(QLabel):
    def __init__(self, text: str, selected: bool = False):
        super().__init__(text)
        self.setFixedHeight(32)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.setStyleSheet(f"""
            QLabel {{
                color: {GREEN if selected else MUTED};
                background: {css_rgba(GREEN, 35) if selected else '#10263d'};
                border: 1px solid {GREEN if selected else '#274d6d'};
                border-radius: 8px;
                padding-left: 12px;
                font: 800 9px "Segoe UI";
            }}
        """)


class OperationsPanel(GlassPanel):
    def __init__(self):
        super().__init__(radius=15, fill=PANEL_3, fill_alpha=214, border="#285474", border_alpha=168)
        self.setMinimumWidth(185)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 15, 16, 15)
        layout.setSpacing(10)
        title = QLabel("Operações de linha")
        title.setStyleSheet(f"color: {CYAN};")
        set_font(title, 14, QFont.Black)
        layout.addWidget(title)
        for n, op in [
            ("1", "L₂ ← L₂ / 2"),
            ("2", "L₁ ← L₁ − L₂"),
            ("3", "Z ← Z + 5L₂"),
        ]:
            layout.addWidget(OperationRow(n, op))
        layout.addStretch(1)
        note = QLabel("L₁: linha da base s₁\nL₂: linha pivô normalizada\nZ: linha da função objetivo")
        note.setStyleSheet(f"color: {MUTED}; line-height: 130%;")
        set_font(note, 9)
        layout.addWidget(note)


class OperationRow(QWidget):
    def __init__(self, number: str, text: str):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        idx = QLabel(number)
        idx.setAlignment(Qt.AlignCenter)
        idx.setFixedSize(38, 30)
        idx.setStyleSheet(f"""
            QLabel {{
                color: {TEXT};
                background: {css_rgba(BLUE, 82)};
                border: 1px solid {CYAN};
                border-radius: 8px;
                font: 800 10px "Segoe UI";
            }}
        """)
        exp = QLabel(text)
        exp.setFixedHeight(30)
        exp.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        exp.setStyleSheet(f"""
            QLabel {{
                color: {TEXT};
                background: #10263d;
                border: 1px solid #274d6d;
                border-radius: 8px;
                padding-left: 10px;
                font: 700 10px "Segoe UI";
            }}
        """)
        layout.addWidget(idx)
        layout.addWidget(exp, 1)


class SummaryPanel(GlassPanel):
    def __init__(self):
        super().__init__(radius=16, fill=PANEL_3, fill_alpha=218, border="#2b5677", border_alpha=175)
        self.setMinimumHeight(330)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(12)
        title = QLabel("Resumo da resolução")
        title.setStyleSheet(f"color: {CYAN};")
        set_font(title, 16, QFont.Black)
        layout.addWidget(title)

        box = GlassPanel(radius=12, fill="#10253c", fill_alpha=235, border="#27506f", border_alpha=160)
        b = QVBoxLayout(box)
        b.setContentsMargins(16, 14, 16, 14)
        b.setSpacing(10)
        for icon, label, value, color in [
            ("refresh", "Iterações", "2", CYAN),
            ("pivot", "Pivôs realizados", "2", GREEN),
            ("check", "Status", "Ótimo", YELLOW),
            ("clock", "Tempo de solução", "00:00:12", CYAN),
        ]:
            b.addWidget(SummaryRow(icon, label, value, color))
        layout.addWidget(box, 1)


class SummaryRow(QWidget):
    def __init__(self, icon: str, label: str, value: str, color: str):
        super().__init__()
        self.setMinimumHeight(52)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.addWidget(IconBox(icon, color, 44))
        col = QVBoxLayout()
        col.setSpacing(1)
        l = QLabel(label)
        l.setStyleSheet(f"color: {MUTED};")
        set_font(l, 9)
        v = QLabel(value)
        v.setStyleSheet(f"color: {TEXT};")
        set_font(v, 16, QFont.Black)
        col.addWidget(l)
        col.addWidget(v)
        layout.addLayout(col, 1)


class FinalPanel(GlassPanel):
    def __init__(self):
        super().__init__(radius=16, fill="#082719", fill_alpha=218, border=GREEN, border_alpha=220)
        self.setMinimumHeight(278)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(12)
        title = QLabel("Resultado final")
        title.setStyleSheet(f"color: {GREEN};")
        set_font(title, 16, QFont.Black)
        layout.addWidget(title)

        mid = QHBoxLayout()
        mid.setSpacing(18)
        check = BigCheck()
        mid.addWidget(check)

        values = QVBoxLayout()
        values.setSpacing(5)
        for txt in ["x₁ = 2", "x₂ = 6", "s₁ = 0", "s₂ = 0"]:
            lbl = QLabel(txt)
            lbl.setStyleSheet(f"color: {TEXT};")
            set_font(lbl, 11, QFont.Bold)
            values.addWidget(lbl)
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background: rgba(180,230,220,0.22);")
        values.addWidget(sep)
        z = QLabel("Z = 36")
        z.setStyleSheet(f"color: {TEXT};")
        set_font(z, 20, QFont.Black)
        values.addWidget(z)
        mid.addLayout(values, 1)
        layout.addLayout(mid)

        ok = QLabel("▱ Solução ótima encontrada")
        ok.setStyleSheet(f"color: {GREEN};")
        set_font(ok, 12, QFont.Black)
        layout.addWidget(ok)
        desc = QLabel("A solução maximiza a função objetivo no ponto x₁ = 2 e x₂ = 6.")
        desc.setWordWrap(True)
        desc.setStyleSheet(f"color: {MUTED};")
        set_font(desc, 9)
        layout.addWidget(desc)
        equation = QLabel("Z = 3x₁ + 5x₂")
        equation.setAlignment(Qt.AlignCenter)
        equation.setStyleSheet(f"color: {MUTED};")
        set_font(equation, 10)
        layout.addStretch(1)
        layout.addWidget(equation)


class BigCheck(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(86, 86)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(self.rect().adjusted(5, 5, -5, -5))
        glow = QRadialGradient(rect.center(), 58)
        glow.setColorAt(0, rgba(GREEN, 68))
        glow.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(glow)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(rect.adjusted(-8, -8, 8, 8))
        painter.setBrush(rgba(GREEN, 28))
        painter.setPen(QPen(QColor(GREEN), 2.0))
        painter.drawEllipse(rect)
        painter.setPen(QPen(QColor(GREEN), 6, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawPolyline(QPolygonF([
            QPointF(rect.left() + 22, rect.center().y() + 4),
            QPointF(rect.left() + 35, rect.center().y() + 18),
            QPointF(rect.left() + 58, rect.center().y() - 14),
        ]))


class SimplexPage(QWidget):
    request_navigate = Signal(str)

    def __init__(self):
        super().__init__()
        self.current_step = 0
        self.headers = ["Base", "x₁", "x₂", "s₁", "s₂", "b"]
        self.tableaus = [
            [
                ["s₁", "2", "1", "1", "0", "10"],
                ["s₂", "1", "2", "0", "1", "14"],
                ["Z", "−3", "−5", "0", "0", "0"],
            ],
            [
                ["s₁", "3/2", "0", "1", "−1/2", "3"],
                ["x₂", "1/2", "1", "0", "1/2", "7"],
                ["Z", "−1/2", "0", "0", "5/2", "35"],
            ],
            [
                ["x₁", "1", "0", "2/3", "−1/3", "2"],
                ["x₂", "0", "1", "−1/3", "2/3", "6"],
                ["Z", "0", "0", "1/3", "7/3", "36"],
            ],
        ]
        self.step_label: QLabel | None = None
        self._build_ui()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(22, 18, 22, 18)
        root.setSpacing(16)

        left = QVBoxLayout()
        left.setSpacing(14)

        header = QHBoxLayout()
        header.setSpacing(12)
        title_block = QVBoxLayout()
        title_block.setSpacing(4)
        title = QLabel("Simplex tabular")
        title.setStyleSheet(f"color: {TEXT};")
        set_font(title, 28, QFont.Black)
        subtitle = QLabel("Resolução algébrica passo a passo")
        subtitle.setStyleSheet(f"color: {MUTED};")
        set_font(subtitle, 13)
        underline = QFrame()
        underline.setFixedSize(72, 4)
        underline.setStyleSheet(f"background: {CYAN}; border-radius: 2px;")
        title_block.addWidget(title)
        title_block.addWidget(subtitle)
        title_block.addWidget(underline, 0, Qt.AlignLeft)
        header.addLayout(title_block, 1)

        controls = QHBoxLayout()
        controls.setSpacing(8)
        prev_btn = StyledButton("◀ Anterior", False, 36)
        next_btn = StyledButton("Próxima ▶", True, 36)
        reset_btn = StyledButton("Reiniciar", False, 36)
        copy_btn = StyledButton("Copiar resultado", False, 36)
        prev_btn.clicked.connect(self.previous_step)
        next_btn.clicked.connect(self.next_step)
        reset_btn.clicked.connect(self.reset_steps)
        copy_btn.clicked.connect(self.copy_result)
        controls.addWidget(prev_btn)
        controls.addWidget(next_btn)
        controls.addWidget(reset_btn)
        controls.addWidget(copy_btn)
        header.addLayout(controls)
        left.addLayout(header)

        top = QHBoxLayout()
        top.setSpacing(12)
        self.initial_panel = TableauPanel(
            "Tableau inicial",
            self.headers,
            self.tableaus[0],
            highlight=(1, 2),
            pivot=True,
        )
        top.addWidget(self.initial_panel, 2)
        top.addWidget(RatioPanel(), 1)
        top.addWidget(OperationsPanel(), 1)
        left.addLayout(top, 1)

        bottom = QHBoxLayout()
        bottom.setSpacing(12)
        bottom.addWidget(TableauPanel("Iteração 1", self.headers, self.tableaus[1]), 1)
        bottom.addWidget(TableauPanel("Iteração 2", self.headers, self.tableaus[2]), 1)
        left.addLayout(bottom, 1)

        footer = GlassPanel(radius=13, fill="#0d2237", fill_alpha=160, border="#235171", border_alpha=120)
        footer_l = QHBoxLayout(footer)
        footer_l.setContentsMargins(18, 10, 18, 10)
        footer_l.setSpacing(10)
        self.step_label = QLabel("Passo atual: 0 · Tableau inicial")
        self.step_label.setStyleSheet(f"color: {MUTED};")
        set_font(self.step_label, 10, QFont.Bold)
        footer_l.addWidget(self.step_label)
        footer_l.addStretch(1)
        footer_l.addWidget(StepChip("Entrada: x₂", True))
        footer_l.addWidget(StepChip("Saída: s₂", True))
        footer_l.addWidget(StepChip("Pivô: 2", True))
        left.addWidget(footer)

        root.addLayout(left, 1)

        right_host = QWidget()
        right_host.setMinimumWidth(270)
        right_host.setMaximumWidth(305)
        right = QVBoxLayout(right_host)
        right.setContentsMargins(0, 0, 0, 0)
        right.setSpacing(14)
        right.addWidget(SummaryPanel(), 1)
        right.addWidget(FinalPanel(), 1)
        root.addWidget(right_host)

    def next_step(self):
        self.current_step = min(2, self.current_step + 1)
        self._sync_step_label()

    def previous_step(self):
        self.current_step = max(0, self.current_step - 1)
        self._sync_step_label()

    def reset_steps(self):
        self.current_step = 0
        self._sync_step_label()

    def copy_result(self):
        text = (
            "Simplex tabular - resultado final\n"
            "Max Z = 3x1 + 5x2\n"
            "Sujeito a: 2x1 + x2 <= 10; x1 + 2x2 <= 14; x1,x2 >= 0\n"
            "Solução ótima: x1 = 2, x2 = 6, Z = 36\n"
            "Iterações: 2 | Status: Ótimo"
        )
        QApplication.clipboard().setText(text)
        QMessageBox.information(self, "Resultado copiado", "Resumo da resolução copiado para a área de transferência.")

    def _sync_step_label(self):
        if not self.step_label:
            return
        labels = [
            "Passo atual: 0 · Tableau inicial · escolher coluna pivô x₂",
            "Passo atual: 1 · normalizar L₂ e zerar x₂",
            "Passo atual: 2 · solução ótima encontrada",
        ]
        self.step_label.setText(labels[self.current_step])
