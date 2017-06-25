#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tetris_model import BoardData, Shape
import math


class TetrisAI(object):
    def __init__(self, boardData):
        self.boardData = boardData

    def nextMove(self):
        if self.boardData.currentShape == Shape.shapeNone:
            return None

        d0 = self.boardData.currentDirection
        y0 = self.boardData.currentY

        strategy = None
        for d in range(4):
            tmpDirection = (d0 + d) % 4
            for x in range(BoardData.width):
                if not self.boardData.tryMove(tmpDirection, x, y0):
                    continue
                
                score = self.calculateScore(tmpDirection, x)
                if not strategy or strategy[2] < score:
                    strategy = (tmpDirection, x, score)

        return strategy

    def calculateScore(self, direction, x0):
        width = BoardData.width
        height = BoardData.height

        y = self.boardData.currentY
        while self.boardData.tryMove(direction, x0, y + 1):
            y += 1

        board = self.boardData.getData()
        for x, y in self.boardData.currentShape.getCoords(direction, x0, y):
            board[x + y * width] = self.boardData.currentShape.shape

        # Term 1: lines to be removed
        fullLines, nearFullLines = 0, 0
        for y in range(height - 1, -1, -1):
            tmpCounts = 0
            for x in range(width):
                if board[x + y * width] != Shape.shapeNone:
                    tmpCounts += 1
            if tmpCounts == width:
                fullLines += 1
            if tmpCounts == width - 1:
                nearFullLines += 1

        # Term 2: max height
        maxHeight = 0
        for x in range(width):
            y = 0
            while y < height and board[x + y * width] == Shape.shapeNone:
                y += 1
            if height - y > maxHeight:
                maxHeight = height - y
        maxHeight -= fullLines

        # Term 3: vertical holes
        vHoles, vHoleFlag = 0, False
        vBlocks = 0
        for x in range(width):
            tmpHoles = 0
            vHoleFlag = False
            for y in range(height - 1, 0, -1):
                if board[x + y * width] == Shape.shapeNone:
                    tmpHoles += 1
                    vHoleFlag = True
                else:
                    if tmpHoles > 0:
                        vHoles += tmpHoles
                        tmpHoles = 0
                    if vHoleFlag:
                        vBlocks += 1

        # Term 4: horizontal holes
        hHoles = 0
        for y in range(height - 1, -1, -1):
            tmpHoles = 0
            for x in range(width):
                if board[x + y * width] == Shape.shapeNone:
                    tmpHoles += 1
                else:
                    if tmpHoles > 0 and tmpHoles < 3:
                        hHoles += tmpHoles
                        tmpHoles = 0
            if tmpHoles > 0 and tmpHoles < 3:
                hHoles += tmpHoles

        # Term 5: roof roughness
        roofY = []
        for x in range(width):
            y = 0
            while y < height and board[x + y * width] == Shape.shapeNone:
                y += 1
            roofY.append(height - y)
        roofDy = [roofY[i] - roofY[i+1] for i in range(len(roofY) - 1)]

        stdY = math.sqrt(sum([y ** 2 for y in roofY]) / len(roofY) - (sum(roofY) / len(roofY)) ** 2)
        stdDY = math.sqrt(sum([y ** 2 for y in roofDy]) / len(roofDy) - (sum(roofDy) / len(roofDy)) ** 2)

        absDy = sum([abs(x) for x in roofDy])

        return fullLines * 3 + nearFullLines * 1.4 - vHoles * 1.8 - hHoles * 0.0 - vBlocks * 0.1 - maxHeight * 0.05 \
            - stdY * 0.0 - stdDY * 0.05 - absDy * 0.2

