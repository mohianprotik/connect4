import numpy as np
import random
import pygame
import sys
import math


WHITE = (255,255,255)
BLACK = (35,126,165)
RED = (199, 0, 57)
ORANGE = (255, 195, 0)
ROW_COUNT = 6
col_cnt = 7
PLAYER = 0
MACHINE_AGENT = 1
EMPTY = 0
PLAYER_PIECE = 1
MACHINE_AGENT_PIECE = 2
WINDOW_LENGTH = 4 
is_DRAW = False

def create_board():
	board = np.zeros((ROW_COUNT,col_cnt))
	return board

def is_valid_location(board, col):
	#print(board[ROW_COUNT-1][col] )
	return board[ROW_COUNT-1][col] == 0

def get_valid_locations(board):
	valid_locations = []
	for col in range(col_cnt):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def winning_move(board, piece):
	is_board_full(board)
	for c in range(col_cnt-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True


	for c in range(col_cnt):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	for c in range(col_cnt-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	for c in range(col_cnt-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True
	
def is_board_full(board):
	cnt = 0
	for c in range(col_cnt):
		for r in range(ROW_COUNT):
			
			if board[r][c] == MACHINE_AGENT_PIECE or board[r][c] == PLAYER_PIECE:
				cnt += 1
	#print(cnt)
	if cnt == col_cnt * ROW_COUNT:
		is_DRAW = True	



def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = MACHINE_AGENT_PIECE

	if window.count(piece) == 4:
		score += 60
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 4
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 1

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 3

	return score

def score_position(board, piece):
	score = 0
	center_array = [int(i) for i in list(board[:, col_cnt//2])]
	center_count = center_array.count(piece)
	score += center_count * 4


	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(col_cnt-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	for c in range(col_cnt):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(col_cnt-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(col_cnt-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, MACHINE_AGENT_PIECE) or len(get_valid_locations(board)) == 0

def minmax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, MACHINE_AGENT_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: 
				return (None, 0)
		else: 
			return (None, score_position(board, MACHINE_AGENT_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, MACHINE_AGENT_PIECE)
			new_score = minmax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: 
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minmax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value



def draw_board(board):
	for c in range(col_cnt):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, WHITE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(col_cnt):
		for r in range(ROW_COUNT):		
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == MACHINE_AGENT_PIECE: 
				pygame.draw.circle(screen, ORANGE, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

board = create_board()
game_over = False
pygame.init()

SQUARESIZE = 90
width = (col_cnt * SQUARESIZE ) 
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, MACHINE_AGENT)

while not game_over:

	for event in pygame.event.get():
	
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == PLAYER:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			#print(is_DRAW)
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))
			
				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, PLAYER_PIECE)
				
					if winning_move(board, PLAYER_PIECE):
						label = myfont.render("You win!!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True
					elif is_DRAW == True:
						label = myfont.render("Match Draw", 1, RED)
						screen.blit(label, (40,10))
						game_over = True

					turn += 1
					turn = turn % 2
		
					draw_board(board)

	if turn == MACHINE_AGENT and not game_over:				
		col, minmax_score = minmax(board, 4, -math.inf, math.inf, True)

		if is_valid_location(board, col):
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, MACHINE_AGENT_PIECE)

			if winning_move(board, MACHINE_AGENT_PIECE):
				label = myfont.render("AI win!!", 1, ORANGE)
				screen.blit(label, (40,10))
				game_over = True
			elif is_DRAW == True:
				label = myfont.render("Match Draw", 1, RED)
				screen.blit(label, (40,10))
				game_over = True
				sys.exit()
			#print(is_DRAW)
			draw_board(board)
			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(10000)

