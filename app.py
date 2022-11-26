from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import cv2

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    file1 = request.files['file1']
    if file.filename == '' or file1.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename1 = secure_filename(file1.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'one.jpeg'))
        file1.save(os.path.join(app.config['UPLOAD_FOLDER'], 'two.jpeg'))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename='one.jpeg', filename1='two.jpeg')
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/result')
def result():
    img_one = UPLOAD_FOLDER + "/one.jpeg"
    img_two = UPLOAD_FOLDER + "/two.jpeg"
    im1 = cv2.imread(img_one)
    im2 = cv2.imread(img_two)
    data1 = im1.shape
    data2 = im2.shape 
    img_one_score = 0 
    img_two_score = 0 
    if data1[0] > data2[0] and data1[1] > data2[1]:
        img_one_score += 1
    else:
        img_two_score += 1 
    
    if img_one_score > img_two_score:
        res = img_one
    else:
        res = img_two

    print(img_one_score)
    print(img_two_score)
    
    print(data1)
    print(data2)
    return render_template('result.html', data=res)



@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
 
if __name__ == "__main__":
    app.run(debug=True)