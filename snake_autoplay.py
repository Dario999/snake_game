import pygame
from random import randrange
import time
import sys
import math
import random
import bisect
from sys import maxsize as infinity

import sys
import math
import random
import bisect
from sys import maxsize as infinity


class Problem:
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def successor(self, state):
        raise NotImplementedError

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self):
        raise NotImplementedError




class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0  # search depth
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):

        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        return Node(next_state, self, action,
                    problem.path_cost(self.path_cost, self.state,
                                      action, next_state))

    def solution(self):
        return [node.action for node in self.path()[1:]]

    def solve(self):
        return [node.state for node in self.path()[0:]]

    def path(self):
        x, result = self, []
        while x:
            result.append(x)
            x = x.parent
        result.reverse()
        return result


    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)




class Queue:

    def __init__(self):
        raise NotImplementedError

    def append(self, item):
        raise NotImplementedError

    def extend(self, items):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __contains__(self, item):
        raise NotImplementedError


class Stack(Queue):


    def __init__(self):
        self.data = []

    def append(self, item):
        self.data.append(item)

    def extend(self, items):
        self.data.extend(items)

    def pop(self):
        return self.data.pop()

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return item in self.data


class FIFOQueue(Queue):


    def __init__(self):
        self.data = []

    def append(self, item):
        self.data.append(item)

    def extend(self, items):
        self.data.extend(items)

    def pop(self):
        return self.data.pop(0)

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return item in self.data


class PriorityQueue(Queue):


    def __init__(self, order=min, f=lambda x: x):
        assert order in [min, max]
        self.data = []
        self.order = order
        self.f = f

    def append(self, item):
        bisect.insort_right(self.data, (self.f(item), item))

    def extend(self, items):
        for item in items:
            bisect.insort_right(self.data, (self.f(item), item))

    def pop(self):
        if self.order == min:
            return self.data.pop(0)[1]
        return self.data.pop()[1]

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return any(item == pair[1] for pair in self.data)

    def __getitem__(self, key):
        for _, item in self.data:
            if item == key:
                return item

    def __delitem__(self, key):
        for i, (value, item) in enumerate(self.data):
            if item == key:
                self.data.pop(i)




def tree_search(problem, fringe):
    fringe.append(Node(problem.initial))
    while fringe:
        node = fringe.pop()
        print(node.state)
        if problem.goal_test(node.state):
            return node
        fringe.extend(node.expand(problem))
    return None


def breadth_first_tree_search(problem):
    return tree_search(problem, FIFOQueue())


def depth_first_tree_search(problem):
    return tree_search(problem, Stack())




def graph_search(problem, fringe):
    closed = set()
    fringe.append(Node(problem.initial))
    while fringe:
        node = fringe.pop()
        if problem.goal_test(node.state):
            return node
        if node.state not in closed:
            closed.add(node.state)
            fringe.extend(node.expand(problem))
    return None


def breadth_first_graph_search(problem):
    return graph_search(problem, FIFOQueue())


def depth_first_graph_search(problem):
    return graph_search(problem, Stack())


def depth_limited_search(problem, limit=50):
    def recursive_dls(node, problem, limit):
        cutoff_occurred = False
        if problem.goal_test(node.state):
            return node
        elif node.depth == limit:
            return 'cutoff'
        else:
            for successor in node.expand(problem):
                result = recursive_dls(successor, problem, limit)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
        if cutoff_occurred:
            return 'cutoff'
        return None

    return recursive_dls(Node(problem.initial), problem, limit)


def iterative_deepening_search(problem):
    for depth in range(sys.maxsize):
        result = depth_limited_search(problem, depth)
        if result is not 'cutoff':
            return result


def uniform_cost_search(problem):

    return graph_search(problem, PriorityQueue(min, lambda a: a.path_cost))




