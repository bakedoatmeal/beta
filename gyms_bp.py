from flask import Flask, render_template, request, redirect, url_for, Blueprint
from database import app, climbers, climbs, gyms, db, mongo
from  bson.objectid import ObjectId

gyms_bp = Blueprint("gyms_bp", __name__, static_folder='static', template_folder='templates')

@gyms_bp.route('/', methods=['POST'])
def gyms_submit():
    """Insert a new gym"""
    gym = {
        'name': request.form.get('name'),
        'city': request.form.get('city'),
        'types': request.form.get('type'),
        'description': request.form.get('description'),
    }
    print(gym)
    gyms.insert_one(gym)
    for gym in gyms.find():
        print(gym)
    return redirect(url_for('index'))

@gyms_bp.route('/new')
def gyms_new():
    return render_template('gyms_new.html')

@gyms_bp.route('/<gym_id>')
def gyms_show(gym_id):
    gym = gyms.find_one({'_id': ObjectId(gym_id)})
    gym_climbs = climbs.find({'gym': ObjectId(gym_id)})

    return render_template('gyms_show.html', gym = gym, climbs=gym_climbs)

@gyms_bp.route('/<gym_id>', methods=['POST'])
def gyms_update(gym_id):
    updated_gym = {
        'name': request.form.get('name'),
        'city': request.form.get('city'),
        'types': request.form.get('type'),
        'description': request.form.get('description'),
    }
    gyms.update_one(
        {'_id': ObjectId(gym_id)}, 
        {'$set': updated_gym}
    )
    return redirect(url_for('gyms_bp.gyms_show', gym_id=gym_id ))


@gyms_bp.route('/<gym_id>/delete', methods=['POST'])
def gyms_delete(gym_id):
    gyms.delete_one({'_id': ObjectId(gym_id)})
    return redirect(url_for('index'))

@gyms_bp.route('/<gym_id>/edit')
def gyms_edit(gym_id):
    gym = gyms.find_one({'_id': ObjectId(gym_id)})
    return render_template('gyms_edit.html', gym = gym)

