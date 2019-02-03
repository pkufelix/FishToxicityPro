from label_image import label_image
 
from flask import Flask,render_template,request,redirect,url_for,make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2

from datetime import timedelta
 

mercury = {'salmon': 'Mercury level (PPM): 0.022.', \
    'trout': 'Mercury level (PPM): 0.071.', \
    'white seabass': 'Mercury level (PPM): 0.354', \
    'rockfish': 'Mercury level (PPM): 0.167', \
    'tuna': 'Mercury level (PPM): 0.386', \
    'largemouth bass': 'Mercury level (PPM): 0.167', \
    'walleye': 'Methylmercury level (PPM): 0.16', \
    'channel catfish': 'Mercury level (PPM): 0.024', \
    'perch': 'Mercury level (PPM): 0.150', \
    'carp': 'Mercury level (PPM): 0.110', \
    'lake whitefish': 'Mercury level (PPM): 0.089', \
    'shad': 'Mercury level (PPM): 0.038'
}
sugg = {'salmon': 'Having 2 servings per week may be OK', \
    'trout': 'Having 2 servings per week may be OK', \
    'white seabass': 'Not suggested to eat more than 1 serving per a week', \
    'rockfish': 'Not suggested to eat more than 1 serving per a week', \
    'tuna': 'Women who are or may become pregnant, nursing mothers, and young children should NOT eat', \
    'largemouth bass': 'Not suggested to eat more than 1 serving per a week', \
    'walleye': 'Having 2 servings per week may be OK', \
    'channel catfish': 'Having 2 servings per week may be OK', \
    'perch': 'Not suggested to eat more than 1 serving per a week', \
    'carp': 'Not suggested to eat more than 1 serving per a week', \
    'lake whitefish': 'Not suggested to eat more than 1 serving per a week', \
    'shad': 'Having 2 servings per week may be OK'
}

ALLOWED_EXTENSIONS = set(['jpg','jpeg'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)

app.send_file_max_age_default = timedelta(seconds=1)
 
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "jpg only!"})
 
        basepath = os.path.dirname(__file__)
 
        upload_path = os.path.join(basepath, 'tmp/images',secure_filename(f.filename))
        f.save(upload_path)
        
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
        results = label_image(upload_path)
        line_output1 = mercury[results[0][0]]
        line_output2 = sugg[results[0][0]]
#return render_template('upload_ok.html',filepath = upload_path, useroutput1=out_sen[0], useroutput2=out_sen[1], useroutput3=out_sen[2], useroutput4='', lineoutput1=line_output1,lineoutput2=line_output2)
        return render_template('upload_ok.html', filepath = upload_path, probresults = results, lineoutput1 = line_output1, lineoutput2 = line_output2)
    return render_template('upload.html')
 
if __name__ == '__main__':
    # app.debug = True
#app.run(host = '0.0.0.0',port = 8987,debug= True)
    app.run(debug= True)
