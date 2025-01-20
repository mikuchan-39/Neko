import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ボードサイズ
BOARD_SIZE = 6

# ボード評価表
EVALUATION_BOARD = [
    [100, -20, 10, 10, -20, 100],
    [-20, -50, -2, -2, -50, -20],
    [10, -2,  1,  1,  -2,  10],
    [10, -2,  1,  1,  -2,  10],
    [-20, -50, -2, -2, -50, -20],
    [100, -20, 10, 10, -20, 100],
]

# 初期ボード
def create_initial_board():
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    mid = BOARD_SIZE // 2
    board[mid - 1, mid - 1] = 1
    board[mid, mid] = 1
    board[mid - 1, mid] = -1
    board[mid, mid - 1] = -1
    return board

# ボード表示
def draw_board(board):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')

    # 背景を緑に設定
    ax.set_facecolor('green')

    # マス目の描画
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            piece = board[x, y]
            if piece == 1:  # 白
                circle = patches.Circle((y + 0.5, BOARD_SIZE - x - 0.5), 0.4, color='white')
                ax.add_patch(circle)
            elif piece == -1:  # 黒
                circle = patches.Circle((y + 0.5, BOARD_SIZE - x - 0.5), 0.4, color='black')
                ax.add_patch(circle)

    ax.set_xlim(0, BOARD_SIZE)
    ax.set_ylim(0, BOARD_SIZE)
    ax.axis('off')  # 縦横の線を非表示
    plt.show()

# 有効な手かどうかを判定
def is_valid_move(board, x, y, player):
    if board[x, y] != 0:
        return False
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        has_opponent_piece = False
        while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
            if board[nx, ny] == -player:
                has_opponent_piece = True
            elif board[nx, ny] == player:
                if has_opponent_piece:
                    return True
                break
            else:
                break
            nx += dx
            ny += dy
    return False

# 合法手を探す
def get_legal_moves(board, player):
    moves = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if is_valid_move(board, x, y, player):
                moves.append((x, y))
    return moves

# 1手を打つ関数
def make_move(board, move, player):
    x, y = move
    board[x, y] = player
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        pieces_to_flip = []
        while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
            if board[nx, ny] == -player:
                pieces_to_flip.append((nx, ny))
            elif board[nx, ny] == player:
                for px, py in pieces_to_flip:
                    board[px, py] = player
                break
            else:
                break
            nx += dx
            ny += dy
    return board

# ゲーム終了判定
def is_game_over(board):
    return not get_legal_moves(board, 1) and not get_legal_moves(board, -1)

# 勝者判定
def determine_winner(board):
    score = np.sum(board)
    if score > 0:
        return "Player 1 (White)"
    elif score < 0:
        return "Player 2 (Black)"
    else:
        return "Draw"

# ボードの評価関数
def evaluate_board(board):
    score = 0
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            score += board[i, j] * EVALUATION_BOARD[i][j]
    return score

# ミニマックスアルゴリズム
def minimax(board, depth, alpha, beta, maximizing_player, player):
    if depth == 0 or is_game_over(board):
        return evaluate_board(board)
    
    legal_moves = get_legal_moves(board, player)
    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            new_board = board.copy()
            make_move(new_board, move, player)
            eval = minimax(new_board, depth - 1, alpha, beta, False, -player)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            new_board = board.copy()
            make_move(new_board, move, player)
            eval = minimax(new_board, depth - 1, alpha, beta, True, -player)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# AIの最善手選択
def choose_best_move(board, player):
    best_move = None
    best_value = float('-inf')
    for move in get_legal_moves(board, player):
        new_board = board.copy()
        make_move(new_board, move, player)
        move_value = minimax(new_board, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing_player=False, player=-player)
        if move_value > best_value:
            best_value = move_value
            best_move = move
    return best_move

# ゲームプレイ
def play_game():
    board = create_initial_board()
    current_player = 1
    while not is_game_over(board):
        draw_board(board)
        if current_player == 1:  # AIのターン
            move = choose_best_move(board, current_player)
        else:  # 相手のターン（ランダムに動く例）
            moves = get_legal_moves(board, current_player)
            move = random.choice(moves) if moves else None
        if move:
            make_move(board, move, current_player)
        current_player = -current_player
    draw_board(board)
    print("Game Over!")
    print("Winner:", determine_winner(board))

# ボード表示
def draw_board(board):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')

    # 背景を緑に設定
    ax.add_patch(patches.Rectangle((0, 0), BOARD_SIZE, BOARD_SIZE, color='green'))

    # マス目の描画
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            piece = board[x, y]
            if piece == 1:  # 白
                circle = patches.Circle((y + 0.5, BOARD_SIZE - x - 0.5), 0.4, color='white')
                ax.add_patch(circle)
            elif piece == -1:  # 黒
                circle = patches.Circle((y + 0.5, BOARD_SIZE - x - 0.5), 0.4, color='black')
                ax.add_patch(circle)

    ax.set_xlim(0, BOARD_SIZE)
    ax.set_ylim(0, BOARD_SIZE)
    ax.axis('off')  # 縦横の線を非表示
    plt.show()
