from flask import Flask, request, render_template, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['photo']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return 'Photo uploaded successfully'

@app.route('/uploads/<filename>')
def send_photo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)