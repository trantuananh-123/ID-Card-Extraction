from database.sql_alchemy_init import db
from database.models.label import Label
from database.models.example import Example

from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin
from flask import request

from api.label_api import label
from api.example_api import example

import os
import cv2
import sys
from PIL import Image

from predict import predict

# Khởi tạo Flask Server Backend
app = Flask(__name__)
app.register_blueprint(label, url_prefix='/label')
app.register_blueprint(example, url_prefix='/example')


# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/id_card_extraction'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = "static"


@app.route('/', methods=['POST'])
def predict_yolov7():
    image = request.files['file']
    if image:
        # Lưu file
        path_to_save = os.path.join(
            app.config['UPLOAD_FOLDER'], image.filename)
        # print("Save = ", path_to_save)
        # image.save(path_to_save)

        # frame = cv2.imread(path_to_save)
        # cv2.imwrite(path_to_save, frame)

        img = predict('D:/Nam-4/Nam-4/HTTM/Flask/yolov7/weights/best.pt',
                      'D:/Nam-4/Nam-4/HTTM/Flask/yolov7/data/my_dataset.yaml', path_to_save)

        result = Image.fromarray(img)
        result.save(path_to_save)

        cv2.imshow('result', img)
        cv2.waitKey(0)
    #     # Nhận diên qua model Yolov6
    #     frame, no_object = yolov6_model.infer(frame)

    #     if no_object > 0:
    #         cv2.imwrite(path_to_save, frame)

    #     del frame
    #     # Trả về đường dẫn tới file ảnh đã bounding box
        return path_to_save  # http://server.com/static/path_to_save


@app.route('/image', methods=['GET'])
def get_image():
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'gt_314.png')
    return render_template("test.html", user_image=image_path)


# @app.route('/label_management', methods=['GET'])
# def label_management():
#     labelList = Label.query.all()
#     result = [label.serialize() for label in labelList]
#     return jsonify(result), 200


# @app.route('/label_management/add', methods=['POST'])
# def label_management_add():
#     if request.data:
#         data = request.get_json()

#         if 'name' not in data or data['name'] == '':
#             return jsonify(
#                 data=None,
#                 message='Tên nhãn không được bỏ trống',
#                 status=400
#             )
#         elif 'status' not in data or data['status'] == '':
#             return jsonify(
#                 data=None,
#                 message='Trạng thái nhãn không được bỏ trống',
#                 status=400
#             )
#         name = data['name']
#         status = data['status']

#         label = Label(name, status)

#         db.session.add(label)
#         db.session.commit()

#         return jsonify(label.serialize()), 200


# Start Backend
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='localhost', port='5000', debug=True)
