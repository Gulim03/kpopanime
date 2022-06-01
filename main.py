import json

import requests
from flask import Flask, request

from db import DataBaseHelper

app = Flask(__name__)
helper = DataBaseHelper()


@app.route('/api/group/<group_name>', methods=['GET', 'PUT', 'DELETE'])
def get_group_info(group_name):
    if request.method == 'GET':
        group = helper.groups.find_one({"name": group_name})
        if group:
            del group['_id']
            return {'data': group}
        return {"error": "not found"}, 404
    if request.method == 'PUT':
        group = json.loads(request.data.decode('utf-8'))
        helper.groups.update_one({"name": group_name}, {"$set": group})
        return {'status': 'ok'}, 202
    if request.method == 'DELETE':
        helper.groups.find_one_and_delete({"name": group_name})
        return {'status': 'ok'}, 204


@app.route('/api/group', methods=['GET', 'POST'])
def get_group_all():
    if request.method == 'GET':
        groups_cursor = helper.groups.find({})
        groups = []
        for group in groups_cursor:
            del group['_id']
            groups.append(group)
        return {'data': groups}
    if request.method == 'POST':
        group = json.loads(request.data.decode('utf-8'))
        helper.groups.insert_one(group)
        return {'status': 'ok'}, 201


@app.route('/api/anime/<title>', methods=['GET'])
def get_anime_info(title):
    anime = helper.anime.find_one({"title": title})
    if anime:
        del anime['_id']
        return {'data': anime}
    return {"error": "No Info"}, 404


@app.route('/api/ip', methods=['GET'])
def get_ip_info():
    response = requests.get(url="http://ident.me")
    if response.status_code == 200:
        return {"ip": response.text}
    return {"error": "No info"}, 500


@app.route('/api/sum', methods=['GET'])
def get_sum_info():
    try:
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))
    except ValueError:
        return {'error': 'invalid value'}, 400
    return {'sum': a + b}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=65616)
