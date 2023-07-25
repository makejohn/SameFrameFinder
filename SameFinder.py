import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QPushButton, QTextEdit, QVBoxLayout
import hashlib
import numpy as np


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.len_label = QLabel('Width')
        self.len_input = QLineEdit()

        self.width_label = QLabel('Height')
        self.width_input = QLineEdit()

        # add file path

        self.file_label = QLabel('File Path')
        self.file_input = QLineEdit()

        self.submit_btn = QPushButton('Submit')
        self.submit_btn.clicked.connect(self.submit)

        self.clear_btn = QPushButton('Clear')
        self.clear_btn.clicked.connect(self.cleartext)

        self.response_text = QTextEdit()

        layout = QVBoxLayout()

        layout.addWidget(self.len_label)
        layout.addWidget(self.len_input)
        layout.addWidget(self.width_label)
        layout.addWidget(self.width_input)
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_input)
        layout.addWidget(self.submit_btn)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.response_text)

        self.setLayout(layout)

    def cleartext(self):
        self.response_text.clear()

    def submit(self):
        try:
            width = int(self.width_input.text())
            height = int(self.len_input.text())
            file_path = self.file_input.text()
        except:
            self.response_text.setText('Please input correct data')
            return
        # read the file
        with open(file_path) as f:
            raw = np.fromfile(f, dtype=np.uint16)
        if raw.size % (width * height) != 0:
            self.response_text.setText('Shape error: make sure your shape is correct')
            return
        else:
            frames = int(raw.size / (width * height))
        # process the error of shape may not be correct
        try:
            image_date = raw.reshape((frames, width, height))
        except:
            print('Shape error: make sure your  shape is correct')
        res = ''
        hash_map = {}
        for i in range(frames):
            img = image_date[i].tobytes()
            md5_hash = hashlib.md5(img).hexdigest()
            if md5_hash in hash_map:
                res += f'Frame {i} is the same as frame {hash_map[md5_hash]}\n'
            else:
                hash_map[md5_hash] = i
        if res == '':
            res = 'No same frames'
        self.response_text.setText(res)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('SameFrameFinder')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
