from flask import Flask, request, jsonify, abort 


app = Flask(__name__)
# using list as data storage just for testing
countries = [{'id':1, 'name':'Nepal', 'capital':'Kathmandu'}
             ,{'id':2, 'name':'India', 'capital':'Delhi'}
             ,{ 'id':3, 'name':'Bhutan', 'capital':'Thimpu'}]

@app.route('/')
def index():
    return 'hello world'


#get all countries
@app.route('/countries', methods = ['GET'])
def get_allcountries():
    return jsonify(countries)

#get a country
@app.route('/countries/<int:country_id>', methods = ['GET'])
def get_country(country_id):
    country = next((c for c in countries if c['id'] == country_id), None)
    if country is None:
        abort(404, description='Country not found')

    return jsonify(country)

#add a country
@app.route('/countries', methods=['POST'])
def add_country():
    if not request.json or 'name' not in request.json:
        abort(400, description = 'Bad request')

    new_country = {
        'id': countries[-1]["id"] + 1,
        'name': request.json["name"],
        'capital': request.json.get('capital', '')
    }
    countries.append(new_country)
    return jsonify(new_country), 201

#update a country
@app.route('/countries/<int:country_id>', methods =['PUT'])
def update_country(country_id):
    country = next((c for c in countries if c["id"]==country_id), None)

    if country is None:
        abort(404, description='Country not Found')
    if not request.json:
        abort(400, description="Bad Request")

    country['name'] = request.json.get('name', country['name'])
    country['capital'] = request.json.get('capital', country['capital'])

    return jsonify(country)


#delete a country
@app.route('/countries/<int:country_id>', methods = ['DELETE'])
def delete_country(country_id):
    country = next((c for c in countries if c["id"]==country_id), None)
    if country is None:
        abort(404, description='Country Not Found')

    countries.remove(country)
    return jsonify({'result':True})


if __name__ == '__main__':
    app.run(debug=True)
