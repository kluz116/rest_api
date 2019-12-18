import MySQLdb
from app import app
from db_config import mysql
from flask import jsonify
from flask import request



@app.route('/users')
def users():
    global cursor
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Users")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)

@app.route('/delete/<int:id>')
def delete_user(id):
    global cursor
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Users WHERE  id=%s", (id,))
        conn.commit()
        resp = jsonify('User deleted successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)


@app.route('/update', methods=['POST'])
def update_user():
    global cursor
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        if _name and _id and request.method == 'POST':
            sql = "UPDATE Users SET name=%s WHERE  id=%s"
            data = (_name, _id)
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)

@app.route('/add_users', methods=['POST'])
def add_user():
    global cursor
    try:
        _json = request.json
        name = _json['name']
        # validate the received values
        if name  and request.method == 'POST':
            sql ="INSERT INTO Users (name) VALUES( %s) "
            data = ([name])
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute(sql,data)
            conn.commit()
            resp = jsonify('User added successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)


@app.route('/userdetails/<int:id>')
def userdetails(id):
    global cursor
    try:
        conn = mysql.connection
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Users  where id = %s", (id,))
        row = cursor.fetchall()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)


@app.route('/usertask/<int:id>')
def userstasks(id):
    global cursor
    try:
        conn = mysql.connection
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Users a join USER_TASKS b on a.id = b.User_id where b.User_id = %s", (id,))
        row = cursor.fetchall()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)


@app.route('/tasks_view/<int:id>')
def tasks_view(id):
    global cursor
    try:
        conn = mysql.connection
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Users a join USER_TASKS b on a.id = b.User_id where b.Id = %s", (id,))
        row = cursor.fetchall()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
@app.route('/update_task', methods=['POST'])
def update_task():
    try:
        _json = request.json
        Id = _json['Id']
        description = _json['description']
        state = _json['state']
        User_id = _json['User_id']

        if description and state and User_id and Id and request.method == 'POST':
            sql = "UPDATE USER_TASKS SET description=%s, User_id=%s, state=%s WHERE Id=%s"
            data = (description, state, User_id, Id,)
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)

@app.route('/add_task', methods=['POST'])
def add_task():
    try:
        _json = request.json
        description = _json['description']
        User_id = _json['User_id']

        if description and User_id  and request.method == 'POST':
            sql = "INSERT INTO USER_TASKS(description,User_id)VALUES(%s,%s) "
            data = ([description, User_id])
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)

@app.route('/tasks')
def tasks():
    global cursor
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Users a join USER_TASKS b on a.id = b.User_id")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)

@app.route('/delete_task/<int:id>')
def delete_task(id):
    global cursor
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("DELETE FROM USER_TASKS WHERE  Id = %s", (id,))
        conn.commit()
        resp = jsonify('Deleted')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run(threaded=True)
