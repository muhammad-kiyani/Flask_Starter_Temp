import os
#import magic
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template,url_for
from werkzeug.utils import secure_filename
import sys
import DiffFinder
from flask import send_file

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','xlsx'])


file_location_holder = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/', methods=['POST','GET'])
def upload_file():
    if request.method == "POST":
       file = request.files["file"]
       file2 = request.files["file2"]
       filename_holder = []
       if file and allowed_file(file.filename):

           filename  = secure_filename(file.filename)
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           flash('File successfully uploaded')
           file_location_holder.append(str(os.path.join(app.config['UPLOAD_FOLDER'], filename)))

       if file2 and allowed_file(file.filename):

           filename = secure_filename(file2.filename)
           file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           flash('File successfully uploaded')
           file_location_holder.append(str(os.path.join(app.config['UPLOAD_FOLDER'], filename)))

    DiffFinder.differenceFinder(file_location_holder[0],file_location_holder[1],str(os.path.join(app.config['UPLOAD_FOLDER'])))
    return redirect('/')


@app.route('/download.html')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = str(os.path.join(app.config['UPLOAD_FOLDER'], 'TrackingChanges.xlsx'))
    renewpath = path.replace('/','\\')
    print('renewPath',renewpath)
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
