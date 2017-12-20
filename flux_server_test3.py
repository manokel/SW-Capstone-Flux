import pymysql.cursors
import socket
import sys



MAX = 100
Massenger = []


def parseMap():
    DBCONN = pymysql.connect(host = 'localhost',
                           user = 'root',
                           password = None,
                           db = 'car_map_data',
                           charset = 'utf8')
    with DBCONN.cursor() as cursor:
        parkinglot = [[0 for col in range(5)] for row in range(10)]
        i = 0
        sql = 'SELECT y, park, car, obstacle, parked FROM map WHERE x = %s'
        for i in range(0,10):
            cursor.execute(sql, (str(i)),)
            results = cursor.fetchall()
            for row in results:
                if row[3] == 1: # obstacle
                    parkinglot[i][row[0]] = 5
                elif row[2] == 1: # car
                    parkinglot[i][row[0]] = 4
                elif row[1] == 1: # park
                    parkinglot[i][row[0]] = 2
                elif row[4] == 1:
                    parkinglot[i][row[0]] = 3
                else:
                    parkinglot[i][row[0]] = 0
        DBCONN.close()
        return parkinglot
        
parkinglot = parseMap()

x = 9 #차량 위치
y = 0 #차량 위치

X = [0,0,0,0,0,0,0,0] #목적지 위치
Y = [0,0,0,0,0,0,0,0] #목적지 위치

pos_num = 0  #목적지 개수
node_num = 0 #목적지까지 가는데 필요한 위치 개수

des_node = [
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [0,0,0]
    ]        #목적지 좌표(x,y,최종 목적지를 나타내는 번호)

tracking_node = [
    [[0  ,MAX,MAX,MAX,MAX,MAX,MAX,MAX],
     [MAX,0  ,4  ,4  ,MAX,MAX,MAX,MAX],
     [MAX,4  ,0  ,MAX,4  ,MAX,MAX,MAX],
     [MAX,4  ,MAX,0  ,4  ,4  ,MAX,MAX],
     [MAX,MAX,4  ,4  ,0  ,MAX,4  ,MAX],
     [MAX,MAX,MAX,4  ,MAX,0  ,4  ,MAX],
     [MAX,MAX,MAX,MAX,4  ,4  ,0  ,MAX],
     [MAX,MAX,MAX,MAX,MAX,MAX,MAX,0  ]],

    [[0  ,MAX,MAX,MAX,MAX,MAX,MAX,MAX],
     [MAX,0  ,4  ,4  ,MAX,MAX,MAX,MAX],
     [MAX,4  ,0  ,MAX,4  ,MAX,MAX,MAX],
     [MAX,4  ,MAX,0  ,4  ,4  ,MAX,MAX],
     [MAX,MAX,4  ,4  ,0  ,MAX,4  ,MAX],
     [MAX,MAX,MAX,4  ,MAX,0  ,4  ,MAX],
     [MAX,MAX,MAX,MAX,4  ,4  ,0  ,MAX],
     [MAX,MAX,MAX,MAX,MAX,MAX,MAX,0  ]],

    [[0  ,MAX,MAX,MAX,MAX,MAX,MAX,MAX],
     [MAX,0  ,4  ,4  ,MAX,MAX,MAX,MAX],
     [MAX,4  ,0  ,MAX,4  ,MAX,MAX,MAX],
     [MAX,4  ,MAX,0  ,4  ,4  ,MAX,MAX],
     [MAX,MAX,4  ,4  ,0  ,MAX,4  ,MAX],
     [MAX,MAX,MAX,4  ,MAX,0  ,4  ,MAX],
     [MAX,MAX,MAX,MAX,4  ,4  ,0  ,MAX],
     [MAX,MAX,MAX,MAX,MAX,MAX,MAX,0  ]],

    [[0  ,MAX,MAX,MAX,MAX,MAX,MAX,MAX],
     [MAX,0  ,4  ,4  ,MAX,MAX,MAX,MAX],
     [MAX,4  ,0  ,MAX,4  ,MAX,MAX,MAX],
     [MAX,4  ,MAX,0  ,4  ,4  ,MAX,MAX],
     [MAX,MAX,4  ,4  ,0  ,MAX,4  ,MAX],
     [MAX,MAX,MAX,4  ,MAX,0  ,4  ,MAX],
     [MAX,MAX,MAX,MAX,4  ,4  ,0  ,MAX],
     [MAX,MAX,MAX,MAX,MAX,MAX,MAX,0  ]],

    [[0  ,MAX,MAX,MAX,MAX,MAX,MAX,MAX],
     [MAX,0  ,4  ,4  ,MAX,MAX,MAX,MAX],
     [MAX,4  ,0  ,MAX,4  ,MAX,MAX,MAX],
     [MAX,4  ,MAX,0  ,4  ,4  ,MAX,MAX],
     [MAX,MAX,4  ,4  ,0  ,MAX,4  ,MAX],
     [MAX,MAX,MAX,4  ,MAX,0  ,4  ,MAX],
     [MAX,MAX,MAX,MAX,4  ,4  ,0  ,MAX],
     [MAX,MAX,MAX,MAX,MAX,MAX,MAX,0  ]],

    [[0  ,MAX,MAX,MAX,MAX,MAX,MAX,MAX],
     [MAX,0  ,4  ,4  ,MAX,MAX,MAX,MAX],
     [MAX,4  ,0  ,MAX,4  ,MAX,MAX,MAX],
     [MAX,4  ,MAX,0  ,4  ,4  ,MAX,MAX],
     [MAX,MAX,4  ,4  ,0  ,MAX,4  ,MAX],
     [MAX,MAX,MAX,4  ,MAX,0  ,4  ,MAX],
     [MAX,MAX,MAX,MAX,4  ,4  ,0  ,MAX],
     [MAX,MAX,MAX,MAX,MAX,MAX,MAX,0  ]],

    [[0  ,MAX,MAX,MAX,MAX,MAX,MAX,MAX],
     [MAX,0  ,4  ,4  ,MAX,MAX,MAX,MAX],
     [MAX,4  ,0  ,MAX,4  ,MAX,MAX,MAX],
     [MAX,4  ,MAX,0  ,4  ,4  ,MAX,MAX],
     [MAX,MAX,4  ,4  ,0  ,MAX,4  ,MAX],
     [MAX,MAX,MAX,4  ,MAX,0  ,4  ,MAX],
     [MAX,MAX,MAX,MAX,4  ,4  ,0  ,MAX],
     [MAX,MAX,MAX,MAX,MAX,MAX,MAX,0  ]],

    [[0  ,MAX,MAX,MAX,MAX,MAX,MAX,MAX],
     [MAX,0  ,4  ,4  ,MAX,MAX,MAX,MAX],
     [MAX,4  ,0  ,MAX,4  ,MAX,MAX,MAX],
     [MAX,4  ,MAX,0  ,4  ,4  ,MAX,MAX],
     [MAX,MAX,4  ,4  ,0  ,MAX,4  ,MAX],
     [MAX,MAX,MAX,4  ,MAX,0  ,4  ,MAX],
     [MAX,MAX,MAX,MAX,4  ,4  ,0  ,MAX],
     [MAX,MAX,MAX,MAX,MAX,MAX,MAX,0  ]]
    ] #각 목적지가 가지는 위치 행렬

