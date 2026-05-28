import sys
from pathlib import Path

from PySide6.QtCore import QEasingCurve, QPointF, QRectF, Qt, Signal, QPropertyAnimation
from PySide6.QtGui import (
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QPolygonF,
    QRadialGradient,
)
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from pages.problems import ProblemsPage
from pages.graphs import GraphsPage
from pages.simplex import SimplexPage
# =========================================================
# RADIA MAX - HOME UI
# PySide6 desktop screen close to the provided target layout.
#
# Expected folder structure:
# radiamax/
#   main.py
#   public/
#     logo.png
#     backgroundCard.png
#
# Install:
#   pip install PySide6
# Run:
#   python main.py
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"
LOGO_PATH = PUBLIC_DIR / "logo.png"
CARD_BG_PATH = PUBLIC_DIR / "backgroundCard.png"

BG = "#020b16"
BG_2 = "#041224"
PANEL = "#07182b"
PANEL_2 = "#0a2038"
LINE = "#1b344f"
LINE_SOFT = "#263b57"
TEXT = "#f7fbff"
MUTED = "#aeb9ca"
CYAN = "#05e6ff"
CYAN_DARK = "#008ab9"
BLUE = "#057fe8"
GREEN = "#20e377"
YELLOW = "#ffc20e"
ORANGE = "#ff9700"


# -----------------------------
# Helpers
# -----------------------------
def qcolor(hex_color: str, alpha: int | None = None) -> QColor:
    c = QColor(hex_color)
    if alpha is not None:
        c.setAlpha(alpha)
    return c


def rgba(hex_color: str, alpha: int) -> QColor:
    return qcolor(hex_color, alpha)


def app_font(size: int, weight: QFont.Weight | int = QFont.Normal) -> QFont:
    f = QFont("Segoe UI")
    f.setPointSize(size)
    f.setWeight(weight)
    return f


def set_font(widget: QWidget, size: int, weight: QFont.Weight | int = QFont.Normal):
    widget.setFont(app_font(size, weight))


def draw_polyline(painter: QPainter, points: list[QPointF]):
    painter.drawPolyline(QPolygonF(points))


