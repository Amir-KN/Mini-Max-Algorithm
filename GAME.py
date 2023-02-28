import turtle
import math
import random
import copy
import time
from time import sleep
from sys import argv

# CA2-Game-Amirhossein Kahrobaeian-810199478

seen_states = [0]
class Sim:
    # Set true for graphical interface
    GUI = False
    screen = None
    selection = []
    turn = ''
    dots = []
    red = []
    blue = []
    available_moves = []
    minimax_depth = 0
    prune = False

    def __init__(self, minimax_depth, prune, gui):
        self.GUI = gui
        self.prune = prune
        self.minimax_depth = minimax_depth
        if self.GUI:
            self.setup_screen()

    def setup_screen(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 800)
        self.screen.title("Game of SIM")
        self.screen.setworldcoordinates(-1.5, -1.5, 1.5, 1.5)
        self.screen.tracer(0, 0)
        turtle.hideturtle()

    def draw_dot(self, x, y, color):
        turtle.up()
        turtle.goto(x, y)
        turtle.color(color)
        turtle.dot(15)

    def gen_dots(self):
        r = []
        for angle in range(0, 360, 60):
            r.append((math.cos(math.radians(angle)), math.sin(math.radians(angle))))
        return r

    def initialize(self):
        self.selection = []
        self.available_moves = []
        for i in range(0, 6):
            for j in range(i, 6):
                if i != j:
                    self.available_moves.append((i, j))
                    
        if random.randint(0, 2) == 1:
            self.turn = 'red'
        else:
            self.turn = 'blue'
        self.dots = self.gen_dots()
        self.red = []
        self.blue = []
        if self.GUI: turtle.clear()
        self.draw()

    def draw_line(self, p1, p2, color):
        turtle.up()
        turtle.pensize(3)
        turtle.goto(p1)
        turtle.down()
        turtle.color(color)
        turtle.goto(p2)

    def draw_board(self):
        for i in range(len(self.dots)):
            if i in self.selection:
                self.draw_dot(self.dots[i][0], self.dots[i][1], self.turn)
            else:
                self.draw_dot(self.dots[i][0], self.dots[i][1], 'dark gray')

    def draw(self):
        if not self.GUI: return 0
        self.draw_board()
        for i in range(len(self.red)):
            self.draw_line((math.cos(math.radians(self.red[i][0] * 60)), math.sin(math.radians(self.red[i][0] * 60))),
                           (math.cos(math.radians(self.red[i][1] * 60)), math.sin(math.radians(self.red[i][1] * 60))),
                           'red')
        for i in range(len(self.blue)):
            self.draw_line((math.cos(math.radians(self.blue[i][0] * 60)), math.sin(math.radians(self.blue[i][0] * 60))),
                           (math.cos(math.radians(self.blue[i][1] * 60)), math.sin(math.radians(self.blue[i][1] * 60))),
                           'blue')
        self.screen.update()
        sleep(1)
                
    def _evaluate(red, blue):
        result = 0
        blue_to = dict(zip(range(6), (0 for _ in range(6))) )
        red_to = dict(zip(range(6), (0 for _ in range(6))) )
        for sel in blue:
            blue_to[sel[0]] += 1
        for sel in red :    
            red_to[sel[0]] += 1
        for num in blue_to.values() :
            if num > 1 :
                result += (num*(num-1))//2
        for num in red_to.values() :
            if num > 1 :
                result -= (num*(num-1))//2

        return result

    def create_new_game(red, blue, available_moves, select, turn ) :
        if select[1] < select[0]:
            select = (select[1], select[0])
        new_red, new_blue  = copy.deepcopy(red), copy.deepcopy(blue)
        if turn == 'red':
            new_red.append(select)
        else:  
            new_blue.append(select)

        new_available_moves = copy.deepcopy(available_moves)
        new_available_moves.remove(select)
        random.shuffle(new_available_moves)
        return new_red, new_blue, new_available_moves

    def pruning_minimax(depth, max_val, min_val, red, blue, available_moves, player_turn):
        seen_states[0] += 1
        r = Sim.gameover(red, blue)
        if r != 0 :
            if r == "blue" :
                return (-float("inf"), None)
            elif r == "red" :
                return (float("inf"), None)
        if depth == 0 :
            return (Sim._evaluate(red, blue), None)

        random.shuffle(available_moves)
        final_move_r, final_move_b = None, None
        if player_turn == "red" :
            max_res = -float("inf")
            for move in available_moves :
                new_red, new_blue, new_avaliable_moves = Sim.create_new_game(red, blue, available_moves, move, "red")
                max_temp = Sim.minimax(depth-1, new_red, new_blue, new_avaliable_moves, "blue")[0]
                if max_temp >= max_res :
                    max_res, final_move_r = max_temp, move
                
                if max_res >= min_val :
                    return (max_res, final_move_r)
                max_val = max(max_res, max_val)
            return max_res, final_move_r
        
        else :
            min_res = float('inf')
            for move in available_moves :
                new_red, new_blue, new_avaliable_moves = Sim.create_new_game(red, blue, available_moves, move, "blue")
                min_temp = Sim.minimax(depth-1, new_red, new_blue, new_avaliable_moves, "red")[0]
                if min_temp <= min_res :
                    min_res, final_move_b = min_temp, move

                if min_res <= max_val :
                    return (min_res, final_move_b)
                min_val = min(min_res, min_val)
            return min_res, final_move_b

    def minimax(depth, red, blue, available_moves, player_turn):
        seen_states[0] += 1
        r = Sim.gameover(red, blue)
        if r != 0 :
            if r == "blue" :
                return (-float("inf"), None)
            elif r == "red" :
                return (float("inf"), None)
        if depth == 0 :
            return (Sim._evaluate(red, blue), None)

        random.shuffle(available_moves)
        final_move_r, final_move_b = None, None
        if player_turn == "red" :
            max_res = -float("inf")
            for move in available_moves :
                new_red, new_blue, new_avaliable_moves = Sim.create_new_game(red, blue, available_moves, move, "red")
                max_temp = Sim.minimax(depth-1, new_red, new_blue, new_avaliable_moves, "blue")[0]
                if max_temp >= max_res :
                    max_res, final_move_r = max_temp, move
            return max_res, final_move_r
        
        else :
            min_res = float('inf')
            for move in available_moves :
                new_red, new_blue, new_avaliable_moves = Sim.create_new_game(red, blue, available_moves, move, "blue")
                min_temp = Sim.minimax(depth-1, new_red, new_blue, new_avaliable_moves, "red")[0]
                if min_temp <= min_res :
                    min_res, final_move_b = min_temp, move
            return min_res, final_move_b
        
    def enemy(self):
        return random.choice(self.available_moves)

    def _swap_turn(self, turn):
        if turn == "red":
            return "blue"
        else:
            return "red"

    def play(self):
        self.initialize()
        while True:
            if self.turn == 'red':
                if self.prune :
                    selection = Sim.pruning_minimax(depth=self.minimax_depth,max_val=-float("inf")\
                        ,min_val=float("inf"), red=self.red,blue=self.blue,\
                        available_moves=self.available_moves, player_turn=self.turn)[1]
                else :
                    selection = Sim.minimax(depth=self.minimax_depth, red=self.red, blue=self.blue\
                                , available_moves=self.available_moves, player_turn=self.turn)[1]
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            else:
                selection = self.enemy()
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            if selection in self.red or selection in self.blue:
                raise Exception("Duplicate Move!!!")
            if self.turn == 'red':
                self.red.append(selection)
            else:
                self.blue.append(selection)

            self.available_moves.remove(selection)
            self.turn = self._swap_turn(self.turn)
            selection = []
            self.draw()
            r = Sim.gameover(self.red, self.blue)
            if r != 0:
                return r

    def gameover(r, b):
        if len(r) >= 3:
            r.sort()
            for i in range(len(r) - 2):
                for j in range(i + 1, len(r) - 1):
                    for k in range(j + 1, len(r)):
                        if r[i][0] == r[j][0] and r[i][1] == r[k][0] and r[j][1] == r[k][1]:
                            return 'blue'
        if len(b) >= 3:
            b.sort()
            for i in range(len(b) - 2):
                for j in range(i + 1, len(b) - 1):
                    for k in range(j + 1, len(b)):
                        if b[i][0] == b[j][0] and b[i][1] == b[k][0] and b[j][1] == b[k][1]:
                            return 'red'
        return 0


if __name__=="__main__":

    game = Sim(minimax_depth=int(argv[1]), prune=True, gui=bool(int(argv[2])))
    results = {"red": 0, "blue": 0}
    n = 2
    s_time = time.time()

    for i in range(n):
        winner = game.play()
        results[winner] += 1
        print(f"Winner of Round {i+1} is {winner}")

    e_time = time.time()
    print("Depth :", argv[1], "& Number Of Play Game(n) : ", n)
    print("Winning Chance : ", results["red"]/(results["red"] + results['blue']))
    print("Mean Execution Time : ", (e_time-s_time)/n)
    print("Mean Seen States : ", seen_states[0]//n )

    