flag = [0,0,0,0,0,0,0,0,0] #dijkstra 알고리즘을 위한 배열
dist = [
    [MAX,MAX,MAX,MAX,MAX,MAX,MAX,MAX],
    [MAX,MAX,MAX,MAX,MAX,MAX,MAX,MAX],
    [MAX,MAX,MAX,MAX,MAX,MAX,MAX,MAX],
    [MAX,MAX,MAX,MAX,MAX,MAX,MAX,MAX],
    [MAX,MAX,MAX,MAX,MAX,MAX,MAX,MAX],
    [MAX,MAX,MAX,MAX,MAX,MAX,MAX,MAX],
    [MAX,MAX,MAX,MAX,MAX,MAX,MAX,MAX],
    [MAX,MAX,MAX,MAX,MAX,MAX,MAX,MAX]
    ] #차량으로부터의 거리를 나타내는 2차원 배열 (차량,(0,0),(0,4),(4,0),(4,4),(8,0),(8,4),목적지)
load = [
    [1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1]
    ] #경로를 나타내는 배열

def car_position(): #차량 위치 찾는 함수
    global x
    global y
    global parkinglot
    i=0
    while i<10:
        j=0
        while j<5:
            if parkinglot[i][j] == 4:
                x=i
                y=j
            j = j+1
        i = i+1
    return;

def des_position(): #목적지 위치 찾는 함수
    global pos_num
    global X
    global Y
    global parkinglot
    i=0
    pos_num = 0
    while i<10:
        j=0
        while j<5:
            if parkinglot[i][j] == 2:
                X[pos_num] = i
                Y[pos_num] = j
                pos_num = pos_num + 1
            j = j + 1
        i = i + 1
    return;

def initiate_des_node(): #목적지 위치 초기화 함수
    global des_node
    i=0
    while i<8:
        j=0
        while j<3:
            des_node[i][j] = 0
            j = j + 1
        i = i + 1
    return;

def trans_node(): #목적지까지 가려면 어디로 가야하는지 찾는 함수
    global node_num
    global pos_num
    global X
    global Y
    global des_node
    i=0
    node_num = 0
    initiate_des_node()
    while i<pos_num:
        if X[i] == 1 or X[i] == 5:
            des_node[node_num][0] = X[i] - 1
            des_node[node_num][1] = Y[i]
            des_node[node_num][2] = i + 1
            node_num = node_num + 1
        elif X[i] == 3 or X[i] == 7:
            des_node[node_num][0] = X[i] + 1
            des_node[node_num][1] = Y[i]
            des_node[node_num][2] = i + 1
            node_num = node_num + 1
        elif Y[i] == 1:
            des_node[node_num][0] = X[i]
            des_node[node_num][1] = Y[i] - 1
            des_node[node_num][2] = i + 1
            node_num = node_num + 1
        else:
            des_node[node_num][0] = X[i]
            des_node[node_num][1] = Y[i] + 1
            des_node[node_num][2] = i + 1
            node_num = node_num + 1
        i = i + 1
    return;

