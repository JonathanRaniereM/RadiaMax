from __future__ import annotations

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
    QRadialGradient,
)
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsOpacityEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

# =========================================================
# RADIA MAX - MÓDULO DA TELA DE PROBLEMAS
# Importado pelo main.py. Não inicia janela própria.
#
# Estrutura esperada:
#   projeto/
#   ├── main.py   (ou este arquivo)
#   └── public/
#       └── logo.png   (opcional; se não existir, desenha fallback)
#
# Instalar:
#   pip install PySide6
#
# Executar:
#   python radiamax_problems_complete_corrigido.py
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"
LOGO_PATH = PUBLIC_DIR / "logo.png"

BG = "#020b16"
BG_2 = "#041224"
PANEL = "#07182b"
PANEL_2 = "#0a2038"
PANEL_3 = "#17304b"
LINE = "#1b344f"
LINE_SOFT = "#2a5374"
TEXT = "#f7fbff"
MUTED = "#aeb9ca"
CYAN = "#05e6ff"
CYAN_DARK = "#008ab9"
BLUE = "#057fe8"
GREEN = "#20e377"
YELLOW = "#ffc20e"
ORANGE = "#ff9700"


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


def css_alpha(hex_color: str, alpha: int) -> str:
    c = QColor(hex_color)
    return f"rgba({c.red()}, {c.green()}, {c.blue()}, {alpha / 255:.3f})"


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

    elif name == "chart":
        painter.drawLine(p(0.16, 0.82), p(0.16, 0.18))
        painter.drawLine(p(0.16, 0.82), p(0.88, 0.82))
        painter.drawPolyline([p(0.25, 0.68), p(0.42, 0.52), p(0.56, 0.60), p(0.80, 0.30)])
        painter.drawLine(p(0.80, 0.30), p(0.80, 0.46))
        painter.drawLine(p(0.80, 0.30), p(0.64, 0.31))

    elif name == "table":
        painter.drawRoundedRect(QRectF(w * 0.14, h * 0.18, w * 0.72, h * 0.64), 2.5, 2.5)
        for y in (0.39, 0.61):
            painter.drawLine(p(0.14, y), p(0.86, y))
        for x in (0.38, 0.62):
            painter.drawLine(p(x, 0.18), p(x, 0.82))

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
        painter.drawPolyline([p(0.36, 0.53), p(0.47, 0.64), p(0.67, 0.39)])

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


class RootFrame(QFrame):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
        grad.setColorAt(0, QColor("#020712"))
        grad.setColorAt(0.52, QColor("#061629"))
        grad.setColorAt(1, QColor("#020812"))
        painter.fillRect(rect, grad)

        # Grid global bem sutil. Na versão anterior ele gritava mais que aluno no recreio.
        painter.setPen(QPen(rgba(CYAN, 7), 1))
        for x in range(-180, rect.width() + 200, 150):
            painter.drawLine(x, 0, x + 280, rect.height())
        for y in range(65, rect.height() + 120, 118):
            painter.drawLine(0, y, rect.width(), y - 82)

        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(rgba("#5d718d", 52), 1.0))
        painter.drawRoundedRect(rect.adjusted(1, 1, -2, -2), 16, 16)
        super().paintEvent(event)


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
        grad.setColorAt(0, QColor(base.red(), base.green(), base.blue(), min(255, self.fill_alpha + 18)))
        grad.setColorAt(0.52, QColor(base.red(), base.green(), base.blue(), self.fill_alpha))
        grad.setColorAt(1, QColor(base.red(), base.green(), base.blue(), max(60, self.fill_alpha - 30)))
        painter.fillPath(path, grad)

        # Leve brilho interno no topo, igual card premium; sem borda dupla carnavalesca.
        top_glow = QLinearGradient(rect.left(), rect.top(), rect.right(), rect.top())
        top_glow.setColorAt(0, QColor(255, 255, 255, 0))
        top_glow.setColorAt(0.5, rgba("#b8eaff", 42))
        top_glow.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setPen(QPen(top_glow, 1))
        painter.drawLine(QPointF(rect.left() + 18, rect.top() + 1), QPointF(rect.right() - 18, rect.top() + 1))

        painter.setPen(QPen(rgba(self.border, self.border_alpha), 1.0))
        painter.drawPath(path)
        super().paintEvent(event)


class LogoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.pixmap = QPixmap(str(LOGO_PATH))
        self.setFixedSize(112, 102)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if not self.pixmap.isNull():
            painter.drawPixmap(QRectF(22, 15, 72, 72).toRect(), self.pixmap)
        else:
            painter.setPen(QPen(QColor(CYAN), 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawRoundedRect(QRectF(31, 22, 56, 56), 10, 10)
            painter.drawLine(QPointF(42, 66), QPointF(74, 36))
            painter.drawLine(QPointF(64, 36), QPointF(78, 36))
            painter.drawLine(QPointF(78, 36), QPointF(78, 50))


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
        bg_alpha = 22 if self.selected else 0
        border = CYAN if self.selected else "transparent"
        self.setStyleSheet(
            f"""
            QPushButton {{
                text-align: left;
                color: {color};
                background: rgba(255,255,255,{bg_alpha / 255:.3f});
                border: none;
                border-left: 5px solid {border};
                border-radius: 9px;
                padding-left: 68px;
                font: 700 15px "Segoe UI";
            }}
            QPushButton:hover {{
                background: rgba(255,255,255,0.060);
                color: {CYAN};
            }}
            """
        )

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        draw_icon(painter, self.icon, QRectF(28, 21, 27, 27), CYAN if self.selected else "#c1cad8", 2.0)


class StatusBox(GlassPanel):
    def __init__(self):
        super().__init__(radius=10, fill="#063044", fill_alpha=115, border="#00a8b8", border_alpha=140)
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
        self.setFixedWidth(218)
        self.buttons: dict[str, NavButton] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 0, 14, 20)
        layout.setSpacing(8)
        layout.addWidget(LogoWidget(), 0, Qt.AlignHCenter)
        layout.addSpacing(10)

        items = [
            ("home", "home", "Início"),
            ("problems", "file", "Problemas"),
            ("graphs", "chart", "Gráficos"),
            ("reports", "table", "Relatórios"),
        ]
        for key, icon, label in items:
            btn = NavButton(key, icon, label, selected=key == "problems")
            btn.activated.connect(self.route_selected.emit)
            self.buttons[key] = btn
            layout.addWidget(btn)
            if key != "reports":
                layout.addSpacing(8)

        layout.addStretch(1)
        layout.addWidget(StatusBox())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(4, 16, 31, 160))
        painter.setPen(QPen(rgba(LINE_SOFT, 135), 1))
        painter.drawLine(self.width() - 1, 0, self.width() - 1, self.height())
        super().paintEvent(event)

    def set_route(self, key: str):
        for k, b in self.buttons.items():
            b.set_selected(k == key)


