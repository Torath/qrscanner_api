# -*- coding: utf-8 -*-
import cv2
from pyzbar.pyzbar import decode
from flask import Flask
from flask import request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from werkzeug.exceptions import BadRequest
import numpy as np

app = Flask(__name__)
api = Api(app)
CORS(app)
parser = reqparse.RequestParser()
parser.add_argument('img')

class DecodeQR(Resource):
    def post(self):

        args = parser.parse_args()
        uploaded_file = request.files['img'].read()
        nparr = np.fromstring(uploaded_file, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

        ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        decoded = decode(image)
        if not decoded:
            raise BadRequest('Nie odnaleziono kodu QR na tym zdjęciu')
        qrcode_data = decoded[0].data.decode('UTF-8')
        arr_qrcode_data = [data for data in qrcode_data.split(';')]
        dct_qrcode_data={}
        for item in arr_qrcode_data:
            item_arr = item.split(':',1)
            dct_qrcode_data[item_arr[0]]=item_arr[1]
        return {'data': dct_qrcode_data}


api.add_resource(DecodeQR, '/')

if __name__ == '__main__':
    app.run(debug=True)
