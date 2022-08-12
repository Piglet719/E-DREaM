import cv2

if __name__ == '__main__':

    cv2.namedWindow("camera", 1)
    # 開啓ip攝像頭
    # admin是賬號，admin是密碼
    video = "http://admin:admin@192.168.88.72:8081/"  # 此處@後的ipv4 地址需要修改為自己的地址
    capture = cv2.VideoCapture(video)

    num = 0
    while True:
        success, img = capture.read()
        cv2.imshow("camera", img)

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
            cv2.imwrite(filename, img)

    capture.release()
    cv2.destroyWindow("camera")
