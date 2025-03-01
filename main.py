import random
import pygame

class Rect:
	def __init__(self, x, y, index):
		self.rect = pygame.Rect(x, y, 70, 70)
		self.index = index
		self.active = True

		self.bgcolor = (32, 33, 36)
		self.color = (255, 255, 255)
		self.text = ''
		self.font = pygame.font.Font('Fonts/PAPYRUS.ttf', 25)
		self.image = self.font.render(self.text, True, self.color)

	def update(self, win):
		if self.active:
			pygame.draw.rect(win, self.color, self.rect, 2, border_radius=5)
		else:
			pygame.draw.rect(win, self.bgcolor, self.rect, border_radius=5)
			pygame.draw.rect(win, self.color, self.rect, 2, border_radius=5)

		self.image = self.font.render(self.text, True, self.color)
		x = self.rect.centerx - self.image.get_width() // 2
		y = self.rect.centery - self.image.get_height() // 2
		win.blit(self.image, (x, y))


def create_board():
	return ['#'] + [' ' for i in range(9)]

def generate_boxes():
	box_list = []
	for i in range(9):
		r = i // 3
		c = i % 3
		x = 20 + 70 * c + 16
		y = 220 + 70 * r + 16
		box = Rect(x, y, i)
		box_list.append(box)

	return box_list

def check_space(cell):
	return cell == ' '

def isBoardFull(board):
	for cell in board:
		if check_space(cell):
			return False

	return True

def check_win(board, mark):
	if (board[1] == board[2] == board[3] == mark):
		value = (True, '123')
	elif (board[4] == board[5] == board[6] == mark):
		value = (True, '456')
	elif (board[7] == board[8] == board[9] == mark):
		value = (True, '789')
	elif (board[7] == board[4] == board[1] == mark):
		value = (True, '147')
	elif (board[8] == board[5] == board[2] == mark):
		value = (True, '258')
	elif (board[9] == board[6] == board[3] == mark):
		value = (True, '369')
	elif (board[1] == board[5] == board[9] == mark):
		value = (True, '159')
	elif (board[3] == board[5] == board[7] == mark):
		value = (True, '357')
	else:
		value = (False, -1)

	return value

pygame.init()
SCREEN = WIDTH, HEIGHT = (288, 512)

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 60

WHITE = (225,225,225)
BLACK = (0, 0, 0)
GRAY = (32, 33, 36)
GRAY1 = (105, 105, 105)
GREY2 = (192, 192, 192)

bg1 = pygame.image.load('Image/bg1.png')
bg1 = pygame.transform.scale(bg1, (WIDTH, HEIGHT-10))

bg2 = pygame.image.load('Image/bg2.png')
bg2 = pygame.transform.scale(bg2, (WIDTH, HEIGHT-10))

replay_image = pygame.image.load('Image/replay.png')
replay_image = pygame.transform.scale(replay_image, (36, 36))
replay_rect = replay_image.get_rect()
replay_rect.x = WIDTH - 110
replay_rect.y = 210


board = create_board()
box_list = generate_boxes()
players = ['X', 'O']
current_player = random.randint(0, 1)
text = players[current_player]


scoreX = 0
scoreO = 0

font1 = pygame.font.Font('Fonts/PAPYRUS.ttf', 17)
font2 = pygame.font.Font('Fonts/CHILLER.ttf', 30)
font3 = pygame.font.Font('Fonts/CHILLER.ttf', 40)

tic_tac_toe = font2.render('Tic Tac Toe', True, WHITE)


result = None
line_pos = None
click_pos = None

running = True
while running:
	if result:
		win.blit(bg2, (0,5))
	else:
		win.blit(bg1, (0,5))

	pygame.draw.rect(win, GRAY1, (10, 10, WIDTH-20, 50), border_radius=20)
	pygame.draw.rect(win, WHITE, (10, 10, WIDTH-20, 50), 2, border_radius=20)
	win.blit(tic_tac_toe, (WIDTH//2-tic_tac_toe.get_width()//2,17))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			click_pos = event.pos

		if event.type == pygame.MOUSEBUTTONUP:
			click_pos = None

	for box in box_list:
		box.update(win)
		if box.active and click_pos:
			if box.rect.collidepoint(click_pos):
				box.active = False

				box.text = text
				if text == 'X':
					box.bgcolor = GRAY1
				else:
					box.bgcolor = GREY2

				board[box.index+1] = text
				current_player = (current_player + 1) % 2
				text = players[current_player]

	check_winner = check_win(board, "X")
	if not result and check_winner[0]:
		result = 'X Won'
		line_pos = check_winner[1]
		scoreX += 1
	check_winner = check_win(board, "O")
	if not result and check_winner[0]:
		result = 'O Won'
		line_pos = check_winner[1]
		scoreO += 1
	if isBoardFull(board) or result:
		for box in box_list:
			box.active = False
		if not result:
			result = 'Draw'
	if line_pos:
		starting = box_list[int(line_pos[0]) - 1].rect.center
		ending = box_list[int(line_pos[-1]) - 1].rect.center

		pygame.draw.line(win, WHITE, starting, ending, 5)

	if result:
		if box_list[-1].rect.bottom <= 500:
			for box in box_list:
				box.rect.y += 1

		result_image = font3.render(result, True, BLACK)
		win.blit(result_image, (50, 210))
		win.blit(replay_image, replay_rect)
		if click_pos and replay_rect.collidepoint(click_pos):
			board = create_board()
			box_list = generate_boxes()
			players = ['X', 'O']
			current_player = random.randint(0, 1)
			text = players[current_player]

			result = None
			line_pos = None

	if text == 'X':
		pygame.draw.rect(win, GRAY1, (35, 150, 80, 30), border_radius=10)
	elif text == 'O':
		pygame.draw.rect(win, GREY2, (165, 150, 80, 30), border_radius=10)

	imgX = font1.render(f'X    {scoreX}', True, BLACK)
	imgO = font1.render(f'O    {scoreO}', True, BLACK)
	win.blit(imgX, (60, 152))
	win.blit(imgO, (180, 152))
	pygame.draw.rect(win, BLACK, (35, 150, 80, 30), 1, border_radius=10)
	pygame.draw.rect(win, BLACK, (165, 150, 80, 30), 1, border_radius=10)

	pygame.draw.rect(win, BLACK, (0, 0, WIDTH, HEIGHT), 5, border_radius=10)
	clock.tick()
	pygame.display.update()
pygame.quit()
