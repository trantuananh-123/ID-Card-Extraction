import matplotlib.pyplot as plt
from PIL import Image
import os
import codecs

from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg

config = Cfg.load_config_from_name('vgg_transformer')
config['weights'] = './weights/my_ocr.pth'
config['device'] = 'cpu'

detector = Predictor(config)


def extract(crop_img):
    img = Image.fromarray(crop_img)
    s = detector.predict(img)
    return s


def extract2(img):
    img = Image.open(img)
    s = detector.predict(img)
    return s


img = Image.open('D:/Captures/108_crops/crop_31.png')
s = detector.predict(img)
print(s)

# root_path = "D:/hệ thống thông minh/Data/"
# for i in range(0, 101):
#     folder = root_path + 'CCCD' + str(i) + '_crops/'
#     for file in os.listdir(folder):
#         if file.endswith(".png") or file.endswith(".jpg"):
#             image = folder + file
#             img = Image.open(image)
#             s = detector.predict(img)
#             with codecs.open(image.split(".")[0] + '.txt', 'w+', 'utf-8') as text_file:
#                 text_file.write('data/' + file + ' ' + s)
#     i = i + 1
#     print(s)

# img = 'D:/Nam-4/Nam-4/Phat-Trien-HTTM/psenet-text-detector-master/outputs/gt_302_crops/crop_21.png'
