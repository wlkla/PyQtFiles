import configparser
import math
from typing import Union
from random import random
from qframelesswindow import TitleBar
from qfluentwidgets.common.icon import toQIcon
from PyQt5.QtGui import QPainter, QColor, QIcon, QPainterPath
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect, QLabel
from qfluentwidgets import FluentIconBase, IconWidget, FluentStyleSheet
from PyQt5.QtCore import QRectF, QSize, QEvent, QRect, pyqtProperty, QPropertyAnimation, QEasingCurve, QObject, \
    pyqtSignal, Qt


def getDistance(p1, p2):
    return math.pow(p1.x - p2.x, 2) + math.pow(p1.y - p2.y, 2)


def findClose(points):
    plen = len(points)
    for i in range(plen):
        closest = [None, None, None, None, None]
        p1 = points[i]
        for j in range(plen):
            p2 = points[j]
            dte1 = getDistance(p1, p2)
            if p1 != p2:
                placed = False
                for k in range(5):
                    if not placed:
                        if not closest[k]:
                            closest[k] = p2
                            placed = True
                for k in range(5):
                    if not placed:
                        if dte1 < getDistance(p1, closest[k]):
                            closest[k] = p2
                            placed = True
        p1.closest = closest


class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Point(QObject):
    valueChanged = pyqtSignal(int)

    def __init__(self, x, ox, y, oy, *args, **kwargs):
        super(Point, self).__init__(*args, **kwargs)
        self.__x = x
        self._x = x
        self.originX = ox
        self._y = y
        self.__y = y
        self.originY = oy
        self.closest = [0, 0, 0, 0, 0]
        self.radius = 2 + random() * 2
        config = configparser.ConfigParser()
        config.read('./config.ini', encoding='utf-8')
        line_color = config.get('Settings', 'line_color')
        circle_color = config.get('Settings', 'circle_color')
        self.lineColor = QColor(*eval(line_color))
        self.circleColor = QColor(*eval(circle_color))

    def initAnimation(self):
        if not hasattr(self, 'xanimation'):
            self.xanimation = QPropertyAnimation(self, b'x', self, easingCurve=QEasingCurve.InOutSine)  # type: ignore
            self.xanimation.valueChanged.connect(self.valueChanged.emit)  # type: ignore
            self.yanimation = QPropertyAnimation(self, b'y', self, easingCurve=QEasingCurve.InOutSine)  # type: ignore
            self.yanimation.valueChanged.connect(self.valueChanged.emit)  # type: ignore
            self.yanimation.finished.connect(self.updateAnimation)  # type: ignore
            self.updateAnimation()

    def updateAnimation(self):
        self.xanimation.stop()
        self.yanimation.stop()
        duration = (1 + random()) * 1000
        self.xanimation.setDuration(int(duration))
        self.yanimation.setDuration(int(duration))
        self.xanimation.setStartValue(self.__x)
        self.xanimation.setEndValue(self.originX - 50 + random() * 100)
        self.yanimation.setStartValue(self.__y)
        self.yanimation.setEndValue(self.originY - 50 + random() * 100)
        self.xanimation.start()
        self.yanimation.start()

    @pyqtProperty(float)
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @pyqtProperty(float)
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y


