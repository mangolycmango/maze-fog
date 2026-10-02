# -*- coding: utf-8 -*-
def main():
    import random
    import time
    import os


    k = 30
    kk = 30


    black = "⚫"
    white = "⚪"
    wall = "██"
    goal = "🔷"
    zd = "💣"

    cnt = 0

    xtc = {}


    def clear_screen():
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")


    def generate_positions():
        """生成玩家、目标、墙体初始位置"""
        player = [(k + 1) // 2, (kk + 1) // 2]

        while True:
            target = [random.randint(1, k), random.randint(1, kk)]
            if target != player:
                break

        while True:
            num_walls = random.randint(250, 400)
            walls = []
            while len(walls) < num_walls:
                wall_pos = [random.randint(1, k), random.randint(1, kk)]
                if wall_pos != player and wall_pos != target and wall_pos not in walls:
                    walls.append(wall_pos)
            break
        return player, target, walls


    def print_board(pos, show_all_walls=0):
        """渲染迷宫地图"""
        hit_walls = list(xtc.keys())
        for i in range(1, k + 1):
            for c in range(1, kk + 1):
                if [i, c] == pos:
                    print(black, end="")
                elif show_all_walls and [i, c] in zdxy:
                    print(zd, end="")
                elif [i, c] == target:
                    print(goal, end="")
                elif [i, c] in walls:
                    if show_all_walls or (i, c) in hit_walls:
                        print(wall, end="")
                    else:
                        print(white, end="")
                else:
                    print(white, end="")
            print()


    def main():
        global player, target, walls, zdxy, cnt, xtc
        player, target, walls = generate_positions()
        tim = time.time()
        zdxy = []

        for i in range(0, random.randint(2, 10)):
            while True:
                zdx = [random.randint(1, k), random.randint(1, kk)]
                if zdx != player and zdx not in walls and zdx != target and zdx not in zdxy:
                    zdxy.append(zdx)
                    break
        startplayer = player.copy()

        while True:

            xtc = {pos: step for pos, step in xtc.items() if cnt - step <= 10}

            if cnt % 100 == 0 and cnt != 0:
                while True:
                    target = [random.randint(1, k), random.randint(1, kk)]
                    if target != player and target not in walls and target not in zdxy:
                        print("目标点已更新")
                        time.sleep(1.5)
                        break

            clear_screen()
            print(f"移动次数：{cnt}\n时间:{time.time() - tim:.2f}秒")
            print_board(player)

            a = input("1:⬅️ 2:➡️ 3:⬆️ 4:⬇️ 0:退出 : ")
            if not a.isdigit():
                input("输入无效，按回车继续...")
                continue
            a = int(a)

            if a == 5:
                print_board(player, show_all_walls=1)
            if a == 6:
                try:
                    print(eval(input()))
                except Exception as cvb:
                    print(cvb)
            if a == 7:
                print(f"walls={walls};target={target};player={player};zdxy={zdxy};cnt={cnt},xtc={xtc}")
            if a == 0:
                clear_screen()
                print("已退出游戏")
                break
            if a not in [1, 2, 3, 4]:
                input("请输入 1-4 或 0，按回车继续...")
                continue

            old_pos = player.copy()
            if a == 1:
                player[1] -= 1
            elif a == 2:
                player[1] += 1
            elif a == 3:
                player[0] -= 1
            elif a == 4:
                player[0] += 1


            if player[0] < 1 or player[0] > k or player[1] < 1 or player[1] > kk:
                player = old_pos
                input("不能移出棋盘！按回车继续...")
                continue

            if player in walls:
                xtc[tuple(player)] = cnt
                player = old_pos
                input("撞到障碍物了！按回车继续...")
                continue

            if player in zdxy:
                zdxy.remove(player)
                while True:
                    player = [random.randint(1, k), random.randint(1, kk)]
                    if player not in walls and player not in zdxy and player != target:
                        break

            if player == target:
                clear_screen()
                print_board(startplayer, show_all_walls=True)
                x = time.time()
                print(f"🎉 恭喜！你用了 {cnt + 1} 步,{x - tim:.2f}秒到达目标！平均每步耗时{(x - tim) * 1.0 / (cnt + 1):.2f}秒")
                break
            cnt += 1


    if __name__ == "__main__":
        main()

if __name__ == "__main__":
    main()
