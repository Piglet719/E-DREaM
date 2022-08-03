import cv2
import numpy as np

dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

markerImage = np.zeros((200, 200), dtype=np.uint8)
for i in range(30):
    markerImage = cv2.aruco.drawMarker(dictionary, i, 200, markerImage, 1)

    filename = 'armark/'+str(i)+'.png'
    cv2.imwrite(filename, markerImage)
