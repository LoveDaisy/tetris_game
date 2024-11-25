# 게임 오버 상태 체크
if BOARD_DATA.gameOver():
    self.gameOver()

# 게임 오버 처리
def gameOver(self):
    self.tboard.msg2Statusbar.emit("Game Over! Press R to Restart.")
    self.isPaused = True
    self.timer.stop()

# 키 입력 처리
def keyPressEvent(self, event):
    if self.isPaused and event.key() == Qt.Key_R:  # 게임 오버 상태에서만 R 키 활성화
        self.restartGame()
    else:
        super(Tetris, self).keyPressEvent(event)

# 게임 재시작
def restartGame(self):
    self.isPaused = False
    self.tboard.initBoard()  # 보드 데이터 초기화
    self.start()  # 게임 재시작
