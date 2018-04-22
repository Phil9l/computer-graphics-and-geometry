#!/usr/bin/env python3

import sys

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from PyQt5.QtGui import QColor, QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QComboBox, QLabel, QLineEdit, QWidget, QApplication, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, QPointF, QRect

import config
from config import WIDTH, HEIGHT


def _hex_color_to_float(color):
    r, g, b = color // 256**2, color // 256 % 256, color % 256
    return r / 255, g / 255, b / 255


class MathTextLabel(QWidget):
    def __init__(self, math_text, width, height, background_color=None, text_color=None, parent=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)
        l = QVBoxLayout(self)
        l.setContentsMargins(0, 0, 0, 0)
        if background_color is None:
            r, g, b, a = self.palette().base().color().getRgbF()
            background_color = (r, g, b)
        if text_color is None:
            text_color = 'white'
        self.background_color = background_color
        self.text_color = text_color

        self._figure = Figure(edgecolor=background_color, facecolor=background_color)
        self._canvas = FigureCanvasQTAgg(self._figure)
        l.addWidget(self._canvas)

        self._figure.clear()
        self.text = self._figure.suptitle(
            math_text,
            horizontalalignment='center',
            verticalalignment='top',
            size=14,
            color=self.text_color,
        )
        self._canvas.draw()
        self.setFixedSize(width, height)

    def update(self, text):
        self._figure.clear()
        self.text = self._figure.suptitle(
            text,
            horizontalalignment='center',
            verticalalignment='top',
            size=14,
            color=self.text_color,
        )
        self._canvas.draw()


