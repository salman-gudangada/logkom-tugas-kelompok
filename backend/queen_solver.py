def construct_prerule(n):
    grid = []
    rule = []
    for i in range(n):
        grid.append([i * n + j + 1 for j in range(n)])
    print(grid)

    # print(grid)
    # bikin rule horizontal
    for i in range(n):
        now = ""
        for j in range(n):
            now = now + str(grid[i][j]) + " "
        now = now + "0"
        rule.append(now)

    print(rule)
    # bikin rule vertikal
    for j in range(n):
        now = ""
        for i in range(n):
            now = now + str(grid[i][j]) + " "
        now = now + "0"
        rule.append(now)
    
    #rule gak nyerang horizontal
    for i in range(n):
        for j in range(n):
            for k in range(j + 1, n):
                s = "-" + str(grid[i][j]) + " " + "-" + str(grid[i][k]) + " 0"
                rule.append(s)

    #rule gak nyerang vertikal
    for i in range(n):
        for j in range(n):
            for k in range(j + 1, n):
                s = "-" + str(grid[j][i]) + " " + "-" + str(grid[k][i]) + " 0"
                rule.append(s)

    #rule gak nyerang diagonal (kiri atas ke kanan bawah)
    for i in range(n - 1):
        x = i
        y = 0
        tmp = []
        while True:
            tmp.append((x, y))
            x = x + 1
            y = y + 1
            if x >= n or y >= n:
                break
        
        for j in range(len(tmp)):
            val1 = grid[tmp[j][0]][tmp[j][1]]
            for k in range(j+1, len(tmp)):
                val2 = grid[tmp[k][0]][tmp[k][1]]
                s = "-" + str(val1) + " " + "-" + str(val2) + " 0"
                rule.append(s)

    for i in range(1, n - 1):
        x = 0
        y = i
        tmp = []
        while True:
            tmp.append((x, y))
            x = x + 1
            y = y + 1
            if x >= n or y >= n:
                break
        
        for j in range(len(tmp)):
            val1 = grid[tmp[j][0]][tmp[j][1]]
            for k in range(j+1, len(tmp)):
                val2 = grid[tmp[k][0]][tmp[k][1]]
                s = "-" + str(val1) + " " + "-" + str(val2) + " 0"
                rule.append(s)

    #rule gak nyerang diagonal (kanan atas ke kiri bawah)
    for i in range(n - 1):
        x = i
        y = n - 1
        tmp = []
        while True:
            tmp.append((x, y))
            x = x + 1
            y = y - 1
            if x >= n or y < 0:
                break
        
        for j in range(len(tmp)):
            val1 = grid[tmp[j][0]][tmp[j][1]]
            for k in range(j+1, len(tmp)):
                val2 = grid[tmp[k][0]][tmp[k][1]]
                s = "-" + str(val1) + " " + "-" + str(val2) + " 0"
                rule.append(s)

    for i in range(1, n - 1):
        x = 0
        y = i
        tmp = []
        while True:
            tmp.append((x, y))
            x = x + 1
            y = y - 1
            if x >= n or y < 0:
                break
        
        for j in range(len(tmp)):
            val1 = grid[tmp[j][0]][tmp[j][1]]
            for k in range(j+1, len(tmp)):
                val2 = grid[tmp[k][0]][tmp[k][1]]
                s = "-" + str(val1) + " " + "-" + str(val2) + " 0"
                rule.append(s)

    # print(rule)
    return rule

def queen(mat):
    n = len(mat)
    rule = construct_prerule(n)

    for i in range(n):
        for j in range(n):
            now = i * n + j + 1
            if mat[i][j] == 1:
                rule.append(str(now) + " 0")
            elif mat[i][j] == 2:
                rule.append("-" + str(now) + " 0")
    # print(rule)
                
    f = open("backend/input.txt", "w")
    f.write("p cnf " + str(n * n) + " " + str(len(rule)) + "\n")
    for s in rule:
        f.write(s + "\n")
    f.close()

    import os
    os.system("minisat backend/input.txt backend/output.txt")

    file_output = open("backend/output.txt", "r")
    verdict = file_output.readline()

    if verdict == "SAT\n":
        result = file_output.readline()
        result = result.split()
        import copy
        ret = copy.deepcopy(mat)
        for i in range(n):
            for j in range(n):
                idx = i * n + j
                if result[idx][0] != '-':
                    ret[i][j] = 1
        return ret
    else:
        return "UNSATISFIABLE"


# construct_prerule(4)