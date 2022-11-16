import matplotlib.pyplot as plt
from PIL import Image
import os
import codecs

from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg

config = Cfg.load_config_from_name('vgg_transformer')
config['weights'] = './weights/ocr.pth'
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


# root_path = "D:/Nam-4/Nam-4/Phat-Trien-HTTM/psenet-text-detector-master/outputs/"
# for i in range(314, 424):
#     folder_name = 'gt_' + str(i) + '_crops/'
#     folder = root_path + folder_name
#     for file in os.listdir(folder):
#         if file.endswith(".png") or file.endswith(".jpg"):
#             image = folder + file
#             img = Image.open(image)
#             s = detector.predict(img)
#             with codecs.open('D:/Nam-4/Nam-4/Phat-Trien-HTTM/psenet-text-detector-master/outputs/result.txt', 'a+', 'utf-8') as text_file:
#                 text_file.write('data/' + folder_name + file + ' ' + s + '\n')
#     i = i + 1
    # print(s)

# img = 'D:/Nam-4/Nam-4/Phat-Trien-HTTM/psenet-text-detector-master/outputs/gt_302_crops/crop_21.png'
