from PIL import Image, ImageEnhance
import cv2
import time
import os

dir = os.getcwd()
ipath = dir+"<Image>.png"
vpath = dir+"<Video>.mp4"
vspath = dir+"cache\\"

try:
    os.mkdir(vspath)
except OSError as error:
    print(error)



def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n 

def img_to_ascii(img, baselength,  bias, contrast, high_detail = False):
    
    #Processing
    img = Image.open(img)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = img.convert('L')

    #Resizing
    x1, y1 = img.size
    img = img.resize((baselength, int(y1 * (baselength/(x1*2)))), Image.ANTIALIAS)


    #Converting to ASCII
    ascii_list = list('''$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|(){{}}?-_+~<>i!lI;:,"^`'.'''.format('{}')) if high_detail else list("@&#*?|()?-_+<>i!lI=-:,. ")
    bias = clamp(bias, 0, 10)
    bias = bias + 4 if high_detail else bias + 24
    print(bias)
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
            converted_frame = img_to_ascii(name, 75, 4, 1.5)
            print(converted_frame)

            #Delay for smooth Printing
            time.sleep(0.03)
        except:
            if loop:
                video_to_ascii(vidpath)
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
        
        cv2.imshow('window', frame)
        cv2.imwrite(name, frame)
        converted_frame = img_to_ascii(name, 180,0, 1.5)
        #Realtime Camera feed -> ASCII
        print(converted_frame)
     
    vid.release() 
    cv2.destroyAllWindows() 

