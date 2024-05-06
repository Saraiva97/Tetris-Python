import pygame
import random
import time

# Definição de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Definição do tamanho da tela e dos blocos
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
BLOCK_SIZE = 20

# Definição do tabuleiro
BOARD_WIDTH = 20
BOARD_HEIGHT = 39

# Velocidade da queda das peças (em segundos)
FALL_SPEED = 0.005


# Formas de Tetris
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3],
     [3, 3]],

    [[4, 4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 0],
     [6, 0],
     [6, 6]],

    [[0, 7],
     [0, 7],
     [7, 7]]
]

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

# Função para desenhar blocos
def draw_block(x, y, color):
    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Função para criar uma nova peça
def new_piece():
    shape = random.choice(SHAPES)
    color = random.choice([RED, GREEN, BLUE, CYAN, ORANGE, YELLOW, PURPLE])
    piece = {
        'shape': shape,
        'color': color,
        'x': BOARD_WIDTH // 2 - len(shape[0]) // 2,
        'y': 0
    }
    return piece

# Função para verificar colisão entre peça e tabuleiro
def check_collision(board, piece, offset):
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell and (piece['y'] + y + offset[1] >= BOARD_HEIGHT or
                         piece['x'] + x + offset[0] < 0 or
                         piece['x'] + x + offset[0] >= BOARD_WIDTH or
                         board[piece['y'] + y + offset[1]][piece['x'] + x + offset[0]]):
                return True
    return False

# Função para mesclar peça com tabuleiro
def merge_piece(board, piece):
    for y, row in enumerate(piece['shape']):
        for x, cell in enumerate(row):
            if cell:
                board[piece['y'] + y][piece['x'] + x] = piece['color']

# Função para remover linhas completas
def remove_completed_lines(board):
    lines_removed = 0
    y = BOARD_HEIGHT - 1
    while y >= 0:
        if all(board[y]):
            del board[y]
            board.insert(0, [0] * BOARD_WIDTH)
            lines_removed += 1
        else:
            y -= 1
    return lines_removed

# Loop principal do jogo
def main():
    board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    piece = new_piece()
    game_over = False
    fall_time = 0
    score = 0

    while not game_over:
        screen.fill(BLACK)

        # Eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not check_collision(board, piece, (-1, 0)):
                    piece['x'] -= 1
                elif event.key == pygame.K_RIGHT and not check_collision(board, piece, (1, 0)):
                    piece['x'] += 1
                elif event.key == pygame.K_DOWN and not check_collision(board, piece, (0, 1)):
                    piece['y'] += 1
                elif event.key == pygame.K_UP:
                    piece['shape'] = [list(reversed(row)) for row in zip(*piece['shape'])]
                    if check_collision(board, piece, (0, 0)):
                        piece['shape'] = [list(reversed(row)) for row in zip(*piece['shape'])]
                elif event.key == pygame.K_SPACE:
                    while not check_collision(board, piece, (0, 1)):
                        piece['y'] += 1

        # Atualização da peça
        if not check_collision(board, piece, (0, 1)):
            piece['y'] += 1
            fall_time += clock.get_rawtime()
            if fall_time / 1000 >= FALL_SPEED:
                fall_time = 0
                if not check_collision(board, piece, (0, 1)):
                    piece['y'] += 1
        else:
            merge_piece(board, piece)
            score += remove_completed_lines(board)
            piece = new_piece()
            if check_collision(board, piece, (0, 0)):
                game_over = True

        # Desenho do tabuleiro
        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                if cell:
                    draw_block(x, y, cell)

        # Desenho da peça atual
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    draw_block(piece['x'] + x, piece['y'] + y, piece['color'])

        # Atualização da tela
        pygame.display.flip()
        clock.tick(5)

    print("Game Over! Pontuação:", score)
    pygame.quit()

if __name__ == "__main__":
    main()
