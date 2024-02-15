import pgzrun
from pgzero.builtins import keyboard
import random
import time

# ウィンドウのサイズ
WIDTH = 600
HEIGHT = 600

# 迷路のマス数
MAZE_WIDTH = 31
MAZE_HEIGHT = 31

# 各マスのサイズ
TILE_SIZE = WIDTH // MAZE_WIDTH

# スタートとゴールの位置
start = (random.randint(0, MAZE_WIDTH-1), random.randint(0, MAZE_HEIGHT-1))
goal = (random.randint(0, MAZE_WIDTH-1), random.randint(0, MAZE_HEIGHT-1))
while start == goal:
    goal = (random.randint(0, MAZE_WIDTH-1), random.randint(0, MAZE_HEIGHT-1))

# DFSアルゴリズムで迷路を生成
def dfs(x, y, maze):
    if (x, y) == goal:
        return True
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx*2, y + dy*2
        def is_valid(nx, ny): return 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and maze[ny][nx] == 0
        if is_valid(nx, ny):
            maze[y+dy][x+dx] = 1
            maze[ny][nx] = 1
            if dfs(nx, ny, maze):
                return True
    return False

# 迷路の初期化
def initialize_maze(width, height):
    return [[0 for _ in range(width)] for _ in range(height)]

# スタートとゴールの設定
def set_start_and_goal(maze, start, goal):
    maze[start[1]][start[0]] = 1
    maze[goal[1]][goal[0]] = 1

# スタートの周囲を通路に設定する関数
def set_paths_around_start(maze, start):
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = start[0] + dx, start[1] + dy
        if set_path_if_valid(maze, nx, ny):
            break

# ゴールの周囲を通路に設定する関数
def set_paths_around_goal(maze, goal):
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = goal[0] + dx, goal[1] + dy
        if set_path_if_valid(maze, nx, ny):
            break

# セルを通路に設定する関数
def set_path_if_valid(maze, x, y):
    if 0 <= x < MAZE_WIDTH and 0 <= y < MAZE_HEIGHT:
        maze[y][x] = 1
        return True
    return False

# 迷路の生成
def generate_new_maze():
    maze = initialize_maze(MAZE_WIDTH, MAZE_HEIGHT)
    set_start_and_goal(maze, start, goal)
    dfs(0, 0, maze)
    set_paths_around_start(maze, start)
    set_paths_around_goal(maze, goal)
    return maze

# 迷路の生成
maze = generate_new_maze()

# プレイヤーの現在の位置
player = start

# プレイヤーの移動を処理する関数
def move(pos, dx, dy):
    x, y = pos
    nx, ny = x + dx, y + dy
    is_within_width = 0 <= nx < MAZE_WIDTH
    is_within_height = 0 <= ny < MAZE_HEIGHT
    is_path = maze[ny][nx] == 1 if is_within_width and is_within_height else False
    if is_within_width and is_within_height:
        is_path = maze[ny][nx] == 1
        if is_path:
            return (nx, ny)
    return pos

# キーが押されてから連続的に移動を開始するまでの時間（秒）
HOLD_TIME = 0.1

# キーが押された時間を記録する辞書
key_press_times = {}

# プレイヤーのキー入力に応じた移動処理
def handle_player_movement():
    global player
    current_time = time.time()
    for key in ['up', 'down', 'left', 'right']:
        if getattr(keyboard, key):
            if key not in key_press_times:
                key_press_times[key] = current_time
                player = move_player_by_key(key)
            elif current_time - key_press_times[key] >= HOLD_TIME:
                player = move_player_by_key(key)
        else:
            key_press_times.pop(key, None)

# キーに応じたプレイヤーの移動
def move_player_by_key(key):
    direction = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
    dx, dy = direction[key]
    return move(player, dx, dy)

# ゲームの更新
def update():
    global player, goal, maze, start
    handle_player_movement()

    # ゴールに到達したら次の迷路を表示
    if player == goal:
        # スタートとゴールの位置を再設定
        start = goal
        goal = (random.randint(0, MAZE_WIDTH-1), random.randint(0, MAZE_HEIGHT-1))
        while start == goal:
            goal = (random.randint(0, MAZE_WIDTH-1), random.randint(0, MAZE_HEIGHT-1))

        maze = generate_new_maze()
        player = start

# ゲームの描画
def draw():
    screen.fill((0, 0, 0))
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            if maze[y][x] == 1:
                screen.draw.filled_rect(Rect((x*TILE_SIZE, y*TILE_SIZE), (TILE_SIZE, TILE_SIZE)), (255, 255, 255))
    screen.draw.filled_rect(Rect((player[0]*TILE_SIZE, player[1]*TILE_SIZE), (TILE_SIZE, TILE_SIZE)), (0, 0, 255))
    screen.draw.filled_rect(Rect((goal[0]*TILE_SIZE, goal[1]*TILE_SIZE), (TILE_SIZE, TILE_SIZE)), (255, 0, 0))

pgzrun.go()
