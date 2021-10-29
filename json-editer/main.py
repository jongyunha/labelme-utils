from layout import App
from PyQt5.QtWidgets import QApplication, QFileDialog, QErrorMessage, QComboBox
from utils.json_function import readJson, deleteLabel, changeLabel
from natsort import natsorted
import os


class JsonEditer(App):
    """
    labelme 의 json label 을 수정 하기 위한 GUI 입니다.
    author: 하종윤
    date: 2020-03-05
    """

    def __init__(self):
        super().__init__()
        self.setupUi()
        self.retranslateUi()
        self.show()
        self.func()

    def func(self):
        """Ui func set"""
        self.openDirBtn.clicked.connect(self.onClickOpenDir)
        self.labelAddBtn.clicked.connect(self.onClickLabelAddBtn)
        self.modifyBtn.clicked.connect(self.onClickModifyBtn)
        self.labelDelBtn.clicked.connect(self.onClickLabelDelBtn)
        self.popupMessage = QErrorMessage(self).showMessage

    def onClickOpenDir(self):
        self.path = QFileDialog.getExistingDirectory()
        self.path.replace("\\", "/")
        self.recursiveFolderSearch(self.path)

    def recursiveFolderSearch(self, path):
        self.jsonFileListWidget.clear()
        self.allLabelsComboBox.clear()
        for root, dirs, files in os.walk(path):
            if files:
                jsons = [
                    os.path.join(root, file)
                    for file in files
                    if str(file).endswith(".json")
                ]
                self.jsonFileListWidget.addItems(jsons)
                self.addLabelMiddleWare(jsons)

    def addLabelMiddleWare(self, jsons):
        labels = []
        for j in jsons:
            data = readJson(j)
            shapes = data["shapes"]
            for shape in shapes:
                labels.append(shape["label"])
        try:
            labels = sorted(labels, key=lambda x: int(x[:2]))
        except:
            labels = natsorted(labels)

        self.onChangeAddLabelComboBox(labels)

    def onChangeAddLabelComboBox(self, labels):
        for label in labels:
            self.addLabelComboBox(label)

    def addLabelComboBox(self, label):
        if self.allLabelsComboBox.findText(label) == -1:
            self.allLabelsComboBox.addItem(label)

    def onClickLabelAddBtn(self):
        cur = self.allLabelsComboBox.currentText()
        self.addLabelListWidget.addItem(cur)

    def onClickLabelDelBtn(self):
        self.jsonDelLabel(self.getLabelListWidgetItems())

    def getLabelListWidgetItems(self):
        return [
            self.addLabelListWidget.item(idx).text()
            for idx in range(self.addLabelListWidget.count())
        ]

    def getJsonFileListWidgetItems(self):
        jsonFiles = []
        for idx in range(self.jsonFileListWidget.count()):
            jsonFiles.append(self.jsonFileListWidget.item(idx).text())
        return jsonFiles

    def jsonDelLabel(self, delLabels):
        jsonFiles = self.getJsonFileListWidgetItems()
        for jsonFile in jsonFiles:
            deleteLabel(jsonFile, delLabels)
        self.popupMessage("success and reloading")
        self.recursiveFolderSearch(self.path)
        self.addLabelListWidget.clear()

    def onClickModifyBtn(self):
        toModifyLabel = self.toModifyLineEdit.text()
        if toModifyLabel:
            changeLabels = self.getLabelListWidgetItems()
            jsonFiles = self.getJsonFileListWidgetItems()
            for jsonFile in jsonFiles:
                changeLabel(jsonFile, toModifyLabel, changeLabels)
        self.popupMessage("success and reloading")
        self.recursiveFolderSearch(self.path)
        self.addLabelListWidget.clear()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    MainWindow = JsonEditer()
    sys.exit(app.exec_())
