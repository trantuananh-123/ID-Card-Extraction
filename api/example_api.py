
from flask import Blueprint, request, render_template
from flask import jsonify, redirect, url_for, abort
import imghdr
import os
from database.models.example import Example

from database.sql_alchemy_init import db

example = Blueprint('example', __name__)


# def validate_image(stream):
#     header = stream.read(512)
#     stream.seek(0)
#     format = imghdr.what(None, header)
#     if not format:
#         return None
#     return '.' + (format if format != 'jpeg' else 'jpg')


@example.route("/get-all", methods=['GET'])
def example_get_all():
    example_list = Example.query.order_by(Example.create_date.desc()).all()
    result = [example.serialize() for example in example_list]
    return render_template('example/example_management.html', example_list=enumerate(result, start=0))


@example.route('/save', methods=['POST'])
def example_save():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        path_to_save = "files/example/"+uploaded_file.filename
        # if path_to_save != validate_image(uploaded_file.stream):
        #     abort(400)
        example = Example(uploaded_file.filename, path_to_save,
                          request.form['status'] == '1')
        db.session.add(example)
        db.session.commit()
        uploaded_file.save(path_to_save)
    return redirect(url_for('example.example_get_all'))


@example.route('/update', methods=['POST'])
def example_update():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        example = Example.query.get(request.form['edit_id'])
        path_to_get = "files/example/" + example.name
        if os.path.exists(path_to_get):
            os.remove(path_to_get)

        path_to_save = "files/example/"+uploaded_file.filename
        example.name = uploaded_file.filename
        example.url = path_to_save
        example.status = request.form['status'] == '1'
        db.session.add(example)
        db.session.commit()
        uploaded_file.save(path_to_save)
    return redirect(url_for('example.example_get_all'))


@ example.route("/detail/<int:id>", methods=['GET'])
def label_detail(id):
    example = Example.query.get(id)

    if example == None:
        return jsonify(
            data=None,
            message='Nhãn không tồn tại',
            status=400
        ), 400

    return jsonify(
        data=example.serialize(),
        message='Lấy thông tin chi tiết nhãn thành công',
        status=200
    ), 200


@example.route('/delete', methods=['POST'])
def example_delete():
    if request.method == 'POST':
        if request.form:
            example = Example.query.get(request.form['delete_id'])
            
            if os.path.exists(example.url):
                os.remove(example.url)
            db.session.delete(example)
            db.session.commit()

            return redirect(url_for('example.example_get_all'))
