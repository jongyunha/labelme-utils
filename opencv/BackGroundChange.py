from shapely.geometry import Point, Polygon
from utils.json_function import readJson
import cv2 as cv


def getShapesPolygons(json):
    data = readJson(json)
    shapes = data["shapes"]
    points = shapes[0]["points"]
    return Polygon(points)


def backgroundChangeBlack(img, polygon, height, width):
    for y in range(height):
        for x in range(width):
            cur = Point(x, y)
            if not cur.within(polygon):
                img.itemset(y, x, 0, 0)
                img.itemset(y, x, 1, 0)
                img.itemset(y, x, 2, 0)
    return img


if __name__ == "__main__":
    from python.osSystemFunc.MainOs import MainOs

    mainos = MainOs("/Users/jongyunha/Desktop/CE_02")
    rmFiles = mainos.getAllSelectText("localization")
    for rmFile in rmFiles:
        mainos.removeFile(rmFile, static=True)
    files = mainos.getAllSelectExtension("jpg")
    for file in files:
        img = cv.imread(file, cv.IMREAD_COLOR)
        height, width = img.shape[:2]
        polygon = getShapesPolygons("sample.json")
        changeImg = backgroundChangeBlack(img, polygon, height, width)
        cv.imwrite(file, changeImg)
    print("success")
