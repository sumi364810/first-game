import pyxel
SCREEN_WIDTH=160
SCREEN_HEIGHT=120
rakkabutu_INTERVAL=2
GAME_OVER_DISPLAY_TIME=60
START_SCENE="start"
PLAY_SCENE="play"
#Yはリストの要素のため、以下が必要となる
class Rakkabutu:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def update(self):
        if self.y<SCREEN_HEIGHT:
            self.y+=5
    def draw(self):
        #左から描画するx座標y座標画像バンク番号画像座標画像の幅高さ消す色
        pyxel.blt(self.x,self.y,0,8,0,8,8,pyxel.COLOR_BLACK)

class App:
    def __init__(self):
        #隠しエンディングの伏線
        pyxel.init(SCREEN_WIDTH,SCREEN_HEIGHT,title="良い世　来い")
        self.number_1=0
        self.number_2=0
        pyxel.load("my_resource.pyxres")
        pyxel.mouse(True)
        self.jp_font=pyxel.Font("umplus_j10r.bdf")
        pyxel.playm(0,loop=True)
        self.current_scene=START_SCENE
        self.countdown_timer = 30 * 30
        self.is_game_clear = False
        # 音楽の再生状態を管理するフラグ
        self.is_music_playing = True
        pyxel.run(self.update,self.draw)
    def reset_play_scene(self):
        self.senpai_x=SCREEN_WIDTH//2-5
        self.senpai_y=SCREEN_HEIGHT*4//5
        self.rakkabututati=[]
        self.is_collision=False
        self.number_1=0
        self.number_2=0
        self.game_over_dislay_timer=GAME_OVER_DISPLAY_TIME
        self.countdown_timer = 30 * 30
        self.is_game_clear = False
       
    def update_start_scene(self):
        # 音楽停止/再生ボタンのクリック処理
        if (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)and SCREEN_WIDTH - 45 <= pyxel.mouse_x <= SCREEN_WIDTH-5 and
        10 <= pyxel.mouse_y <= 30):
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if self.is_music_playing:
                    pyxel.stop()  # 音楽を停止
                    self.is_music_playing = False
                else:
                    pyxel.playm(0, loop=True)  # 音楽を再開
                    self.is_music_playing = True
            return # ボタンがクリックされた場合、ここで処理を終了
        
         # ゲーム開始処理
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)or pyxel.btnp(pyxel.KEY_SPACE):
            self.reset_play_scene()
            self.current_scene = PLAY_SCENE

    def update_play_scene(self):
        #ゲームオーバー時
        if self.is_collision or (self.number_2>=114 and self.number_1>=51):
            if self.game_over_dislay_timer>0:
                self.game_over_dislay_timer-=1
            else:
                self.current_scene=START_SCENE

            return
        # カウントダウンの更新
        if self.countdown_timer > 0:
            self.countdown_timer -= 1
        else:
            self.is_game_clear = True
            #game overじゃないけど（名前は間違えてるけど）操作はあってる
            if self.game_over_dislay_timer > 0:
                self.game_over_dislay_timer -= 1
            else:
                self.current_scene = START_SCENE
            return

        # 仮想ボタンのクリック処理
        if (2 <= pyxel.mouse_x <=20 and SCREEN_HEIGHT // 2 <= pyxel.mouse_y <= SCREEN_HEIGHT // 2 + 30):
            self.senpai_x = max(self.senpai_x - 3, 0)  # 左矢印キーの役割
        if (SCREEN_WIDTH - 20 <= pyxel.mouse_x <= SCREEN_WIDTH - 2 and SCREEN_HEIGHT // 2 <= pyxel.mouse_y <= SCREEN_HEIGHT // 2 + 30):
            self.senpai_x = min(self.senpai_x + 3, SCREEN_WIDTH - 16)  # 右矢印キーの役割
        if (2 <= pyxel.mouse_x <= 20 and SCREEN_HEIGHT // 2 - 35 <= pyxel.mouse_y <= SCREEN_HEIGHT // 2-5 ):
             self.senpai_x = max(self.senpai_x - 6, 0)  # 下矢印キーの役割
        if (SCREEN_WIDTH - 20 <= pyxel.mouse_x <= SCREEN_WIDTH - 2 and SCREEN_HEIGHT // 2 - 35 <= pyxel.mouse_y <= SCREEN_HEIGHT // 2-5):
             self.senpai_x = min(self.senpai_x + 6, SCREEN_WIDTH - 16) # 上矢印キーの役割
        # 左矢印ボタン
        pyxel.text(2, SCREEN_HEIGHT // 2+10, "←", pyxel.COLOR_BLACK,self.jp_font)
        # 右矢印ボタン
        pyxel.text(SCREEN_WIDTH - 10, SCREEN_HEIGHT // 2 +10, "→", pyxel.COLOR_BLACK,self.jp_font)
        # 下矢印ボタン
        pyxel.text(2, SCREEN_HEIGHT // 2 -20, "←←", pyxel.COLOR_BLACK,self.jp_font)
        # 上矢印ボタン
        pyxel.text(SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2 -20, "→→", pyxel.COLOR_BLACK,self.jp_font)
        # 先輩の移動（キーボード）
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.senpai_x = min(self.senpai_x + 3, SCREEN_WIDTH - 16)
        if pyxel.btn(pyxel.KEY_LEFT):
            self.senpai_x = max(self.senpai_x - 3, 0)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.senpai_x = max(self.senpai_x - 6, 0)
        if pyxel.btn(pyxel.KEY_UP):
            self.senpai_x = min(self.senpai_x + 6, SCREEN_WIDTH - 16)

        #落下物の追加
        if pyxel.frame_count%rakkabutu_INTERVAL==0:
            self.rakkabututati.append(Rakkabutu(pyxel.rndi(0,SCREEN_WIDTH-8),0))

        #落下物の落下
        for Rakkabutu in self.rakkabututati.copy():
            Rakkabutu.update()
            #衝突
            if (self.senpai_x<=Rakkabutu.x<=self.senpai_x+8 and
                self.senpai_y<=Rakkabutu.y<=self.senpai_y+8):
                self.is_collision=True
            #画面外に出た落下物を削除
            if Rakkabutu.y>=SCREEN_HEIGHT:
                self.rakkabututati.remove(Rakkabutu)

    def update(self):
        if self.current_scene==START_SCENE:
            self.update_start_scene()
        elif self.current_scene==PLAY_SCENE:
            self.update_play_scene()
    def draw_start_scene(self):
        if (self.number_2>=114 and self.number_1>=51)and not self.is_collision:
            pyxel.blt(0,0,1,0,0,160,120)
        else:
            pyxel.blt(0,0,0,32,0,160,120)
        # ボタンの描画
        pyxel.rect(SCREEN_WIDTH - 45, 10, 40, 20, pyxel.COLOR_BROWN)
        button_text = "音楽停止" if self.is_music_playing else "音楽再生"
        pyxel.text(SCREEN_WIDTH - 45, 15, button_text, pyxel.COLOR_BLACK,self.jp_font)
        pyxel.text(5,10,
                   "「30秒よけ続けろ！」",pyxel.COLOR_BROWN,self.jp_font)
        pyxel.text(10,SCREEN_HEIGHT-20,
                   "ゲーム開始:space or タップ",pyxel.COLOR_BLACK,self.jp_font)
        pyxel.text(5,SCREEN_HEIGHT-40,
                   "高速移動:★上下矢印 ☆→→←←",pyxel.COLOR_BLACK,self.jp_font)
        pyxel.text(5,SCREEN_HEIGHT-60,
                   "移動   :★右左矢印 ☆  →←",pyxel.COLOR_BLACK,self.jp_font)
        pyxel.text(5,SCREEN_HEIGHT-80,
                   "          ★pc    ☆スマホ",pyxel.COLOR_BLACK,self.jp_font)

    def draw_play_scene(self):
        pyxel.cls(pyxel.COLOR_DARK_BLUE)
        #落下物
        for Rakkabutu in self.rakkabututati:
            Rakkabutu.draw()
        #先輩
        pyxel.blt(self.senpai_x,self.senpai_y,0,16,0,16,16,pyxel.COLOR_YELLOW)
        # 仮想ボタンの描画
        # 左矢印ボタン
        pyxel.text(2, SCREEN_HEIGHT // 2+10, "←", pyxel.COLOR_BLACK,self.jp_font)
        # 右矢印ボタン
        pyxel.text(SCREEN_WIDTH - 10, SCREEN_HEIGHT // 2 +10, "→", pyxel.COLOR_BLACK,self.jp_font)
        # 下矢印ボタン
        pyxel.text(2, SCREEN_HEIGHT // 2 -20, "←←", pyxel.COLOR_BLACK,self.jp_font)
        # 上矢印ボタン
        pyxel.text(SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2 -20, "→→", pyxel.COLOR_BLACK,self.jp_font)

        #端の数字
        pyxel.text(SCREEN_WIDTH//2+10,5,f"{self.number_1}",pyxel.COLOR_BROWN)
        pyxel.text(SCREEN_WIDTH//2-15,5,f"{self.number_2}",pyxel.COLOR_BROWN)
        if self.senpai_x==144:
            self.number_1+=1
        if self.senpai_x==0:
            self.number_2+=1
        if (self.number_2>=114 and self.number_1>=51)and not self.is_collision:
            pyxel.text(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 2 - 10,
                       "【隠し演出】やりますねぇ！", pyxel.COLOR_WHITE, self.jp_font)

         # カウントダウンの描画
        pyxel.text(SCREEN_WIDTH-20, 5, f"{self.countdown_timer // 30}", pyxel.COLOR_WHITE, self.jp_font)
        # ゲームオーバー時の描画
        if self.is_collision:
            pyxel.text(SCREEN_WIDTH//2-30,SCREEN_HEIGHT//2-10,
                       "ゲイ夢 Over",pyxel.COLOR_BLACK,self.jp_font)

        # ゲームクリア時の描画
        if self.is_game_clear:
            pyxel.text(SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 - 10,
                       "ゲイ夢 clear!", pyxel.COLOR_YELLOW, self.jp_font)
            
    def draw(self):
        if self.current_scene==START_SCENE:
            self.draw_start_scene()
        elif self.current_scene==PLAY_SCENE:
            self.draw_play_scene()


App()  


