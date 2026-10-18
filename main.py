k = 30
kk = 30
MIN_DIF = 5  # 这里修改最低等级


def hash(x):
    import hashlib
    ITER = 3000000
    SALT = b"salt2026fixed"
    return hashlib.pbkdf2_hmac("sha512", x.encode(), SALT, ITER).hex()


lj = []
dif = 0.0

player = []
target = []
walls = []
zdxy = []
xtc = {}
cnt = 0
notuser = 0
ast = 1
listt = ["zdxy", "player", "target", "walls", "cnt", "xtc", "dif", "lj", "old_pos"]


def main():
    global player, target, walls, zdxy, xtc, listt, cnt, notuser, MIN_DIF, ast, k, kk
    global lj, dif, startplayer, old_pos
    import random
    import os
    import sys
    import time
    from ast import literal_eval
    arav = sys.argv[1:]
    from pathfinding.core.grid import Grid
    from pathfinding.finder.a_star import AStarFinder
    from pathfinding.core.diagonal_movement import DiagonalMovement
    notuser = 1
    black = "⚫"
    white = "⚪"
    wall = "██"
    goal = "🔷"
    cnt = 0
    zd = "💣"
    ljlj = "🟦"
    xtc = {}
    startplayer = []
    old_pos = []
    if arav:
        try:
            random.seed(int(arav[0]))
        except ValueError:
            pass

    def clear_screen():
        print("\033c", end="")
        try:
            if os.name == "nt":
                cmd = "cls"
            else:
                cmd = "clear"
            os.system(cmd)
        except BaseException:
            print("\n" * 50)

    def generate_positions():
        global lj, dif
        total_try = 0
        while 1:
            print(total_try, end="\r")
            total_try += 1
            player = None
            while True:
                rx = random.randint(1, k)
                ry = random.randint(1, kk)
                player = [rx, ry]
                break
            target = None
            while True:
                rx = random.randint(1, k)
                ry = random.randint(1, kk)
                target = [rx, ry]
                if target != player:
                    break
            num_walls = random.randint(80, 360)
            walls = []
            while len(walls) < num_walls:
                wx = random.randint(1, k)
                wy = random.randint(1, kk)
                wall_pos = [wx, wy]
                if wall_pos != player and wall_pos != target and wall_pos not in walls:
                    walls.append(wall_pos)
            matrix = []
            for gy in range(1, kk + 1):
                row = []
                for gx in range(1, k + 1):
                    if [gx, gy] in walls:
                        row.append(0)
                    else:
                        row.append(1)
                matrix.append(row)
            px, py = player
            tx, ty = target
            matrix[py - 1][px - 1] = 1
            matrix[ty - 1][tx - 1] = 1
            grid = Grid(matrix=matrix)
            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
            start = grid.node(px - 1, py - 1)
            end = grid.node(tx - 1, ty - 1)
            path, runs = finder.find_path(start, end, grid)
            if path != []:
                lj = list(path)
                d = [(node.x + 1, node.y + 1) for node in lj]
                lj = d.copy()
                max_len = 58
                raw = len(lj) / max_len
                dif = round(raw * 5.0, 1)
                if dif >= MIN_DIF:
                    print(f"本次迷宫难度:{dif},一共尝试生成 {total_try} 次")
                    return player, target, walls

    if os.path.isfile("maze.dat"):
        try:
            tmp = {}
            with open("maze.dat", "r") as f:
                for item in f.read().split(";"):
                    if "=" in item:
                        key, val = item.split("=", 1)
                        tmp[key] = literal_eval(val)
            for key, val in tmp.items():
                globals()[key] = val
            ast = 0
        except Exception:
            pass

    if ast: player, target, walls = generate_positions()

    def print_board(pos, show_all_walls=0, x=None):
        if x is None:
            x = []
        global target
        hit_walls = list(xtc.keys())
        for c in range(1, kk + 1):
            for i in range(1, k + 1):
                if [i, c] == pos:
                    print(black, end="")
                elif (i, c) in x and [i, c] != target:
                    print(ljlj, end="")
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

    if ast:
        zdxy = []
        bomb_count = random.randint(2, 10)
        for i in range(0, bomb_count):
            while 1:
                zdx = [random.randint(1, k), random.randint(1, kk)]
                if zdx != player and zdx not in walls and zdx != target and zdx not in zdxy:
                    zdxy.append(zdx)
                    break
        startplayer = player.copy()

    def sc(mode: bool, g):
        global target, walls, player, k, kk
        from pathfinding.core.grid import Grid
        from pathfinding.finder.a_star import AStarFinder
        from pathfinding.core.diagonal_movement import DiagonalMovement
        def has_path(matrix, sx, sy, ex, ey):
            grid = Grid(matrix=matrix)
            start = grid.node(sx - 1, sy - 1)
            end = grid.node(ex - 1, ey - 1)
            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
            path, _ = finder.find_path(start, end, grid)
            converted_path = [(node.x + 1, node.y + 1) for node in path]
            return bool(path), converted_path

        x = []
        for ry in range(1, kk + 1):
            o = []
            for rx in range(1, k + 1):
                if [rx, ry] in walls:
                    o.append(0)
                else:
                    o.append(1)
            x.append(o)
        sx, sy = player
        ex, ey = target
        if not mode:  # 更新目标点
            ex, ey = g
        else:
            sx, sy = g
        return has_path(x, sx, sy, ex, ey)

    ts = ""
    tim = time.time()
    while True:
        old_pos = player.copy()
        xtc = {pos: step for pos, step in xtc.items() if cnt - step <= 10}
        if cnt % 100 == 0 and cnt != 0:
            while True:
                target = [random.randint(1, k), random.randint(1, kk)]
                if target != player and target not in walls and target not in zdxy and sc(0, target)[0]:
                    lj = sc(0, target)[1]
                    print("目标点已更新")
                    time.sleep(1.5)
                    break
        clear_screen()
        if ts != "":
            print(ts)
            ts = ""
        print(f"移动次数：{cnt}\n时间:{time.time() - tim:.2f}秒")
        print_board(player)
        try:
            a = input("1:⬆️ 2:⬇️ 3:⬅️ 4:➡️ 0:⏏️ : ")
        except KeyboardInterrupt:
            clear_screen()
            print("已退出游戏")
            sys.exit(0)
        if not a.isdigit():
            input("输入无效，按回车继续...")
            continue
        a = int(a)
        if a == 5:
            print_board(player, show_all_walls=1)
            input("回车继续")
            continue
        if a == 6:
            if notuser == 0:
                if hash(input(
                        "请输入密码:")) != '94f3da6cd4e6332e071b252b37bf1ef03a0a8aaf125dddadd3c7278e55bbaeac2b65462389b85f4e73fb8736592a3fe3e9d6bde563ac51217f931c0e63fae241':
                    print("密码错误")
                    time.sleep(2)
                    continue
            res = ""
            try:
                import builtins

                glb = builtins.globals()
                glb["dif"] = dif
                glb["lj"] = lj
                rrr = input()
                if rrr == "eval" or not rrr:
                    res = eval(input("请输入:\n"))
                else:
                    res = "."
                    exec(input("请输入:\n"))
                    res = "执行成功"

                dif = glb["dif"]
                lj = glb["lj"]
                print(res)
                input("回车继续")
            except Exception as cvb:
                if res == ".":
                    print('执行失败')
                print(cvb)
                input("回车继续")
            continue
        if a == 7:
            add = "ast=0"
            add += f";startplayer={repr(startplayer)}"
            for i in listt:
                add += f";{i}={repr(globals()[i])}"
            with open("maze.dat", "w") as f:
                f.write(add)
            input("回车继续")
            continue
        if a == 8:
            player = target.copy()
        if a == 9:
            print_board(startplayer, 1, lj)
            input("回车继续")
            continue

        if a == 0:
            clear_screen()
            if input("是否退出游戏？(y/n): ").lower() == "y":
                print("已退出游戏")
                sys.exit(0)
            else:
                continue
        if a not in [1, 2, 3, 4] and a != 8:
            input("请输入 1‑4 或 0，按回车继续")
            continue

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
            input("不能移出棋盘，按回车继续")
            continue
        if player in walls:
            xtc[tuple(player)] = cnt
            player = old_pos
            input("撞到障碍物，按回车继续")
            continue

        if player in zdxy:
            ts = "💣 踩到炸弹！被随机传送到安全空地"
            zdxy.remove(player)
            while True:
                nx = random.randint(1, k)
                ny = random.randint(1, kk)
                np = [nx, ny]
                if np not in walls and np not in zdxy and np != target and sc(1, np)[0]:
                    lj = sc(1, np)[1]
                    player = np
                    break

        if player == target:
            clear_screen()
            print_board(startplayer, show_all_walls=True)
            x = time.time()
            print(f"🎉 恭喜通关！总步数 {cnt + 1}，用时 {x - tim:.2f} 秒，平均每步 {(x - tim) / (cnt + 1):.2f}")
            gf=input("是否重新开始？(y/n): ").lower()
            if gf=="y":
                main()
            else:
                sys.exit(0)
        cnt += 1


if __name__ == "__main__":
    main()