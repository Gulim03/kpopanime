import json

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/api/group/<group_name>', methods=['GET', 'PUT', 'DELETE'])
def get_group_info(group_name):
    if request.method == 'GET':
        with open('groups.json') as file_:
            try:
                groups = json.load(file_)
                for group in groups:
                    if group['name'] == group_name.lower():
                        return group, 200
            except json.decoder.JSONDecodeError:
                return {"error": "not found"}, 404
        return {"error": "not found"}, 404
    if request.method == 'PUT':
        with open('groups.json', 'r') as file_:
            groups = json.load(file_)
        with open('groups.json', 'w+') as file_:
            group = json.loads(request.data.decode('utf-8'))
            for i in range(len(groups)):
                if groups[i]['name'].lower() == group_name.lower():
                    del groups[i]
                groups.append(group)
            json.dump(groups, file_)
        return {'status': 'ok'}, 202

    if request.method == 'DELETE':
        with open('groups.json', 'r') as file_:
            groups = json.load(file_)
        with open('groups.json', 'w+') as file_:
            for i in range(len(groups)):
                if groups[i]['name'].lower() == group_name.lower():
                    del groups[i]
            json.dump(groups, file_)
        return {'status': 'ok'}, 204


@app.route('/api/group', methods=['GET', 'POST'])
def get_group_all():
    if request.method == 'GET':
        try:
            with open('groups.json') as file_:
                groups = json.load(file_)
            return {"data": groups}, 200
        except json.decoder.JSONDecodeError:
            return {"data": []}, 200
    if request.method == 'POST':
        try:
            with open('groups.json', 'r') as file_:
                groups = json.load(file_)
        except json.decoder.JSONDecodeError:
            groups = []
        with open('groups.json', 'w+') as file_:
            group = json.loads(request.data.decode('utf-8'))
            groups.append(group)
            json.dump(groups, file_)
        return {'status': 'ok'}, 201


@app.route('/api/anime/<title>', methods=['GET'])
def get_anime_info(title):
    if title.lower() == 'naruto':
        return {'title': 'Naruto',
                'main_character': 'Naruto',
                'episodes_count': 720,
                'dubers': [
                    {"name": "JAM"}
                ]
                }, 200
    elif title.lower() == 'onepunchman':
        return {'title': 'One Punch-Man',
                'episodes_count': 28,
                'main_character': 'Saitama',
                'dubers': [
                    {"name": "JAM"}
                ]
                }, 200
    else:
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
