from flask import Flask, request, redirect, url_for, abort
from flask_cors import CORS, cross_origin
from flask import jsonify
import base as base


app = Flask(__name__)
cors = CORS(app)

@app.route("/ignition")
@cross_origin()
def ignition():
    return jsonify({"Engine Status" : "WebApp for dataExtraction is alive and kicking"}), 200

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload_file():

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return jsonify({"Message" : "File Not Found"}), 200
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file:
            # saving file in raw folder
            # TODO: Save it with client name and timestamp
            result = base.init(file)
            return result

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5005, threaded = True)
