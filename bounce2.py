from tkinter import *
import random
import time


class Widget(object):  # 画面上で動く物の基本となるクラス

    def __init__(self, window, size, color, pos, speed=[0, 0]):
        self.window = window
        self.size = size
        self.color = color
        self.pos = pos
        self.speed = speed

    def acty(self):  # インスタンスを動かす
        self.window.move(self.id, self.speed[0], self.speed[1])

    def xturn(self):  # 横軸の方向転換
        self.speed[0] *= -1

    def yturn(self):  # 縦軸の方向転換
        self.speed[1] *= -1

    def current_speed(self):  # 現在の速度
        return self.speed


class Ball(Widget):  # Widgetを継承する、ボールのためのクラス
    def __init__(self, window, size, color, pos, speed):
        super().__init__(window, size, color, pos, speed)
        self.id = self.window.create_oval(self.pos[0], self.pos[1],
                                          self.pos[0]+self.size,
                                          self.pos[1]+self.size,
                                          fill=self.color)

    def current_place(self):  # 今いる場所
        return self.window.coords(self.id)

    def hit_check(self, obj):  # 当たったかどうかのチェック
        own_pos = self.current_place()
        obj_pos = obj.current_place()
        own_center = (own_pos[0] + own_pos[2])/2
        if (own_center > obj_pos[0] and own_center < obj_pos[2]) \
                and (own_pos[1] <= obj_pos[3] and own_pos[3] >= obj_pos[1]):
            return 1
        else:
            return 0


class Bar(Widget):  # Widgetを継承する、長方形物体用のクラス
    def __init__(self, window, size, color, pos):
        super().__init__(window, size, color, pos)
        self.point = 0
        self.id = self.window.create_rectangle(self.pos[0], self.pos[1],
                                               self.pos[0]+self.size[0],
                                               self.pos[1]+self.size[1],
                                               fill=self.color)

    def current_place(self):  # 今いる場所
        return self.window.coords(self.id)

    def current_point(self):  # ☆現在の得点
        return self.point

    def add_point(self, add=1):  # ☆得点加算
        self.point += add


class Player_Racket(Bar):  # Barを継承する、プレイヤーラケット用のクラス
    def __init__(self, window, size, color, pos, step=10):
        super().__init__(window, size, color, pos)
        self.step = step
        self.window.bind_all('<Key>', self.control)

    def control(self, event):  # 操作設定
        if event.keysym == "Right":
            self.speed = [self.step, 0]
        elif event.keysym == "Left":
            self.speed = [-self.step, 0]
        else:
            return
        self.acty()


class COM_Racket(Bar):  # ☆Barを継承する、COMラケット用のクラス

    def __init__(self, window, size, color, pos, step=10, count=10,
                 distance=100):
        super().__init__(window, size, color, pos)
        self.step = step
        self.count_range = count
        self.counter = 0
        self.distance = distance

    def control(self, obj):
        self.counter += 1
        if self.counter == self.count_range:
            self.counter = 0
            self.speed[0] = random.randrange(-self.step, self.step)
            if (obj.current_place()[0] - self.current_place()[0] >=
                self.distance and self.speed[0] < 0) \
                    or (self.current_place()[2] - obj.current_place()[2] >=
                        self.distance and self.speed[0] > 0):
                self.xturn()
        self.acty()


# ウィンドウの設定
tk = Tk()
canvas_size = [500, 400]
canvas = Canvas(tk, width=canvas_size[0], height=canvas_size[1])
tk.title("熱くなれよ!!!")
canvas.pack()

# ☆画面表示の設定
canvas.create_text(50, 150, text='COM', fill='green', font=('メイリオ', 20))
canvas.create_text(50, 250, text='YOU', fill='red', font=('メイリオ', 20))
canvas.create_text(50, 200, text='TIME', fill='purple', font=('メイリオ', 20))
enemy_score = canvas.create_text(130, 150, fill='green', font=('メイリオ', 20))
my_score = canvas.create_text(130, 250, fill='red', font=('メイリオ', 20))
play_time = canvas.create_text(130, 200, fill='purple', font=('メイリオ', 20))


def show_score(player_score, score):
    canvas.itemconfig(player_score, text=str(score))


def show_time(time_text, time_game):
    canvas.itemconfig(time_text, text=str(time_game))


# ☆試合の設定
finish_point = 3

# ボールとラケットの設定
ball_radius = 50
ball_start = [random.randrange(50, 400), random.randrange(50, 100)]
ball_init_speed = [2.0, 2.0]
bar_size = [100, 10]
player_start = [200, 340]
# ☆COMの設定
com_start = [200, 50]
com_distance = 100

# ボールとラケットのインスタンス作成
ball = Ball(canvas, ball_radius, 'blue', ball_start, ball_init_speed)
player_racket = Player_Racket(canvas, bar_size, 'red', pos=player_start)
com_racket = COM_Racket(canvas, bar_size, 'green', pos=com_start,
                        distance=com_distance)

# ☆時刻設定
game_start = int(time.perf_counter())
game_time = game_start

while True:
    ball.acty()  # ボールを動かす
    ball_pos = ball.current_place()
    ball_speed = ball.current_speed()

    com_racket.control(ball)  # ☆COMを動かす

    # ☆画面表示の更新
    show_score(my_score, player_racket.current_point())
    show_score(enemy_score, com_racket.current_point())
    show_time(play_time, game_time-game_start)
    now_time = int(time.perf_counter())

    if now_time - game_time >= 1:  # ☆一秒経過したら時刻表示切り替え
        game_time = now_time

    if player_racket.current_point() >= finish_point:  # ☆プレイヤーの勝利
        judge_text = 'YOU WIN'
        judge_color = 'blue'
        break
    if com_racket.current_point() >= finish_point:  # ☆COMの勝利
        judge_text = 'YOU LOSE'
        judge_color = 'red'
        break
    if ball_pos[2] >= canvas_size[0] or ball_pos[0] <= 0:
        ball.xturn()
    if ball_pos[3] >= canvas_size[1]:  # ☆COMの得点
        com_racket.add_point()
        ball.yturn()
    if ball_pos[1] <= 0:  # ☆プレイヤーの得点
        player_racket.add_point()
        ball.yturn()
    if (ball.hit_check(player_racket) == 1 and ball_speed[1] > 0) \
            or (ball.hit_check(com_racket) == 1 and ball_speed[1] < 0):
        ball.yturn()  # ☆相手のラケットに当たった場合を追加

    tk.update()
    time.sleep(0.01)

# ☆結果発表
canvas.create_text(250, 200, text=judge_text,
                   fill=judge_color, font=('メイリオ', 30))
tk.update()
time.sleep(10)
