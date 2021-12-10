from dns.query import tls
from flask_pymongo import PyMongo
from flask import Flask, render_template
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for
from  bson.objectid import ObjectId
from dotenv import load_dotenv
import os
import pymongo
import certifi

app = Flask(__name__)
ca = certifi.where()
load_dotenv()
DATABASE_URL = f'mongodb+srv://janecui:{os.environ.get("password")}@playlistr.k3tyy.mongodb.net/Playlister?retryWrites=true&w=majority'
client = MongoClient(DATABASE_URL, tlsCAFile=ca)
app.config['MONGO_URI'] = DATABASE_URL
mongo = PyMongo(app, tlsCAFile=ca)
db = client.Donations
climbers = db.climbers
climbs = db.climbs
gyms = db.gyms



sample_gym = [{
        'name': 'Bloc Shop',
        'types': 'Bouldering',
        'description': 'Description here',
        'city': 'Montreal',
    }]

sample_climber = [{
    '_id': 12,
    'fullname': 'Jane Cui',
    'username': 'bakedoatmeal',
    'level': 'beginner-intermediate',
    'homegym': 'Bloc Shop',
}]

@app.route('/')
def index():
    """Return homepage"""
    return render_template('climbers_index.html', climbers=climbers.find(), gyms=gyms.find(), climbs=climbs.find())

@app.route('/climbers/new')
def climbers_new():
    return render_template('climbers_new.html', gyms = gyms.find())

@app.route('/gyms/new')
def gyms_new():
    return render_template('gyms_new.html')

@app.route('/climbers', methods=['POST'])
def climbers_submit():
    """Submit a new climber."""
    if 'photo-video' in request.files: 
        photo_video = request.files['photo-video']
        mongo.save_file(photo_video.filename, photo_video)
    climber = {
        'username': request.form.get('username'),
        'fullname': request.form.get('fullname'),
        'level': request.form.get('level'),
        'homegym': request.form.get('homegym'),
        'profile-photo': photo_video.filename
    }
    climbers.insert_one(climber)
    return redirect(url_for('index'))

@app.route('/gyms', methods=['POST'])
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

@app.route('/climbers/<climber_id>')
def climbers_show(climber_id):
    """Show a single user's information."""
    # TODO: Change this to objectID later!
    climber = climbers.find_one({'_id': ObjectId(climber_id)})
    climber_climbs = climbs.find({'climber_id': ObjectId(climber_id)})

    return render_template('climbers_show.html', climber = climber, climbs=climber_climbs, gyms=list(gyms.find()))

@app.route('/gyms/<gym_id>')
def gyms_show(gym_id):
    gym = gyms.find_one({'_id': ObjectId(gym_id)})
    gym_climbs = climbs.find({'gym': ObjectId(gym_id)})

    return render_template('gyms_show.html', gym = gym, climbs=gym_climbs)

#TODO: Add update route for climbers
#TODO: Also, can make sub templates for html files

@app.route('/gyms/<gym_id>/edit')
def gyms_edit(gym_id):
    gym = gyms.find_one({'_id': ObjectId(gym_id)})
    return render_template('gyms_edit.html', gym = gym)

@app.route('/gyms/<gym_id>', methods=['POST'])
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
    return redirect(url_for('gyms_show', gym_id=gym_id ))

@app.route('/climbers/<climber_id>/delete', methods=['POST'])
def climbers_delete(climber_id):
    climbers.delete_one({'_id': ObjectId(climber_id)})
    return redirect(url_for('index'))

@app.route('/gyms/<gym_id>/delete', methods=['POST'])
def gyms_delete(gym_id):
    gyms.delete_one({'_id': ObjectId(gym_id)})
    return redirect(url_for('index'))

@app.route('/climbers/climbs', methods=['POST'])
def climbs_new():
    """Submit a new donation"""
    print(request.files)
    
    climb = {
        'gym': ObjectId(request.form.get('gym')),
        'grade': request.form.get('grade'),
        'date': request.form.get('date'), 
        'climber_id': ObjectId(request.form.get('climber_id')),
        'username': request.form.get('username'),
    }
    if 'photo-video' in request.files: 
        photo_video = request.files['photo-video']
        mongo.save_file(photo_video.filename, photo_video)
        climb['photo_video_name'] = photo_video.filename
    climbs.insert_one(climb)
    # return redirect(url_for('climbers_show', climber_id=request.form.get('climber_id')))
    return redirect(url_for('climbers_show', climber_id=request.form.get('climber_id')))

@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

@app.route('/climbers/climbs/<donation_id>', methods=['POST'])
def climbs_delete(donation_id):
    climbs.delete_one({'_id': ObjectId(donation_id)})
    return redirect(url_for('climbers_show', climber_id=request.form.get('climber_id')))


if __name__ == '__main__':
    app.run(debug=True)
