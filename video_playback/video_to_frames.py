import cv2
test = cv2.VideoCapture('ghost_sample_1.mp4')

frame_num = 0
while(test.isOpened()):
    ret, frame = test.read()
    if ret == True:
        cv2.imwrite('ghost_sample_1_frames/ghost_sample_1_f{:03d}.png'.format(frame_num), frame)
        frame_num+=1
    else: 
        break

test.release()

