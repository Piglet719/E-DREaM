import cv2
from cv2 import aruco
import numpy as np

marker_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

arucoParams = cv2.aruco.DetectorParameters_create()

if __name__ == '__main__':

    cv2.namedWindow("camera", 1)
    # 開啓ip攝像頭
    # admin是賬號，admin是密碼
    video = "http://admin:admin@192.168.88.72:8081/"  # 此處@後的ipv4 地址需要修改為自己的地址
    capture = cv2.VideoCapture(video)

    num = 0
    while True:
        success, frame = capture.read()
        if not success:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        marker_corners, marker_IDs, reject = aruco.detectMarkers(
            gray_frame, marker_dict, parameters=arucoParams
        )
        if marker_corners:
            for ids, corners in zip(marker_IDs, marker_corners):
                cv2.polylines(frame, [corners.astype(np.int32)],
                              True, (0, 255, 255), 4, cv2.LINE_AA)
                corners = corners.reshape(4, 2)
                corners = corners.astype(int)
                top_right = corners[0].ravel()
                cv2.putText(frame, f"id: {ids[0]}", top_right,
                            cv2.FONT_HERSHEY_PLAIN, 1.3, (200, 100, 0), 2, cv2.LINE_AA)
                # print(ids, " ", corners)
        cv2.imshow("frame", frame)

        # 按鍵處理，注意，焦點應當在攝像頭窗口，不是在終端命令行窗口
        key = cv2.waitKey(10)

        if key == 27:
            # esc鍵斷開連接
            print("esc break...")
            break
        if key == ord(' '):
            # 保存一張圖像到工作目錄
            num = num + 1
            filename = "frames_%s.jpg" % num
            cv2.imwrite(filename, frame)

    capture.release()
    cv2.destroyWindow("camera")
