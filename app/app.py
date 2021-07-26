from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'citiesData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Actor Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_male')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, actors=result)


@app.route('/view/<int:actor_id>', methods=['GET'])
def record_view(actor_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_male WHERE id=%s', actor_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', actor=result[0])


@app.route('/edit/<int:actor_id>', methods=['GET'])
def form_edit_get(actor_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_male WHERE id=%s', actor_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', actor=result[0])


@app.route('/edit/<int:actor_id>', methods=['POST'])
def form_update_post(actor_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Year'),
                 request.form.get('Age'),
                 request.form.get('Name'),
                 request.form.get('Movie'), actor_id)
    sql_update_query = """UPDATE oscar_age_male t SET t.Year = %s, t.Age = %s,
    t.Name = %s, t.Movie = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/actors/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Actor Form')


@app.route('/actors/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Year'),
                 request.form.get('Age'),
                 request.form.get('Name'),
                 request.form.get('Movie'))
    sql_insert_query = """INSERT INTO oscar_age_male (Year, Age, Name, Movie) VALUES (%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:actor_id>', methods=['POST'])
def form_delete_post(actor_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM oscar_age_male WHERE id = %s """
    cursor.execute(sql_delete_query, actor_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/actors', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_male')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/actors/<int:actor_id>', methods=['GET'])
def api_retrieve(actor_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_male WHERE id=%s', actor_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/actors/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/actors/<int:actor_id>', methods=['PUT'])
def api_edit(actor_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/actors/<int:actor_id>', methods=['DELETE'])
def api_delete(actor_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)