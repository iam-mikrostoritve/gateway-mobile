import os

import grpc
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

import proto_pb2
import proto_pb2_grpc

load_dotenv()

app = Flask(__name__)
cors = CORS(app)

USER_SERVICE_URL = os.getenv('USER_SERVICE_URL')
channel = grpc.insecure_channel('localhost:9000')
TRANSACTION_SERVICE_URL = os.getenv('TRANSACTION_SERVICE_URL')

artist_stub = proto_pb2_grpc.ArtistGrpcServiceStub(channel)
label_stub = proto_pb2_grpc.LabelGrpcServiceStub(channel)
record_stub = proto_pb2_grpc.RecordGrpcServiceStub(channel)

@app.route('/', methods=['GET'])
def health_check():
    return {'Status': 'Running'}, 200

@app.route('/api/artists', methods=['GET'])
def get_artists():
    response = artist_stub.GetAll(proto_pb2.Empty())
    artists = []
    for artist in response:
        artists.append(from_proto(artist))
    return artists, 200


@app.route('/api/artists/<id>', methods=['GET'])
def get_artist_by_id(id):
    response = artist_stub.GetById(proto_pb2.ArtistIdProto(id=id))
    return from_proto(response), 200


@app.route('/api/labels', methods=['GET'])
def get_labels():
    response = label_stub.GetAll(proto_pb2.Empty())
    labels = []
    for label in response:
        labels.append(from_proto(label))
    return labels, 200


@app.route('/api/labels/<id>', methods=['GET'])
def get_label_by_id(id):
    response = label_stub.GetById(proto_pb2.LabelIdProto(id=id))
    return from_proto(response), 200


@app.route('/api/records', methods=['GET'])
def get_records():
    response = record_stub.GetAll(proto_pb2.Empty())
    records = []
    for record in response:
        records.append(from_proto(record))
    return records, 200


@app.route('/api/records/<id>', methods=['GET'])
def get_record_by_id(id):
    response = record_stub.GetById(proto_pb2.RecordIdProto(id=id))
    return from_proto(response), 200


def from_proto(proto) -> dict:
    return {field.name: value for field, value in proto.ListFields()}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
