from flask import Flask, jsonify, request, abort
from mysql import connector

app = Flask(__name__)


# MSSQL server set locally
def get_db_connection():
    conn = connector.connect(host = "localhost", database="resttest" ,user = "root", password = "toor")
    return conn

# Just for checking the status
@app.route('/')
def index():
    return 'Hello World'

# Get all countries list
@app.route('/countries', methods=['GET'])
def getcountries():
    sqldb = get_db_connection()
    cursor = sqldb.cursor()
    cursor.execute('select * from country;')
    results = cursor.fetchall()
    cursor.close()
    sqldb.close()
    return jsonify(results)

# Get a single country by ID
@app.route('/countries/<int:country_id>', methods=['GET'])
def get_country(country_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM countries WHERE id = %s;", (country_id,))
    country = cursor.fetchone()
    cursor.close()
    conn.close()
    if country is None:
        abort(404, description="Country not found")
    return jsonify(country)

# Add a new country
@app.route('/countries', methods=['POST'])
def add_country():
    if not request.json or 'name' not in request.json:
        abort(400, description="Bad Request")
    new_country = {
        'name': request.json['name'],
        'capital': request.json.get('capital', ''),
    }
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO countries (name, capital) VALUES (%s, %s) RETURNING *;",
        (new_country['name'], new_country['capital'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(new_country), 201

# Update an existing country
@app.route('/countries/<int:country_id>', methods=['PUT'])
def update_country(country_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM countries WHERE id = %s;", (country_id,))
    country = cursor.fetchone()

    if country is None:
        abort(404, description="Country not found")
    if not request.json:
        abort(400, description="Bad Request")

    name = request.json.get('name', country['name'])
    capital = request.json.get('capital', country['capital'])

    cursor.execute(
        "UPDATE countries SET name = %s, capital = %s WHERE id = %s RETURNING *;",
        (name, capital, country_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'id': country_id, 'name': name, 'capital': capital})

# Delete a country
@app.route('/countries/<int:country_id>', methods=['DELETE'])
def delete_country(country_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM countries WHERE id = %s RETURNING *;", (country_id,))
    deleted_country = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if deleted_country is None:
        abort(404, description="Country not found")
    
    return jsonify({"result": True})


if __name__ == '__main__':
    app.run(debug=True)


    