def memoize(fn, slot=None):
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        def memoized_fn(*args):
            if args not in memoized_fn.cache:
                memoized_fn.cache[args] = fn(*args)
            return memoized_fn.cache[args]

        memoized_fn.cache = {}
    return memoized_fn


def best_first_graph_search(problem, f):
    f = memoize(f, 'f')
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = PriorityQueue(min, f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                incumbent = frontier[child]
                if f(child) < f(incumbent):
                    del frontier[incumbent]
                    frontier.append(child)
    return None


def greedy_best_first_graph_search(problem, h=None):
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, h)


def astar_search(problem, h=None):
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


def recursive_best_first_search(problem, h=None):
    h = memoize(h or problem.h, 'h')

    def RBFS(problem, node, flimit):
        if problem.goal_test(node.state):
            return node, 0
        successors = node.expand(problem)
        if len(successors) == 0:
            return None, infinity
        for s in successors:
            s.f = max(s.path_cost + h(s), node.f)
        while True:
            successors.sort(key=lambda x: x.f)
            best = successors[0]
            if best.f > flimit:
                return None, best.f
            if len(successors) > 1:
                alternative = successors[1].f
            else:
                alternative = infinity
            result, best.f = RBFS(problem, best, min(flimit, alternative))
            if result is not None:
                return result, best.f

    node = Node(problem.initial)
    node.f = h(node)
    result, bestf = RBFS(problem, node, infinity)
    return result




def distance(a, b):

    return math.hypot((a[0] - b[0]), (a[1] - b[1]))


class Graph:
    def __init__(self, dictionary=None, directed=True):
        self.dict = dictionary or {}
        self.directed = directed
        if not directed:
            self.make_undirected()
        else:
            nodes_no_edges = list({y for x in self.dict.values()
                                   for y in x if y not in self.dict})
            for node in nodes_no_edges:
                self.dict[node] = {}

    def make_undirected(self):
        for a in list(self.dict.keys()):
            for (b, dist) in self.dict[a].items():
                self.connect1(b, a, dist)

    def connect(self, node_a, node_b, distance_val=1):
        self.connect1(node_a, node_b, distance_val)
        if not self.directed:
            self.connect1(node_b, node_a, distance_val)

    def connect1(self, node_a, node_b, distance_val):
        self.dict.setdefault(node_a, {})[node_b] = distance_val

    def get(self, a, b=None):
        links = self.dict.get(a)
        if b is None:
            return links
        else:
            return links.get(b)

    def nodes(self):

        return list(self.dict.keys())


def UndirectedGraph(dictionary=None):
    return Graph(dictionary=dictionary, directed=False)


def RandomGraph(nodes=list(range(10)), min_links=2, width=400, height=300,
                curvature=lambda: random.uniform(1.1, 1.5)):
    g = UndirectedGraph()
    g.locations = {}
    # Build the cities
    for node in nodes:
        g.locations[node] = (random.randrange(width), random.randrange(height))
    # Build roads from each city to at least min_links nearest neighbors.
    for i in range(min_links):
        for node in nodes:
            if len(g.get(node)) < min_links:
                here = g.locations[node]

                def distance_to_node(n):
                    if n is node or g.get(node, n):
                        return math.inf
                    return distance(g.locations[n], here)

                neighbor = nodes.index(min(nodes, key=distance_to_node))
                d = distance(g.locations[neighbor], here) * curvature()
                g.connect(node, neighbor, int(d))
    return g


class GraphProblem(Problem):


    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal)
        self.graph = graph

    def actions(self, state):
        return list(self.graph.get(state).keys())

    def result(self, state, action):
        return action

    def path_cost(self, c, state1, action, state2):
        return c + (self.graph.get(state1, state2) or math.inf)

    def h(self, node):
        locs = getattr(self.graph, 'locations', None)
        if locs:
            return int(distance(locs[node.state], locs[self.goal]))
        else:
            return math.inf

def ateApple(head,jauki):
    lista = list(jauki)
    return lista.__contains__(head)

