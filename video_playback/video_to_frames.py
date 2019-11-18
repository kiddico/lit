import cv2
test = cv2.VideoCapture('ghost_sample_2.mp4')

frame_num = 0
while(test.isOpened()):
    ret, frame = test.read()
    if ret == True:
        cv2.imwrite('ghost_sample_2_f{}.png'.format(frame_num), frame)
        frame_num+=1
    else: 
        break

test.release()
