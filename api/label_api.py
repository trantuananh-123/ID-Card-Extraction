from flask import Blueprint, request, render_template
from flask import jsonify, redirect, url_for

from database.sql_alchemy_init import db

from database.models.label import Label

label = Blueprint('label', __name__)


@label.route("/get-all", methods=['GET'])
def label_get_all():
    label_list = Label.query.order_by(Label.create_date.desc()).all()
    result = [label.serialize() for label in label_list]
    return render_template('label/label_management.html', label_list=enumerate(result, start=0))


@label.route("/save", methods=['POST'])
def label_save():
    print(request.form)
    if request.form:
        data = request.form

        name = data['name']
        status = data['status'] == '1'

        label = Label(name, status)

        db.session.add(label)
        db.session.commit()

        return redirect(url_for('label.label_get_all'))


@label.route("/update", methods=['POST'])
def label_update():
    if request.method == 'POST':
        if request.form:
            label = Label.query.get(request.form['edit_id'])
            data = request.form
            
            label.name = data['name']
            label.status = data['status'] == '1'

            print(label.serialize())

            db.session.commit()

        return redirect(url_for('label.label_get_all'))


@label.route("/detail/<int:id>", methods=['GET'])
def label_detail(id):
    label = Label.query.get(id)

    if label == None:
        return jsonify(
            data=None,
            message='Nhãn không tồn tại',
            status=400
        ), 400

    return jsonify(
        data=label.serialize(),
        message='Lấy thông tin chi tiết nhãn thành công',
        status=200
    ), 200


@label.route("/delete", methods=['POST'])
def label_delete():
    print(request.form)
    if request.method == 'POST':
        if request.form:
            label = Label.query.get(request.form['delete_id'])
            db.session.delete(label)
            db.session.commit()

            return redirect(url_for('label.label_get_all'))