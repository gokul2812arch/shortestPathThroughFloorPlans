import cv2
import converter as conv
import mazeSolverBfs as ms
   
def click_event(event, x, y, flags, params):
    #img = cv2.imread('20210531072856.jpg', 1)
    #cv2.imshow('image', img)

    if event == cv2.EVENT_LBUTTONDOWN:
        coord.append((x,y))
  
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x,y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('image', img)
        #print(coord)

        if len(coord) == 2:
            #print("hello")
            b , a , d, c= int(coord[0][0]/img_scale_factor), int(coord[0][1]/img_scale_factor), int(coord[1][0]/img_scale_factor), int(coord[1][1]/img_scale_factor)
            height, width, walls, filename_image, start, goal , solution , explored = ms.reu_bfs_maze_solver_bfs(grid_width_max,png_plan,text_file, output_png, (a,b), (c,d))
            coord.pop(0)
            coord.pop(0)
            
      

if __name__=="__main__":
    from PIL import Image, ImageDraw, ImageFilter

    for i in range(5): 
        png_plan = "20210531072856.png"
        text_file = "plan1.txt"
        output_png = "plan1.png"
        grid_width_max = 100
        grid_search_factor = 10


        img = cv2.imread(png_plan, 1)
        cv2.imshow('image', img)
        img_scale_factor, w, h = conv.load_plan_image(png_plan, text_file, grid_width_max, grid_search_factor)   # (filename_img, filename_text, grid_width_max = 100 ,grid_search_factor = 10)

        coord = []
        cv2.setMouseCallback('image', click_event)
        #print("hello")

        cv2.waitKey(0)
        img = cv2.imread(output_png, 1)
        cv2.imshow('image', img)

        cv2.waitKey(0)



    cv2.destroyAllWindows()