def initiate_tracking_node(): #거리 행렬 초기화 함수
    global tracking_node
    i=0
    init = [
     [0  ,MAX,MAX,MAX,MAX,MAX,MAX,MAX],
     [MAX,0  ,4  ,4  ,MAX,MAX,MAX,MAX],
     [MAX,4  ,0  ,MAX,4  ,MAX,MAX,MAX],
     [MAX,4  ,MAX,0  ,4  ,4  ,MAX,MAX],
     [MAX,MAX,4  ,4  ,0  ,MAX,4  ,MAX],
     [MAX,MAX,MAX,4  ,MAX,0  ,4  ,MAX],
     [MAX,MAX,MAX,MAX,4  ,4  ,0  ,MAX],
     [MAX,MAX,MAX,MAX,MAX,MAX,MAX,0  ]
     ]
    while i<8:
        j=0
        while j<8:
            k=0
            while k<8:
                tracking_node[i][j][k] = init[j][k]
                k = k + 1
            j = j + 1
        i = i + 1
    return;

def tracking_start(): #거리행렬에 차량 위치 넣는 함수
    global x
    global y
    global node_num
    global tracking_node
    i=0
    initiate_tracking_node()
    while i < node_num:
        if x == 0 and y == 0:
            tracking_node[i][0][1] = 0
            tracking_node[i][1][0] = 0
        elif x == 0 and y == 4:
            tracking_node[i][0][2] = 0
            tracking_node[i][2][0] = 0
        elif x == 4 and y == 0:
            tracking_node[i][0][3] = 0
            tracking_node[i][3][0] = 0
        elif x == 4 and y == 4:
            tracking_node[i][0][4] = 0
            tracking_node[i][4][0] = 0
        elif x == 8 and y == 0:
            tracking_node[i][0][5] = 0
            tracking_node[i][5][0] = 0
        elif x == 8 and y == 4:
            tracking_node[i][0][6] = 0
            tracking_node[i][6][0] = 0
        elif x >= 9:
            tracking_node[i][0][5] = 1
            tracking_node[i][5][0] = 1
        else:
            if x == 0:
                tracking_node[i][0][1] = y
                tracking_node[i][1][0] = y
                tracking_node[i][0][2] = 4 - y
                tracking_node[i][2][0] = 4 - y
            elif x == 4:
                tracking_node[i][0][3] = y
                tracking_node[i][3][0] = y
                tracking_node[i][0][4] = 4 - y
                tracking_node[i][4][0] = 4 - y
            elif x == 8:
                tracking_node[i][0][5] = y
                tracking_node[i][5][0] = y
                tracking_node[i][0][6] = 4 - y
                tracking_node[i][6][0] = 4 - y
            elif y == 0 and x < 4:
                tracking_node[i][0][1] = x
                tracking_node[i][1][0] = x
                tracking_node[i][0][3] = 4 - x
                tracking_node[i][3][0] = 4 - x
            elif y == 4 and x < 4:
                tracking_node[i][0][2] = x
                tracking_node[i][2][0] = x
                tracking_node[i][0][4] = 4 - x
                tracking_node[i][4][0] = 4 - x
            elif y == 0 and x > 4:
                tracking_node[i][0][3] = x - 4
                tracking_node[i][3][0] = x - 4
                tracking_node[i][0][5] = 8 - x
                tracking_node[i][5][0] = 8 - x
            elif y == 4 and x > 4:
                tracking_node[i][0][4] = x - 4
                tracking_node[i][4][0] = x - 4
                tracking_node[i][0][6] = 8 - x
                tracking_node[i][6][0] = 8 - x
        i = i+1
    return;

