import sys
from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QWidget,
)
import pandas as pd


class ExcelReaderApp(QWidget):
    def __init__(self):
        super(ExcelReaderApp, self).__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Add buttons to select Excel files
        self.btn1 = QPushButton("Select First Excel File", self)
        self.btn1.clicked.connect(lambda: self.select_file(1))
        layout.addWidget(self.btn1)

        self.btn2 = QPushButton("Select Second Excel File", self)
        self.btn2.clicked.connect(lambda: self.select_file(2))
        layout.addWidget(self.btn2)

        self.btn3 = QPushButton("Select Third Excel File", self)
        self.btn3.clicked.connect(lambda: self.select_file(3))
        layout.addWidget(self.btn3)

        # Add a run button to print Excel contents
        self.run = QPushButton("Run", self)
        self.run.clicked.connect(self.run_process)
        layout.addWidget(self.run)

        self.filePaths = [None, None, None]
        self.setLayout(layout)

    def select_file(self, file_number):
        file_dialog = QFileDialog()
        file_path = file_dialog.getOpenFileName(
            self, "Open file", "c:\\", "Excel files (*.xlsx *.xls *.csv)"
        )
        if file_path[0]:
            self.filePaths[file_number - 1] = file_path[0]

    def run_process(self):
        print("hey")
        for file_path in self.filePaths:
            if file_path is not None:
                df = pd.read_excel(file_path)
                print(df.to_string())  # Print data frame to console


def main():
    app = QApplication(sys.argv)
    ex = ExcelReaderApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
