from PIL import Image, ImageEnhance
import cv2
import time
import os

dir = os.getcwd()
ipath = dir+"<Image>.png"
vpath = dir+"<Video>.mp4"
vspath = dir+"cache\\"

try:
    if not os.path.exists(vspath):
        os.mkdir(vspath)
except OSError as error:
    print(error)

#TODO-change it to terminal based printing with dynamic size
def img_to_ascii(img, baselength,  bias, contrast = 1.3, high_detail = False):
    
    #Processing
    img = ImageEnhance.Contrast(Image.open(img)).enhance(contrast).convert('L')


    #Resizing
    x1, y1 = img.size
    img = img.resize((baselength, int(y1 * (baselength/(x1*2)))), Image.ANTIALIAS)


    #Converting to ASCII
    ascii_list = list('''$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|(){{}}?-_+~<>i!lI;:,"^`'.'''.format('{}')) if high_detail else list("@&#*?|()?-_+<>i!lI=-:,. ")
    bias = 0 if bias < 0 else 10 if bias > 10 else bias #Clamp value between 0 and 10
    bias = bias + 4 if high_detail else bias + 24
    px = img.getdata()
    px_img = "".join([ascii_list[i//bias] for i in px])
    ascii_img = "\n".join([px_img[index:(index+baselength)] for index in range(0, len(px_img), baselength)])

    return ascii_img

#print(img_to_ascii(ipath, 200, 0, 2))

def video_to_ascii(vidpath, loop = True):
    vid = cv2.VideoCapture(vidpath)
        
    while True:
        try:
            ret, frame = vid.read()
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break
            
            #Generate Cache frame for video read
            name = dir + 'cache\\cacheframe.jpg'
            
            cv2.imwrite(name, frame)
            fps = vid.get(cv2.CAP_PROP_FPS)
            converted_frame = img_to_ascii(name, 75, 4, 1.5)
            print(converted_frame)

            #Delay for smooth Printing
            time.sleep(0.03)
        except:
            if loop:
                video_to_ascii(1/fps)
            else:
                break
     
    vid.release() 
    cv2.destroyAllWindows() 
                
def realtime_ascii():
    vid = cv2.VideoCapture(0)
        
    while True:
        ret, frame = vid.read()
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
        
        name = dir + 'cache\\cacheframe.jpg'
        fps = vid.get(cv2.CAP_PROP_FPS)
        
        cv2.imshow('window', frame)
        cv2.imwrite(name, frame)
        converted_frame = img_to_ascii(name, 180,0, 1.2)
        #Realtime Camera feed -> ASCII
        print(converted_frame)
        time.sleep(1/fps)
     
    vid.release() 
    cv2.destroyAllWindows() 