def tracking_des(): #거리 행렬에 목적지 위치 넣는 함수
    global node_num
    global des_node
    global tracking_node
    global x
    global y
    i = 0
    while i < node_num:
        if des_node[i][0] == 0:
            tracking_node[i][1][7] = des_node[i][1]
            tracking_node[i][7][1] = des_node[i][1]
            tracking_node[i][2][7] = 4 - des_node[i][1]
            tracking_node[i][7][2] = 4 - des_node[i][1]
            if x == 0:
                if y > des_node[i][1]:
                    tracking_node[i][0][7] = y - des_node[i][1]
                    tracking_node[i][7][0] = y - des_node[i][1]
                elif y > des_node[i][1]:
                    tracking_node[i][0][7] = des_node[i][1] - y
                    tracking_node[i][7][0] = des_node[i][1] - y
                else :
                    tracking_node[i][0][7] = 0
                    tracking_node[i][7][0] = 0
        elif des_node[i][0] == 4:
            tracking_node[i][3][7] = des_node[i][1]
            tracking_node[i][7][3] = des_node[i][1]
            tracking_node[i][4][7] = 4 - des_node[i][1]
            tracking_node[i][7][4] = 4 - des_node[i][1]
            if x == 4:
                if y > des_node[i][1]:
                    tracking_node[i][0][7] = y - des_node[i][1]
                    tracking_node[i][7][0] = y - des_node[i][1]
                elif y > des_node[i][1]:
                    tracking_node[i][0][7] = des_node[i][1] - y
                    tracking_node[i][7][0] = des_node[i][1] - y
                else :
                    tracking_node[i][0][7] = 0
                    tracking_node[i][7][0] = 0
        elif des_node[i][0] == 8:
            tracking_node[i][5][7] = des_node[i][1]
            tracking_node[i][7][5] = des_node[i][1]
            tracking_node[i][6][7] = 4 - des_node[i][1]
            tracking_node[i][7][6] = 4 - des_node[i][1]
            if x == 8:
                if y > des_node[i][1]:
                    tracking_node[i][0][7] = y - des_node[i][1]
                    tracking_node[i][7][0] = y - des_node[i][1]
                elif y > des_node[i][1]:
                    tracking_node[i][0][7] = des_node[i][1] - y
                    tracking_node[i][7][0] = des_node[i][1] - y
                else :
                    tracking_node[i][0][7] = 0
                    tracking_node[i][7][0] = 0
        elif des_node[i][1] == 0 and des_node[i][0] < 4:
            tracking_node[i][1][7] = des_node[i][0]
            tracking_node[i][7][1] = des_node[i][0]
            tracking_node[i][3][7] = 4 - des_node[i][0]
            tracking_node[i][7][3] = 4 - des_node[i][0]
            if y == 0 and x < 4 :
                if x > des_node[i][0]:
                    tracking_node[i][0][7] = x - des_node[i][0]
                    tracking_node[i][7][0] = x - des_node[i][0]
                elif x > des_node[i][0]:
                    tracking_node[i][0][7] = des_node[i][0] - x
                    tracking_node[i][7][0] = des_node[i][0] - x
                else :
                    tracking_node[i][0][7] = 0
                    tracking_node[i][7][0] = 0
        elif des_node[i][1] == 4 and des_node[i][0] < 4:
            tracking_node[i][2][7] = des_node[i][0]
            tracking_node[i][7][2] = des_node[i][0]
            tracking_node[i][4][7] = 4 - des_node[i][0]
            tracking_node[i][7][4] = 4 - des_node[i][0]
            if y == 4 and x < 4 :
                if x > des_node[i][0]:
                    tracking_node[i][0][7] = x - des_node[i][0]
                    tracking_node[i][7][0] = x - des_node[i][0]
                elif x > des_node[i][0]:
                    tracking_node[i][0][7] = des_node[i][0] - x
                    tracking_node[i][7][0] = des_node[i][0] - x
                else :
                    tracking_node[i][0][7] = 0
                    tracking_node[i][7][0] = 0
        elif des_node[i][1] == 0 and des_node[i][0] > 4:
            tracking_node[i][3][7] = des_node[i][0] - 4
            tracking_node[i][7][3] = des_node[i][0] - 4
            tracking_node[i][5][7] = 8 - des_node[i][0]
            tracking_node[i][7][5] = 8 - des_node[i][0]
            if y == 0 and x > 4 :
                if x > des_node[i][0]:
                    tracking_node[i][0][7] = x - des_node[i][0]
                    tracking_node[i][7][0] = x - des_node[i][0]
                elif x > des_node[i][0]:
                    tracking_node[i][0][7] = des_node[i][0] - x
                    tracking_node[i][7][0] = des_node[i][0] - x
                else :
                    tracking_node[i][0][7] = 0
                    tracking_node[i][7][0] = 0
        elif des_node[i][1] == 4 and des_node[i][0] > 4:
            tracking_node[i][4][7] = des_node[i][0] - 4
            tracking_node[i][7][4] = des_node[i][0] - 4
            tracking_node[i][6][7] = 8 - des_node[i][0]
            tracking_node[i][7][6] = 8 - des_node[i][0]
            if y == 4 and x > 4 :
                if x > des_node[i][0]:
                    tracking_node[i][0][7] = x - des_node[i][0]
                    tracking_node[i][7][0] = x - des_node[i][0]
                elif x > des_node[i][0]:
                    tracking_node[i][0][7] = des_node[i][0] - x
                    tracking_node[i][7][0] = des_node[i][0] - x
                else :
                    tracking_node[i][0][7] = 0
                    tracking_node[i][7][0] = 0
        i = i+1
    return;

def dijkstra(): #최단거리와 경로를 찾는 함수
    global node_num
    global flag
    global dist
    global load
    global tracking_node
    k = 0
    temp = 0
    MIN = MAX
    while k<node_num:
        i = 0
        while i < 8:
            flag[i] = 0
            dist[k][i] = MAX
            load[k][i] = 1
            i = i + 1
        dist[k][0] = 0
        i = 0
        while i < 8:
            MIN = MAX
            j = 0
            while j < 8:
                if MIN > dist[k][j] and flag[j] == 0:
                    MIN = dist[k][j]
                    temp = j
                j = j + 1
            flag[temp] = 1
            j = 0
            while j < 8:
                if dist[k][j] > tracking_node[k][temp][j] + dist[k][temp] and tracking_node[k][temp][j] != MAX:
                    dist[k][j] = tracking_node[k][temp][j] + dist[k][temp]
                    load[k][j] = load[k][temp] * 10 + j + 1
                j = j + 1
            i = i + 1
        k = k + 1
    return;

