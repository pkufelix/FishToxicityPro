from load_graph_labels import load_graph_labels
from label_image import label_image
from load_example import load_example
from flask import Flask,render_template,request,redirect,url_for,make_response,jsonify
from werkzeug.utils import secure_filename
import os
from datetime import timedelta

graph, labels = load_graph_labels()
ALLOWED_EXTENSIONS = set(['jpg','jpeg','png','bmp', 'gif'])
basepath = os.path.dirname(__file__)
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)

app.send_file_max_age_default = timedelta(seconds=1)

@app.route('/')

@app.route('/index')
def index():
    return redirect(url_for('upload'))

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        if "submit" in request.form:
            if 'file' not in request.files:
                return render_template("upload.html")
            f = request.files['file']
            if not allowed_file(f.filename):
                return render_template("upload.html")

            #if not (f and allowed_file(f.filename)):
            #    return jsonify({"error": 1001, "msg": "jpg only!"})
     
            upload_path = os.path.join(basepath, 'tmp/images',secure_filename(f.filename))
            f.save(upload_path)            
            results,line_output1,line_output2 = label_image(upload_path, graph, labels)
            upload_path = os.path.join(basepath, 'static/images/test.jpg')
        if "example1" in request.form:
            upload_path = os.path.join(basepath, 'static/images/ex1.jpg')
            results, line_output1, line_output2 = load_example(1)
        if "example2" in request.form:
            upload_path = os.path.join(basepath, 'static/images/ex2.jpg')
            results, line_output1, line_output2 = load_example(2)
        if "example3" in request.form:
            upload_path = os.path.join(basepath, 'static/images/ex3.jpg')
            results, line_output1, line_output2 = load_example(3)
        if int(results[0][1][:2]) < 50:
            conf = 'FishToxicityPro is not sure about its prediction!!'
        else:
            conf = 'It is a ... %s!' % results[0][0]
        return render_template('upload_ok.html', filepath = upload_path, probresults = results, confidence = conf, lineoutput1 = line_output1, lineoutput2 = line_output2)
    return render_template('upload.html')
 
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug= True, use_reloader=False)