def out_of_range(glava):
    x = glava[0]
    y = glava[1]
    if x > 9 or x < 0:
        return False
    elif y > 9 or y < 0:
        return False
    else:
        return True

def coalision(zmija,glava):
    lista_zmija = list(zmija)
    if lista_zmija.__contains__(glava):
        return False
    else:
        return True


#ProdolziPravo
def prodolziPravo(state):
    nasoka = state[0]
    zmija = state[1]
    zeleni_jabolki = state[2]
    crveni_jabolki = state[3]
    glava = zmija[len(zmija)-1]
    new_glava = glava
    if nasoka == 'R':
        new_glava = glava[0],glava[1]+1
    elif nasoka == 'L':
        new_glava = glava[0],glava[1]-1
    elif nasoka == 'U':
        new_glava = glava[0]-1,glava[1]
    else:
        new_glava = glava[0]+1,glava[1]

    if out_of_range(new_glava) and coalision(zmija,new_glava):
        if ateApple(new_glava,crveni_jabolki):
            return state
        elif ateApple(new_glava,zeleni_jabolki):
            lista_zmija = list(zmija)
            lista_zmija.append(new_glava)
            lista_zeleni_jauki = list(zeleni_jabolki)
            lista_zeleni_jauki.remove(new_glava)
            return (nasoka,tuple(lista_zmija),tuple(lista_zeleni_jauki),tuple(crveni_jabolki))
        else:
            lista_zmija = list(zmija)
            lista_zmija.append(new_glava)
            lista_zmija.pop(0)
            return (nasoka,tuple(lista_zmija),tuple(zeleni_jabolki),tuple(crveni_jabolki))

    return state


#SvrtiDesno
def svrtiDesno(state):
    nasoka = state[0]
    zmija = state[1]
    zeleni_jabolki = state[2]
    crveni_jabolki = state[3]
    glava = zmija[len(zmija) - 1]
    new_glava = glava
    new_nasoka = nasoka
    if nasoka == 'R':
        new_glava = glava[0] + 1, glava[1]
        new_nasoka = "D"
    elif nasoka == 'L':
        new_glava = glava[0] - 1, glava[1]
        new_nasoka = "U"
    elif nasoka == 'U':
        new_glava = glava[0], glava[1] + 1
        new_nasoka = "R"
    else:
        new_glava = glava[0], glava[1] - 1
        new_nasoka = "L"

    if out_of_range(new_glava) and coalision(zmija,new_glava):
        if ateApple(new_glava, crveni_jabolki):
            return state
        elif ateApple(new_glava, zeleni_jabolki):
            lista_zmija = list(zmija)
            lista_zmija.append(new_glava)
            lista_zeleni_jauki = list(zeleni_jabolki)
            lista_zeleni_jauki.remove(new_glava)
            return (new_nasoka, tuple(lista_zmija), tuple(lista_zeleni_jauki), tuple(crveni_jabolki))
        else:
            lista_zmija = list(zmija)
            lista_zmija.append(new_glava)
            lista_zmija.pop(0)
            return (new_nasoka, tuple(lista_zmija), tuple(zeleni_jabolki), tuple(crveni_jabolki))

    return state

