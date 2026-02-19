# Pygame Chess
A simple interactive Chess game written using Pygame and python-chess. 

<img width="337" alt="Screenshot 2023-11-09 at 21 11 56" src="https://github.com/Cuberates/pygame-chess/assets/79352883/2cc05c67-60e0-44ce-84cb-5fab125474f3">

# Usage
- It is precisely recommended to install all necessary libraries: `pip3 install chess pygame stockfish`
- The game is powered by [Stockfish](https://stockfishchess.org/). In the source file, initialize the path to the Stockfish binary file. 
```python
# Initialize Stockfish
try:
   stockfish = Stockfish(path="PATH TO STOCKFISH BINARY")
   stockfish_elo = 800
   stockfish_elo = input("Input Stockfish ELO (Default is 800): ")
   # stockfish.update_engine_parameters({"Minimum Thinking Time": 0})
   stockfish.set_elo_rating(stockfish_elo)
except: 
   print("Stockfish path is incorrect")
```
- To run the game: ```python3 pygame-chess.py```

