## calls to `minesweeper.py` in runner

initialize game and ai
```python
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
```

### ai game-play
The ai will play a round (reveal a square) if the user clicks on ai-play btn
` ai.make_safe_move()` will return a safe move or `None`; if no safe moves  `ai.make_random_move()`

### regular user round
```python
   if move:
        if game.is_mine(move):
            lost = True
        else:
            nearby = game.nearby_mines(move)
            revealed.add(move)
            ai.add_knowledge(move, nearby)
```

## about minesweeper

### Class Minesweeper
- initializes data for a board with params ` (height=8, width=8, mines=8)` and places the mine count(`mines`) at random coordinates.

- methods
    - `is_mine(self,cell)`: returns whether cell is a mine 
    - and `nearby_mines(self, cell)`: returns number to be revealed in cell.

    - `won(self)`:  checks if all mines have been correctly flagged

### Class Sentences
sentences are stored as items in `MinesweeperAI.knowledge` list, wich is a property of an instance of `MinesweeperAI`. Each time there is new information, `MinesweeperAi` will ask each `sentence` in `knowledge` to update internally.