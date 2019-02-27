from tkinter import *
import random
import time


class Widget(object):  # 画面上で動く物の基本となるクラス
    def __init__(self, window, size, color, pos, speed=0):
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
                                          self.pos[0] + self.size,
                                          self.pos[1] + self.size,
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

# ウィンドウの設定
tk = Tk()
canvas_size = [500, 400]
canvas = Canvas(tk, width=canvas_size[0], height=canvas_size[1])
tk.title("球打ちゲーム(仮)")
canvas.pack()

# ボールとラケットの設定
ball_radius = 50
ball_start = [random.randrange(50, 400), random.randrange(50, 100)]
ball_init_speed = [2.0, 2.0]
bar_size = [100, 10]
player_start = [200, 340]

# ボールとラケットのインスタンス作成
ball = Ball(canvas, ball_radius, 'blue', ball_start, ball_init_speed)
player_racket = Player_Racket(canvas, bar_size, 'red', pos=player_start)

while True:
    ball.acty()  # ボールを動かす
    ball_pos = ball.current_place()
    ball_speed = ball.current_speed()

    if ball_pos[2] >= canvas_size[0] or ball_pos[0] <= 0:
        ball.xturn()
    if ball_pos[3] >= canvas_size[1]:
        break
    elif ball_pos[1] <= 0:
        ball.yturn()
    elif ball.hit_check(player_racket) == 1 and ball_speed[1] > 0:
        ball.yturn()  # ラケットに当たったら

    tk.update()
    time.sleep(0.01)

# ゲームオーバー
judge_text = 'GAME OVER'
judge_color = 'blue'
canvas.create_text(250, 200, text=judge_text,
                   fill=judge_color, font=('メイリオ', 30))
tk.update()
time.sleep(10)
