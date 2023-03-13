import cv2 as cv
import numpy as np
import math
from random import shuffle

mode = True
img = np.full((480, 640, 3), 255, dtype=np.uint8)
drawing = False
ix, iy = -1, -1
B = [i for i in range(256)]
G = [i for i in range(256)]
R = [i for i in range(256)]
triangle_pts = []

def onMouse(event, x, y, flags, param):
    global ix, iy, drawing, mode, B, G, R, img, triangle_pts
    # 마우스를 클릭했다면
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        shuffle(B), shuffle(G), shuffle(R)
        if mode == 1:
            triangle_pts.append((ix, iy))

            # 점 그리기(3개 되면 삼각형으로 연결)
            cv.circle(param, (ix, iy), 3, (B[0], G[0], R[0]), -1)
            cv.imshow('paint_mode', img)
            # Draw the triangle once three vertices are selected
            if len(triangle_pts) == 3:
                pts = np.array(triangle_pts, np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv.polylines(param, [pts], True, (B[0], G[0], R[0]), 3)
                triangle_pts.clear()
                cv.imshow('paint_mode', img)
    # 마우스가 움직인다면 삼각형, 원 그리기
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing:
            paint_img = img.copy()
            if mode == 2:
                cv.rectangle(param, (ix, iy), (x, y), (B[0], G[0], R[0]), -1)
                cv.imshow('paint_mode', img)
            elif mode == 0:
                r = (ix - x) ** 2 + (iy - y) ** 2
                r = int(math.sqrt(r))
                cv.circle(param, (ix, iy), r, (B[0], G[0], R[0]), -1)
                cv.imshow('paint_mode', img)
    # 마우스 클릭했다 떼면 그리기 멈추기
    elif event == cv.EVENT_LBUTTONUP:
        if drawing:
            drawing = False


def mouseBrush():
    global mode, img

    cv.namedWindow('paint_mode')
    cv.setMouseCallback('paint_mode', onMouse, param=img)

    while True:
        cv.imshow('paint_mode', img)
        # ESC
        k = cv.waitKey(0) & 0xFF
        if k == 27:
            break
        # mode(m)
        elif k == ord('m'):
            mode = mode + 1
            mode = mode % 3

    cv.destroyAllWindows()

mouseBrush()
