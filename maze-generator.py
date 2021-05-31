import sys

# create the walls of the maze    
def Create_maze(height, width, animation = False, directory = 0):
    """create the maze"""
    import random
    # height 
    # width 
                
    def get_neighbours(cell, open_cells, height, width,visited_cells ):
        """get possible nieghbors and actions"""
        row, col = cell
        candidates = [
            ("up", (row - 2, col)),
            ("down", (row + 2, col)),
            ("left", (row, col - 2)), 
            ("right", (row, col + 2))
        ]
        
        result = []
        for action, (r, c) in candidates:
            if 0 <= r < height*2 and 0 <= c < width*2 and (r,c) not in visited_cells: 
                result.append((action, (r, c)))
        return result 
       
    def connect_cells(new_cell, current_cell):
        """return cell in between"""
        x, y = new_cell
        i, j = current_cell
        return (x, int((y + j) / 2)) if x == i else (int((x + i) / 2),y)
            
    
    # create the grid  
    all_cells = set()                                            
    open_cells = set()                                              #open_cells   set
    for i in range(height):
        for j in range(width):
            open_cells.add((i*2,j*2))     
    for i in range(height*2):
        for j in range(width*2):
            all_cells.add((i,j))
    wall_cells = all_cells - open_cells                            # wall_cells   set 
    
    #print(all_cells)
    #print(open_cells)
    #print(wall_cells)
    
    # start 
    current_cell = random.sample(open_cells, 1)[0]
    visited_cells = set()                                          #visited_cells    set 
    visited_cells.add(current_cell)
    nu_visited_cells = 1
    
    #print("current cell", current_cell)
    # for visualization 
    backtrack = []                                             # backtrack = list

    #stack 
    stack = []
    count = 1 
    while nu_visited_cells < len(open_cells):
        neighbours = get_neighbours(current_cell, open_cells, height, width,visited_cells)
        #print(neighbours)
        if len(neighbours) > 0:
            new_cell = random.sample(neighbours, 1)[0][1]
            visited_cells.add(new_cell)
            #print("new_cell",new_cell)
            con_cell = connect_cells(current_cell, new_cell)
            wall_cells.remove(con_cell)
            stack.append(current_cell)
            #old_cell = current_cell
            current_cell = new_cell
            nu_visited_cells += 1
        else: 
            #con_cell = connect_cells(old_cell, current_cell)
            #backtrack.append(con_cell)
            backtrack.append(current_cell)
            current_cell = stack.pop(-1)

        # animation 
        if animation == True:
            filename = directory + "maize_h" +str(height) + "_w" + str(width) + "_s" + str(seed) + "_c" + str(count) + ".png"
            count += 1 
            output_image(height, width, wall_cells, filename, backtrack,  animation = True)



    print("maze generated")
    #print("wall_cells", wall_cells)
    #print()
    #print("visited cells", visited_cells)
    return(wall_cells)
    #return(wall_cells)

# get neighbours 
def get_all_neighbours(cell, height, width ):
    """get possible nieghbors and actions"""
    row, col = cell
    candidates = [
        ("up", (row - 1, col)),
        ("down", (row + 1, col)),
        ("left", (row, col - 1)), 
        ("right", (row, col + 1))
    ]
    
    result = []
    for action, (r, c) in candidates:
        if 0 <= r < height*2 and 0 <= c < width*2: 
            result.append((r, c))
    return result 

# generate output image of the maze 
def output_image(height, width, wall_cells, filename, backtrack = 0 ,animation = False):
    from PIL import Image, ImageDraw
    cell_size = 50
    cell_border = 2 

    img = Image.new("RGBA", (width*cell_size*2-cell_size, height*cell_size*2-cell_size), "white")
    draw = ImageDraw.Draw(img)

    # make rectangle 
    def draw_fun(draw, i, j, cell_size, cell_border, fill):
        draw.rectangle(
                    ([(j*cell_size + cell_border, i*cell_size+cell_border),
                     ((j+1)*cell_size-cell_border, (i+1)*cell_size-cell_border)]),
                    fill=fill
                )
        return img

    def fill_gaps(listA, height, width):
        listB = []
        for item in listA:
            A = get_all_neighbours(item, height, width)
            for itemj in A:
                listB.append(itemj)

        listC = listA + listB 
        return listC

    if type(backtrack) == list: 
        new_backtrack = fill_gaps(backtrack, height, width)
        #new_backtrack = backtrack 
        for i,j in new_backtrack:
            fill = (64, 208, 231)
            draw_fun(draw, i, j, cell_size, cell_border, fill)

    for i,j in list(wall_cells):
        fill = (0, 53, 73)
        draw_fun(draw, i, j, cell_size, cell_border, fill)

    img.save(filename)
    if animation == False:
        print("image saved")

# generate text file
def output_txt(height, width, wall_cells, filename):
    with open (filename, "w+") as f:
        for i in range(height*2+1):
            text = ""
            for j in range(width*2+1):
                if i == 0 or j ==0:
                    text += "#"
                else:
                    cell = (i-1,j-1)
                    if cell in wall_cells:
                        text += "#"
                    else: 
                        text += " "
            f.write(text + "\n")
    print("text file created")
                
if __name__ == '__main__':
    import random

    height = 10
    width = 15
    seed = 15

    random.seed(seed)
    #directory = r"D:\DATA\WEBSITE\001\A028_maze solver\maze\maze generator\ "
    #filename = directory + "maize_" +str(height) + "_" + str(width) + "_" + str(seed) + ".png"
    #directory_animation = r"D:\DATA\WEBSITE\001\A028_maze solver\maze\maze generator\generation1\ "
    #filename_txt = directory + "maize_" +str(height) + "_" + str(width) + "_" + str(seed) + ".txt"

     
    #wall_cells = Create_maze(height, width, False, directory_animation )     # create animation and the maize
    #output_image(height, width, wall_cells,filename)                        # create the final output image 
    #output_txt(height, width, wall_cells, filename_txt)


    for i in range(1):
        seed = i 
        random.seed(seed)

        directory = r"D:\DATA\WEBSITE\001\A028_maze solver\maze\maze generator\ "
        filename = directory + "maize_" +str(height) + "_" + str(width) + "_" + str(seed) + ".png"
        directory_animation = r"D:\DATA\WEBSITE\001\A028_maze solver\maze\maze generator\generation1\ "
        filename_txt = directory + "maize_" +str(height) + "_" + str(width) + "_" + str(seed) + ".txt"
       
        wall_cells = Create_maze(height, width, False, directory_animation )
        output_image(height, width, wall_cells,filename)
        output_txt(height, width, wall_cells, filename_txt)






        