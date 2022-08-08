"""
setID		:= setBoat | setArray | setArrayPlus | setI | setJ
ID		    := arrayJ | boat | arrayPlus
TIME		:= arrayLength | arrayLengthInloop
stats		:= setID ID | add INT | if ifCon swap | repeat TIME
funcdef	    := define stats
plus		:= iPlus | jPlus
"""

import cv2
import cv2.aruco as aruco


def imgDetection():
    total = 0
    #cap = cv2.VideoCapture(0)

    global frame
    frame = cv2.imread('test2.jpg')
    frame = cv2.resize(frame, None, fx=1, fy=1,
                       interpolation=cv2.INTER_CUBIC)  # resize img
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters_create()

    '''    detectMarkers(...)
        detectMarkers(image, dictionary[, corners[, ids[, parameters[, rejectedI
        mgPoints]]]]) -> corners, ids, rejectedImgPoints
        '''
    # lists of ids and the corners beloning to each id
    #corners, idss, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    corners, ids, rejectedImgPoints = aruco.detectMarkers(
        gray, aruco_dict, parameters=parameters)

    gray = aruco.drawDetectedMarkers(gray, corners)
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    # verify *at least* one ArUco marker was detected
    if len(corners) > 0 and len(frame) > 0:
        total = total + 1

        # flatten the ArUco IDs list
        ids = ids.flatten()

        sort_ids = []
        for(markerCorner, markerID) in zip(corners, ids):

            # extract the marker corners (which are always returned in
            # top-left, top-right, bottom-right, and bottom-left order)
            corners = markerCorner.reshape((4, 2))
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

            sort_ids.append((markerID, cX, cY, topLeft,
                            topRight, bottomRight, bottomLeft))

        # Sort left to right and top to bottom
        # (id,x,y)
        print(sort_ids)
        sort_ids = sorted(sort_ids, key=lambda x: x[1] + 3 * x[2])
        print(sort_ids)
    return(sort_ids)


tokens = imgDetection()

x = 0
body = []
FunctionDef = []
FunctionBody = []
FunctionAssign1 = []
FunctionAssign2 = []
FunctionAssign3 = []
# print without quotes and brackets
translation = {39: None, 91: None, 93: None, 40: None, 41: None}
translation2 = {39: None}  # print without quotes
print("Module(body=[", end='')


def error():
    cv2.putText(frame, "Syntax Error",
                (tokens[x][3][0], tokens[x][3][1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.line(frame, tokens[x][3], tokens[x][4], (0, 0, 255), 2)
    cv2.line(frame, tokens[x][4], tokens[x][5], (0, 0, 255), 2)
    cv2.line(frame, tokens[x][5], tokens[x][6], (0, 0, 255), 2)
    cv2.line(frame, tokens[x][6], tokens[x][3], (0, 0, 255), 2)
    cv2.imshow("Image", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    exit()


def addX():
    # move to next token
    global x
    if x > len(tokens):
        print("Out of bounds")
        exit()
    else:
        x += 1


def getTokenNum():
    return tokens[x][0]


def ID():
    if getTokenNum() == 2:
        # print("arrayJ")
        FunctionAssign1.append('value=Name(id="arrayJ"))')
        addX()
    elif getTokenNum() == 3:
        # print("arrayPlus")
        FunctionAssign2.append('value=Name(id="arrayPlus"))')
        addX()
    elif getTokenNum() == 6:
        # print("boat")
        FunctionAssign3.append('value=Name(id="boat"))')
        addX()
    else:
        error()


def TIME():
    if getTokenNum() == 4:
        # print("arrayLength")
        print("args=[Name(id='arrayLength')]), ", end='')
        addX()
        stats()
    elif getTokenNum() == 5:
        # print("arrayLengthInloop")
        print("args=[Name(id='arrayLengthInloop')]), ", end='')
        addX()
        stats()
    else:
        error()


def stats():
    if getTokenNum() == 13 or getTokenNum() == 14 or getTokenNum() == 15 or getTokenNum() == 16 or getTokenNum() == 17:
        if getTokenNum() == 13:
            # print("setArray")
            FunctionAssign2.append('Assign(targets=[Name(id="array")]')
        elif getTokenNum() == 14:
            # print("setArrayPlus")
            FunctionAssign3.append('Assign(targets=[Name(id="arrayPlus")]')
        elif getTokenNum() == 15:
            # print("setBoat")
            FunctionAssign1.append('Assign(targets=[Name(id="boat")]')
        elif getTokenNum() == 16:
            # print("setI")
            FunctionAssign1.append('Assign(targets=[Name(id="i")]')
        elif getTokenNum() == 17:
            # print("setJ")
            FunctionAssign1.append('Assign(targets=[Name(id="j")]')
        addX()
        ID()
    elif getTokenNum() == 2 or getTokenNum() == 3 or getTokenNum() == 6:
        if getTokenNum() == 2:
            # print("arrayJ")
            FunctionAssign1.append('value=Name(id="arrayJ"))')
        elif getTokenNum() == 3:
            # print("arrayPlus")
            FunctionAssign2.append('value=Name(id="arrayPlus"))')
        elif getTokenNum() == 6:
            # print("boat")
            FunctionAssign3.append('value=Name(id="boat"))')
        addX()
        ID()
    elif getTokenNum() == 1:
        # print("add")
        addX()
        if getTokenNum() == 19:
            print("add 10")
        elif getTokenNum() == 20:
            print("add 7")
        elif getTokenNum() == 21:
            print("add 3")
        elif getTokenNum() == 22:
            print("add 1")
        elif getTokenNum() == 23:
            print("add 6")
        else:
            error()
    elif getTokenNum() == 8:
        # print("if")
        print("If(", end='')
        addX()
        if getTokenNum() == 9:
            # print("ifCon")
            print(
                'test=Compare(left=Subscript(value=Name(id="array"), slice=Name(id="j")), ops=[Gt()], comparators=[Subscript(value=Name(id="array"), slice=BinOp(left=Name(id="j"), op=Add(), right=Constant(value=1),)]),', end='')
            addX()
            if getTokenNum() == 18:
                # print("swap")
                print('body=[Expr(value=Call(func=Name(id="swap")))]', end='')
                addX()
            else:
                error()

        else:
            error()
    elif getTokenNum() == 12:
        # print("repeat")
        print("For(", end='')
        addX()
        TIME()
    else:
        error()


def funcdef():
    if getTokenNum() == 7:
        # print("define")
        print("FunctionDef(", end='')
        FunctionDef.append('name="swap"')
        FunctionDef.append('body=')
        body.append(tuple(FunctionDef))
        print(str(body).translate(translation), end='')
        addX()
        stats()
    else:
        error()


def plus():
    if getTokenNum() == 10:
        print("iPlus")
    elif getTokenNum() == 11:
        print("jPlus")
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


while x < len(tokens):
    match(tokens[x][0])

if len(FunctionAssign1) != 0:
    FunctionBody.append(str(tuple(FunctionAssign1)).translate(translation2))
if len(FunctionAssign2) != 0:
    FunctionBody.append(str(tuple(FunctionAssign2)).translate(translation2))
if len(FunctionAssign3) != 0:
    FunctionBody.append(str(tuple(FunctionAssign3)).translate(translation2))

if len(FunctionAssign1) != 0 or len(FunctionAssign2) != 0 or len(FunctionAssign3) != 0:
    print(str(FunctionBody).translate(translation2), end='')

print("])")
cv2.imshow("Image", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
