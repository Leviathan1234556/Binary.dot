import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from PIL import Image
from flask_caching import Cache
from flask_moment import Moment
from flask import send_from_directory

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['CACHE_TYPE'] = 'simple'
db = SQLAlchemy(app)
cache = Cache(app)
moment = Moment(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    prize_money = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(100), nullable=True)  # Store the file path


    def __repr__(self):
        return f"Event('{self.name}', '{self.description}', '{self.prize_money}', '{self.image_filename}')"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_tables():
    with app.app_context():
        db.create_all()

def save_image(file, filename):
    img = Image.open(file.stream)
    img.thumbnail((128, 128))
    img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
@app.route('/', methods=['GET', 'POST'])
def upload_event():
    if request.method == 'POST':
        event_name = request.form['event_name']
        event_description = request.form['event_description']
        prize_money = request.form['prize_money']
        file = request.files['image']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            new_event = Event(name=event_name, description=event_description, prize_money=prize_money, image_filename=filepath)
            db.session.add(new_event)
            db.session.commit()
            flash('Event created successfully!')
            return redirect(url_for('view_events'))

    return render_template('host.html')

@app.route('/events')
def view_events():
    events = Event.query.all()
    return render_template('view_events.html', events=events)


@app.route('/event/<string:filename>')
def view_event(filename):
    event = Event.query.filter_by(image_filename=filename).first()
    return render_template('view_event.html', event=event)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return json.dumps({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return json.dumps({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        save_image(file, filename)
        return json.dumps({'filename': filename})
    else:
        return json.dumps({'error': 'Invalid file type'}), 400


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('/uploads', filename)

if __name__ == '__main__':
    app.run(debug=True)