class Client(QWidget):
    def __init__(self, tasks=()):
        super().__init__()
        self.tasks = tasks
        self.formula = None

        self.axis_pen = QPen()
        self.func_pen = QPen()
        self.coords_pen = QPen()
        self.square_pen = QPen()
        self.last_coords = QPoint(0, 0)

        self.setMouseTracking(True)
        self.axis_pen.setWidth(3)
        self.func_pen.setWidth(3)

        self.axis_pen.setColor(QColor.fromRgb(config.AXIS_COLOR))
        self.func_pen.setColor(QColor.fromRgb(config.FUNCTION_COLOR))
        self.coords_pen.setColor(QColor.fromRgb(config.GRID_COLOR))
        self.square_pen.setColor(QColor.fromRgb(config.HIGHLIGHTED_SQUARE_COLOR))

        self.padding = 0
        self.panelWidth = 200
        self.tracking = False

        self.task_number = 0
        self.steps_count = WIDTH

        self.init_vars()
        self.init_UI()

    @property
    def current_task(self):
        return self.tasks[self.task_number]

    @property
    def step_size(self):
        return (self.g_right_bottom.x() - self.g_left_top.x()) / self.steps_count

    def init_vars(self):
        self.a = 1
        self.b = 1
        self.c = 1
        init_offset = 15

        self.g_left_top = QPoint(-init_offset, -init_offset)
        self.g_right_bottom = QPoint(init_offset, init_offset)

        self.alpha = self.g_left_top.x()
        self.beta = self.g_right_bottom.x()

    def _update_formula(self, text=None):
        if text is None:
            text = ''
        if self.formula is not None:
            self.formula.update(text)

    def init_UI(self):
        self.setGeometry(800 - WIDTH // 2, 450 - HEIGHT // 2, WIDTH, HEIGHT)

        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(config.PALETTE_COLOR))
        self.setPalette(p)

        combo = QComboBox(self)
        combo.addItems(["Task {}".format(i + 1) for i in range(len(self.tasks))])
        combo.move(60, 15)
        combo.activated[str].connect(self.task_selection_handler)

        self.formula = MathTextLabel(
            self.current_task.FORMULA, 180, 60,
            background_color=_hex_color_to_float(config.PALETTE_COLOR),
            parent=self,
        )
        self.formula.setGeometry(10, 270, 140, 80)
        self.parameters = [QLineEdit(self) for _ in range(3)]
        offset = 70

        for i in range(len(self.parameters)):
            self.parameters[i].setGeometry(65, offset + 40 * i, 50, 20)
            self.parameters[i].setText("1")
            label = QLabel(self)
            label.setText("{}    = ".format(chr(i + ord('a'))))
            label.setGeometry(10, offset + 40 * i, 50, 20)
            label.setStyleSheet("color: white")

        self.parameters[0].textChanged.connect(self.update_a_param)
        self.parameters[1].textChanged.connect(self.update_b_param)
        self.parameters[2].textChanged.connect(self.update_c_param)

        label = QLabel(self)
        label.setGeometry(10, offset + 120, 50, 20)
        label.setText("α    = ")
        label.setStyleSheet('color: white')
        self.alpha_field = QLineEdit(self)
        self.alpha_field.setGeometry(65, offset + 120, 50, 20)
        self.alpha_field.setText(str(self.alpha))
        self.alpha_field.textChanged.connect(self.update_alpha_param)

        label = QLabel(self)
        label.setGeometry(10, offset + 160, 50, 20)
        label.setText("β    = ")
        label.setStyleSheet('color: white')
        self.beta_field = QLineEdit(self)
        self.beta_field.setGeometry(65, offset + 160, 50, 20)
        self.beta_field.setText(str(self.beta))
        self.beta_field.textChanged.connect(self.update_beta_param)

        self.right_y_text_field = QLineEdit(self)
        self.right_y_text_field.setGeometry(65, offset + 300, 50, 20)
        self.right_y_text_field.setText(str(self.g_right_bottom.y()))
        self.right_y_text_field.textChanged.connect(self.update_right_y_param)

        self.left_x_text_field = QLineEdit(self)
        self.left_x_text_field.setGeometry(10, offset + 340, 50, 20)
        self.left_x_text_field.setText(str(self.g_left_top.x()))
        self.left_x_text_field.textChanged.connect(self.update_left_x_param)

        self.right_x_text_field = QLineEdit(self)
        self.right_x_text_field.setGeometry(120, offset + 340, 50, 20)
        self.right_x_text_field.setText(str(self.g_right_bottom.x()))
        self.right_x_text_field.textChanged.connect(self.update_right_x_param)

        self.left_y_text_field = QLineEdit(self)
        self.left_y_text_field.setGeometry(65, offset + 380, 50, 20)
        self.left_y_text_field.setText(str(self.g_left_top.y()))
        self.left_y_text_field.textChanged.connect(self.update_left_y_param)

        self.setWindowTitle('Points')
        self.show()

    def task_selection_handler(self, text):
        self.task_number = int(text.split()[-1]) - 1
        self._update_formula(self.current_task.FORMULA)
        self.update()

    def update_left_x_param(self):
        try:
            self.g_left_top.setX(float(self.left_x_text_field.text()))
            self.update()
        except ValueError:
            pass

    def update_left_y_param(self):
        try:
            self.g_left_top.setY(float(self.left_y_text_field.text()))
            self.update()
        except ValueError:
            pass

    def update_right_x_param(self):
        try:
            self.g_right_bottom.setX(float(self.right_x_text_field.text()))
            self.update()
        except ValueError:
            pass

    def update_right_y_param(self):
        try:
            self.g_right_bottom.setY(float(self.right_y_text_field.text()))
            self.update()
        except ValueError:
            pass

    def update_a_param(self):
        try:
            self.a = self.parameters[0].text()
            self.update()
        except ValueError:
            pass

    def update_b_param(self):
        try:
            self.b = self.parameters[0].text()
            self.update()
        except ValueError:
            pass

    def update_c_param(self):
        try:
            self.c = self.parameters[0].text()
            self.update()
        except ValueError:
            pass

    def update_alpha_param(self):
        try:
            self.alpha = self.alpha_field.text()
            self.update()
        except ValueError:
            pass

    def update_beta_param(self):
        try:
            self.beta = self.beta_field.text()
            self.update()
        except ValueError:
            pass

    def left_top(self):
        return QPointF(self.panelWidth, 0)

    def right_bottom(self):
        return QPointF(self.width(), self.height())

    def real_width(self):
        return self.right_bottom().x() - self.left_top().x()

    def real_height(self):
        return self.right_bottom().y() - self.left_top().y()

    def g_width(self):
        return self.g_right_bottom.x() - self.g_left_top.x()

    def g_height(self):
        return self.g_right_bottom.y() - self.g_left_top.y()

    def get_x_scale(self):
        if self.g_width() == 0:
            return self.real_width()
        return self.real_width() / self.g_width()

    def get_y_scale(self):
        if self.g_height() == 0:
            return self.real_height()
        return self.real_height() / self.g_height()

    def get_real_coord(self, t_coords):
        relative_t_coords = t_coords - self.g_left_top
        relative_real_coords = QPointF(relative_t_coords.x() * self.get_x_scale(),
                                       self.real_height() - relative_t_coords.y() * self.get_y_scale())
        return relative_real_coords + self.left_top()

    def draw_grid(self, qp, *args):
        qp.setPen(self.axis_pen)
        p0 = self.get_real_coord(QPointF(self.g_left_top.x(), 0))
        p1 = self.get_real_coord(QPointF(self.g_right_bottom.x(), 0))
        p2 = self.get_real_coord(QPointF(0, self.g_left_top.y()))
        p3 = self.get_real_coord(QPointF(0, self.g_right_bottom.y()))

        if self.g_left_top.y() < 0:
            qp.drawLine(p0, p1)

        if self.g_left_top.x() < 0:
            qp.drawLine(p2, p3)
        qp.setPen(self.coords_pen)

        for i in range(int(self.g_left_top.x()), int(self.g_right_bottom.x() + 1)):
            p1 = self.get_real_coord(QPointF(i, self.g_right_bottom.y()))
            p0 = self.get_real_coord(QPointF(i, self.g_left_top.y()))
            if p0.x() > self.left_top().x():
                qp.drawLine(p0, p1)

        for i in range(int(self.g_left_top.y()), int(self.g_right_bottom.y() + 1)):
            p1 = self.get_real_coord(QPointF(self.g_right_bottom.x(), i))
            p0 = self.get_real_coord(QPointF(self.g_left_top.x(), i))
            qp.drawLine(p0, p1)

    def _highlight_squares(self, qp, *args):
        qp.setBrush(QColor.fromRgb(config.HIGHLIGHTED_SQUARE_BACKGROUND_COLOR))
        qp.setPen(self.square_pen)
        func = self.current_task
        for state in func.plot_all(self.step_size, self.steps_count, self.g_left_top.x(), self.alpha, self.beta, *args):
            p0 = state.x // 1, state.y // 1
            cp = self.get_real_coord(QPointF(*p0))
            qp.drawRect(cp.x(), cp.y() - self.get_y_scale(), self.get_x_scale(), self.get_y_scale())

    def draw_func(self, qp, *args):
        if self.current_task.HIGHLIGHT_SQUARES:
            self._highlight_squares(qp, *args)
        func = self.current_task
        qp.setPen(self.func_pen)
        qp.setBrush(QColor.fromRgb(config.BACKGROUND_COLOR))

        prev_point = None
        for state in func.plot_all(self.step_size, self.steps_count, self.g_left_top.x(), self.alpha, self.beta, *args):
            self.func_pen.setColor(QColor.fromRgb(state.color))
            qp.setPen(self.func_pen)

            current_point = self.get_real_coord(QPointF(state.x, state.y))
            if state.need_line and prev_point is not None and abs(
                            current_point.y() - prev_point.y()) < self.real_height() * 8:
                qp.drawLine(prev_point, current_point)
            prev_point = current_point

    def paintEvent(self, _):
        try:
            self.b = self.parameters[1].text()
        except ValueError:
            pass
        try:
            self.c = self.parameters[2].text()
        except ValueError:
            pass

        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor.fromRgb(config.BACKGROUND_COLOR))
        qp.setBrush(QColor.fromRgb(config.BACKGROUND_COLOR))
        qp.drawRect(self.left_top().x(), self.left_top().y(), self.real_width(), self.real_height())
        self.draw_grid(qp)

        self.draw_func(qp, self.a, self.b, self.c)
        qp.end()