class Header(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(94)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(22, 0, 28, 0)
        layout.setSpacing(14)

        brand = QLabel(f'<span style="color:{TEXT};">Radia</span><span style="color:{CYAN};">Max</span>')
        set_font(brand, 27, QFont.Black)
        layout.addWidget(brand)

        divider = QFrame()
        divider.setFixedSize(1, 36)
        divider.setStyleSheet("background: rgba(170,190,220,0.25);")
        layout.addWidget(divider)

        subtitle = QLabel("Cadastro e modelagem de problemas de programação linear")
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
            f"color: {TEXT}; background: #259e64; border: 1px solid {GREEN}; border-radius: 31px;"
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
        painter.fillRect(self.rect(), QColor(3, 11, 22, 126))
        painter.setPen(QPen(rgba(LINE_SOFT, 150), 1))
        painter.drawLine(0, self.height() - 1, self.width(), self.height() - 1)
        super().paintEvent(event)


class StyledButton(QPushButton):
    def __init__(self, text: str, primary: bool = False, height: int = 42):
        super().__init__(text)
        self.primary = primary
        self.setFixedHeight(height)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(self._style(False))

    def _style(self, hover: bool) -> str:
        if self.primary:
            bg = "#14c9e8" if not hover else "#25def7"
            return f"""
                QPushButton {{
                    background: {bg};
                    color: white;
                    border: none;
                    border-radius: 14px;
                    padding: 0 16px;
                    font: 800 11px "Segoe UI";
                }}
                QPushButton:hover {{ background: #25def7; }}
            """
        return f"""
            QPushButton {{
                background: rgba(8, 28, 49, 0.55);
                color: {TEXT};
                border: 1px solid #2a5677;
                border-radius: 14px;
                padding: 0 16px;
                font: 800 11px "Segoe UI";
            }}
            QPushButton:hover {{
                color: {CYAN};
                border-color: {CYAN};
                background: rgba(9, 38, 64, 0.72);
            }}
        """


class StyledLineEdit(QLineEdit):
    def __init__(self, text: str = "", placeholder: str = ""):
        super().__init__(text)
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(46)
        self.setStyleSheet(f"""
            QLineEdit {{
                background: #0c2238;
                color: {TEXT};
                border: 1px solid #255173;
                border-radius: 12px;
                padding: 0 14px;
                font: 700 11px "Segoe UI";
            }}
            QLineEdit:focus {{ border-color: {CYAN}; }}
        """)


class SegmentedControl(GlassPanel):
    def __init__(self):
        super().__init__(radius=12, fill="#0c2238", fill_alpha=228, border="#255173", border_alpha=190)
        self.setFixedHeight(46)
        self.value = "max"
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)
        self.btn_max = QPushButton("Maximização")
        self.btn_min = QPushButton("Minimização")
        for btn in (self.btn_max, self.btn_min):
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(34)
        self.btn_max.clicked.connect(lambda: self.set_value("max"))
        self.btn_min.clicked.connect(lambda: self.set_value("min"))
        layout.addWidget(self.btn_max)
        layout.addWidget(self.btn_min)
        self.set_value("max")

    def set_value(self, value: str):
        self.value = value
        active = f"""
            QPushButton {{
                background: {CYAN};
                color: white;
                border: 1px solid {CYAN};
                border-radius: 11px;
                font: 800 11px "Segoe UI";
            }}
        """
        inactive = f"""
            QPushButton {{
                background: transparent;
                color: {MUTED};
                border: none;
                border-radius: 11px;
                font: 800 11px "Segoe UI";
            }}
            QPushButton:hover {{ color: {TEXT}; }}
        """
        self.btn_max.setChecked(value == "max")
        self.btn_min.setChecked(value == "min")
        self.btn_max.setStyleSheet(active if value == "max" else inactive)
        self.btn_min.setStyleSheet(active if value == "min" else inactive)


class ToggleSwitch(QPushButton):
    def __init__(self, checked: bool = True):
        super().__init__()
        self.setCheckable(True)
        self.setChecked(checked)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(52, 28)
        self.clicked.connect(self.update)
        self.setStyleSheet("QPushButton { border: none; background: transparent; }")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(1, 1, self.width() - 2, self.height() - 2)
        bg = QColor("#1f4967") if self.isChecked() else QColor("#1c3550")
        painter.setBrush(bg)
        painter.setPen(QPen(QColor("#2e5778"), 1))
        painter.drawRoundedRect(rect, 14, 14)
        knob_x = self.width() - 24 if self.isChecked() else 4
        painter.setBrush(QColor("#47e28c") if self.isChecked() else QColor("#d9e0ea"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(knob_x, 4, 20, 20))


class ToggleField(GlassPanel):
    def __init__(self):
        super().__init__(radius=12, fill="#0c2238", fill_alpha=228, border="#255173", border_alpha=190)
        self.setFixedHeight(46)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 8, 10, 8)
        label = QLabel("Exigir valor inteiro")
        label.setStyleSheet(f"color: {TEXT};")
        set_font(label, 11, QFont.Bold)
        layout.addWidget(label)
        layout.addStretch(1)
        layout.addWidget(ToggleSwitch(True))