def tracking(dest): #경로에 따라 불을 켜는 함수
    global load
    global parkinglot
    global x
    global y
    global des_node
    node_a = 1
    node_b = 1
    j = 0
    temp = load[dest][7]
    while temp >10 :
        node_a = temp % 10
        temp = int(temp / 10)
        node_b = temp % 10
        if node_a != 8:
            if node_a == 2:
                if node_b == 3:
                    parkinglot[0][0] = 1
                    parkinglot[0][1] = 1
                    parkinglot[0][2] = 1
                    parkinglot[0][3] = 1
                    parkinglot[0][4] = 1
                elif node_b == 4:
                    parkinglot[0][0] = 1
                    parkinglot[1][0] = 1
                    parkinglot[2][0] = 1
                    parkinglot[3][0] = 1
                    parkinglot[4][0] = 1
                else:
                    if x == 0:
                        j = 0
                        while j < y:
                            parkinglot[0][j] = 1
                            j = j + 1
                    else :
                        j = 0
                        while j < x:
                            parkinglot[j][0] = 1
                            j = j + 1
            elif node_a == 3:
                if node_b == 2:
                    parkinglot[0][0] = 1
                    parkinglot[0][1] = 1
                    parkinglot[0][2] = 1
                    parkinglot[0][3] = 1
                    parkinglot[0][4] = 1
                elif node_b == 5:
                    parkinglot[0][4] = 1
                    parkinglot[1][4] = 1
                    parkinglot[2][4] = 1
                    parkinglot[3][4] = 1
                    parkinglot[4][4] = 1
                else:
                    if x == 0:
                        j = 4
                        while j > y:
                            parkinglot[0][j] = 1
                            j = j - 1
                    else :
                        j = 0
                        while j < x:
                            parkinglot[j][4] = 1
                            j = j + 1
            elif node_a == 4:
                if node_b == 2:
                    parkinglot[0][0] = 1
                    parkinglot[1][0] = 1
                    parkinglot[2][0] = 1
                    parkinglot[3][0] = 1
                    parkinglot[4][0] = 1
                elif node_b == 5:
                    parkinglot[4][0] = 1
                    parkinglot[4][1] = 1
                    parkinglot[4][2] = 1
                    parkinglot[4][3] = 1
                    parkinglot[4][4] = 1
                elif node_b == 6:
                    parkinglot[4][0] = 1
                    parkinglot[5][0] = 1
                    parkinglot[6][0] = 1
                    parkinglot[7][0] = 1
                    parkinglot[8][0] = 1
                else:
                    if x == 4:
                        j = 0
                        while j < y:
                            parkinglot[4][j] = 1
                            j = j + 1
                    else :
                        if x < 4:
                            j = 4
                            while j > x:
                                parkinglot[j][0] = 1
                                j = j - 1
                        else:
                            j = 4
                            while j < x:
                                parkinglot[j][0] = 1
                                j = j + 1
            elif node_a == 5:
                if node_b == 3:
                    parkinglot[0][4] = 1
                    parkinglot[1][4] = 1
                    parkinglot[2][4] = 1
                    parkinglot[3][4] = 1
                    parkinglot[4][4] = 1
                elif node_b == 4:
                    parkinglot[4][0] = 1
                    parkinglot[4][1] = 1
                    parkinglot[4][2] = 1
                    parkinglot[4][3] = 1
                    parkinglot[4][4] = 1
                elif node_b == 7:
                    parkinglot[4][4] = 1
                    parkinglot[5][4] = 1
                    parkinglot[6][4] = 1
                    parkinglot[7][4] = 1
                    parkinglot[8][4] = 1
                else:
                    if x == 4:
                        j = 4
                        while j > y:
                            parkinglot[4][j] = 1
                            j = j - 1
                    else :
                        if x < 4:
                            j = 4
                            while j > x:
                                parkinglot[j][4] = 1
                                j = j - 1
                        else:
                            j = 4
                            while j < x:
                                parkinglot[j][4] = 1
                                j = j + 1
            elif node_a == 6:
                if node_b == 4:
                    parkinglot[4][0] = 1
                    parkinglot[5][0] = 1
                    parkinglot[6][0] = 1
                    parkinglot[7][0] = 1
                    parkinglot[8][0] = 1
                elif node_b == 7:
                    parkinglot[8][0] = 1
                    parkinglot[8][1] = 1
                    parkinglot[8][2] = 1
                    parkinglot[8][3] = 1
                    parkinglot[8][4] = 1
                else:
                    if x == 8:
                        j = 0
                        while j < y:
                            parkinglot[8][j] = 1
                            j = j + 1
                    else :
                        if x < 8:
                            j = 8
                            while j > x:
                                parkinglot[j][0] = 1
                                j = j - 1
                        else:
                            j = 8
                            while j < x:
                                parkinglot[j][0] = 1
                                j = j + 1
            elif node_a == 7:
                if node_b == 5:
                    parkinglot[4][4] = 1
                    parkinglot[5][4] = 1
                    parkinglot[6][4] = 1
                    parkinglot[7][4] = 1
                    parkinglot[8][4] = 1
                elif node_b == 6:
                    parkinglot[8][0] = 1
                    parkinglot[8][1] = 1
                    parkinglot[8][2] = 1
                    parkinglot[8][3] = 1
                    parkinglot[8][4] = 1
                else:
                    if x == 8:
                        j = 4
                        while j > y:
                            parkinglot[8][j] = 1
                            j = j - 1
                    else :
                        j = 8
                        while j > x:
                            parkinglot[j][4] = 1
                            j = j - 1
            if parkinglot[x][y] == 1:
                parkinglot[x][y] = 4
        else:
            if node_b == 1:
                if x == des_node[dest][0]:
                    if y < des_node[dest][1]:
                        j = des_node[dest][1]
                        while j > y:
                            parkinglot[x][j] = 1
                            j = j - 1
                    else:
                        j = des_node[dest][1]
                        while j < y:
                            parkinglot[x][j] = 1
                            j = j + 1
                else:
                    if x < des_node[dest][0]:
                        j = des_node[dest][0]
                        while j > x:
                            parkinglot[j][y] = 1
                            j = j - 1
                    else:
                        j = des_node[dest][0]
                        while j < x:
                            parkinglot[j][y] = 1
                            j = j + 1
            else:
                if node_b == 2:
                    if des_node[dest][0] == 0:
                        j = 0
                        while j <= des_node[dest][1]:
                            parkinglot[0][j] = 1
                            j = j + 1
                    else:
                        j = 0
                        while j <= des_node[dest][0]:
                            parkinglot[j][0] = 1
                            j = j + 1
                elif node_b == 3:
                    if des_node[dest][0] == 0:
                        j = 4
                        while j >= des_node[dest][1]:
                            parkinglot[0][j] = 1
                            j = j - 1
                    else:
                        j = 0
                        while j <= des_node[dest][0]:
                            parkinglot[j][4] = 1
                            j = j + 1
                elif node_b == 4:
                    if des_node[dest][0] == 4:
                        j = 0
                        while j <= des_node[dest][1]:
                            parkinglot[4][j] = 1
                            j = j + 1
                    elif des_node[dest][0] < 4:
                        j = 4
                        while j >= des_node[dest][0]:
                            parkinglot[j][0] = 1
                            j = j - 1
                    else:
                        j = 4
                        while j <= des_node[dest][0]:
                            parkinglot[j][0] = 1
                            j = j + 1
                elif node_b == 5:
                    if des_node[dest][0] == 4:
                        j = 4
                        while j >= des_node[dest][1]:
                            parkinglot[4][j] = 1
                            j = j - 1
                    elif des_node[dest][0] < 4:
                        j = 4
                        while j >= des_node[dest][0]:
                            parkinglot[j][4] = 1
                            j = j - 1
                    else:
                        j = 4
                        while j <= des_node[dest][0]:
                            parkinglot[j][4] = 1
                            j = j + 1
                elif node_b == 6:
                    if des_node[dest][0] == 8:
                        j = 0
                        while j <= des_node[dest][1]:
                            parkinglot[8][j] = 1
                            j = j + 1
                    else:
                        j = 8
                        while j >= des_node[dest][0]:
                            parkinglot[j][0] = 1
                            j = j - 1
                else:
                    if des_node[dest][0] == 8:
                        j = 4
                        while j >= des_node[dest][1]:
                            parkinglot[8][j] = 1
                            j = j - 1
                    else:
                        j = 8
                        while j >= des_node[dest][0]:
                            parkinglot[j][4] = 1
                            j = j - 1
            parkinglot[des_node[dest][0]][des_node[dest][1]] = 6
    return;

