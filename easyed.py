#создай тут фоторедактор Easy Editor!
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget
from PIL import Image
from PIL import ImageOps
import os

from PIL.ImageFilter import SHARPEN


app = QApplication([])
win = QWidget()

#Виджеты
btn_dir = QPushButton('Папка')
win.resize(700,400)
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_zerkalo = QPushButton('Зеркало')
btn_rezko = QPushButton('Резкость')
btn_ch_and_b = QPushButton('Ч/б')
btn_save = QPushButton('Сохранить')
btn_original = QPushButton('Сбросить фильтры')
list_photo = QListWidget()
photo = QLabel('Картинка')

#Линии
row = QHBoxLayout()
row_toots = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()

#Добовление виджетов к линиям
col1.addWidget(btn_dir)
col1.addWidget(list_photo)
col2.addWidget(photo, 95)

row_toots.addWidget(btn_left)
row_toots.addWidget(btn_right)
row_toots.addWidget(btn_zerkalo)
row_toots.addWidget(btn_rezko)
row_toots.addWidget(btn_ch_and_b)
row_toots.addWidget(btn_save)
row_toots.addWidget(btn_original)

#Добовление линий к главным линиям
col2.addLayout(row_toots)
row.addLayout(col1, 20)
row.addLayout(col2, 80)


workdir = ''
files = list()
extensions = list()
def filter(files, extensions):
    result = list()
    for filename in files:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
    return result
        
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def showFilenamesList():
    extensions =['.jpg', '.gif', '.png', '.bmp', '.svg']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    list_photo.clear()
    for filename in filenames:
        list_photo.addItem(filename)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.original_image = None
        self.filename = None
        self.dir = None
        self.savedir = "Modified/"
        
    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)
        self.original_image = self.image.copy()

    def saveImage(self):
        path = os.path.join(workdir, self.savedir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def showImage(self, path):
        pixmapimage = QPixmap(path) 
        label_widht, label_height = photo.width(), photo.height()
        scaled_pixmap = pixmapimage.scaled(label_widht, label_height, Qt.KeepAspectRatio)
        photo.setPixmap(scaled_pixmap)
        photo.setVisible(True)

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)

    def turn_left(self):
        self.image = self.image.rotate(90)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)

    def turn_right(self):
        self.image = self.image.rotate(270)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)
        
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)

    def resetImage(self):
        if self.original_image:
            self.image = self.original_image.copy()
            image_path = os.path.join(workdir,self.filename)
            self.showImage(image_path)
    
    def rezko(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.savedir, self.filename)
        self.showImage(image_path)


workimage = ImageProcessor()

def showChosenImage():
    if list_photo.currentRow() >= 0:
        filename = list_photo.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)



list_photo.currentRowChanged.connect(showChosenImage)
btn_ch_and_b.clicked.connect(workimage.do_bw)
btn_zerkalo.clicked.connect(workimage.do_flip)
btn_left.clicked.connect(workimage.turn_left)
btn_right.clicked.connect(workimage.turn_right)
btn_original.clicked.connect(workimage.resetImage)
btn_rezko.clicked.connect(workimage.rezko)
btn_dir.clicked.connect(showFilenamesList)
win.setLayout(row)
win.show()
app.exec()