from flask import Flask, request, redirect, url_for, abort
from flask_cors import CORS, cross_origin
from flask import jsonify
import base as base
import pymongo
from bson import Binary, Code
from bson.json_util import dumps
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


@app.route('/wordlist', methods=['GET', 'POST'])
@cross_origin()
def get_word_list():
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["dataextraction"]
        mycol = mydb["keywords"]
    except Exception as e:
        print(e)
        return jsonify({
            "error":e
        }), 500
    if(request.method == 'GET'):
        try:
            word_list = mycol.find_one()
            return jsonify({
                "words":dumps(word_list)
            }),200
        except Exception as e:
            print(e)
            return jsonify({
                "error": e
            }), 500
    elif(request.method == 'POST'):
        try:
            print(request.json)
            category = request.json['category']
            print(category)
            word_object = request.json['wordObject']
            print(word_object)
            mycol.update_one({}, {"$set": {category: word_object}})
            return jsonify({
                "status": "done"
            }),200
        except Exception as e:
            print(e)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5005, threaded = True)
