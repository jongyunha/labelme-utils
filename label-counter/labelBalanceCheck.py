from utils.json_function import readJson
from collections import Counter
import os
import pandas as pd


def getAllJsonFiles(inputPath):
    """재귀적 폴더 탐색 모든 json file return"""
    jsonFiles = []
    for root, dirs, files in os.walk(inputPath):
        if files:
            jsonFiles.extend(
                [os.path.join(root, file) for file in files if file.endswith(".json")]
            )
    return jsonFiles


def getAllLabelUniqueCount(jsonFiles, medical=True):
    """모든 json 파일의 고유 레이블 수를 카운트 합니다."""
    uniqueLabels = []
    for jsonfile in jsonFiles:
        data = readJson(jsonfile)
        shapes = data["shapes"]
        if medical:
            for shape in shapes:
                shape["label"] = (
                    "_".join(shape["label"].split("_")[:-1])
                    if shape["label"].count("_") == 2
                    else shape["label"]
                )
        uniqueLabels.extend(list(set([shape["label"] for shape in shapes])))
    return dict(Counter(uniqueLabels))


def getAllFlagUniqueCount(jsonFiles):
    uniqueFlags = []
    for jsonfile in jsonFiles:
        data = readJson(jsonfile)
        flags = data["flags"]
        uniqueFlags.extend(
            list(set([flag for flag, boolean in flags.items() if boolean]))
        )
    return dict(Counter(uniqueFlags))


def createDataFrame():
    return [
        pd.DataFrame(columns=["label", "label_count"]),
        pd.DataFrame(columns=["flag", "flag_count"]),
    ]


def saveDataFrame(labelData, flagData):
    try:
        labelDf, flagDf = createDataFrame()
        labelDf["label"] = list(labelData.keys())
        labelDf["label_count"] = list(labelData.values())
        flagDf["flag"] = list(flagData.keys())
        flagDf["flag_count"] = list(flagData.values())
        inputSavePath = input("input save path: ").replace("\\", "/")
        inputSaveFileName = input("\ninput save file name: ")

        writer = pd.ExcelWriter(
            "%s.xlsx" % os.path.join(inputSavePath, inputSaveFileName),
            engine="xlsxwriter",
        )
        labelDf.to_excel(writer, sheet_name="label", index=False)
        flagDf.to_excel(writer, sheet_name="flag", index=False)
        writer.save()
        print("success")
    except:
        print("failure")


if __name__ == "__main__":
    inputPath = input("input work path: ").replace("\\", "/")
    jsonFiles = getAllJsonFiles(inputPath)
    labelCountData = getAllLabelUniqueCount(jsonFiles)
    flagCountData = getAllFlagUniqueCount(jsonFiles)
    saveDataFrame(labelCountData, flagCountData)
