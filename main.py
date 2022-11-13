from database.sql_alchemy_init import db
from database.models.label import Label
from database.models.model import Model
from models.crop_image import CropImage
from models.result import Result

from flask import Flask, render_template, jsonify, redirect, url_for
from flask_cors import CORS, cross_origin
from flask import request
from flask_dropzone import Dropzone

from api.label_api import label
from api.model_api import model
from api.example_api import example

import os
import cv2
import sys
from PIL import Image
from io import BytesIO
from scipy import misc

from predict import predict
from extract import extract, extract2
from corner import corner

# Khởi tạo Flask Server Backend
app = Flask(__name__)
app.register_blueprint(label, url_prefix='/label')
app.register_blueprint(example, url_prefix='/example')
app.register_blueprint(model, url_prefix='/model')

# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/id_card_extraction'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = "files/results"
app.config['CROP_IMAGE_FOLDER'] = "static/images"

db.init_app(app)
dropzone = Dropzone(app)

# Apply Flask CORS
CORS(app)


@app.route('/predict', methods=['POST'])
def predict_yolov7():
    image = request.files['file']
    if image:
        # Lưu file
        path_root = os.path.join(
            app.config['UPLOAD_FOLDER'], image.filename.split('.')[0])
        path_to_save = os.path.join(path_root, image.filename)
        os.makedirs(path_root, exist_ok=True)

        image.save(path_to_save)

        # frame = cv2.imread(path_to_save)
        # cv2.imwrite(path_to_save, frame)

        original_image, img, coordinate, classes, confidence, classes_id = predict('./weights/best(1).pt',
                                                                                   './data/my_dataset.yaml', path_to_save)

        result = Image.fromarray(img)
        result.save(path_to_save)

        # cv2.imshow('result', img)
        # cv2.waitKey(0)

        response = []
        for coor, _class, conf, _class_id in zip(coordinate, classes, confidence, classes_id):
            x1, y1, x2, y2 = coor[0].item(), coor[1].item(
            ), coor[2].item(), coor[3].item()
            name = _class

            crop_image = CropImage(_class_id, name, x1, x2, y1, y2, conf)
            response.append(crop_image)

        response = [item.serialize() for item in response]
        response = sorted(response, key=lambda x: x.get('id'))

        result = []
        for item in response:
            crop_img = original_image[int(item.get('y1')) - 2:int(item.get('y2')) + 2, int(
                item.get('x1')) - 2:int(item.get('x2')) + 2]
            # data = Image.fromarray(crop_img)
            result_item = Result(item.get('name').split("_")[
                                 0], extract(crop_img))
            result.append(result_item)
            # data.save(f"{path_root}/{item.get('name')}.png")

        result = [item.serialize() for item in result]
        return render_template('client/home.html', result_list=result)
        # return jsonify(
        #     data=result,
        #     message='Xuất thông tin thành công',
        #     status=200
        # ), 200


@app.route('/')
def index():
    return render_template('client/home.html')


@app.route('/crop_image')
def crop_image():
    return render_template('crop_image/crop_image.html')


@app.route('/extract_image')
def extract_image():
    return render_template('extract_image/extract_image.html')


@app.route('/corner_image')
def corner_image():
    return render_template('corner_image/corner_image.html')


@app.route('/crop_image/crop', methods=['POST'])
def crop_image_crop():
    image = request.files['file']
    if image:
        # Lưu file
        path_root = os.path.join(
            "./static/images/", image.filename.split('.')[0])
        path_to_save = os.path.join("./static/images/", image.filename)
        os.makedirs(path_root, exist_ok=True)

        image.save(path_to_save)

        # frame = cv2.imread(path_to_save)
        # cv2.imwrite(path_to_save, frame)

        original_image, img, coordinate, classes, confidence, classes_id = predict('./weights/best(1).pt',
                                                                                   './data/my_dataset.yaml', path_to_save)

        result = Image.fromarray(img)
        result.save(path_to_save)

        # cv2.imshow('result', img)
        # cv2.waitKey(0)

        response = []
        for coor, _class, conf, _class_id in zip(coordinate, classes, confidence, classes_id):
            x1, y1, x2, y2 = coor[0].item(), coor[1].item(
            ), coor[2].item(), coor[3].item()
            name = _class

            crop_image = CropImage(_class_id, name, x1, x2, y1, y2, conf)
            response.append(crop_image)

        response = [item.serialize() for item in response]
        response = sorted(response, key=lambda x: x.get('id'))

        result = []
        for item in response:
            crop_img = original_image[int(item.get('y1')) - 2:int(item.get('y2')) + 2, int(
                item.get('x1')) - 2:int(item.get('x2')) + 2]
            data = Image.fromarray(crop_img)
            # result_item = Result(item.get('name').split("_")[
            #                      0], extract(crop_img))
            result.append(
                f"../../static/images/{image.filename.split('.')[0]}/{item.get('name')}.png")
            data.save(
                f"./static/images/{image.filename.split('.')[0]}/{item.get('name')}.png")

        # result = [item.serialize() for item in result]
        return render_template('crop_image/crop_image.html', result_list=result)
        # return jsonify(
        #     data=result,
        #     message='Xuất thông tin thành công',
        #     status=200
        # ), 200


@app.route('/extract_image/extract', methods=['POST'])
def extract_image_extract():
    image = request.files['file']
    if image:
        path = os.path.join("./static/images/gt_316/", image.filename)
        path = path.replace("\\", "/")
        # imgdata = imgsrcstring.split(',')[1]
        # decoded = base64.b64decode(imgdata)
        result = extract2(path)
        return render_template('extract_image/extract_image.html', result=result)


@app.route('/corner_image/corner', methods=['POST'])
def corner_image_corner():
    image = request.files['file']
    if image:
        path = os.path.join("./static/images/", image.filename)
        path = path.replace("\\", "/")
        # imgdata = imgsrcstring.split(',')[1]
        # decoded = base64.b64decode(imgdata)
        img = corner(path)
        im = Image.fromarray(img)
        path = os.path.join("./static/images/corner_result/", image.filename)
        im.save(path)
        print(path)
        return render_template('corner_image/corner_image.html', result=path)


# Start Backend
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='localhost', port='5000', debug=True)
