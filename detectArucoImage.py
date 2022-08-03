import argparse
import imutils
import cv2
import sys

# 構造參數解析器並解析參數
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="Path to the input image containing the ArUCo tag")
ap.add_argument("-t", "--type", type=str,
                default="DICT_ARUCO_ORIGINAL", help="Type of ArUCo to detect")
args = vars(ap.parse_args())

# 定義 OpenCV 支持的每個可能的 ArUco 標籤的名稱
ARUCO_DICT = {"DICT_4X4_50": cv2.aruco.DICT_4X4_50, "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
              "DICT_4X4_250": cv2.aruco.DICT_4X4_250, "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
              "DICT_5X5_50": cv2.aruco.DICT_5X5_50, "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
              "DICT_5X5_250": cv2.aruco.DICT_5X5_250, "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
              "DICT_6X6_50": cv2.aruco.DICT_6X6_50, "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
              "DICT_6X6_250": cv2.aruco.DICT_6X6_250, "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
              "DICT_7X7_50": cv2.aruco.DICT_7X7_50, "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
              "DICT_7X7_250": cv2.aruco.DICT_7X7_250, "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
              "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
              "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
              "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
              "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
              "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11}

# 從磁盤加載輸入圖像並調整其大小
print("[INFO] Loading image...")
image = cv2.imread(args["image"])
image = imutils.resize(image, width=600)

# 驗證 OpenCV 是否支持提供的 ArUco 標籤
if ARUCO_DICT.get(args["type"], None) is None:
    print("[INFO] ArUCo tag of '{}' is not supported!".format(args["type"]))
    sys.exit(0)

# 加載 ArUCo 字典，抓取 ArUCo 參數並檢測標記
print("[INFO] Detecting '{}' tags...".format(args["type"]))
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters_create()
(corners, ids, rejected) = cv2.aruco.detectMarkers(
    image, arucoDict, parameters=arucoParams)

# 驗證至少一個 ArUCo 標記被檢測到
if len(corners) > 0:
    # 展平 ArUCo ID 列表
    ids = ids.flatten()
    # 循環檢測到的 ArUCo 標記
    for (markerCorner, markerID) in zip(corners, ids):
        # 提取始終按以下順序返回的標記:
        # TOP-LEFT, TOP-RIGHT, BOTTOM-RIGHT, BOTTOM-LEFT
        corners = markerCorner.reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners
        # 將每個 (x, y) 座標對轉換為整數
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))
        # 繪製 ArUCo 檢測的邊界框
        cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
        cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
        cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
        cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
        # 計算並繪製 ArUCo 標記的中心 (x, y) 座標
        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)
        cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
        print("[INFO] ArUco marker ID: {}".format(markerID))
        # 在圖像上繪製 ArUCo 標記 ID
        cv2.putText(image, str(
            markerID), (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # 顯示輸出圖像
        cv2.imshow("Image", image)
        cv2.waitKey(0)
