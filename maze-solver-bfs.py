import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class Frontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

# height, width, walls, start, goal   will read maze file and gove this output 
def load_maze(filename):

    # Read file and set height and width of maze
    with open(filename) as f:
        contents = f.read()

    # Validate start and goal
    if contents.count("A") != 1:
        raise Exception("maze must have exactly one start point")
    if contents.count("B") != 1:
        raise Exception("maze must have exactly one goal")

    # Determine height and width of maze
    contents = contents.splitlines()
    height = len(contents)                             # height = int
    width = max(len(line) for line in contents)        # width = int

    # make maze 
    walls = []                                         #walls = [[,...],[,...],...]  
    for i in range(height):
        row = []
        for j in range(width):
            try:
                if contents[i][j] == "A":
                    start = (i, j)                    #start = (i,j)
                    row.append(False)
                elif contents[i][j] == "B":
                    goal = (i, j)                     #goal = (i,j)
                    row.append(False)
                elif contents[i][j] == " ":
                    row.append(False)
                else:
                    row.append(True)
            except IndexError:
                row.append(False)
        walls.append(row)
    return height, width, walls, start, goal 

class Maze():

    def __init__(self, height, width, walls, start, goal):
        self.height = height               
        self.width = width                
        self.walls = walls
        self.start = start 
        self.goal = goal 
        self.solution = None



    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result


    def solve(self, animate, animation_directory):
        """Finds a solution to maze, if one exists."""


        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        self.open_list = []
        self.closed_list = []
        start = Node(state=self.start, parent=None, action=None)
        frontier = Frontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()
        count = 1 

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return self.solution, self.explored

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


            if animate == True:
                filename = animation_directory + "maize_h" +str(height) + "_w" + str(width) + "_s" + "solution" + "_c" + str(count) + ".png"
                count += 1
                output_image(height, width, walls, filename, start.state, goal , None , True , self.explored)

# print maize 
def print_m(walls, start, goal, solution=None):
    solution = solution[1] if solution is not None else None
    print()
    for i, row in enumerate(walls):
        for j, col in enumerate(row):
            if col == 1:
                print("█", end="")
            elif (i, j) == start:
                print("A", end="")
            elif (i, j) == goal:
                print("B", end="")
            elif solution is not None and (i,j) in solution:
                print("*", end="")
            else:
                print(" ", end="")
        print()
    print()

# generate output image of the maze 
def output_image(height, width, walls, filename, start, goal , solution = None ,animation = False, explored_set = None):
    from PIL import Image, ImageDraw
    cell_size = 50
    cell_border = 2 

    img = Image.new("RGBA", (width*cell_size, height*cell_size), "white")
    draw = ImageDraw.Draw(img)

    # make rectangle 
    def draw_fun(draw, i, j, cell_size, cell_border, fill):
        draw.rectangle(
                    ([(j*cell_size + cell_border, i*cell_size+cell_border),
                     ((j+1)*cell_size-cell_border, (i+1)*cell_size-cell_border)]),
                    fill=fill
                )
        return img

    # make solution readable 
    if explored_set != None:
        for i, j in list(explored_set):
            fill = (64, 208, 231)
            draw_fun(draw, i, j, cell_size, cell_border, fill)

    if solution != None:
        solution = solution[1] if solution is not None else None 
        for i,j in list(solution):
            fill = (252, 255, 72)
            draw_fun(draw, i, j, cell_size, cell_border, fill)

    for i, row in enumerate(walls):
        for j, col in enumerate(row):
            if col:
                fill = (0, 53, 73)
                draw_fun(draw, i, j, cell_size, cell_border, fill)

    i, j = start
    fill = (255, 0, 0)
    draw_fun(draw, i, j, cell_size, cell_border, fill)

    i, j = goal
    fill = (0, 255, 0)
    draw_fun(draw, i, j, cell_size, cell_border, fill)


    img.save(filename)
    if animation == False:
        print("image saved")


if __name__ == '__main__':
    import random
    random.seed(45)
    maze_text_directory = r"D:\DATA\WEBSITE\001\A028_maze solver\maze\ "   
    filename_txt = "plan.txt"
    filename_maze_txt = maze_text_directory[:-1] + filename_txt 

    height, width, walls, start, goal = load_maze(filename_maze_txt)
    maze1 = Maze(height, width, walls, start, goal)

    animation_directory = r"D:\DATA\WEBSITE\001\A028_maze solver\maze\maze generator\solve1\ "
    solution, explored = maze1.solve(False, animation_directory)

    print_m(walls, start, goal, solution)

    directory = r"D:\DATA\WEBSITE\001\A028_maze solver\maze\ "
    filename = directory + "maize_" +str(height) + "_" + str(width) + "_" + "solution" + ".png"

    output_image(height, width, walls, filename, start, goal , solution , False, explored)


    

