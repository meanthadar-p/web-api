import flask
from flask import request, jsonify
from db import ConnectDatabase as db

app = flask.Flask(__name__)
app.config['DEBUG'] = True
persons_db = 'database/persons.db'


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return "<h1>Test</h1><p>test API using Python Flask</p>"


@app.route('/api/v1/resource/persons/all', methods=['GET'])
def api_all():
    all_persons = db.execute_query(persons_db, 'SELECT * FROM persons')
    return jsonify(all_persons)


@app.route('/api/v1/resource/person', methods=['GET'])
def api_person():
    query_parameters = request.args

    person_id = query_parameters.get('id')
    job = query_parameters.get('job')

    query = 'SELECT * FROM persons WHERE'
    to_filter = []

    if person_id:
        query += ' person_id=? AND'
        to_filter.append(person_id)
    if job:
        query += ' job=? AND'
        to_filter.append(job)
    if not (id or job):
        return page_not_found(404)

    query = query[:-4] + ';'

    persons = db.execute_query(persons_db, query, to_filter)

    return jsonify(persons)


@app.route('/api/v1/resource/person/insert', methods=['POST'])
def api_person_insert():
    request_parameter = request.args

    person_id = request_parameter.get('person_id')
    name = request_parameter.get('name')
    job = request_parameter.get('job')

    query = 'INSERT INTO persons VALUES(?, ?, ?);'
    to_filter = [person_id, name, job]

    result = db.execute_query(persons_db, query, to_filter)
    return jsonify(result)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>ERROR 404</h1><p>page not found</p>", 404


app.run()
