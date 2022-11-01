import matplotlib.pyplot as plt
from PIL import Image

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

# img = 'files/results/gt_316/address_1.png'
# img = Image.open(img)
# s = detector.predict(img)
# print(s)