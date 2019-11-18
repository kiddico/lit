import cv2
video_in = cv2.VideoCapture('ghost_sample_1.mp4')

frame_num = 0
while(video_in.isOpened()):
    ret, frame = video_in.read()
    if ret == True:
        cv2.imwrite('ghost_sample_1_frames/ghost_sample_1_f{:03d}.png'.format(frame_num), frame)
        frame_num+=1
    else:
        break

video_in.release()