def initiate_led(): #LED초기화 함수
    global parkinglot
    i = 0
    while i < 10:
        j = 0
        while j < 5:
            if parkinglot[i][j] == 1 or parkinglot[i][j] == 6:
                parkinglot[i][j] = 0
            j = j + 1
        i = i + 1
    return;

def update_tracking(): #경로를 벗어났을때 새로 경로 찾는 함수
    destination = 0
    initiate_led()
    car_position()
    des_position()
    trans_node()
    tracking_start()
    tracking_des()
    dijkstra()
    i = 0
    MIN = MAX
    while i < node_num:
        if MIN > dist[i][7]:
            MIN = dist[i][7]
            destination = i
        i = i + 1
    tracking(destination)
    return;

def print_parking_lot(): #주차장 데이터를 출력하는 함수
    global parkinglot
    global Massenger
    i = 0
    display = [
        ["○","○","○","○","○"],
        ["○","○","○","○","○"],
        ["○","○","○","○","○"],
        ["○","○","○","○","○"],
        ["○","○","○","○","○"],
        ["○","○","○","○","○"],
        ["○","○","○","○","○"],
        ["○","○","○","○","○"],
        ["○","○","○","○","○"],
        ["○","○","○","○","○"]
        ]
    while i < 10:
        j = 0
        msg = ''
        while j < 5:
            if parkinglot[i][j] == 0:
                display[i][j] = "○" #꺼진 led
                #msg = str(i)+':'+str(j)+':'+'0'
            elif parkinglot[i][j] == 1:
                display[i][j] = "●" #켜진 led
                msg = str(i)+':'+str(j)+':'+'1'+':'+'0'
            elif parkinglot[i][j] == 2:
                display[i][j] = "□" #빈자리
            elif parkinglot[i][j] == 3:
                display[i][j] = "■" #주차된 자리
            elif parkinglot[i][j] == 4:
                display[i][j] = "★" #차량
            elif parkinglot[i][j] == 6:
                display[i][j] = "☆" #도착지점을 알려주는 지점
                msg = str(i)+':'+str(j)+':'+'2'+':'+'0'
            else:
                display[i][j] = "※"
            j = j + 1
        Massenger.append(msg)
        i = i + 1
    i = 0
    while i < 10:
        print(display[i])
        i = i + 1
    return;