#SvrtiLevo
def svrtiLevo(state):
    nasoka = state[0]
    zmija = state[1]
    zeleni_jabolki = state[2]
    crveni_jabolki = state[3]
    glava = zmija[len(zmija) - 1]
    new_glava = glava
    new_nasoka = nasoka
    if nasoka == 'R':
        new_glava = glava[0] - 1, glava[1]
        new_nasoka = "U"
    elif nasoka == 'L':
        new_glava = glava[0] + 1, glava[1]
        new_nasoka = "D"
    elif nasoka == 'U':
        new_glava = glava[0], glava[1] - 1
        new_nasoka = "L"
    else:
        new_glava = glava[0], glava[1] + 1
        new_nasoka = "R"

    if out_of_range(new_glava) and coalision(zmija,new_glava):
        if ateApple(new_glava, crveni_jabolki):
            return state
        elif ateApple(new_glava, zeleni_jabolki):
            lista_zmija = list(zmija)
            lista_zmija.append(new_glava)
            lista_zeleni_jauki = list(zeleni_jabolki)
            lista_zeleni_jauki.remove(new_glava)
            return (new_nasoka, tuple(lista_zmija), tuple(lista_zeleni_jauki), tuple(crveni_jabolki))
        else:
            lista_zmija = list(zmija)
            lista_zmija.append(new_glava)
            lista_zmija.pop(0)
            return (new_nasoka, tuple(lista_zmija), tuple(zeleni_jabolki), tuple(crveni_jabolki))

    return state



#da ne se izede samata sebe i da ne izleze nadvor od tablata 10x10(pocnuva od 0 do 9)

class Snake(Problem):

    def __init__(self,initial,goal):
        self.initial = initial
        self.goal = goal


    def goal_test(self, state):
        return len(state[2]) == 0

    def successor(self, state):
        successors = dict()
        new_State = prodolziPravo(state)
        if new_State != state:
            successors["ProdolzhiPravo"] = new_State
        new_State = svrtiDesno(state)
        if new_State != state:
            successors["SvrtiDesno"] = new_State
        new_State = svrtiLevo(state)
        if new_State != state:
            successors["SvrtiLevo"] = new_State

        return successors

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

#
# if __name__ == '__main__':
#     n = int(input())
#     zeleni_jabolki = [tuple(map(int, input().split(','))) for _ in range(n)]
#     m = int(input())
#     crveni_jabolki = [tuple(map(int, input().split(','))) for _ in range(m)]
#
#     zmija = ((0,0),(1,0),(2,0))
#
#     snake = Snake(('D',zmija,tuple(zeleni_jabolki),tuple(crveni_jabolki)),None)
#     answer = breadth_first_graph_search(snake)
#     print(answer.solution())




pygame.init()
screen = pygame.display.set_mode((600,600))
playerImg = pygame.image.load('venv/snake.png')
tailImg = pygame.image.load('venv/snake1.png')
appleImg = pygame.image.load('venv/apple.png')


snakeX = 60
snakeY = 0
tail = [(0,0)]
appleX = 120
appleY = 120
appleEaten = False
direction = 3
first = True
lastKey = pygame.K_RIGHT;
theEnd = False


def drawTail(tail):
    for temp in tail:
        screen.blit(tailImg,temp)


def moveInDirection(direction):
    time.sleep(0.3)
    global snakeX
    global snakeY
    global tail
    oldX = snakeX
    oldY = snakeY
    if direction == 1:
        if snakeY == 540:
            snakeY = 0
        else:
            snakeY += 60
    elif direction == 2:
        if snakeY == 0:
            snakeY = 540
        else:
            snakeY -= 60
    elif direction == 3:
        if snakeX == 540:
            snakeX = 0
        else:
            snakeX += 60
    elif direction == 4:
        if snakeX == 0:
            snakeX = 540
        else:
            snakeX -= 60
    tail.append((oldX, oldY))
    tail.pop(0)


def drawSnake(x,y):
    screen.blit(playerImg,(x,y))

def drawApple(x,y):
    screen.blit(appleImg,(x,y))


def checkEaten():
    global snakeX
    global snakeY
    global appleX
    global appleY
    global appleEaten
    if snakeX == appleX and snakeY == appleY:
        appleEaten = True
    else:
        appleEaten = False

def moveUp():
    global snakeY
    global snakeX
    global tail
    snakeY -= 60
    tail.append((snakeX,snakeY))
    tail.pop(0)

def moveDown():
    global snakeY
    global snakeX
    global tail
    snakeY += 60
    tail.append((snakeX,snakeY))
    tail.pop(0)