class NumberField(GlassPanel):
    def __init__(self, value: str = "3"):
        super().__init__(radius=12, fill="#0c2238", fill_alpha=228, border="#255173", border_alpha=190)
        self.setFixedHeight(46)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 8, 12, 8)
        number = QLabel(value)
        number.setStyleSheet(f"color: {TEXT};")
        set_font(number, 15, QFont.Bold)
        markers = QVBoxLayout()
        markers.setSpacing(4)
        for color in (CYAN, YELLOW):
            m = QFrame()
            m.setFixedSize(24, 8)
            m.setStyleSheet(f"background: {color}; border-radius: 4px;")
            markers.addWidget(m)
        layout.addWidget(number)
        layout.addStretch(1)
        layout.addLayout(markers)


class FormField(QWidget):
    def __init__(self, label_text: str, child: QWidget):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(7)
        label = QLabel(label_text)
        label.setStyleSheet(f"color: {TEXT};")
        set_font(label, 10, QFont.Bold)
        layout.addWidget(label)
        layout.addWidget(child)


class CoeffBox(StyledLineEdit):
    def __init__(self, text: str):
        super().__init__(text)
        self.setFixedSize(76, 42)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f"""
            QLineEdit {{
                background: #0d2a47;
                color: {TEXT};
                border: 1px solid #275478;
                border-radius: 11px;
                padding: 0;
                font: 800 12px "Segoe UI";
            }}
            QLineEdit:focus {{ border-color: {CYAN}; }}
        """)


class ExpressionBox(GlassPanel):
    def __init__(self):
        super().__init__(radius=15, fill="#0d2237", fill_alpha=232, border="#235171", border_alpha=180)
        self.setFixedHeight(96)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        z = QLabel("Z =")
        z.setStyleSheet(f"color: {TEXT};")
        set_font(z, 22, QFont.Black)
        layout.addWidget(z)

        sequence = [CoeffBox("3"), "x₁", "+", CoeffBox("2"), "x₂", "+", CoeffBox("1"), "x₃"]
        for item in sequence:
            if isinstance(item, QWidget):
                layout.addWidget(item)
            else:
                label = QLabel(item)
                label.setStyleSheet(f"color: {CYAN if item == '+' else TEXT};")
                set_font(label, 18 if item == "+" else 16, QFont.Bold)
                layout.addWidget(label)
        layout.addStretch(1)
        layout.addWidget(StyledButton("Editar expressão", primary=False, height=44))


class CellLabel(QLabel):
    def __init__(self, text: str, strong: bool = False, pill: bool = False, color: str = TEXT):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f"""
            QLabel {{
                color: {color};
                background: {'#0e2a45' if pill else 'transparent'};
                border: {'1px solid #275478' if pill else 'none'};
                border-radius: {'9px' if pill else '0px'};
                padding: {'4px 8px' if pill else '0px'};
            }}
        """)
        set_font(self, 10, QFont.Bold if strong else QFont.Normal)


class VariablesBox(GlassPanel):
    def __init__(self):
        super().__init__(radius=16, fill="#0d2237", fill_alpha=224, border="#235171", border_alpha=160)
        self.setMinimumHeight(205)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 14)
        layout.setSpacing(9)

        title = QLabel("Variáveis de decisão")
        title.setStyleSheet(f"color: {TEXT};")
        set_font(title, 14, QFont.Bold)
        sub = QLabel("Descrição das variáveis do modelo.")
        sub.setStyleSheet(f"color: {MUTED};")
        set_font(sub, 10)
        layout.addWidget(title)
        layout.addWidget(sub)

        table = GlassPanel(radius=10, fill="#0a2038", fill_alpha=70, border="#235171", border_alpha=130)
        table_l = QVBoxLayout(table)
        table_l.setContentsMargins(0, 0, 0, 0)
        table_l.setSpacing(0)
        layout.addWidget(table, 1)

        header = QHBoxLayout()
        header.setContentsMargins(12, 8, 12, 8)
        for txt, stretch in [("Variável", 1), ("Descrição", 2), ("Condição", 1)]:
            h = CellLabel(txt, True, False, "#b8c7d9")
            header.addWidget(h, stretch)
        table_l.addLayout(header)

        for var, desc, cond in [("x₁", "Tratamento A", "≥ 0"), ("x₂", "Tratamento B", "≥ 0"), ("x₃", "Tratamento C", "≥ 0")]:
            row_wrap = QFrame()
            row_wrap.setFixedHeight(34)
            row_wrap.setStyleSheet("QFrame { border-top: 1px solid rgba(70, 120, 160, 0.26); }")
            row = QHBoxLayout(row_wrap)
            row.setContentsMargins(12, 5, 12, 5)
            row.addWidget(CellLabel(var, True), 1)
            row.addWidget(CellLabel(desc, False, False, MUTED), 2)
            row.addWidget(CellLabel(cond, True, True), 1)
            table_l.addWidget(row_wrap)


