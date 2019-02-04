from label_image import label_image

from flask import Flask,render_template,request,redirect,url_for,make_response,jsonify
from werkzeug.utils import secure_filename
import os

from datetime import timedelta

ALLOWED_EXTENSIONS = set(['jpg','jpeg','png'])
 
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

        results,line_output1,line_output2 = label_image(upload_path)

        return render_template('upload_ok.html', filepath = upload_path, probresults = results, lineoutput1 = line_output1, lineoutput2 = line_output2)
    return render_template('upload.html')
 
if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 5000,debug= True)
