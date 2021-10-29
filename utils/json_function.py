import json
import sys


def readJson(jsonFile) -> json:
    """json 을 읽는 함수"""
    with open(jsonFile) as jf:
        return json.load(jf)


def writeJson(jsonFile: str, data: json) -> None:
    """json 을 수정하거나 만드는 함수"""
    with open(jsonFile, "w") as jf:
        json.dump(data, jf, indent=2)


def deleteLabel(jsonFile, deleteLabels) -> None:
    """json 에 있는 라벨을 삭제하는 함수"""
    res = []
    data = readJson(jsonFile)
    shapes = data["shapes"]
    for shape in shapes:
        label = shape["label"]
        if label not in deleteLabels:
            res.append(shape)
    data["shapes"] = res
    writeJson(jsonFile, data)


def changeLabel(jsonFile, modify, changeLabels):
    data = readJson(jsonFile)
    shapes = data["shapes"]
    for shape in shapes:
        label = shape["label"]
        if label in changeLabels:
            shape["label"] = modify
    writeJson(jsonFile, data)


def deleteEmpolyeeNum(jsonFiles):
    """의료 사원번호 제거"""
    for jsonfile in jsonFiles:
        try:
            data = readJson(jsonfile)
            shapes = data["shapes"]
            for shape in shapes:
                shape["label"] = (
                    "_".join(shape["label"].split("_")[:-1])
                    if shape["label"].count("_") == 2
                    else shape["label"]
                )
            writeJson(jsonfile, data)
        except:
            print("%s 의 파일 확인완료" % jsonfile)
            sys.exit()


if __name__ == "__main__":
    import os

    inputPath = input("input work path: ").replace("\\", "/")
    for root, path, files in os.walk(inputPath):
        if files:
            jsons = [os.path.join(root, f) for f in files if f.endswith(".json")]
            deleteEmpolyeeNum(jsons)
    print("success")
