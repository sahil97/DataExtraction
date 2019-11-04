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


@app.route('/wordlist', methods=['GET'])
@cross_origin()
def get_word_list():
    return jsonify({
        "words": ['Type','Wood','material','sorting','colour', 'subfloor', 'underlay', 'others', 'Industri', 'eik',
        'rustik', 'full spectre', 'betong', 'plast', 'priming', 'heltre', 'ask', 'natur', 'sparkel', 'ullpapp',
        'sliping', '1-stav', 'lønn', 'select', 'gips', '2mm', 'lakk', '2-stav', 'lerk', 'edel', 'spon', '3mm', 'olje',
        '3-stav', 'valnøtt', 'sauvage', 'avrettingsmasse', 'aquastop', 'behandlet', 'stavparkett', 'bøk',
        'markant', 'GRANAB', 'silencio', 'dim', '6-36mm', 'ubehandlet', 'plank', 'afrikansk eik','exclusive',
        'Nivell',' etafoam', 'børstet', 'fiskebein', 'furu', 'family', 'subfloor', 'gips', 'strukturert', 'lamell',
        'gran', 'trend', 'lim', '1-lags','favorit', '2-lags', '3-lags', 'laminat', 'vinyl', 'vinylklikk'
    ]
    }),200



@app.route('/upload2', methods=['POST'])
@cross_origin()
def upload_file_2():
    print("IN ROUTES")
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
            result = base.parse2(file)
            return result


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5005, threaded = True)
