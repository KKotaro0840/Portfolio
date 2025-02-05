import pygame as pg
import random

def main():
    # Pygame 初期化
    pg.init()
    pg.display.set_caption("守れ！ひたすら撃て！")
    disp_w, disp_h = 800, 600
    screen = pg.display.set_mode((disp_w, disp_h))
    clock = pg.time.Clock()
    font = pg.font.Font(None, 36)

    # ゲームの初期設定
    player_img = pg.image.load("data/player.png")  # プレイヤー画像
    enemy_img1 = pg.image.load("data/enemy1.png")  # 敵タイプ1画像
    enemy_img2 = pg.image.load("data/enemy2.png")  # 敵タイプ2画像
    bullet_img = pg.image.load("data/bullet.png")  # 弾画像
    bomb_img = pg.image.load("data/bomb.png")      # ボム画像

    player_s = pg.Vector2(48, 48)  # プレイヤーサイズ
    enemy_s = pg.Vector2(48, 48)   # 敵のサイズ
    bullet_s = pg.Vector2(8, 16)   # 弾のサイズ

    # プレイヤーの初期位置
    player_p = pg.Vector2(disp_w // 2, disp_h - player_s.y - 10)
    player_speed = 5

    # 弾リスト
    bullets = []

    # 敵リスト
    enemies = []
    enemy_spawn_timer = 0
    fast_enemy_timer = 10  # 高速な敵が出現するタイミング（秒）

    # ボム関連
    bomb_cooldown = 0      # クールダウンタイマー
    bomb_cooldown_time = 15  # クールダウンの時間

    # スコアと時間
    score = 0
    frame_count = 0
    game_over = False

    # ゲームループ
    while not game_over:
        # イベント処理
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over = True

        # キー入力
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            player_p.x = max(0, player_p.x - player_speed)  # 左に移動
        if keys[pg.K_RIGHT]:
            player_p.x = min(disp_w - player_s.x, player_p.x + player_speed)  # 右に移動
        if keys[pg.K_z] and frame_count % 10 == 0:  # Zキーで弾を発射（間隔制御）
            bullets.append(pg.Vector2(player_p.x + player_s.x / 2 - bullet_s.x / 2, player_p.y))
        if keys[pg.K_x] and bomb_cooldown == 0:  # Xキーでボムを使用
            bomb_cooldown = bomb_cooldown_time * 30  # 15秒のクールダウン
            enemies.clear()  # 全敵を一掃
            score += 100 * len(enemies)  # 一掃した分だけスコア加算

        # 敵のスポーン
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= 30:  # 毎秒2体程度スポーン
            enemy_spawn_timer = 0
            enemy_type = random.choice(["slow", "fast"])
            enemy_img = enemy_img1 if enemy_type == "slow" else enemy_img2
            enemy_speed = 2 if enemy_type == "slow" else 4
            enemies.append({"pos": pg.Vector2(random.randint(0, disp_w - enemy_s.x), 0), "speed": enemy_speed, "img": enemy_img})

        # 弾の移動と削除
        bullets = [b + pg.Vector2(0, -8) for b in bullets if b.y > 0]

        # 敵の移動
        for enemy in enemies:
            enemy["pos"].y += enemy["speed"]

        # 衝突判定
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if (enemy["pos"].x < bullet.x < enemy["pos"].x + enemy_s.x and
                        enemy["pos"].y < bullet.y < enemy["pos"].y + enemy_s.y):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 100 if enemy["speed"] == 2 else 500
                    break

        # プレイヤーの位置に敵が到達したらゲームオーバー
        for enemy in enemies:
            if enemy["pos"].y > player_p.y:
                game_over = True

        # ボムのクールダウン
        if bomb_cooldown > 0:
            bomb_cooldown -= 1

        # 背景描画
        screen.fill(pg.Color("black"))

        # プレイヤー描画
        screen.blit(player_img, player_p)

        # 弾描画
        for bullet in bullets:
            screen.blit(bullet_img, bullet)

        # 敵描画
        for enemy in enemies:
            screen.blit(enemy["img"], enemy["pos"])

        # スコア描画
        score_text = font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, (10, 10))

        # クールダウン描画
        if bomb_cooldown > 0:
            cooldown_text = font.render(f"Bomb cooldown: {bomb_cooldown // 30}", True, "red")
            screen.blit(cooldown_text, (10, 50))

        # フレームカウントとスコア更新
        frame_count += 1
        if frame_count % 30 == 0:  # 毎秒加算
            score += 10

        # 画面更新とフレームレート制御
        pg.display.update()
        clock.tick(30)

    # ゲーム終了
    pg.quit()
    print("Game Over! Score:", score)


if __name__ == "__main__":
    main()
