import sys

from PIL import Image, ImageEnhance
import cv2
import time
import os

dir = os.getcwd()
print(dir)
ipath = f"{dir}\\<ImagePath>.png"
vpath = f"{dir}\\<Video>.mp4"
vspath = f"{dir}\\cache\\"

w, h = os.get_terminal_size()



try:
    if not os.path.exists(vspath):
        os.mkdir(vspath)
except OSError as error:
    print(error)


def img_to_ascii(img, baselength,  bias, contrast = 1.2, high_detail = False):

    #Processing
    img = ImageEnhance.Contrast(Image.open(img)).enhance(contrast).convert('L')


    #Resizing
    x1, y1 = img.size
    img = img.resize((baselength, int(y1 * (baselength/(x1*2)))))


    #Converting to ASCII
    ascii_list = list('''$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|(){{}}?-_+~<>i!lI;:,"^`'.'''.format('{}')) if high_detail else list("@&#*?|()?-_+<>i!lI=-:,. ")
    bias = 0 if bias < 0 else 10 if bias > 10 else bias #Clamp value between 0 and 10
    bias = bias + 4 if high_detail else bias + 24
    px = img.getdata()
    px_img = "".join([ascii_list[i//bias] for i in px])
    ascii_img = "\n".join([px_img[index:(index+baselength)] for index in range(0, len(px_img), baselength)])

    return ascii_img


def video_to_ascii(vidpath, loop = True):
    os.system('cls' if os.name == 'nt' else 'clear')
    vid = cv2.VideoCapture(vidpath)

    while True:
        try:
            ret, frame = vid.read()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            #Generate Cache frame for video read
            name = f'{dir}\\cache\\cacheframe.jpg'

            cv2.imwrite(name, frame)
            converted_frame = img_to_ascii(name, w, 4, 1.2)
            print(converted_frame)
            os.system('cls' if os.name == 'nt' else 'clear')

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
    os.system('cls' if os.name == 'nt' else 'clear')
    vid = cv2.VideoCapture(0)

    while True:
        w, h = os.get_terminal_size()
        ret, frame = vid.read()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        name = f'{dir}\\cache\\cacheframe.jpg'

        #cv2.imshow('window', frame)
        cv2.imwrite(name, frame)
        converted_frame = img_to_ascii(name, w,0, 1.2, True)
        #Realtime Camera feed -> ASCII
        print(converted_frame)
        time.sleep(1/30)
        os.system('cls' if os.name == 'nt' else 'clear')



    vid.release()
    cv2.destroyAllWindows()

i = input('V for video, C for camera feed, X to exit: ')

if i == 'V':
    video_to_ascii(vpath)
elif i == 'C':
    realtime_ascii()
elif i=='X':
    sys.exit()
