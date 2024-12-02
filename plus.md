1.Restart Functionality

Pressing the R key resets the game.
The game board is cleared, and a new Tetris piece is spawned.

2.Game Over State Handling

The game now detects when the player has lost(Game Over).
When the game is over, a "Game Over!" message is displayed on the screen in red.
During the Game Over state, all controls except the restart (R) key are disabled.
Add gameOver method to detect game over condition in model.py