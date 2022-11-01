from flask import Blueprint, request, render_template
from flask import jsonify, redirect, url_for

from database.sql_alchemy_init import db

from database.models.model import Model

import os

model = Blueprint('model', __name__)


@model.route("/get-all", methods=['GET'])
def model_get_all():
    model_list = Model.query.order_by(Model.create_date.desc()).all()
    result = [model.serialize() for model in model_list]
    return render_template('model/model_management.html', model_list=enumerate(result, start=0))


@model.route("/save", methods=['POST'])
def model_save():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        path_to_save = "files/model/" + uploaded_file.filename
        model = Model(uploaded_file.filename, path_to_save,
                      request.form['status'] == '1')
        db.session.add(model)
        db.session.commit()

        uploaded_file.save(path_to_save)
        return redirect(url_for('model.model_get_all'))


@model.route("/update", methods=['POST'])
def model_update():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        model = Model.query.get(request.form['edit_id'])
        path_to_get = "files/model/" + model.name
        
        if os.path.exists(path_to_get):
            os.remove(path_to_get)
        
        path_to_save = "files/model/" + uploaded_file.filename
        model.name = uploaded_file.filename
        model.url = path_to_save
        model.status = request.form['status'] == '1'
        db.session.add(model)
        db.session.commit()

        uploaded_file.save(path_to_save)
        return redirect(url_for('model.model_get_all'))


@model.route("/detail/<int:id>", methods=['GET'])
def model_detail(id):
    model = Model.query.get(id)

    if model == None:
        return jsonify(
            data=None,
            message='Mô hình không tồn tại',
            status=400
        ), 400

    return jsonify(
        data=model.serialize(),
        message='Lấy thông tin chi tiết mô hình thành công',
        status=200
    ), 200


@model.route("/delete", methods=['POST'])
def model_delete():
    print(request.form)
    if request.method == 'POST':
        if request.form:
            model = Model.query.get(request.form['delete_id'])
            db.session.delete(model)
            db.session.commit()

            return redirect(url_for('model.model_get_all'))


# @model.route('/', methods=['POST'])
# def upload_file():
#     uploaded_file = request.files['file']
#     if uploaded_file.filename != '':
#         path_to_save = os.path.join(
#             app.config['MODEL_UPLOAD_FOLDER'], (uploaded_file.filename)).replace("\\", "/")
#         model = Model(uploaded_file.filename, path_to_save,
#                       request.form['status'] == '1')
#         db.session.add(model)
#         db.session.commit()

#         uploaded_file.save(path_to_save)
#     return redirect(url_for('index'))
