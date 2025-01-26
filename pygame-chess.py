import chess
import pygame
import random
import time
from stockfish import Stockfish
import math

# Intialize Pygame instances
pygame.init()
pygame.display.set_caption('pygame-chess')

board = chess.Board()
board_color = [(118,150,86), (238,238,210), (188, 203, 74), (245, 245, 138)]
board_size = 60 * 8
buffer = []
square_size = board_size / 8
screen = pygame.display.set_mode((board_size, board_size))
game_clock = pygame.time.Clock()

def get_coordinate_from_index(board_index) -> (int, int): 
   row = math.ceil(board_index / 8)
   col = board_index - ((row - 1) * 8) 
   return (row - 1, col - 1)

def show_piece(current_piece, row, col):
   current_piece_path = "resources/pieces/"
   if current_piece.symbol().islower(): current_piece_path = current_piece_path + current_piece.symbol()
   else: current_piece_path = current_piece_path + 'w' + current_piece.symbol().lower()
   current_piece_path = current_piece_path + ".png"
   current_piece_png = pygame.image.load(current_piece_path)
   current_piece_png = pygame.transform.scale(current_piece_png, (square_size, square_size))
   screen.blit(current_piece_png, (col * square_size, row * square_size))

def render_piece():
   for board_index in range(0, 64):
      current_piece = board.piece_at(board_index)
      current_square = get_coordinate_from_index(board_index + 1)
      row, col = current_square[0], current_square[1]
      if (current_piece != None): show_piece(current_piece, 7-row, col)
      
def highlight_square(row, col): 
   pygame.draw.rect(screen, board_color[((row + col) % 2 == 0)+ 2], 
   pygame.Rect(col * square_size, row * square_size, square_size, square_size))
   # current_piece = board.piece_at((7 - row) * 8 + col)
   current_piece = board.piece_at((7-row) * 8 + col)
   if(current_piece != None): show_piece(current_piece, row, col) 

def make_move (move_uci):
   board.push_uci(move_uci)
   render_board()
   render_piece()


def computer_move():
   current_fen = str(board.fen())
   stockfish.set_fen_position(current_fen)
   top_moves = stockfish.get_top_moves(1)
   choose_move = random.choice(top_moves)
   make_move(choose_move['Move']) 
   if board.turn: print("White: ", end="")
   else: print("Black: ", end="")
   print(choose_move, "Evaluation:", end="")
   if(choose_move['Centipawn'] != None): print(choose_move['Centipawn'] / 100)
   else: print('-')

def render_board(): 
   for board_index in range(0, 64):
      current_square = get_coordinate_from_index(board_index + 1)
      row, col = current_square[0], current_square[1]
      pygame.draw.rect(screen, board_color[(row + col) % 2 == 0], 
                       pygame.Rect(col * square_size, row * square_size, square_size, square_size)) 
def main():
   game_running = True
   while game_running == True:
      # random_move() 
      pygame.display.flip()  
      pos = pygame.mouse.get_pos()
      row, col = math.floor(pos[1] / square_size), math.floor(pos[0] / square_size)
      square_uci = chr(col+ord('a'))+chr((8-row)+ord('0'))
      piece = board.piece_at((7 - row) * 8 + col)
      if piece != None: 
         pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
         # Highlight the square
      else: pygame.mouse.set_cursor()
      for event in pygame.event.get(): 
         if event.type == pygame.QUIT: 
            game_running = False
         if event.type == pygame.MOUSEBUTTONDOWN:
            if piece != None:
               highlight_square(row, col)
               # We also want to highlight all possible moves the piece can make
               for move in board.legal_moves: 
                  query = move.uci()[0:2:1]
                  if square_uci == query: 
                     # print(move.uci()[2:4:1])
                     good_square = move.uci()[2:4:1]
                     r = ord(good_square[1]) - ord('1')
                     c = ord(good_square[0]) - ord('a')
                     # pygame.draw.rect(screen, board_color[((r + c) % 2 == 0) + 2], 
                     # pygame.Rect(c * square_size, (7-r) * square_size, square_size, square_size))
                     highlight_square(7-r, c)
            if piece or len(buffer) >= 1: buffer.append(square_uci)
            # print(buffer)
            if(len(buffer) >= 2): 
               try: 
                  make_move(buffer[0]+buffer[1])
                  pygame.display.flip()
                  computer_move()
               except: 
                  print("Illegal Move")
                  render_board()
                  render_piece()
                  pygame.display.flip()
               buffer.clear()
      if board.outcome() != None: 
         board.set_fen(chess.STARTING_FEN)
         time.sleep(3)
      game_clock.tick(60)
   pygame.quit()
render_board() 
render_piece() 

# Initialize Stockfish
try:
   stockfish = Stockfish(path="PATH TO STOCKFISH BINARY")
   stockfish_elo = 800
   stockfish_elo = input("Input Stockfish ELO (Default is 800): ")
   # stockfish.update_engine_parameters({"Minimum Thinking Time": 0})
   stockfish.set_elo_rating(stockfish_elo)
except: 
   print("Stockfish path is incorrect")
if __name__ == "__main__": 
   main()