class SplashScreen(QWidget):
    def __init__(self, icon: Union[str, QIcon, FluentIconBase], app_name, record_text, parent=None, enableShadow=True):
        super().__init__(parent=parent)
        self.resize(1100, 750)
        self.setMouseTracking(True)
        self.points = []
        self.target = Target(self.width() / 2, self.height() / 2)
        self.initPoints()
        self._icon = icon
        self._iconSize = QSize(96, 96)

        self.titleBar = TitleBar(self)
        self.iconWidget = IconWidget(icon, self)
        self.shadowEffect = QGraphicsDropShadowEffect(self)

        self.iconWidget.setFixedSize(self._iconSize)
        self.shadowEffect.setColor(QColor(0, 0, 0, 50))
        self.shadowEffect.setBlurRadius(15)
        self.shadowEffect.setOffset(0, 4)

        self.softwareNameLabel = QLabel(app_name, self)
        self.softwareNameLabel.setGeometry(QRect(0, 160, 1100, 100))
        self.softwareNameLabel.setStyleSheet('font: 30pt "隶书";')
        self.softwareNameLabel.setAlignment(Qt.AlignCenter)

        self.recordLabel = QLabel(record_text, self)
        self.recordLabel.setGeometry(QRect(0, 500, 1100, 100))
        self.recordLabel.setStyleSheet('font: 14pt "隶书";')
        self.recordLabel.setAlignment(Qt.AlignCenter)

        FluentStyleSheet.FLUENT_WINDOW.apply(self.titleBar)

        if enableShadow:
            self.iconWidget.setGraphicsEffect(self.shadowEffect)

        if parent:
            parent.installEventFilter(self)

    def update(self, *args):
        super(SplashScreen, self).update()

    def setIcon(self, icon: Union[str, QIcon, FluentIconBase]):
        self._icon = icon
        self.update()

    def icon(self):
        return toQIcon(self._icon)

    def setIconSize(self, size: QSize):
        self._iconSize = size
        self.iconWidget.setFixedSize(size)
        self.update()

    def iconSize(self):
        return self._iconSize

    def setTitleBar(self, titleBar: QWidget):
        self.titleBar.deleteLater()
        self.titleBar = titleBar
        titleBar.setParent(self)
        titleBar.raise_()
        self.titleBar.resize(self.width(), self.titleBar.height())

    def eventFilter(self, obj, e: QEvent):
        if obj is self.parent():
            if e.type() == QEvent.Resize:
                self.resize(e.size())
            elif e.type() == QEvent.ChildAdded:
                self.raise_()

        return super().eventFilter(obj, e)

    def resizeEvent(self, e):
        iw, ih = self.iconSize().width(), self.iconSize().height()
        self.iconWidget.move(self.width() // 2 - iw // 2, self.height() // 2 - ih // 2)
        self.titleBar.resize(self.width(), self.titleBar.height())

    def finish(self):
        self.close()

    def paintEvent(self, e):
        super(SplashScreen, self).paintEvent(e)
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.white)
        self.animate(painter)
        painter.end()

    def mouseMoveEvent(self, event):
        super(SplashScreen, self).mouseMoveEvent(event)
        self.target.x = event.x()
        self.target.y = event.y()
        self.update()

    def initPoints(self):
        self.points.clear()
        stepX = self.width() / 20
        stepY = self.height() / 20
        for x in range(0, self.width(), int(stepX)):
            for y in range(0, self.height(), int(stepY)):
                ox = x + random() * stepX
                oy = y + random() * stepY
                point = Point(ox, ox, oy, oy)
                point.valueChanged.connect(self.update)  # type: ignore
                self.points.append(point)
        findClose(self.points)

    def animate(self, painter):
        for p in self.points:
            value = abs(getDistance(self.target, p))
            if value < 4000:
                p.lineColor.setAlphaF(0.3)
                p.circleColor.setAlphaF(0.6)
            elif value < 20000:
                p.lineColor.setAlphaF(0.1)
                p.circleColor.setAlphaF(0.3)
            elif value < 40000:
                p.lineColor.setAlphaF(0.02)
                p.circleColor.setAlphaF(0.1)
            else:
                p.lineColor.setAlphaF(0)
                p.circleColor.setAlphaF(0)

            if p.lineColor.alpha():
                for pc in p.closest:
                    if not pc:
                        continue
                    path = QPainterPath()
                    path.moveTo(p.x, p.y)
                    path.lineTo(pc.x, pc.y)
                    painter.save()
                    painter.setPen(p.lineColor)
                    painter.drawPath(path)
                    painter.restore()
            painter.save()
            painter.setPen(Qt.NoPen)
            painter.setBrush(p.circleColor)
            painter.drawRoundedRect(QRectF(
                p.x - p.radius, p.y - p.radius, 2 * p.radius, 2 * p.radius), p.radius, p.radius)
            painter.restore()
            p.initAnimation()