def draw_icon(painter: QPainter, name: str, rect: QRectF, color: QColor | str, line_width: float | None = None):
    """Draws vector icons directly on a QPainter. No QWidget.render hacks."""
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

    if name == "home":
        path = QPainterPath(p(0.14, 0.48))
        path.lineTo(p(0.50, 0.18))
        path.lineTo(p(0.86, 0.48))
        painter.drawPath(path)
        painter.drawRoundedRect(QRectF(w * 0.27, h * 0.45, w * 0.46, h * 0.40), 2.5, 2.5)
        painter.drawLine(p(0.44, 0.85), p(0.44, 0.64))
        painter.drawLine(p(0.56, 0.64), p(0.56, 0.85))

    elif name in ("file", "file-plus"):
        painter.drawRoundedRect(QRectF(w * 0.25, h * 0.14, w * 0.50, h * 0.72), 3, 3)
        painter.drawLine(p(0.58, 0.14), p(0.75, 0.31))
        painter.drawLine(p(0.58, 0.14), p(0.58, 0.32))
        painter.drawLine(p(0.58, 0.32), p(0.75, 0.32))
        painter.drawLine(p(0.36, 0.49), p(0.62, 0.49))
        painter.drawLine(p(0.36, 0.63), p(0.55, 0.63))
        if name == "file-plus":
            painter.drawLine(p(0.62, 0.66), p(0.90, 0.66))
            painter.drawLine(p(0.76, 0.52), p(0.76, 0.80))

    elif name == "folder":
        path = QPainterPath(p(0.12, 0.35))
        path.lineTo(p(0.36, 0.35))
        path.lineTo(p(0.44, 0.48))
        path.lineTo(p(0.88, 0.48))
        path.lineTo(p(0.88, 0.80))
        path.lineTo(p(0.12, 0.80))
        path.closeSubpath()
        painter.drawPath(path)

    elif name == "chart":
        painter.drawLine(p(0.16, 0.82), p(0.16, 0.18))
        painter.drawLine(p(0.16, 0.82), p(0.88, 0.82))
        draw_polyline(painter, [p(0.25, 0.68), p(0.42, 0.52), p(0.56, 0.60), p(0.80, 0.30)])
        painter.drawLine(p(0.80, 0.30), p(0.80, 0.46))
        painter.drawLine(p(0.80, 0.30), p(0.64, 0.31))

    elif name == "table":
        painter.drawRoundedRect(QRectF(w * 0.14, h * 0.18, w * 0.72, h * 0.64), 2.5, 2.5)
        for y in (0.39, 0.61):
            painter.drawLine(p(0.14, y), p(0.86, y))
        for x in (0.38, 0.62):
            painter.drawLine(p(x, 0.18), p(x, 0.82))

    elif name == "calculator":
        painter.drawRoundedRect(QRectF(w * 0.20, h * 0.13, w * 0.60, h * 0.74), 5, 5)
        painter.drawRoundedRect(QRectF(w * 0.33, h * 0.24, w * 0.34, h * 0.16), 2, 2)
        painter.setBrush(c)
        painter.setPen(Qt.NoPen)
        for row in range(3):
            for col in range(3):
                painter.drawEllipse(QPointF(w * (0.35 + col * 0.15), h * (0.56 + row * 0.12)), w * 0.027, h * 0.027)

    elif name == "cap":
        path = QPainterPath(p(0.12, 0.43))
        path.lineTo(p(0.50, 0.24))
        path.lineTo(p(0.88, 0.43))
        path.lineTo(p(0.50, 0.62))
        path.closeSubpath()
        painter.setBrush(c)
        painter.setPen(QPen(c, lw, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawPath(path)
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(p(0.72, 0.50), p(0.72, 0.70))
        painter.drawEllipse(QPointF(w * 0.72, h * 0.74), w * 0.025, h * 0.025)

    elif name == "history":
        painter.drawArc(QRectF(w * 0.16, h * 0.16, w * 0.68, h * 0.68), 45 * 16, 285 * 16)
        painter.drawLine(p(0.24, 0.49), p(0.11, 0.49))
        painter.drawLine(p(0.24, 0.49), p(0.25, 0.34))
        painter.drawLine(p(0.50, 0.31), p(0.50, 0.53))
        painter.drawLine(p(0.50, 0.53), p(0.64, 0.62))

    elif name == "apps":
        painter.setBrush(c)
        painter.setPen(Qt.NoPen)
        for row in range(3):
            for col in range(3):
                painter.drawEllipse(QPointF(w * (0.30 + col * 0.20), h * (0.30 + row * 0.20)), w * 0.05, h * 0.05)

    elif name == "check":
        painter.drawEllipse(QRectF(w * 0.18, h * 0.18, w * 0.64, h * 0.64))
        draw_polyline(painter, [p(0.34, 0.52), p(0.46, 0.64), p(0.69, 0.39)])

    elif name == "bell":
        painter.drawArc(QRectF(w * 0.25, h * 0.22, w * 0.50, h * 0.50), 0, 180 * 16)
        painter.drawLine(p(0.25, 0.48), p(0.18, 0.72))
        painter.drawLine(p(0.75, 0.48), p(0.82, 0.72))
        painter.drawLine(p(0.18, 0.72), p(0.82, 0.72))
        painter.drawLine(p(0.42, 0.84), p(0.58, 0.84))

    elif name == "help":
        painter.drawEllipse(QRectF(w * 0.16, h * 0.16, w * 0.68, h * 0.68))
        painter.setFont(app_font(max(10, int(w * 0.46)), QFont.Bold))
        painter.drawText(QRectF(0, -h * 0.03, w, h), Qt.AlignCenter, "?")

    elif name == "shield":
        path = QPainterPath(p(0.50, 0.15))
        path.lineTo(p(0.78, 0.27))
        path.lineTo(p(0.76, 0.58))
        path.quadTo(p(0.72, 0.77), p(0.50, 0.89))
        path.quadTo(p(0.28, 0.77), p(0.24, 0.58))
        path.lineTo(p(0.22, 0.27))
        path.closeSubpath()
        painter.drawPath(path)
        draw_polyline(painter, [p(0.36, 0.53), p(0.47, 0.64), p(0.67, 0.39)])

    elif name == "clock":
        painter.drawEllipse(QRectF(w * 0.18, h * 0.18, w * 0.64, h * 0.64))
        painter.drawLine(p(0.50, 0.31), p(0.50, 0.53))
        painter.drawLine(p(0.50, 0.53), p(0.65, 0.62))

    elif name == "arrow":
        painter.drawLine(p(0.25, 0.50), p(0.72, 0.50))
        painter.drawLine(p(0.56, 0.35), p(0.72, 0.50))
        painter.drawLine(p(0.56, 0.65), p(0.72, 0.50))

    painter.restore()


class VectorIcon(QWidget):
    def __init__(self, name: str, color: str = CYAN, size: int = 28):
        super().__init__()
        self.name = name
        self.color = color
        self.setFixedSize(size, size)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        draw_icon(painter, self.name, QRectF(0, 0, self.width(), self.height()), self.color)


# -----------------------------
# Base containers
# -----------------------------
class RootFrame(QFrame):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
        grad.setColorAt(0, QColor("#020712"))
        grad.setColorAt(0.48, QColor("#061629"))
        grad.setColorAt(1, QColor("#020812"))
        painter.fillRect(rect, grad)

        # subtle global perspective grid, less aggressive than the current screen
        painter.setPen(QPen(rgba(CYAN, 8), 1))
        for x in range(-180, rect.width() + 200, 150):
            painter.drawLine(x, 0, x + 280, rect.height())
        for y in range(65, rect.height() + 120, 118):
            painter.drawLine(0, y, rect.width(), y - 82)

        # outer shell
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(rgba("#5d718d", 58), 1.1))
        painter.drawRoundedRect(rect.adjusted(1, 1, -2, -2), 16, 16)
        super().paintEvent(event)


class GlassPanel(QFrame):
    def __init__(self, radius: int = 16, fill: str = PANEL, fill_alpha: int = 118, border: str = LINE, border_alpha: int = 145):
        super().__init__()
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

        grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
        base = QColor(self.fill)
        grad.setColorAt(0, QColor(base.red(), base.green(), base.blue(), self.fill_alpha + 18))
        grad.setColorAt(1, QColor(base.red(), base.green(), base.blue(), max(50, self.fill_alpha - 28)))
        painter.fillPath(path, grad)

        painter.setPen(QPen(rgba(self.border, self.border_alpha), 1))
        painter.drawPath(path)
        super().paintEvent(event)


# -----------------------------
# Sidebar
# -----------------------------
class LogoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.pixmap = QPixmap(str(LOGO_PATH))
        self.setFixedSize(120, 108)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if not self.pixmap.isNull():
            painter.drawPixmap(QRectF(22, 16, 74, 74).toRect(), self.pixmap)
        else:
            # fallback mark, only if public/logo.png is missing
            painter.setPen(QPen(QColor(CYAN), 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawRoundedRect(QRectF(32, 24, 54, 54), 10, 10)
            painter.drawLine(QPointF(42, 66), QPointF(74, 36))
            painter.drawLine(QPointF(64, 36), QPointF(76, 36))
            painter.drawLine(QPointF(76, 36), QPointF(76, 48))


class NavButton(QPushButton):
    activated = Signal(str)

    def __init__(self, key: str, icon: str, label: str, selected: bool = False):
        super().__init__(label)
        self.key = key
        self.icon = icon
        self.selected = selected
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(70)
        self.clicked.connect(lambda: self.activated.emit(self.key))
        self.update_style()

    def set_selected(self, selected: bool):
        self.selected = selected
        self.update_style()
        self.update()

    def update_style(self):
        color = CYAN if self.selected else TEXT
        bg = QColor(255, 255, 255, 18 if self.selected else 0).name(QColor.HexArgb)
        border = CYAN if self.selected else "transparent"
        self.setStyleSheet(
            f"""
            QPushButton {{
                text-align: left;
                color: {color};
                background: {bg};
                border: none;
                border-left: 5px solid {border};
                border-radius: 8px;
                padding-left: 66px;
                font: 600 15px "Segoe UI";
            }}
            QPushButton:hover {{
                background: {QColor(255, 255, 255, 14).name(QColor.HexArgb)};
                color: {CYAN};
            }}
            """
        )

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        draw_icon(painter, self.icon, QRectF(26, 21, 27, 27), CYAN if self.selected else "#c1cad8", 2.0)


class StatusBox(GlassPanel):
    def __init__(self):
        super().__init__(radius=9, fill="#063044", fill_alpha=108, border="#00a8b8", border_alpha=120)
        self.setFixedHeight(112)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(11)

        row = QHBoxLayout()
        dot = QWidget()
        dot.setFixedSize(12, 12)
        dot.setStyleSheet(f"background: {GREEN}; border-radius: 6px;")
        label = QLabel("Sistema operacional")
        label.setStyleSheet(f"color: {GREEN};")
        set_font(label, 10, QFont.Bold)
        row.addWidget(dot)
        row.addWidget(label)
        row.addStretch(1)
        layout.addLayout(row)

        bottom = QHBoxLayout()
        version = QLabel("Versão 1.0.0")
        version.setStyleSheet(f"color: {MUTED};")
        set_font(version, 10)
        bottom.addWidget(version)
        bottom.addStretch(1)
        bottom.addWidget(VectorIcon("shield", GREEN, 28))
        layout.addLayout(bottom)


class Sidebar(QWidget):
    route_selected = Signal(str)

    def __init__(self):
        super().__init__()
        self.setFixedWidth(230)
        self.buttons: dict[str, NavButton] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 20)
        layout.setSpacing(8)
        layout.addWidget(LogoWidget(), 0, Qt.AlignHCenter)
        layout.addSpacing(10)

        items = [
            ("home", "home", "Início"),
            ("problems", "file", "Problemas"),
            ("simplex", "calculator", "Simplex"),
            ("graphs", "chart", "Gráficos"),
            ("reports", "table", "Relatórios"),
        ]
        for key, icon, label in items:
            btn = NavButton(key, icon, label, selected=key == "home")
            btn.activated.connect(self.route_selected.emit)
            self.buttons[key] = btn
            layout.addWidget(btn)
            if key != "reports":
                layout.addSpacing(8)

        layout.addStretch(1)
        layout.addWidget(StatusBox())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(4, 16, 31, 152))
        painter.setPen(QPen(rgba(LINE_SOFT, 135), 1))
        painter.drawLine(self.width() - 1, 0, self.width() - 1, self.height())
        super().paintEvent(event)

    def set_route(self, key: str):
        for k, b in self.buttons.items():
            b.set_selected(k == key)


# -----------------------------
# Header
# -----------------------------
class Header(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(100)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(28, 0, 28, 0)
        layout.setSpacing(14)

        brand = QLabel(f'<span style="color:{TEXT};">Radia</span><span style="color:{CYAN};">Max</span>')
        set_font(brand, 27, QFont.Black)
        layout.addWidget(brand)

        divider = QFrame()
        divider.setFixedSize(1, 36)
        divider.setStyleSheet("background: rgba(170,190,220,0.25);")
        layout.addWidget(divider)

        subtitle = QLabel("Solução inteligente para Programação Linear")
        subtitle.setStyleSheet(f"color: {MUTED};")
        set_font(subtitle, 12)
        layout.addWidget(subtitle)
        layout.addStretch(1)

        layout.addWidget(VectorIcon("bell", "#c5ccda", 28))
        layout.addSpacing(16)
        layout.addWidget(VectorIcon("help", "#c5ccda", 28))
        layout.addSpacing(12)

        divider2 = QFrame()
        divider2.setFixedSize(1, 40)
        divider2.setStyleSheet("background: rgba(170,190,220,0.28);")
        layout.addWidget(divider2)
        layout.addSpacing(12)

        avatar = QLabel("LA")
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setFixedSize(62, 62)
        avatar.setStyleSheet(
            f"color: {TEXT}; background: #008db0; border: 1px solid {CYAN}; border-radius: 31px;"
        )
        set_font(avatar, 18, QFont.Bold)
        layout.addWidget(avatar)

        user_col = QVBoxLayout()
        user_col.setSpacing(2)
        name = QLabel("Lenir de Abreu")
        role = QLabel("Professor")
        name.setStyleSheet(f"color: {TEXT};")
        role.setStyleSheet(f"color: {MUTED};")
        set_font(name, 11, QFont.Bold)
        set_font(role, 10)
        user_col.addWidget(name)
        user_col.addWidget(role)
        layout.addLayout(user_col)

        arrow = QLabel("⌄")
        arrow.setStyleSheet(f"color: {MUTED};")
        set_font(arrow, 18)
        layout.addWidget(arrow)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(3, 11, 22, 118))
        painter.setPen(QPen(rgba(LINE_SOFT, 150), 1))
        painter.drawLine(0, self.height() - 1, self.width(), self.height() - 1)
        super().paintEvent(event)


# -----------------------------
# Hero action cards
# -----------------------------

class ActionCard(QPushButton):
    """
    Card vetorial e responsivo.
    Correção principal: não usa IconWidget/font, porque nesta versão do arquivo
    os ícones são desenhados por draw_icon() e a fonte por app_font().
    """

    def __init__(self, icon: str, title: str, color: str, accent: str, border: str):
        super().__init__()
        self.icon_name = icon
        self.title = title
        self.color = QColor(color)
        self.accent = QColor(accent)
        self.border = QColor(border)

        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(160)
        self.setMinimumWidth(102)
        self.setMaximumWidth(170)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setAttribute(Qt.WA_StyledBackground, False)

        self.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                padding: 0;
                margin: 0;
            }
        """)

    def _a(self, color: QColor | str, alpha: int) -> QColor:
        c = QColor(color) if isinstance(color, str) else QColor(color)
        c.setAlpha(alpha)
        return c

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        hovered = self.underMouse()
        pressed = self.isDown()

        rect = QRectF(self.rect().adjusted(1.2, 1.2, -1.2, -1.2))
        if pressed:
            rect.adjust(1.5, 1.5, -1.5, -1.5)

        path = QPainterPath()
        path.addRoundedRect(rect, 13, 13)

        # Base escura com cor do módulo, sem "estourar" neon.
        bg = QLinearGradient(rect.topLeft(), rect.bottomRight())
        bg.setColorAt(0.00, self._a(self.accent, 48 if hovered else 34))
        bg.setColorAt(0.38, QColor(5, 18, 35, 210))
        bg.setColorAt(0.70, QColor(3, 13, 27, 224))
        bg.setColorAt(1.00, self._a(self.accent, 34 if hovered else 20))
        painter.fillPath(path, bg)

        # Brilho interno central.
        glow = QRadialGradient(QPointF(rect.center().x(), rect.top() + 62), 112)
        glow.setColorAt(0.00, self._a(self.color, 70 if hovered else 48))
        glow.setColorAt(0.44, self._a(self.color, 18 if hovered else 10))
        glow.setColorAt(1.00, QColor(0, 0, 0, 0))
        painter.fillPath(path, glow)

        # Sombra interna inferior para separar texto/botão.
        lower = QLinearGradient(0, rect.top() + rect.height() * 0.56, 0, rect.bottom())
        lower.setColorAt(0.00, QColor(0, 0, 0, 0))
        lower.setColorAt(1.00, QColor(0, 5, 14, 118))
        painter.fillPath(path, lower)

        # Borda fina.
        painter.setPen(QPen(self._a(self.border, 230 if hovered else 170), 1.15))
        painter.drawPath(path)

        # Realce horizontal superior discreto.
        top_line = QLinearGradient(rect.left() + 14, rect.top(), rect.right() - 14, rect.top())
        top_line.setColorAt(0.00, QColor(0, 0, 0, 0))
        top_line.setColorAt(0.50, self._a(self.color, 150 if hovered else 88))
        top_line.setColorAt(1.00, QColor(0, 0, 0, 0))
        painter.setPen(QPen(top_line, 1))
        painter.drawLine(QPointF(rect.left() + 14, rect.top() + 1), QPointF(rect.right() - 14, rect.top() + 1))

        # Círculo do ícone.
        circle_size = min(64, max(48, self.width() * 0.44))
        circle_rect = QRectF(
            (self.width() - circle_size) / 2,
            16,
            circle_size,
            circle_size,
        )

        circle_outer = QRadialGradient(circle_rect.center(), circle_size * 0.92)
        circle_outer.setColorAt(0.00, self._a(self.color, 76 if hovered else 50))
        circle_outer.setColorAt(0.62, self._a(self.color, 18))
        circle_outer.setColorAt(1.00, QColor(0, 0, 0, 0))
        painter.setBrush(circle_outer)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(circle_rect.adjusted(-9, -9, 9, 9))

        circle_fill = QRadialGradient(circle_rect.center(), circle_size * 0.70)
        circle_fill.setColorAt(0.00, self._a(self.color, 42))
        circle_fill.setColorAt(1.00, self._a("#00162b", 192))
        painter.setBrush(circle_fill)
        painter.setPen(QPen(self._a(self.color, 230), 1.35))
        painter.drawEllipse(circle_rect)

        icon_size = min(40, max(28, circle_size * 0.54))
        icon_rect = QRectF(
            (self.width() - icon_size) / 2,
            circle_rect.top() + (circle_size - icon_size) / 2,
            icon_size,
            icon_size,
        )
        draw_icon(painter, self.icon_name, icon_rect, self.color, 2.25)

        # Texto: posição controlada para não bater no botão inferior.
        title_font_size = 13 if self.width() < 145 else 14
        painter.setPen(QColor(TEXT))
        painter.setFont(app_font(title_font_size, QFont.Bold))
        painter.drawText(
            QRectF(8, 88, self.width() - 16, 42),
            Qt.AlignCenter | Qt.TextWordWrap,
            self.title,
        )

       


class HeroPanel(QFrame):
    new_problem = Signal()
    load_example = Signal()
    tutorial = Signal()
    history = Signal()

    def __init__(self):
        super().__init__()
        self.background = QPixmap(str(CARD_BG_PATH))
        self.setAttribute(Qt.WA_StyledBackground, False)
        self.setMinimumHeight(376)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(34, 30, 24, 24)
        layout.setSpacing(0)

        top_wrap = QWidget()
        top_wrap.setFixedHeight(146)

        top = QVBoxLayout(top_wrap)
        top.setContentsMargins(0, 0, 0, 0)
        top.setSpacing(6)

        welcome = QLabel("Bem-vindo")
        welcome.setStyleSheet(f"color: {CYAN};")
        set_font(welcome, 14, QFont.Bold)

        title = QLabel("Pronto para otimizar\nsuas soluções")
        title.setStyleSheet(f"color: {TEXT};")
        set_font(title, 30, QFont.Black)
        title.setFixedHeight(92)

        underline = QFrame()
        underline.setFixedSize(62, 3)
        underline.setStyleSheet(f"background: {CYAN}; border-radius: 1px;")

        top.addWidget(welcome)
        top.addWidget(title)
        top.addWidget(underline)
        top.addStretch(1)

        layout.addWidget(top_wrap, 0)
        layout.addStretch(1)

        cards_wrap = QWidget()
        cards_wrap.setFixedHeight(164)

        cards = QHBoxLayout(cards_wrap)
        cards.setContentsMargins(0, 0, 0, 0)
        cards.setSpacing(14)
        cards.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        actions = [
            (ActionCard("file-plus", "Novo\nproblema", CYAN, BLUE, BLUE), self.new_problem.emit),
            (ActionCard("folder", "Carregar\nexemplo", CYAN, CYAN_DARK, CYAN), self.load_example.emit),
            (ActionCard("cap", "Ver\ntutorial", GREEN, GREEN, GREEN), self.tutorial.emit),
            (ActionCard("history", "Histórico", YELLOW, ORANGE, ORANGE), self.history.emit),
        ]

        for card, slot in actions:
            card.clicked.connect(slot)
            cards.addWidget(card, 1)

        cards.addStretch(0)
        layout.addWidget(cards_wrap, 0)

    def _draw_fallback_background(self, painter: QPainter, path: QPainterPath):
        rect = QRectF(self.rect().adjusted(1, 1, -1, -1))

        grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
        grad.setColorAt(0, QColor("#020a18"))
        grad.setColorAt(0.62, QColor("#06182f"))
        grad.setColorAt(1, QColor("#020814"))
        painter.fillPath(path, grad)

        painter.setPen(QPen(rgba(BLUE, 90), 1))

        origin_x = rect.width() * 0.52
        origin_y = rect.height() * 0.34

        for i in range(16):
            y = origin_y + i * 10
            pts = []
            for j in range(30):
                x = origin_x + j * 16
                z = -60 * (2.718 ** (-((j - 17) ** 2) / 26)) + 18 * (2.718 ** (-((j - 9) ** 2) / 18))
                pts.append(QPointF(x, y + z + j * 1.5))
            painter.drawPolyline(QPolygonF(pts))

        for j in range(4, 30, 3):
            pts = []
            for i in range(16):
                y = origin_y + i * 10
                x = origin_x + j * 16
                z = -60 * (2.718 ** (-((j - 17) ** 2) / 26)) + 18 * (2.718 ** (-((j - 9) ** 2) / 18))
                pts.append(QPointF(x, y + z + j * 1.5))
            painter.drawPolyline(QPolygonF(pts))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(self.rect().adjusted(0.8, 0.8, -0.8, -0.8))

        path = QPainterPath()
        path.addRoundedRect(rect, 14, 14)

        painter.setClipPath(path)

        if not self.background.isNull():
            crop_left = 18
            crop_top = 14
            crop_right = 18
            crop_bottom = 14

            source = QRectF(
                crop_left,
                crop_top,
                self.background.width() - crop_left - crop_right,
                self.background.height() - crop_top - crop_bottom,
            )

            target = QRectF(
                rect.left() - 8,
                rect.top() - 6,
                rect.width() + 16,
                rect.height() + 12,
            )

            painter.drawPixmap(target, self.background, source)
        else:
            self._draw_fallback_background(painter, path)

        shade = QLinearGradient(0, 0, self.width(), 0)
        shade.setColorAt(0.00, rgba("#020914", 120))
        shade.setColorAt(0.38, rgba("#020914", 48))
        shade.setColorAt(0.72, rgba("#020914", 8))
        shade.setColorAt(1.00, rgba("#020914", 0))
        painter.fillPath(path, shade)

        bottom_shadow = QLinearGradient(0, self.height() * 0.52, 0, self.height())
        bottom_shadow.setColorAt(0.00, QColor(0, 0, 0, 0))
        bottom_shadow.setColorAt(1.00, rgba("#000814", 72))
        painter.fillPath(path, bottom_shadow)

        painter.setClipping(False)

        border_grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
        border_grad.setColorAt(0.00, rgba(CYAN, 90))
        border_grad.setColorAt(0.45, rgba("#6eaed2", 40))
        border_grad.setColorAt(1.00, rgba("#1b344f", 100))

        painter.setPen(QPen(border_grad, 1.0))
        painter.drawPath(path)

        super().paintEvent(event)

def paintEvent(self, event):
    painter = QPainter(self)
    painter.setRenderHint(QPainter.Antialiasing)

    rect = QRectF(self.rect().adjusted(0.8, 0.8, -0.8, -0.8))
    path = QPainterPath()
    path.addRoundedRect(rect, 14, 14)

    painter.setClipPath(path)

    if not self.background.isNull():
        # Corta a borda interna da própria imagem.
        # A imagem tinha uma moldura própria; isso remove essa margem visual.
        crop_left = 18
        crop_top = 14
        crop_right = 18
        crop_bottom = 14

        source = QRectF(
            crop_left,
            crop_top,
            self.background.width() - crop_left - crop_right,
            self.background.height() - crop_top - crop_bottom,
        )

        # Estica levemente a imagem para preencher melhor o card.
        # Como está com clip arredondado, não vaza para fora.
        target = QRectF(
            rect.left() - 8,
            rect.top() - 6,
            rect.width() + 16,
            rect.height() + 12,
        )

        painter.drawPixmap(target, self.background, source)
    else:
        self._draw_fallback_background(painter, path)

    # Camada de leitura, mais suave.
    shade = QLinearGradient(0, 0, self.width(), 0)
    shade.setColorAt(0.00, rgba("#020914", 130))
    shade.setColorAt(0.38, rgba("#020914", 58))
    shade.setColorAt(0.72, rgba("#020914", 10))
    shade.setColorAt(1.00, rgba("#020914", 0))
    painter.fillPath(path, shade)

    # Sombra inferior mais controlada.
    bottom_shadow = QLinearGradient(0, self.height() * 0.52, 0, self.height())
    bottom_shadow.setColorAt(0.00, QColor(0, 0, 0, 0))
    bottom_shadow.setColorAt(1.00, rgba("#000814", 78))
    painter.fillPath(path, bottom_shadow)

    painter.setClipping(False)

    # Agora só fica a borda real do card, não a borda da imagem.
    border_grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
    border_grad.setColorAt(0.00, rgba(CYAN, 95))
    border_grad.setColorAt(0.45, rgba("#6eaed2", 45))
    border_grad.setColorAt(1.00, rgba("#1b344f", 105))

    painter.setPen(QPen(border_grad, 1.0))
    painter.drawPath(path)

    super().paintEvent(event)
# -----------------------------
# Graph preview
# -----------------------------
class LegendItem(QWidget):
    def __init__(self, color: str, label: str, filled: bool = False):
        super().__init__()
        self.color = color
        self.label = label
        self.filled = filled
        self.setFixedHeight(30)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        y = self.height() / 2
        if self.filled:
            painter.fillRect(QRectF(0, y - 6, 32, 12), rgba(BLUE, 58))
            painter.setPen(QPen(QColor(self.color), 1.3))
            painter.drawRect(QRectF(0, y - 6, 32, 12))
        else:
            pen = QPen(QColor(self.color), 2)
            pen.setDashPattern([5, 4])
            painter.setPen(pen)
            painter.drawLine(QPointF(0, y), QPointF(34, y))
        painter.setPen(QColor(MUTED))
        painter.setFont(app_font(10))
        painter.drawText(QRectF(50, 0, self.width() - 50, self.height()), Qt.AlignVCenter | Qt.AlignLeft, self.label)


class GraphCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(195)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        left, top, right, bottom = 62, 14, w - 24, h - 34

        # grid
        painter.setPen(QPen(rgba("#ffffff", 22), 1))
        for i in range(11):
            x = left + i * ((right - left) / 10)
            painter.drawLine(QPointF(x, top), QPointF(x, bottom))
        for i in range(7):
            y = bottom - i * ((bottom - top) / 6)
            painter.drawLine(QPointF(left, y), QPointF(right, y))

        # axes
        axis_pen = QPen(QColor("#cfd7e5"), 1.25)
        painter.setPen(axis_pen)
        painter.drawLine(QPointF(left, bottom), QPointF(right, bottom))
        painter.drawLine(QPointF(left, bottom), QPointF(left, top))
        # arrow tips
        painter.drawLine(QPointF(right, bottom), QPointF(right - 9, bottom - 5))
        painter.drawLine(QPointF(right, bottom), QPointF(right - 9, bottom + 5))
        painter.drawLine(QPointF(left, top), QPointF(left - 5, top + 9))
        painter.drawLine(QPointF(left, top), QPointF(left + 5, top + 9))

        plot_w = right - left
        plot_h = bottom - top

        def map_xy(x, y):
            return QPointF(left + (x / 10) * plot_w, bottom - (y / 7) * plot_h)

        # feasible region
        region_points = [map_xy(0, 0), map_xy(2.8, 3), map_xy(5.0, 3), map_xy(6.0, 0)]
        region = QPainterPath(region_points[0])
        for pt in region_points[1:]:
            region.lineTo(pt)
        region.closeSubpath()
        painter.fillPath(region, rgba(BLUE, 100))
        painter.setPen(QPen(QColor(CYAN), 2))
        painter.drawPath(region)

        # restrictions
        pen1 = QPen(QColor(CYAN), 2)
        pen1.setDashPattern([7, 5])
        painter.setPen(pen1)
        painter.drawLine(map_xy(0, 7.2), map_xy(7.5, 0.4))

        pen2 = QPen(QColor(GREEN), 2)
        pen2.setDashPattern([7, 5])
        painter.setPen(pen2)
        painter.drawLine(map_xy(0, 4.0), map_xy(8.6, 0))

        pen3 = QPen(QColor(YELLOW), 2)
        pen3.setDashPattern([6, 4])
        painter.setPen(pen3)
        painter.drawLine(map_xy(0, 0), map_xy(6.0, 0))
        painter.drawLine(map_xy(0, 0), map_xy(0, 4.0))

        # objective/extra faint lines
        painter.setPen(QPen(rgba(BLUE, 78), 1.05))
        painter.drawLine(map_xy(1.6, 5.6), map_xy(7.1, 1.7))
        painter.drawLine(map_xy(2.9, 6.0), map_xy(7.0, 2.0))
        painter.drawLine(map_xy(2.2, 6.7), map_xy(6.5, 3.1))

        # markers
        painter.setBrush(QColor(YELLOW))
        painter.setPen(Qt.NoPen)
        for point in [map_xy(0, 0), map_xy(0, 4), map_xy(6, 0)]:
            painter.drawEllipse(point, 4.3, 4.3)
        painter.setBrush(QColor(BG))
        painter.setPen(QPen(QColor(CYAN), 2))
        painter.drawEllipse(map_xy(3.4, 3.0), 6, 6)

        # labels
        painter.setPen(QColor("#dbe3ef"))
        painter.setFont(app_font(9))
        for y in (0, 2, 4, 6):
            painter.drawText(QRectF(left - 30, map_xy(0, y).y() - 8, 22, 16), Qt.AlignRight | Qt.AlignVCenter, str(y))
        for x in (0, 2, 4, 6, 8, 10):
            painter.drawText(QRectF(map_xy(x, 0).x() - 10, bottom + 10, 22, 16), Qt.AlignCenter, str(x))
        painter.drawText(QPointF(left - 34, top + 8), "x₂")
        painter.drawText(QPointF(right + 8, bottom + 8), "x₁")


class GraphPanel(GlassPanel):
    def __init__(self):
        super().__init__(radius=14, fill=PANEL, fill_alpha=94, border=LINE_SOFT, border_alpha=130)
        self.setFixedHeight(220)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(26, 18, 20, 12)
        layout.setSpacing(20)

        legend = QVBoxLayout()
        legend.setSpacing(7)
        title = QLabel("Prévia gráfica")
        title.setStyleSheet(f"color: {TEXT};")
        set_font(title, 15, QFont.Bold)
        legend.addWidget(title)
        legend.addSpacing(10)
        legend.addWidget(LegendItem(CYAN, "Restrição 1"))
        legend.addWidget(LegendItem(GREEN, "Restrição 2"))
        legend.addWidget(LegendItem(YELLOW, "Restrição 3"))
        legend.addWidget(LegendItem(BLUE, "Região viável", True))
        legend.addStretch(1)
        layout.addLayout(legend)
        layout.addWidget(GraphCanvas(), 1)


# -----------------------------
# Right side panels
# -----------------------------
class ResourceButton(QPushButton):
    def __init__(self, icon: str, label: str, color: str, bg: str):
        super().__init__()
        self.icon = icon
        self.label = label
        self.color = QColor(color)
        self.bg = QColor(bg)
        self.setFixedHeight(82)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("QPushButton { border: none; background: transparent; }")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.underMouse():
            hover_path = QPainterPath()
            hover_path.addRoundedRect(QRectF(self.rect().adjusted(0, 1, 0, -1)), 9, 9)
            painter.fillPath(hover_path, rgba("#ffffff", 12))

        square = QRectF(0, 10, 58, 58)
        path = QPainterPath()
        path.addRoundedRect(square, 9, 9)
        fill = QColor(self.bg)
        fill.setAlpha(130)
        painter.fillPath(path, fill)
        painter.setPen(QPen(self.color, 1.25))
        painter.drawPath(path)

        inner_glow = QRadialGradient(square.center(), 48)
        glow = QColor(self.color)
        glow.setAlpha(62)
        inner_glow.setColorAt(0, glow)
        inner_glow.setColorAt(1, QColor(glow.red(), glow.green(), glow.blue(), 0))
        painter.fillPath(path, inner_glow)

        draw_icon(painter, self.icon, QRectF(14, 24, 30, 30), self.color, 2.2)

        painter.setPen(QColor(TEXT))
        painter.setFont(app_font(15, QFont.Bold))
        painter.drawText(QRectF(82, 0, self.width() - 90, self.height()), Qt.AlignVCenter | Qt.AlignLeft, self.label)

        painter.setPen(QPen(rgba("#ffffff", 26), 1))
        painter.drawLine(QPointF(0, self.height() - 1), QPointF(self.width(), self.height() - 1))


class ResourcesPanel(GlassPanel):
    feature_selected = Signal(str)

    def __init__(self):
        super().__init__(radius=16, fill=PANEL, fill_alpha=82, border=LINE_SOFT, border_alpha=130)
        self.setMinimumHeight(420)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 20)
        layout.setSpacing(18)

        title = QLabel("Recursos")
        title.setStyleSheet(f"color: {TEXT};")
        set_font(title, 21, QFont.Black)
        layout.addWidget(title)

        list_box = GlassPanel(radius=12, fill=PANEL_2, fill_alpha=112, border=LINE_SOFT, border_alpha=125)
        box = QVBoxLayout(list_box)
        box.setContentsMargins(24, 16, 24, 12)
        box.setSpacing(8)

        items = [
            ("simplex", "calculator", "Simplex", CYAN, BLUE),
            ("graphic", "chart", "Análise gráfica", GREEN, GREEN),
            ("integer", "apps", "Solução inteira", YELLOW, ORANGE),
            ("table", "table", "Tabela", CYAN, BLUE),
        ]
        for key, icon, label, color, bg in items:
            btn = ResourceButton(icon, label, color, bg)
            btn.clicked.connect(lambda checked=False, route=key: self.feature_selected.emit(route))
            box.addWidget(btn)

        layout.addWidget(list_box, 1)


class StatBlock(QWidget):
    def __init__(self, icon: str, value: str, label: str, color: str):
        super().__init__()
        self.icon = icon
        self.value = value
        self.label = label
        self.color = color

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        cx = self.width() / 2
        draw_icon(painter, self.icon, QRectF(cx - 14, 11, 28, 28), self.color, 2.1)
        painter.setPen(QColor(TEXT))
        painter.setFont(app_font(20, QFont.Black))
        painter.drawText(QRectF(0, 50, self.width(), 34), Qt.AlignCenter, self.value)
        painter.setPen(QColor(MUTED))
        painter.setFont(app_font(10))
        painter.drawText(QRectF(0, 88, self.width(), 28), Qt.AlignCenter, self.label)


class StatsPanel(GlassPanel):
    def __init__(self):
        super().__init__(radius=14, fill=PANEL, fill_alpha=86, border=LINE_SOFT, border_alpha=130)
        self.setFixedHeight(170)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 24, 18, 24)
        layout.setSpacing(0)

        stats = [
            ("file", "24", "Problemas", CYAN),
            ("check", "18", "Resoluções", GREEN),
            ("chart", "12", "Gráficos", YELLOW),
            ("clock", "36", "Iterações", CYAN),
        ]
        for i, s in enumerate(stats):
            layout.addWidget(StatBlock(*s), 1)
            if i < len(stats) - 1:
                line = QFrame()
                line.setFixedWidth(1)
                line.setStyleSheet(f"background: {LINE_SOFT};")
                layout.addWidget(line)


# -----------------------------
# Pages
# -----------------------------
class HomePage(QWidget):
    action_requested = Signal(str)
    feature_requested = Signal(str)

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(18)

        left = QVBoxLayout()
        left.setSpacing(14)
        hero = HeroPanel()
        hero.new_problem.connect(lambda: self.action_requested.emit("new_problem"))
        hero.load_example.connect(lambda: self.action_requested.emit("load_example"))
        hero.tutorial.connect(lambda: self.action_requested.emit("tutorial"))
        hero.history.connect(lambda: self.action_requested.emit("history"))
        left.addWidget(hero, 1)
        left.addWidget(GraphPanel())
        layout.addLayout(left, 1)

        right_wrap = QWidget()
        right_wrap.setMinimumWidth(370)
        right_wrap.setMaximumWidth(430)
        right_wrap.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        right = QVBoxLayout(right_wrap)
        right.setContentsMargins(0, 0, 0, 0)
        right.setSpacing(14)
        resources = ResourcesPanel()
        resources.feature_selected.connect(self.feature_requested.emit)
        right.addWidget(resources, 1)
        right.addWidget(StatsPanel())
        layout.addWidget(right_wrap)


class PlaceholderPage(QWidget):
    def __init__(self, title: str, subtitle: str, icon: str):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        panel = GlassPanel(radius=16, fill=PANEL, fill_alpha=106)
        p = QVBoxLayout(panel)
        p.setContentsMargins(34, 34, 34, 34)
        p.setSpacing(12)
        p.addWidget(VectorIcon(icon, CYAN, 48), 0, Qt.AlignLeft)
        h = QLabel(title)
        h.setStyleSheet(f"color: {TEXT};")
        set_font(h, 26, QFont.Black)
        s = QLabel(subtitle)
        s.setStyleSheet(f"color: {MUTED};")
        set_font(s, 12)
        p.addWidget(h)
        p.addWidget(s)
        p.addStretch(1)
        layout.addWidget(panel)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RadiaMax")
        self.resize(1600, 900)
        self.setMinimumSize(1280, 760)

        root = RootFrame()
        self.setCentralWidget(root)
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.route_selected.connect(self.go_to)
        root_layout.addWidget(self.sidebar)

        main = QWidget()
        main_layout = QVBoxLayout(main)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(Header())

        self.stack = QStackedWidget()
        self.home = HomePage()
        self.home.action_requested.connect(self.handle_action)
        self.home.feature_requested.connect(self.handle_feature)
        self.problems = ProblemsPage()
        if hasattr(self.problems, 'request_navigate'):
            self.problems.request_navigate.connect(self.go_to)

        self.pages = {
            "home": self.home,
            "problems": self.problems,
            "simplex": SimplexPage(),
            "graphs": GraphsPage(),
            "reports": PlaceholderPage(
                "Relatórios",
                "Histórico, iterações, tabelas e exportação dos resultados calculados.",
                "table",
            ),
        }
        for page in self.pages.values():
            self.stack.addWidget(page)
        main_layout.addWidget(self.stack, 1)
        root_layout.addWidget(main, 1)
        self._animation = None

    def go_to(self, key: str):
        page = self.pages.get(key)
        if page is None:
            return
        self.sidebar.set_route(key)
        if self.stack.currentWidget() is page:
            return
        self.stack.setCurrentWidget(page)
        effect = QGraphicsOpacityEffect(page)
        page.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity", self)
        anim.setDuration(180)
        anim.setStartValue(0.25)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.finished.connect(lambda: page.setGraphicsEffect(None))
        anim.start()
        self._animation = anim

    def handle_action(self, action: str):
        if action == "new_problem":
            self.go_to("problems")
        elif action == "load_example":
            self.go_to("problems")
            QMessageBox.information(self, "Exemplo carregado", "Aqui você carrega um modelo radioterápico de exemplo.")
        elif action == "tutorial":
            QMessageBox.information(self, "Tutorial", "Fluxo: cadastrar modelo, validar restrições, montar tableau e resolver.")
        elif action == "history":
            self.go_to("reports")

    def handle_feature(self, feature: str):
        if feature == "simplex":
            self.go_to("simplex")
        elif feature == "graphic":
            self.go_to("graphs")
        elif feature == "integer":
            QMessageBox.information(self, "Solução inteira", "Módulo preparado para Branch and Bound / programação inteira.")
        elif feature == "table":
            self.go_to("reports")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