def main():
    global parkinglot
    global x
    global y
    global DBCONN
    print_parking_lot()
    print(" ")
    print(" ")
    roop = 1
    parseMap()
    while roop == 1:
        destination = 0
        initiate_led()
        car_position()
        des_position()
        trans_node()
        ##if pos_num == 0:
        ##    print("빈 자리가 없습니다.")
        ##    roop = 0
        if True:
            tracking_start()
            tracking_des()
            dijkstra()
            i = 0
            MIN = MAX
            while i < node_num:
                if MIN > dist[i][7]:
                    MIN = dist[i][7]
                    destination = i
                i = i + 1
            tracking(destination)
            print_parking_lot()
            print(" ")
            print(" ")
            break
            """
            con = 1
            while con == 1:
                key = input("이동중(wsad로 이동, q로 강제 종료): ")
                if key == "q":
                    print("종료합니다")
                    con = 0
                    roop = 0
                else:
                    if key == "w":
                        if x != 0:
                            if parkinglot[x - 1][y] == 1:
                                parkinglot[x][y] = 0
                                parkinglot[x - 1][y] = 4
                                x = x - 1
                                print_parking_lot()
                                print("위로 이동")
                                print(" ")
                                print(" ")
                            elif parkinglot[x - 1][y] == 0:
                                parkinglot[x][y] = 0
                                parkinglot[x - 1][y] = 4
                                update_tracking()
                                print_parking_lot()
                                print("경로 이탈")
                                print(" ")
                                print(" ")
                            elif parkinglot[x - 1][y] == 6:
                                parkinglot[x][y] = 0
                                parkinglot[x - 1][y] = 4
                                x = x - 1
                                print_parking_lot()
                                print("근처에 주차할 자리가 있습니다.")
                                print(" ")
                                print(" ")
                            elif parkinglot[x - 1][y] == 2:
                                parkinglot[x][y] = 0
                                parkinglot[x - 1][y] = 3
                                print_parking_lot()
                                roop2 = 1
                                keep = input("주차 성공! 차량을 더 들이겠습니까?(y/n) :")
                                while roop2 == 1:
                                    if keep == "y":
                                        parkinglot[9][0] = 4
                                        print(" ")
                                        print(" ")
                                        con = 0
                                        roop2 = 0
                                    elif keep == "n":
                                        print(" ")
                                        print(" ")
                                        print("종료합니다")
                                        con = 0
                                        roop = 0
                                        roop2 = 0
                                    else:
                                        print(" ")
                                        print(" ")
                                        print_parking_lot()
                                        keep = input("잘못 누르셨습니다. 다시 입력하십시오.(y/n) :")
                            else:
                                print(" ")
                                print(" ")
                                print_parking_lot()
                                print("이동할 수 없습니다.")
                                print(" ")
                                print(" ")
                        else:
                            print(" ")
                            print(" ")
                            print_parking_lot()
                            print("이동할 수 없습니다.")
                            print(" ")
                            print(" ")
                    elif key == "s":
                        if x != 9:
                            if parkinglot[x + 1][y] == 1:
                                parkinglot[x][y] = 0
                                parkinglot[x + 1][y] = 4
                                x = x + 1
                                print_parking_lot()
                                print("아래로 이동")
                                print(" ")
                                print(" ")
                            elif parkinglot[x + 1][y] == 0:
                                parkinglot[x][y] = 0
                                parkinglot[x + 1][y] = 4
                                update_tracking()
                                print_parking_lot()
                                print("경로 이탈")
                                print(" ")
                                print(" ")
                            elif parkinglot[x + 1][y] == 6:
                                parkinglot[x][y] = 0
                                parkinglot[x + 1][y] = 4
                                x = x + 1
                                print_parking_lot()
                                print("근처에 주차할 자리가 있습니다.")
                                print(" ")
                                print(" ")
                            elif parkinglot[x + 1][y] == 2:
                                parkinglot[x][y] = 0
                                parkinglot[x + 1][y] = 3
                                print_parking_lot()
                                roop2 = 1
                                keep = input("주차 성공! 차량을 더 들이겠습니까?(y/n) :")
                                while roop2 == 1:
                                    if keep == "y":
                                        parkinglot[9][0] = 4
                                        print(" ")
                                        print(" ")
                                        con = 0
                                        roop2 = 0
                                    elif keep == "n":
                                        print(" ")
                                        print(" ")
                                        print("종료합니다")
                                        con = 0
                                        roop = 0
                                        roop2 = 0
                                    else:
                                        print(" ")
                                        print(" ")
                                        print_parking_lot()
                                        keep = input("잘못 누르셨습니다. 다시 입력하십시오.(y/n) :")
                            else:
                                print(" ")
                                print(" ")
                                print_parking_lot()
                                print("이동할 수 없습니다.")
                                print(" ")
                                print(" ")
                        else:
                            print(" ")
                            print(" ")
                            print_parking_lot()
                            print("이동할 수 없습니다.")
                            print(" ")
                            print(" ")
                    elif key == "a":
                        if y != 0:
                            if parkinglot[x][y - 1] == 1:
                                parkinglot[x][y] = 0
                                parkinglot[x][y - 1] = 4
                                y = y - 1
                                print_parking_lot()
                                print("왼쪽으로 이동")
                                print(" ")
                                print(" ")
                            elif parkinglot[x][y - 1] == 0:
                                parkinglot[x][y] = 0
                                parkinglot[x][y - 1] = 4
                                update_tracking()
                                print_parking_lot()
                                print("경로 이탈")
                                print(" ")
                                print(" ")
                            elif parkinglot[x][y - 1] == 6:
                                parkinglot[x][y] = 0
                                parkinglot[x][y - 1] = 4
                                y = y - 1
                                print_parking_lot()
                                print("근처에 주차할 자리가 있습니다.")
                                print(" ")
                                print(" ")
                            elif parkinglot[x][y - 1] == 2:
                                parkinglot[x][y] = 0
                                parkinglot[x][y - 1] = 3
                                print_parking_lot()
                                roop2 = 1
                                keep = input("주차 성공! 차량을 더 들이겠습니까?(y/n) :")
                                while roop2 == 1:
                                    if keep == "y":
                                        parkinglot[9][0] = 4
                                        print(" ")
                                        print(" ")
                                        con = 0
                                        roop2 = 0
                                    elif keep == "n":
                                        print(" ")
                                        print(" ")
                                        print("종료합니다")
                                        con = 0
                                        roop = 0
                                        roop2 = 0
                                    else:
                                        print(" ")
                                        print(" ")
                                        print_parking_lot()
                                        keep = input("잘못 누르셨습니다. 다시 입력하십시오.(y/n) :")
                            else:
                                print(" ")
                                print(" ")
                                print_parking_lot()
                                print("이동할 수 없습니다.")
                                print(" ")
                                print(" ")
                        else:
                            print(" ")
                            print(" ")
                            print_parking_lot()
                            print("이동할 수 없습니다.")
                            print(" ")
                            print(" ")
                    elif key == "d":
                        if y != 4:
                            if parkinglot[x][y + 1] == 1:
                                parkinglot[x][y] = 0
                                parkinglot[x][y + 1] = 4
                                y = y + 1
                                print_parking_lot()
                                print("오른쪽으로 이동")
                                print(" ")
                                print(" ")
                            elif parkinglot[x][y + 1] == 0:
                                parkinglot[x][y] = 0
                                parkinglot[x][y + 1] = 4
                                update_tracking()
                                print_parking_lot()
                                print("경로 이탈")
                                print(" ")
                                print(" ")
                            elif parkinglot[x][y + 1] == 6:
                                parkinglot[x][y] = 0
                                parkinglot[x][y + 1] = 4
                                y = y + 1
                                print_parking_lot()
                                print("근처에 주차할 자리가 있습니다.")
                                print(" ")
                                print(" ")
                            elif parkinglot[x][y + 1] == 2:
                                parkinglot[x][y] = 0
                                parkinglot[x][y + 1] = 3
                                print_parking_lot()
                                roop2 = 1
                                keep = input("주차 성공! 차량을 더 들이겠습니까?(y/n) :")
                                while roop2 == 1:
                                    if keep == "y":
                                        parkinglot[9][0] = 4
                                        print(" ")
                                        print(" ")
                                        con = 0
                                        roop2 = 0
                                    elif keep == "n":
                                        print(" ")
                                        print(" ")
                                        print("종료합니다")
                                        con = 0
                                        roop = 0
                                        roop2 = 0
                                    else:
                                        print(" ")
                                        print(" ")
                                        print_parking_lot()
                                        keep = input("잘못 누르셨습니다. 다시 입력하십시오.(y/n) :")
                            else:
                                print(" ")
                                print(" ")
                                print_parking_lot()
                                print("이동할 수 없습니다.")
                                print(" ")
                                print(" ")
                        else:
                            print(" ")
                            print(" ")
                            print_parking_lot()
                            print("이동할 수 없습니다.")
                            print(" ")
                            print(" ")
                    else:
                        print(" ")
                        print(" ")
                        print_parking_lot()
                        print("명령 거부")
                        print(" ")
                        print(" ")
                        
    """
            
