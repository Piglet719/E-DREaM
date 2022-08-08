import cv2
from cv2 import aruco
import time


def drawLines(name):
    try:
        cv2.putText(frame, name,
                    (tokens[x][3][0], tokens[x][3][1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.line(frame, tokens[x][3], tokens[x][4], (0, 255, 0), 2)
        cv2.line(frame, tokens[x][4], tokens[x][5], (0, 255, 0), 2)
        cv2.line(frame, tokens[x][5], tokens[x][6], (0, 255, 0), 2)
        cv2.line(frame, tokens[x][6], tokens[x][3], (0, 255, 0), 2)
    except:
        capture.release()
        cv2.destroyWindow("frame")


def error():
    try:
        cv2.putText(frame, "Syntax Error",
                    (tokens[x][3][0], tokens[x][3][1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.line(frame, tokens[x][3], tokens[x][4], (0, 0, 255), 2)
        cv2.line(frame, tokens[x][4], tokens[x][5], (0, 0, 255), 2)
        cv2.line(frame, tokens[x][5], tokens[x][6], (0, 0, 255), 2)
        cv2.line(frame, tokens[x][6], tokens[x][3], (0, 0, 255), 2)
    except:
        capture.release()
        cv2.destroyWindow("frame")


def addX():
    # move to next token
    global x
    x += 1
    if x >= len(tokens):
        return


def getTokenNum():
    if x < len(tokens):
        return tokens[x][0]
    else:
        return


def ID():
    if getTokenNum() == None:
        return
    elif getTokenNum() == 2:
        # print("arrayJ")
        drawLines("arrayJ")
        addX()
    elif getTokenNum() == 3:
        # print("arrayPlus")
        drawLines("arrayPlus")
        addX()
    elif getTokenNum() == 6:
        # print("boat")
        drawLines("boat")
        addX()
    else:
        error()


def TIME():
    if getTokenNum() == None:
        return
    elif getTokenNum() == 4:
        # print("arrayLength")
        drawLines("arrayLength")
        addX()
        stats()
    elif getTokenNum() == 5:
        # print("arrayLengthInloop")
        drawLines("arrayLengthInloop")
        addX()
        stats()
    else:
        error()


def stats():
    if getTokenNum() == None:
        return
    elif getTokenNum() == 13 or getTokenNum() == 14 or getTokenNum() == 15 or getTokenNum() == 16 or getTokenNum() == 17:
        if getTokenNum() == 13:
            # print("setArray")
            drawLines("setArray")
        elif getTokenNum() == 14:
            # print("setArrayPlus")
            drawLines("setArrayPlus")
        elif getTokenNum() == 15:
            # print("setBoat")
            drawLines("setBoat")
        elif getTokenNum() == 16:
            # print("setI")
            drawLines("setI")
        elif getTokenNum() == 17:
            # print("setJ")
            drawLines("setJ")
        addX()
        ID()
    elif getTokenNum() == 2 or getTokenNum() == 3 or getTokenNum() == 6:
        if getTokenNum() == 2:
            # print("arrayJ")
            drawLines("arrayJ")
        elif getTokenNum() == 3:
            # print("arrayPlus")
            drawLines("arrayPlus")
        elif getTokenNum() == 6:
            # print("boat")
            drawLines("boat")
        addX()
        ID()
    elif getTokenNum() == 1:
        # print("add")
        drawLines("add")
        addX()
        if getTokenNum() == 19:
            # print("add 10")
            drawLines("10")
        elif getTokenNum() == 20:
            # print("add 7")
            drawLines("7")
        elif getTokenNum() == 21:
            # print("add 3")
            drawLines("3")
        elif getTokenNum() == 22:
            # print("add 1")
            drawLines("1")
        elif getTokenNum() == 23:
            # print("add 6")
            drawLines("6")
        else:
            error()
    elif getTokenNum() == 8:
        # print("if")
        drawLines("if")
        addX()
        if getTokenNum() == 9:
            # print("ifCon")
            drawLines("ifCon")
            addX()
            if getTokenNum() == 18:
                # print("swap")
                drawLines("swap")
                addX()
            else:
                error()

        else:
            error()
    elif getTokenNum() == 12:
        # print("repeat")
        drawLines("repeat")
        addX()
        TIME()
    else:
        error()


def funcdef():
    if getTokenNum() == None:
        return
    elif getTokenNum() == 7:
        # print("define")
        drawLines("define")
        addX()
        stats()
    else:
        error()


def plus():
    if getTokenNum() == None:
        return
    elif getTokenNum() == 10:
        # print("iPlus")
        drawLines("iPlus")
    elif getTokenNum() == 11:
        # print("jPlus")
        drawLines("jPlus")
    else:
        error()


def match(i):
    if i == 1:
        stats()
    elif i == 2 or i == 3 or i == 6:
        ID()
    elif i == 4 or i == 5:
        TIME()
    elif i == 7:
        funcdef()
    elif i == 8:
        stats()
    elif i == 10 or i == 11:
        plus()
    elif i == 12 or i == 13 or i == 14 or i == 15 or i == 16 or i == 17:
        stats()
    else:
        error()


if __name__ == '__main__':

    cv2.namedWindow("camera", 1)
    # 開啓ip攝像頭
    # admin是賬號，admin是密碼
    video = "http://admin:admin@192.168.88.72:8081/"  # 此處@後的ipv4 地址需要修改為自己的地址
    capture = cv2.VideoCapture(video)

    while True:
        sort_ids = []
        success, frame = capture.read()
        if not success:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        marker_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        arucoParams = cv2.aruco.DetectorParameters_create()
        marker_corners, marker_IDs, reject = aruco.detectMarkers(
            gray_frame, marker_dict, parameters=arucoParams
        )
        if marker_corners:
            marker_IDs = marker_IDs.flatten()
            for ids, corners in zip(marker_IDs, marker_corners):
                corners = corners.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                # convert each of the (x, y)-coordinate pairs to integers
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                # compute and draw the center (x, y)-coordinates of the
                # ArUco marker
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(frame, (cX, cY), 4, (255, 0, 0), -1)
                sort_ids.append((ids, cX, cY, topLeft,
                                 topRight, bottomRight, bottomLeft))
            # Sort left to right and top to bottom
            # (id,x,y)
            sort_ids = sorted(sort_ids, key=lambda x: x[1] + 3 * x[2])
            tokens = sort_ids
            x = 0
            while x < len(tokens):
                match(tokens[x][0])
        cv2.imshow("frame", frame)
        time.sleep(0.5)

        # 按鍵處理，注意，焦點應當在攝像頭窗口，不是在終端命令行窗口
        key = cv2.waitKey(10)

        if key == 27:
            # esc鍵斷開連接
            print("esc break...")
            break

    capture.release()
    cv2.destroyWindow("frame")
