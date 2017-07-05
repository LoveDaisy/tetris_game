# Tetris Game

It is a python implementatino of Tetris Game, and a simple AI to play game automatically.

Need python3 and PyQt5 to be installed.

* `tetris_game.py` is the main application.
* `tetris_model.py` is the data model for this game.
* `tetris_ai.py` is the AI part.

### Play manually

If you want play by yourself, you should uncomment this line in `tetris_game.py`:

```python
# TETRIS_AI = None
```

Or just comment this line:

```python
from tetris_ai import TETRIS_AI
```

### Play rules

Just like classical Tetris Game. You use *up* key to rotate a shape, *left* key to move left and *right* key to move right. Also you can use *space* key to drop down current shape immediately. If you want a pause, just press *P* key. The right panel shows the next shape.

~ HAVE FUN ~

![Screenshot](doc/pics/screenshot_01.png)