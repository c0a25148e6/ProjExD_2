import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(5,0),
}


def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数:こうかとんRectかばくだんRect
    戻り値: タプル (横方向判定結果, 縦方向判定結果) 
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: # 横方向判定
        yoko = False
    if rct.top <0 or HEIGHT < rct.bottom: # 縦方向判定
        tate = False
    return yoko, tate



def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する関数
    引数 screen: 画面Surface
    """
    # 黒い矩形を描画するための空のSurfaceを作り、半透明にする
    bg_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bg_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    bg_img.set_alpha(128)
    screen.blit(bg_img, [0, 0]) # 画面に貼り付け

    # Game Overの文字を描画
    font = pg.font.Font(None, 80)
    txt = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(txt, txt_rct)

    # 泣いているこうかとん画像をロードして表示
    kk_img = pg.image.load("fig/8.png") # 8.pngを泣いている画像と想定
    kk_rct1 = kk_img.get_rect(center=(WIDTH/2 - 200, HEIGHT/2))
    kk_rct2 = kk_img.get_rect(center=(WIDTH/2 + 200, HEIGHT/2))
    screen.blit(kk_img, kk_rct1)
    screen.blit(kk_img, kk_rct2)

    pg.display.update()
    time.sleep(5) # 画面を更新して5秒待機
    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    #爆弾の初期化
    bb_img = pg.Surface((20,20)) # 一辺が20の正方形のSurface
    pg.draw.circle(bb_img,(255,0,0),(10,10),10) # 中心に半径10の赤い円を描画
    bb_img.set_colorkey((0,0,0)) # 四隅の黒を透過させる
    bb_rct = bb_img.get_rect() # 画像Surfaceに対応する画像Rectを取得
    bb_rct.centerx = random.randint(0,WIDTH) # 位置を表す変数に乱数を設定
    bb_rct.centery = random.randint(0,HEIGHT)
    vx, vy = +5, +5 # 横方向速度
    
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] # 横方向の移動量
                sum_mv[1] += mv[1] # 縦方向の移動量
                
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) # 動きをなかったことにする
        screen.blit(kk_img, kk_rct)
        
        bb_rct.move_ip(vx, vy) # メソッドで速度に応じて位置を移動
        
        # 爆弾の画面外判定
        yoko, tate = check_bound(bb_rct)
        if not yoko: # 横方向にはみ出たら
            vx *= -1 
        if not tate: # 縦方向にはみ出たら
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
