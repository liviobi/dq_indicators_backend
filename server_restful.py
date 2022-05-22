# in vscode press ctrl+shift+p
# and type python:Select Interpreter

import copy
from flask import Flask
from flask import request
from flask_restful import abort, reqparse, Api, Resource
from pkg_resources import require
import werkzeug
import os
from flask_cors import CORS
from config import cfg
import nltk


from functions import computeIndicator, deleteFileFromFolder, getListOfFilesNames, setJavaIndicatorsProcessing

app = Flask(__name__)
api = Api(app)

UPLOAD_DIR = cfg["uploadDir"]
CORS(app)

# dictionary
files = dict()


indicatorsTemplate = {
    "parsable": None,
    "confidence_tokenizer": None,
    "confidence_pos": None,
    "confidence_ner": None,
    "confidence_chunker": None,
    "fit": None,
    "spelling_mistakes": None,
    "avg_sentence_len": None,
    "perc_lowercase": None,
    "perc_uppercase": None,
    "lexical_diversity": None,
    "recognized_by_pos": None,
    "acronyms": None,
    "present_in_dictionary": None,
    "readability_cli": None,
    "readability_ari": None, }

javaIndicators = ["parsable",
                  "confidence_tokenizer",
                  "confidence_pos",
                  "confidence_ner",
                  "confidence_chunker", ]

# save file to folder and update dictionary


def saveFile(file, uploadDir):
    file.save(os.path.join(uploadDir, file.filename))
    files[file.filename] = copy.deepcopy(indicatorsTemplate)


# delete file from folder and update dictionary
def deleteFile(filename, uploadDir):
    deleteFileFromFolder(os.path.join(uploadDir, filename))
    del files[filename]


class FileList(Resource):

    def get(self):
        result = dict()
        result["files"] = list(files.keys())
        return result

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "file", type=werkzeug.datastructures.FileStorage, location='files')
        # self.parser.add_argument('title')
        args = parser.parse_args()
        file = args.get("file")
        if(not file):
            abort(400, message="No file found in message")
        saveFile(file, UPLOAD_DIR)
        return {'message': 'added file'}, 201

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("filename")
        args = parser.parse_args()
        filename = args.get("filename")
        if filename not in files:
            abort(404, message="File not found")
        else:
            deleteFile(filename, UPLOAD_DIR)
            return {'message': 'deleted file f{filename}'}, 201


class Indicator(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "filename", type=str, help="Provide the filename", required=True)
        parser.add_argument(
            "indicator", type=str, help="Provide which indicator you want", required=True)
        args = parser.parse_args()
        filename = args["filename"]
        indicator = args["indicator"]
        # if the file is not present abort
        if(filename not in files):
            abort(404, message="File not found")
        # if indicator not present in the template
        if(indicator not in indicatorsTemplate):
            abort(404, message="Invalid indicator")
        # if indicator not computed
        if(files[filename][indicator] == None):
            files[filename][indicator] = "processing"
            # since the java indicators are processed together I need to set them all as processing
            # to avoid to run the same computation everytime for each of them
            if(indicator in javaIndicators):
                setJavaIndicatorsProcessing(files, filename)
            computeIndicator(files, filename, indicator)

        return {'indicator': files[filename][indicator]}, 200


api.add_resource(FileList, '/file')
api.add_resource(Indicator, '/indicators')


if __name__ == '__main__':
    # initialize the dict of files
    for filename in getListOfFilesNames(UPLOAD_DIR):
        files[filename] = copy.deepcopy(indicatorsTemplate)

    nltk.download('averaged_perceptron_tagger')
    nltk.download('universal_tagset')

    app.run(debug=True, port=cfg["port"], host=cfg["host"])
