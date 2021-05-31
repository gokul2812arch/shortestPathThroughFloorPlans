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
def load_maze(filename, start_cell, end_cell):
    """height, width, walls, start, goal = load_maze(filename_text, start_cell, end_cell)""" 

    # Read file and set height and width of maze
    with open(filename) as f:
        contents = f.read()

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
                    row.append(False)
                elif contents[i][j] == "B":
                    row.append(False)
                elif contents[i][j] == " ":
                    row.append(False)
                else:
                    row.append(True)
            except IndexError:
                row.append(False)
        walls.append(row)
        start = start_cell
        goal = end_cell
    return height, width, walls, start, goal 

class Maze():
    """Maze(height, width, walls, start, goal)"""

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


    def solve(self):
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
def output_image(grid_width_max,png_plan, height, width, walls, filename, start, goal , solution = None , explored_set = None):
    """output_image(png_plan, height, width, walls, filename_image, start, goal , solution , explored)"""
    import random
    from PIL import Image, ImageDraw
    import math

    cell_size = 50
    cell_border = 2 

    img = Image.new("RGBA", (width*cell_size, height*cell_size), (255, 255, 255, 10))
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
            fill = (64, 208, 231, 150)
            draw_fun(draw, i, j, cell_size, cell_border, fill)

    if solution != None:
        solution = solution[1] if solution is not None else None 
        for i,j in list(solution):
            fill = (252, 255, 72, 150)
            draw_fun(draw, i, j, cell_size, cell_border, fill)

    # for i, row in enumerate(walls):
    #     for j, col in enumerate(row):
    #         if col:
    #             fill = (0, 53, 73)
    #             draw_fun(draw, i, j, cell_size, cell_border, fill)

    i, j = start
    fill = (255, 0, 0, 150)
    draw_fun(draw, i, j, cell_size, cell_border, fill)

    i, j = goal
    fill = (0, 255, 0, 150)
    draw_fun(draw, i, j, cell_size, cell_border, fill)


    
    img2 = Image.open(png_plan)
    w1, h1 = img2.size
    img_scale_factor = math.floor(w1/grid_width_max)

    cw1 = grid_width_max * img_scale_factor
    ch1 = math.floor(h1 / img_scale_factor) * img_scale_factor

    img2 = img2.crop((0, 0, cw1, ch1))
    img2 = img2.resize((w1, h1),  Image.ANTIALIAS)
    img = img.resize((w1, h1),  Image.ANTIALIAS)

    img2.paste(img, (0,0), mask = img)
    
    img2.save(filename)

    pass

# main file 
def reu_bfs_maze_solver_bfs(grid_width_max,png_plan, filename_text, filename_image, start_cell, end_cell): 

    height, width, walls, start, goal = load_maze(filename_text, start_cell, end_cell)
    maze1 = Maze(height, width, walls, start, goal)
    solution, explored = maze1.solve()
    output_image(grid_width_max,png_plan, height, width, walls, filename_image, start, goal , solution , explored)
    return height, width, walls, filename_image, start, goal , solution , explored

if __name__ == '__main__':
    height, width, walls, filename_image, start, goal , solution , explored = reu_bfs_maze_solver_bfs(100,"20210531072856.png","plan1.txt", "plan1.png", (1,1), (1,2))
    #height, width, walls, filename_image, start, goal , solution , explored = ms.reu_bfs_maze_solver_bfs(grid_width_max,png_plan,text_file, output_png, (a,b), (c,d))
    #print(solution[1])



    

