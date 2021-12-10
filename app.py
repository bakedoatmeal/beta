from flask import Flask, render_template
from flask import Flask, render_template, request, redirect, url_for
from database import app, client, mongo, db, climbers, climbs, gyms
from climbers_bp import climbers_bp
from gyms_bp import gyms_bp

app.register_blueprint(climbers_bp, url_prefix="/climbers")
app.register_blueprint(gyms_bp, url_prefix="/gyms")

@app.route('/')
def index():
    """Return homepage"""
    return render_template('climbers_index.html', climbers=list(climbers.find()), gyms=list(gyms.find()), climbs=climbs.find())

@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


if __name__ == '__main__':
    app.run(debug=True)