class ConstraintsBox(GlassPanel):
    def __init__(self):
        super().__init__(radius=16, fill="#0d2237", fill_alpha=224, border="#235171", border_alpha=160)
        self.setMinimumHeight(205)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 14)
        layout.setSpacing(9)

        head = QHBoxLayout()
        left = QVBoxLayout()
        left.setSpacing(4)
        title = QLabel("Restrições")
        title.setStyleSheet(f"color: {TEXT};")
        set_font(title, 14, QFont.Bold)
        sub = QLabel("Defina coeficientes, sinal e limite de cada restrição.")
        sub.setStyleSheet(f"color: {MUTED};")
        set_font(sub, 10)
        left.addWidget(title)
        left.addWidget(sub)
        add_btn = StyledButton("+ Adicionar restrição", primary=True, height=34)
        add_btn.setFixedWidth(164)
        head.addLayout(left)
        head.addStretch(1)
        head.addWidget(add_btn)
        layout.addLayout(head)

        table = GlassPanel(radius=10, fill="#0a2038", fill_alpha=70, border="#235171", border_alpha=130)
        table_l = QVBoxLayout(table)
        table_l.setContentsMargins(0, 0, 0, 0)
        table_l.setSpacing(0)
        layout.addWidget(table, 1)

        headers = ["x₁", "x₂", "x₃", "Sinal", "Valor", "Ação"]
        stretches = [1, 1, 1, 1, 1, 0]
        header = QHBoxLayout()
        header.setContentsMargins(12, 8, 12, 8)
        for txt, stretch in zip(headers, stretches):
            h = CellLabel(txt, True, False, "#b8c7d9")
            if txt == "Ação":
                h.setFixedWidth(48)
            header.addWidget(h, stretch)
        table_l.addLayout(header)

        rows = [("2", "1", "0", "≤", "8"), ("1", "2", "1", "≥", "6"), ("1", "1", "1", "=", "10")]
        for row_values in rows:
            row_wrap = QFrame()
            row_wrap.setFixedHeight(34)
            row_wrap.setStyleSheet("QFrame { border-top: 1px solid rgba(70, 120, 160, 0.26); }")
            row = QHBoxLayout(row_wrap)
            row.setContentsMargins(12, 4, 12, 4)
            for txt in row_values:
                row.addWidget(CellLabel(txt, True, True), 1)
            x = QLabel("×")
            x.setAlignment(Qt.AlignCenter)
            x.setFixedSize(24, 24)
            x.setStyleSheet("QLabel { color: #bed0df; background: #173d60; border-radius: 12px; }")
            set_font(x, 10, QFont.Bold)
            action_holder = QWidget()
            action_l = QHBoxLayout(action_holder)
            action_l.setContentsMargins(12, 0, 12, 0)
            action_l.addWidget(x, 0, Qt.AlignCenter)
            action_holder.setFixedWidth(48)
            row.addWidget(action_holder, 0)
            table_l.addWidget(row_wrap)


