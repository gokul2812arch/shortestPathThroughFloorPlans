import sys

def obstacle_found(px, i, j, img_scale_factor, grid_search_factor ):
    """ (px, i, j, img_scale_factor, grid_search_factor ) """
    x = j * img_scale_factor
    y = i * img_scale_factor
    step = img_scale_factor/ grid_search_factor

    obs_bool = []
    for item in range(grid_search_factor):
        try:
            colour = px[int(x+5*step), int(y+(item*step))]
        except Exception as e:
            colour = (0,0,0)

        if colour == (0,0,0):
            obs_bool.append(1)

        try:
            colour = px[int(x+(item*step)),int(y+5*step) ]
        except Exception as e:
            colour = (0,0,0)

        if colour == (0,0,0):
            obs_bool.append(1)

        if len(obs_bool) > int(grid_search_factor/5):
            #print("obs found ", i, j)
            return True
    #print("no obs at ", i, j)
    return False 

def load_plan_image(filename_img, filename_text, grid_width_max = 100 ,grid_search_factor = 10):
    """load image   (filename_img, filename_text, grid_width_max = 100 ,grid_search_factor = 10)"""
    from PIL import Image, ImageDraw
    import math

    img = Image.open(filename_img)
    
    width, height = img.size
    img_scale_factor = math.floor(width/grid_width_max)
    grid_height_max = math.floor( height/img_scale_factor)

    with open (filename_text, "w+") as f:
        px = img.load()
        for i in range(grid_height_max):
            text = ""
            for j in range(grid_width_max):
                if obstacle_found(px, i , j , img_scale_factor, grid_search_factor): 
                    text += "#"
                else: 
                    text += " "
            f.write(text + "\n")
        #print("text file created")

    return img_scale_factor, width, height

if __name__ == '__main__':
    img_scale_factor, w, h = load_plan_image("20210531072856.jpg", "plan1.txt", 100, 10)
