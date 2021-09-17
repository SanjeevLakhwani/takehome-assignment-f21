from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""

@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

@app.route("/shows", methods=['GET'])
def get_all_shows():
    return create_response({"shows": db.get('shows')})

@app.route("/shows/<id>", methods=['DELETE'])
def delete_show(id):
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists")
    db.deleteById('shows', int(id))
    return create_response(message="Show deleted")


# TODO: Implement the rest of the API here!

@app.route("/shows/<id>", methods=['GET'])
def get_specific_show(id):
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists")
    return create_response(db.getById('shows', int(id)), 200,"show found")

@app.route("/shows", methods=['POST'])
def create_show():
    if (request.form.get("episodes_seen")==None or request.form.get("name")==None):
        missing = (' (episodes_seen)' if (request.form.get("episodes_seen")==None) else '')+(' (name)' if (request.form.get("name")==None) else '')
        return create_response({}, 422, '"episodes_seen" and "name" are required parameters. You are missing:{}'.format(missing))

    if (not request.form.get("episodes_seen").isnumeric()):
        return create_response({}, 422, '"episodes_seen" should be a numeric value')
    
    return create_response(db.create('shows',{"episodes_seen": int(request.form.get("episodes_seen")),
    "name": request.form.get("name")
    }), 201, "succesfully created the show")

@app.route("/shows/<id>", methods=['PUT'])
def edit_show(id):
    new_data = {}
    if request.form.get("episodes_seen")!=None:
        new_data["episodes_seen"]=request.form.get("episodes_seen")
    if request.form.get("name")!=None:
        new_data["name"]=request.form.get("name")

    ret = db.updateById("shows", int(id), new_data)

    if ret==None:
        return create_response({}, 404, "Id not found")

    return create_response(ret, 200,"show updated")

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)