class SummaryPanel(GlassPanel):
    def __init__(self):
        super().__init__(radius=16, fill=PANEL_3, fill_alpha=222, border="#2b5677", border_alpha=175)
        self.setMinimumHeight(220)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 18, 24, 18)
        layout.setSpacing(10)
        title = QLabel("Resumo do modelo")
        title.setStyleSheet(f"color: {TEXT};")
        set_font(title, 16, QFont.Black)
        sub = QLabel("Pré-visualização do problema montado.")
        sub.setStyleSheet(f"color: {MUTED};")
        set_font(sub, 10)
        layout.addWidget(title)
        layout.addWidget(sub)

        box = GlassPanel(radius=14, fill="#10253c", fill_alpha=235, border="#27506f", border_alpha=165)
        box_l = QVBoxLayout(box)
        box_l.setContentsMargins(18, 14, 18, 14)
        box_l.setSpacing(5)
        for txt, color, strong in [
            ("max Z = 3x₁ + 2x₂ + x₃", CYAN, True),
            ("2x₁ + x₂ + 0x₃ ≤ 8", TEXT, False),
            ("x₁ + 2x₂ + x₃ ≥ 6", TEXT, False),
            ("x₁ + x₂ + x₃ = 10 | x ≥ 0 | inteiro", TEXT, False),
        ]:
            lbl = QLabel(txt)
            lbl.setStyleSheet(f"color: {color};")
            set_font(lbl, 10 if strong else 9, QFont.Bold if strong else QFont.Normal)
            box_l.addWidget(lbl)
        layout.addWidget(box, 1)


class BulletItem(QWidget):
    def __init__(self, color: str, text: str):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        dot = QFrame()
        dot.setFixedSize(10, 10)
        dot.setStyleSheet(f"background: {color}; border-radius: 5px;")
        lbl = QLabel(text)
        lbl.setWordWrap(True)
        lbl.setStyleSheet(f"color: {MUTED};")
        set_font(lbl, 10)
        layout.addWidget(dot, 0, Qt.AlignTop)
        layout.addWidget(lbl, 1)


class TipsPanel(GlassPanel):
    def __init__(self):
        super().__init__(radius=16, fill=PANEL_3, fill_alpha=222, border="#2b5677", border_alpha=175)
        self.setMinimumHeight(220)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 18, 24, 18)
        layout.setSpacing(8)
        title = QLabel("Dicas de preenchimento")
        title.setStyleSheet(f"color: {TEXT};")
        set_font(title, 16, QFont.Black)
        sub = QLabel("Campos importantes para evitar erro na apresentação.")
        sub.setStyleSheet(f"color: {MUTED};")
        set_font(sub, 10)
        layout.addWidget(title)
        layout.addWidget(sub)
        layout.addSpacing(3)
        layout.addWidget(BulletItem(CYAN, "Use o sinal correto em cada restrição."))
        layout.addWidget(BulletItem(GREEN, "Mantenha o número de variáveis consistente."))
        layout.addWidget(BulletItem(YELLOW, "Se quiser bonificação, marque solução inteira."))


class CounterBadge(QLabel):
    def __init__(self, number: str, label: str):
        super().__init__(f"  {number}  {label}  ")
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(22)
        self.setStyleSheet(f"""
            QLabel {{
                color: #b7c8d8;
                background: #10263d;
                border: 1px solid #274d6d;
                border-radius: 11px;
                font: 800 10px "Segoe UI";
                padding: 0 8px;
            }}
        """)


