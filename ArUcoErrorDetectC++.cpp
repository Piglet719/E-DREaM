#include <opencv2/aruco.hpp>
#include <opencv2/opencv.hpp>
#define MAXCODESIZE 500

using namespace cv;

Mat inputImage, outputImage;
struct ARUCO
{
    int id;
    Point2f center;
    std::vector<Point2f> corner;
};
int cnt;
ARUCO code[MAXCODESIZE];
int x = 0;

void stats();

void addX() {
    if (x < cnt) {
        x++;
    }
    else {
        std::cout << "Out of bounds";
        exit(0);
    }
}

int getTokenNum() {
    if (x < cnt) {
        return code[x].id;
    }
    else {
        std::cout << "Out of bounds";
        exit(0);
    }
}

void draw(String name) {
    line(outputImage, code[x].corner[0], code[x].corner[1], Scalar(0, 255, 0), 2);
    line(outputImage, code[x].corner[1], code[x].corner[2], Scalar(0, 255, 0), 2);
    line(outputImage, code[x].corner[2], code[x].corner[3], Scalar(0, 255, 0), 2);
    line(outputImage, code[x].corner[3], code[x].corner[0], Scalar(0, 255, 0), 2);
    putText(outputImage, name, code[x].center, FONT_HERSHEY_SIMPLEX, 1, Scalar(0, 255, 0), 2);
}

void error() {
    line(outputImage, code[x].corner[0], code[x].corner[1], Scalar(0, 0, 255), 2);
    line(outputImage, code[x].corner[1], code[x].corner[2], Scalar(0, 0, 255), 2);
    line(outputImage, code[x].corner[2], code[x].corner[3], Scalar(0, 0, 255), 2);
    line(outputImage, code[x].corner[3], code[x].corner[0], Scalar(0, 0, 255), 2);
    putText(outputImage, "Syntax Error", code[x].center, FONT_HERSHEY_SIMPLEX, 1, Scalar(0, 0, 255), 2);
    imshow("result", outputImage);
    waitKey();
    exit(0);
}

void ID() {
    if (getTokenNum() == 2) {
        //std::cout << "arrayJ";
        draw("arrayJ");
        addX();
    }
    else if (getTokenNum() == 3) {
        //std::cout << "arrayPlus";
        draw("arrayPlus");
        addX();
    }
    else if (getTokenNum() == 6) {
        //std::cout << "boat";
        draw("boat");
        addX();
    }
    else {
        error();
    }
}

void TIME() {
    if (getTokenNum() == 4) {
        //std::cout << "arrayLength";
        draw("arrayLength");
        addX();
        stats();
    }
    else if (getTokenNum() == 5) {
        //std::cout << "arrayLengthInloop";
        draw("arrayLengthInloop");
        addX();
        stats();
    }
    else {
        error();
    }
}

void stats() {
    if (getTokenNum() == 13 || getTokenNum() == 14 || getTokenNum() == 15 || getTokenNum() == 16 || getTokenNum() == 17) {
        if (getTokenNum() == 13) {
            //std::cout << "setArray";
            draw("setArray");
        }
        else if (getTokenNum() == 14) {
            //std::cout << "setArrayPlus";
            draw("setArrayPlus");
        }
        else if (getTokenNum() == 15) {
            //std::cout << "setBoat";
            draw("setBoat");
        }
        else if (getTokenNum() == 16) {
            //std::cout << "setI";
            draw("setI");
        }
        else if (getTokenNum() == 17) {
            //std::cout << "setJ";
            draw("setJ");
        }
        addX();
        ID();
    }
    else if (getTokenNum() == 2 || getTokenNum() == 3 || getTokenNum() == 6) {
        if (getTokenNum() == 2) {
            //std::cout << "arrayJ";
            draw("arrayJ");
        }
        else if (getTokenNum() == 3) {
            //std::cout << "arrayPlus";
            draw("arrayPlus");
        }
        else if (getTokenNum() == 6) {
            //std::cout << "boat";
            draw("boat");
        }
        addX();
        ID();
    }
    else if (getTokenNum() == 1) {
        //std::cout << "add";
        draw("add");
        addX();
        if (getTokenNum() == 19) {
            //std::cout << "10";
            draw("10");
        }
        else if (getTokenNum() == 20) {
            //std::cout << "7";
            draw("7");
        }
        else if (getTokenNum() == 21) {
            //std::cout << "3";
            draw("3");
        }
        else if (getTokenNum() == 22) {
            //std::cout << "1";
            draw("1");
        }
        else if (getTokenNum() == 23) {
            //std::cout << "6";
            draw("6");
        }
        else {
            error();
        }
    }
    else if (getTokenNum() == 8) {
        //std::cout << "if";
        draw("if");
        addX();
        if (getTokenNum() == 9) {
            //std::cout << "ifCon";
            draw("ifCon");
            addX();
            if (getTokenNum() == 18) {
                //std::cout << "swap";
                draw("swap");
                addX();
            }
            else {
                error();
            }
        }
        else {
            error();
        }
    }
    else if (getTokenNum() == 12) {
        //std::cout << "repeat";
        draw("repeat");
        addX();
        TIME();
    }
    else {
        error();
    }
}

void funcdef() {
    if (getTokenNum() == 7) {
        //std::cout << "define";
        draw("define");
        addX();
        stats();
    }
    else {
        error();
    }
}

void plus() {
    if (getTokenNum() == 10) {
        //std::cout << "iPlus";
        draw("iPlus");
    }
    else if (getTokenNum() == 11) {
        //std::cout << "jPlus";
        draw("jPlus");
    }
    else {
        error();
    }
}

void match(int i) {
    if (i == 1) {
        stats();
    }
    else if (i == 2 || i == 3 || i == 6) {
        ID();
    }
    else if (i == 4 || i == 5) {
        TIME();
    }
    else if (i == 7) {
        funcdef();
    }
    else if (i == 8) {
        stats();
    }
    else if (i == 10 || i == 11) {
        plus();
    }
    else if (i == 12 || i == 13 || i == 14 || i == 15 || i == 16 || i == 17) {
        stats();
    }
    else {
        error();
    }
}

void main() {

    inputImage = imread("D:\\internship\\NCU\\practice\\test2.jpg");

    // Load the dictionary that was used to generate the markers.
    Ptr<aruco::Dictionary> dictionary = aruco::getPredefinedDictionary(aruco::DICT_6X6_250);

    // Initialize the detector parameters using default values
    Ptr<aruco::DetectorParameters> parameters = aruco::DetectorParameters::create();

    // Declare the vectors that would contain the detected marker corners and the rejected marker candidates
    std::vector<std::vector<Point2f>> markerCorners, rejectedCandidates;

    // The ids of the detected markers are stored in a vector
    std::vector<int> markerIds;

    // Detect the markers in the image
    aruco::detectMarkers(inputImage, dictionary, markerCorners, markerIds, parameters, rejectedCandidates);

    if (markerIds.size() > 0) {
        for (int j = 0; j < markerCorners.size(); j++) {
            code[j].id = markerIds[markerCorners.size() - j - 1];
            code[j].center = (markerCorners[markerCorners.size() - j - 1][0] + markerCorners[markerCorners.size() - j - 1][1] + markerCorners[markerCorners.size() - j - 1][2] + markerCorners[markerCorners.size() - j - 1][3]) / 4.0;
            code[j].corner = markerCorners[markerCorners.size() - j - 1];
        }
        outputImage = inputImage.clone();
        cnt = markerIds.size();
        while (x < cnt) {
            match(code[x].id);
        }
    }
    imshow("result", outputImage);
    waitKey();
}