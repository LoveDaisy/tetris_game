#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tetris_model import BOARD_DATA, Shape
import math
from datetime import datetime
import numpy as np


class TetrisAI(object):

    def nextMove(self):
        t1 = datetime.now()
        if BOARD_DATA.currentShape == Shape.shapeNone:
            return None

        currentDirection = BOARD_DATA.currentDirection
        currentY = BOARD_DATA.currentY
        _, _, minY, _ = BOARD_DATA.nextShape.getBoundingOffsets(0)
        nextY = -minY

        strategy = None
        for d0 in range(4):
            minX, maxX, _, _ = BOARD_DATA.currentShape.getBoundingOffsets(d0)
            for x0 in range(-minX, BOARD_DATA.width - maxX):
                for d1 in range(4):
                    minX, maxX, _, _ = BOARD_DATA.nextShape.getBoundingOffsets(d1)
                    for x1 in range(-minX, BOARD_DATA.width - maxX):
                        score = self.calculateScore(d0, x0, d1, x1)
                        if not strategy or strategy[2] < score:
                            strategy = (d0, x0, score)
        print(datetime.now() - t1)
        return strategy

    def dropDown(self, data, shape, direction, x0):
        dy = BOARD_DATA.height - 1
        for x, y in shape.getCoords(direction, x0, 0):
            yy = 0
            while yy + y < BOARD_DATA.height and (yy + y < 0 or data[(y + yy), x] == Shape.shapeNone):
                yy += 1
            yy -= 1
            if yy < dy:
                dy = yy
        for x, y in shape.getCoords(direction, x0, 0):
            data[(y + dy), x] = shape.shape

    def calculateScore(self, d0, x0, d1, x1):
        # print("calculateScore")
        t1 = datetime.now()
        width = BOARD_DATA.width
        height = BOARD_DATA.height

        board = np.array(BOARD_DATA.getData()).reshape((BOARD_DATA.height, BOARD_DATA.width))
        
        self.dropDown(board, BOARD_DATA.currentShape, d0, x0)
        self.dropDown(board, BOARD_DATA.nextShape, d1, x1)
        # print(datetime.now() - t1)

        # Term 2: max height
        maxHeight = 0
        roofY = []
        for x in range(width):
            y = 0
            while y < height and board[y, x] == Shape.shapeNone:
                y += 1
            roofY.append(height - y)
            if height - y > maxHeight:
                maxHeight = height - y
        # print(datetime.now() - t1)

        # Term 1: lines to be removed
        fullLines, nearFullLines = 0, 0
        for y in range(height - 1, height - maxHeight, -1):
            tmpCounts = 0
            for x in range(width):
                if board[y, x] != Shape.shapeNone:
                    tmpCounts += 1
            if tmpCounts == width:
                fullLines += 1
            if tmpCounts == width - 1:
                nearFullLines += 1
        maxHeight -= fullLines
        # print(datetime.now() - t1)

        # Term 3: vertical holes
        vHoles, vHoleFlag = 0, False
        vBlocks = 0
        for x in range(width):
            tmpHoles = 0
            vHoleFlag = False
            for y in range(height - 1, 0, -1):
                if board[y, x] == Shape.shapeNone:
                    tmpHoles += 1
                    vHoleFlag = True
                else:
                    if tmpHoles > 0:
                        vHoles += tmpHoles
                        tmpHoles = 0
                    if vHoleFlag:
                        vBlocks += 1
        # print(datetime.now() - t1)

        # Term 5: roof roughness
        roofDy = [roofY[i] - roofY[i+1] for i in range(len(roofY) - 1)]

        stdY = math.sqrt(sum([y ** 2 for y in roofY]) / len(roofY) - (sum(roofY) / len(roofY)) ** 2)
        stdDY = math.sqrt(sum([y ** 2 for y in roofDy]) / len(roofDy) - (sum(roofDy) / len(roofDy)) ** 2)

        absDy = sum([abs(x) for x in roofDy])
        # print(datetime.now() - t1)

        return fullLines * 3 + nearFullLines * 1.4 - vHoles ** 2 * 0.5 - vBlocks * 0.1 - maxHeight * 0.05 \
            - stdY * 0.0 - stdDY * 0.05 - absDy * 0.2


TETRIS_AI = TetrisAI()