class ActionsPanel(GlassPanel):
    def __init__(self):
        super().__init__(radius=16, fill=PANEL_3, fill_alpha=222, border="#2b5677", border_alpha=175)
        self.setMinimumHeight(250)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 18, 24, 16)
        layout.setSpacing(12)
        title = QLabel("Ações")
        title.setStyleSheet(f"color: {TEXT};")
        set_font(title, 16, QFont.Black)
        sub = QLabel("Valide o modelo ou siga para a resolução.")
        sub.setStyleSheet(f"color: {MUTED};")
        set_font(sub, 10)
        layout.addWidget(title)
        layout.addWidget(sub)

        row1 = QHBoxLayout()
        row1.setSpacing(10)
        row1.addWidget(StyledButton("Validar modelo"))
        row1.addWidget(StyledButton("Limpar campos"))

        row2 = QHBoxLayout()
        row2.setSpacing(10)
        row2.addWidget(StyledButton("Salvar rascunho"))
        row2.addWidget(StyledButton("Resolver problema", primary=True))

        badges = QHBoxLayout()
        badges.setSpacing(8)
        badges.addWidget(CounterBadge("3", "variáveis"))
        badges.addWidget(CounterBadge("3", "restrições"))
        badges.addWidget(CounterBadge("1", "objetivo"))
        badges.addStretch(1)

        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addStretch(1)
        layout.addLayout(badges)


class ProblemConfigPanel(GlassPanel):
    def __init__(self):
        super().__init__(radius=18, fill=PANEL_3, fill_alpha=216, border="#285474", border_alpha=178)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 22, 26, 22)
        layout.setSpacing(16)

        title = QLabel("Configuração do problema")
        title.setStyleSheet(f"color: {TEXT};")
        set_font(title, 18, QFont.Bold)
        sub = QLabel("Escolha o tipo de problema e as opções gerais.")
        sub.setStyleSheet(f"color: {MUTED};")
        set_font(sub, 10)
        layout.addWidget(title)
        layout.addWidget(sub)

        top_grid = QGridLayout()
        top_grid.setHorizontalSpacing(16)
        top_grid.setVerticalSpacing(12)
        top_grid.addWidget(FormField("Tipo de problema", SegmentedControl()), 0, 0)
        top_grid.addWidget(FormField("Solução inteira", ToggleField()), 0, 1)
        top_grid.addWidget(FormField("Número de variáveis", NumberField("3")), 0, 2)
        top_grid.addWidget(FormField("Nome do problema", StyledLineEdit("", "Ex.: Modelo radioterápico")), 0, 3)
        top_grid.setColumnStretch(0, 3)
        top_grid.setColumnStretch(1, 3)
        top_grid.setColumnStretch(2, 2)
        top_grid.setColumnStretch(3, 4)
        layout.addLayout(top_grid)

        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background: rgba(110,150,190,0.23);")
        layout.addWidget(divider)

        obj_title = QLabel("Função objetivo")
        obj_title.setStyleSheet(f"color: {TEXT};")
        set_font(obj_title, 16, QFont.Bold)
        obj_sub = QLabel("Informe os coeficientes da função que será otimizada.")
        obj_sub.setStyleSheet(f"color: {MUTED};")
        set_font(obj_sub, 10)
        layout.addWidget(obj_title)
        layout.addWidget(obj_sub)
        layout.addWidget(ExpressionBox())

        bottom = QHBoxLayout()
        bottom.setSpacing(16)
        bottom.addWidget(VariablesBox(), 1)
        bottom.addWidget(ConstraintsBox(), 1.55)
        layout.addLayout(bottom, 1)


class ProblemsPage(QWidget):
    request_navigate = Signal(str)

    def __init__(self):
        super().__init__()

        # Sem título duplicado aqui. O header global já diz onde o usuário está.
        # Isso libera altura útil para o painel e evita corte nas tabelas.
        layout = QHBoxLayout(self)
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(18)

        left = QVBoxLayout()
        left.setContentsMargins(0, 0, 0, 0)
        left.setSpacing(0)
        left.addWidget(ProblemConfigPanel(), 1)
        layout.addLayout(left, 1)

        right_host = QWidget()
        right_host.setFixedWidth(420)
        right_host.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        right = QVBoxLayout(right_host)
        right.setContentsMargins(0, 0, 0, 0)
        right.setSpacing(18)

        # Os três cards da direita agora distribuem toda a altura útil,
        # alinhando o final do bloco com o painel grande da esquerda.
        right.addWidget(SummaryPanel(), 1)
        right.addWidget(TipsPanel(), 1)
        right.addWidget(ActionsPanel(), 1)

        layout.addWidget(right_host)