def updateDB(MAPDATA):
    DBCONN = pymysql.connect(host = 'localhost',
                           user = 'root',
                           password = None,
                           db = 'car_map_data',
                           charset = 'utf8')
    with DBCONN.cursor() as cursor:
            sql = 'UPDATE map SET car = %s, parked = %s WHERE x = %s and y = %s'
            cursor.execute(sql, (MAPDATA[2], MAPDATA[3], MAPDATA[0], MAPDATA[1]))
            DBCONN.commit()
    DBCONN.close()
    
def Binding(port):
    s = socket.socket()
    host = ''
    s.bind((host,port))
    s.listen(5)
    return s

def splitDatas(MAPSECTOR):
    for i in range(len(MAPSECTOR)):
            MAPDATA = MAPSECTOR[i].split(':')
            updateDB(MAPDATA)

def sendData(c, addr):
    i = 0
    data = '0:8:1:0'
     
    print(data)
    byte_data = str.encode(data)
    c.sendall(byte_data)
    
    
def read(s):
    try:
        msg = s.recv(1024)
        s.close()
    except socket.error as msg:
        sys.stderr.write('error %s' %msg[1])
        s.close()
        print('close')
        sys.exit(2)
    return msg

def readData(s):
        print('data is received')
        data = read(s).decode('utf-8')
        print(' %s' % data)
        #splitDatas(data.split(','))
        
def thread(s):
    c, addr = s.accept()
    sendData(c, addr)
    readData(c)

def server():
    if __name__ == '__main__':
        port = 12345
        port2 = 32000
        s = Binding(port)
        s2 = Binding(port2)
        while True:
            main()
            thread(s)
            #print(port)
            #thread(s2)
            #print(port2)
#server()
            
server()

