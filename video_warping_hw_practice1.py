import cv2
import numpy as np
import copy


points_src = []

vidcap = cv2.VideoCapture("H:\RV_lec\data/data2_360.mp4")
sucess, image = vidcap.read()

def mouse_event_handler(event, x, y, flags, param):
    global points_src
    if event == cv2.EVENT_LBUTTONDOWN:
        points_src.append((x,y))   #클릭 좌표 추출
        # points_src = np.append(points_src, np.array((x,y)))


while sucess:
    success, image = vidcap.read() #이게 있어야 계속해서 이미지 생성하고 동영상처럼 재생?
    video = cv2.resize(image, (1280, 720))
    window_name = "Bird-Eye-View"
    view_size = (360,720)
    points_dst = np.array([[0,0], [view_size[0],0], [0, view_size[1]], [view_size[0], view_size[1]]])
    
    cv2.namedWindow(window_name) 
    cv2.setMouseCallback(window_name, mouse_event_handler)
    while len(points_src) < 4:
        display = copy.deepcopy(video)        
        idx = min(len(points_src), len(points_dst))
        if len(points_src) > 0:            
            display = cv2.circle(display, points_src[idx-1], 5, (0, 255, 0), -1) #마우스로 찍은 점 표시, 인덱스는0부터 시작
        cv2.imshow(window_name, display)
        if cv2.waitKey(1) == ord('q'): break
        print(points_src)
    
    
    #좌표 선택 좌상 > 우상 > 좌하 > 우하
    p1 = points_src[0]
    p2 = points_src[1]
    p3 = points_src[2]
    p4 = points_src[3]
    
    cv2.circle(video, p1, 5, (0,0,255), -1)
    cv2.circle(video, p2, 5, (0,0,255), -1)
    cv2.circle(video, p3, 5, (0,0,255), -1)
    cv2.circle(video, p4, 5, (0,0,255), -1)
    
    # Apply Geometrical Transformation
    #pts1 = np.float32([p1, p2, p3, p4])
    pts1 = np.float32([p1, p2, p3, p4])
    
    #pts2 = np.float32([[0,0], [0,720], [1280,0], [1280,720]])
    pts2 = np.float32(points_dst)
    
    
    
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    transformed_video = cv2.warpPerspective(video,matrix, view_size)
    
    #points_src = np.array(points_src, dtype=np.float32)
    #H, inliner_mask = cv2.findHomography(points_src, points_dst, cv2.RANSAC)
    #rectify = cv2.warpPerspective(video, H, view_size)
    
    
    
    cv2.imshow("video", video)
    cv2.imshow("warping", transformed_video)
    #cv2.imshow("warping", rectify)
    
    if cv2.waitKey(20) == 27:
        break
    
    