def moveLeft():
    global snakeX
    global snakeY
    global tail
    snakeX -= 60
    tail.append((snakeX, snakeY))
    tail.pop(0)

def moveRight():
    global snakeX
    global snakeY
    global tail
    snakeX += 60
    tail.append((snakeX, snakeY))
    tail.pop(0)



def generateRandomApple():
    randomX = randrange(10)
    randomY = randrange(10)
    print(randomX)
    print(randomY)
    global appleX
    global appleY
    global tail
    while True:
        if randomX == 0:
            appleX = 0
        elif randomX == 1:
            appleX = 60
        elif randomX == 2:
            appleX = 120
        elif randomX == 3:
            appleX = 180
        elif randomX == 4:
            appleX = 240
        elif randomX == 5:
            appleX = 300
        elif randomX == 6:
            appleX = 360
        elif randomX == 7:
            appleX = 420
        elif randomX == 8:
            appleX = 480
        else:
            appleX = 540

        if randomY == 0:
            appleY = 0
        elif randomY == 1:
            appleY = 60
        elif randomY == 2:
            appleY = 120
        elif randomY == 3:
            appleY = 180
        elif randomY == 4:
            appleY = 240
        elif randomY == 5:
            appleY = 300
        elif randomY == 6:
            appleY = 360
        elif randomY == 7:
            appleY = 420
        elif randomY == 8:
            appleY = 480
        else:
            appleY = 540

        if (appleX,appleY) in tail:
            randomX = randrange(10)
            randomY = randrange(10)
        else:
            break


def checkTheEnd(tail,sX,sY):
    if (sX,sY) in tail:
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Game Over!', True, (255,255,255), (150,150,150))
        textRect = text.get_rect()
        textRect.center = (630 // 2, 600 // 2)
        screen.blit(text, textRect)
        global theEnd
        theEnd = True

running = True

class Snake(Problem):

    def __init__(self,initial,goal):
        self.initial = initial
        self.goal = goal

    def goal_test(self, state):
        return True

    def successor(self, state):
        successors = dict()
        return successors

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(self)[action]

while running:
    screen.fill((192,192,192))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            lastKey = event.key;



            if lastKey == pygame.K_RIGHT:
                direction = 3
            if lastKey == pygame.K_LEFT:
                direction = 4
            if lastKey == pygame.K_UP:
                direction = 2
            if lastKey == pygame.K_DOWN:
                direction = 1

    checkTheEnd(tail, snakeX, snakeY)
    moveInDirection(direction)

    if appleEaten:
        generateRandomApple()


    checkEaten()

    if appleEaten:
        tail.insert(0,tail.__getitem__(0))

    print(snakeX)
    print(snakeY)
    print(tail)

    if theEnd == False:
        drawApple(appleX,appleY)
        drawTail(tail)
        drawSnake(snakeX,snakeY)
    else:
        running = False

    pygame.display.update()







    # 5  zeleni
    # 0, 6
    # 2, 2
    # 4, 9
    # 6, 2
    # 6, 4
    # 4 crveni
    # 3, 4
    # 4, 6
    # 6, 3
    # 1, 6

    # ['SvrtiLevo', 'ProdolzhiPravo', 'SvrtiDesno', 'ProdolzhiPravo', 'ProdolzhiPravo', 'ProdolzhiPravo',
    #  'ProdolzhiPravo', 'SvrtiLevo', 'ProdolzhiPravo', 'SvrtiLevo', 'ProdolzhiPravo', 'SvrtiDesno', 'ProdolzhiPravo',
    #  'ProdolzhiPravo', 'ProdolzhiPravo', 'ProdolzhiPravo', 'SvrtiLevo', 'ProdolzhiPravo', 'ProdolzhiPravo',
    #  'ProdolzhiPravo', 'ProdolzhiPravo', 'SvrtiLevo', 'ProdolzhiPravo', 'ProdolzhiPravo']
