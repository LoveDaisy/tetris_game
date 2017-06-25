#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, random
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor

from tetris_model import BoardData, Shape
from tetris_ai import TetrisAI


class Tetris(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)

        self.statusbar = self.statusBar()
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        self.tboard.start()

        self.resize(200, 440)
        self.center()
        self.setWindowTitle('Tetris')
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


class Board(QFrame):
    msg2Statusbar = pyqtSignal(str)
    boardData = BoardData()
    speed = 10

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()
        self.ai = TetrisAI(Board.boardData)

    def initBoard(self):
        self.timer = QBasicTimer()
        # self.isWaitingAfterLine = False

        self.score = 0

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.boardData.clear()

    def start(self):
        if self.isPaused:
            return

        self.isStarted = True
        # self.isWaitingAfterLine = False
        self.score = 0
        self.boardData.clear()

        self.msg2Statusbar.emit(str(self.score))

        self.boardData.createNewPiece()
        self.timer.start(Board.speed, self)

    def pause(self):
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.msg2Statusbar.emit("paused")
        else:
            self.timer.start(Board.speed, self)

        self.updateData()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.ai:
                nextMove = self.ai.nextMove()
                if nextMove:
                    k = 0
                    while self.boardData.currentDirection != nextMove[0] and k < 4:
                        self.boardData.rotateRight()
                        k += 1
                    k = 0
                    while self.boardData.currentX != nextMove[1] and k < 5:
                        if self.boardData.currentX > nextMove[1]:
                            self.boardData.moveLeft()
                        else:
                            self.boardData.moveRight()
                        k += 1
                    self.score += self.boardData.dropDown()
                    # self.score += self.boardData.moveDown()
            else:
                self.score += self.boardData.moveDown()
            self.updateData()
        else:
            super(Board, self).timerEvent(event)
        print("score: {0}".format(self.score))

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()

        # Draw backboard
        for x in range(BoardData.width):
            for y in range(BoardData.height):
                val = Board.boardData.getValue(x, y)
                self.drawSquare(painter, x, y, val)

        # Draw current shape
        for x, y in Board.boardData.getCurrentShapeCoord():
            val = Board.boardData.currentShape.shape
            self.drawSquare(painter, x, y, val)

    def squareWidth(self):
        return self.contentsRect().width() // BoardData.width

    def squareHeight(self):
        return self.contentsRect().height() // BoardData.height

    def drawSquare(self, painter, x, y, val):
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        if val == 0:
            return

        dx = self.squareWidth()
        dy = self.squareHeight()
        x *= dx
        y *= dy

        color = QColor(colorTable[val])
        painter.fillRect(x + 1, y + 1, dx - 2, dy - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + dy - 1, x, y)
        painter.drawLine(x, y, x + dx - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + dy - 1, x + dx - 1, y + dy - 1)
        painter.drawLine(x + dx - 1, y + dy - 1, x + dx - 1, y + 1)

    def keyPressEvent(self, event):
        
        if not self.isStarted or self.boardData.currentShape == Shape.shapeNone:
            super(Board, self).keyPressEvent(event)
            return

        key = event.key()
        
        if key == Qt.Key_P:
            self.pause()
            return
            
        if self.isPaused:
            return
        elif key == Qt.Key_Left:
            self.boardData.moveLeft()
        elif key == Qt.Key_Right:
            self.boardData.moveRight()
        elif key == Qt.Key_Down:
            self.boardData.rotateRight()
        elif key == Qt.Key_Up:
            self.boardData.rotateLeft()
        elif key == Qt.Key_Space:
            self.score += self.boardData.dropDown()
        else:
            super(Board, self).keyPressEvent(event)

        self.updateData()

    def updateData(self):
        self.msg2Statusbar.emit(str(self.score))
        self.update()


if __name__ == '__main__':
    random.seed(32)
    app = QApplication([])
    tetris = Tetris()
    sys.exit(app.exec_())
