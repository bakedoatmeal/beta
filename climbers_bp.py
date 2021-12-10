from flask import Flask, render_template, request, redirect, url_for, Blueprint
from database import app, climbers, climbs, gyms, db, mongo
from  bson.objectid import ObjectId

climbers_bp = Blueprint("climbers_bp", __name__, static_folder='static', template_folder='templates')

@climbers_bp.route('/', methods=['POST'])
def climbers_submit():
    """Submit a new climber."""
    if 'profile-photo' in request.files: 
        profile_photo = request.files['profile-photo']
        mongo.save_file(profile_photo.filename, profile_photo)
    climber = {
        'username': request.form.get('username'),
        'fullname': request.form.get('fullname'),
        'level': request.form.get('level'),
        'homegym': request.form.get('homegym'),
        'profile-photo': profile_photo.filename
    }
    climbers.insert_one(climber)
    return redirect(url_for('index'))

@climbers_bp.route('/new')
def climbers_new():
    return render_template('climbers_new.html', gyms = gyms.find())

@climbers_bp.route('/<climber_id>', methods=['POST'])
def climbers_update(climber_id):
    """Update climber."""
    if 'profile-photo' in request.files: 
        profile_photo = request.files['profile-photo']
        mongo.save_file(profile_photo.filename, profile_photo)
    updated_climber = {
        'username': request.form.get('username'),
        'fullname': request.form.get('fullname'),
        'level': request.form.get('level'),
        'homegym': request.form.get('homegym'),
        'profile-photo': profile_photo.filename
    }
    climbers.update_one(
        {'_id': ObjectId(climber_id)},
        {'$set': updated_climber}
    )
    return redirect(url_for('climbers_bp.climbers_show', climber_id=climber_id))

@climbers_bp.route('/<climber_id>')
def climbers_show(climber_id):
    """Show a single user's information."""
    # TODO: Change this to objectID later!
    climber = climbers.find_one({'_id': ObjectId(climber_id)})
    climber_climbs = climbs.find({'climber_id': ObjectId(climber_id)})

    return render_template('climbers_show.html', climber = climber, climbs=climber_climbs, gyms=list(gyms.find()))

@climbers_bp.route('/<climber_id>/edit')
def climbers_edit(climber_id):
    climber = climbers.find_one({'_id': ObjectId(climber_id)})
    return render_template('climbers_edit.html', climber = climber, gyms=gyms.find())

@climbers_bp.route('/<climber_id>/delete', methods=['POST'])
def climbers_delete(climber_id):
    climbers.delete_one({'_id': ObjectId(climber_id)})
    return redirect(url_for('index'))

@climbers_bp.route('/climbs/<climb_id>', methods=['POST'])
def climbs_delete(climb_id):
    climbs.delete_one({'_id': ObjectId(climb_id)})
    return redirect(url_for('climbers_bp.climbers_show', climber_id=request.form.get('climber_id')))

@climbers_bp.route('/climbs', methods=['POST'])
def climbs_new():
    """Submit a new donation"""
    print(request.files)
    
    climb = {
        'gym': ObjectId(request.form.get('gym')),
        'grade': int(request.form.get('grade')),
        'date': request.form.get('date'),
        'climber_id': ObjectId(request.form.get('climber_id')), 
        'climber': climbers.find_one({'climber_id': ObjectId(request.form.get('climber_id'))}),
        'username': request.form.get('username'),
    }
    if 'photo-video' in request.files: 
        photo_video = request.files['photo-video']
        mongo.save_file(photo_video.filename, photo_video)
        climb['photo_video_name'] = photo_video.filename
    climbs.insert_one(climb)
    print(climb)
    # return redirect(url_for('climbers_show', climber_id=request.form.get('climber_id')))
    return redirect(url_for('climbers_bp.climbers_show', climber_id=request.form.get('climber_id')))
