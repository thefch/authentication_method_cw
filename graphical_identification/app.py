import os

from flask import Flask, render_template, make_response, request

from src.Database import Database
from controller import validate_keyword, set_combination

app = Flask(__name__)
app.debug = True

database = Database()


#   TODO
#       * check validation for / and range of values
#


@app.route('/validate', methods=['POST'])
def validate():
    try:
        grid_keyword = request.form["grid_keyword"]
        keydown_keyword = request.form["keydown_keyword"]
        entered_keyword = request.form["entered_keyword"]
        print(grid_keyword)
        is_valid, combination, keys, clicks = validate_keyword(entered_keyword, keydown_keyword, grid_keyword)
        if is_valid:
            set_combination(combination, keys, clicks)
        else:
            # return back to login page
            pass

    except Exception as e:
        raise e

    img_path = "static/images/kitten.jpg"
    path = os.path.abspath(img_path)
    rsp = make_response(render_template("login.html", img_path=img_path))

    return rsp


# @app.route('/check_login', methods=['POST'])
# def check_login():
#     try:
#         grid_keyword = request.form["grid_keyword"]
#         keydown_keyword = request.form["keydown_keyword"]
#         entered_keyword = request.form["entered_keyword"]
#
#         print(grid_keyword)
#         print(keydown_keyword)
#         print(entered_keyword)
#
#     except Exception as e:
#         raise e
#
#     img_path = "static/images/kitten.jpg"
#     path = os.path.abspath(img_path)
#     rsp = make_response(render_template("login.html", img_path=img_path))
#
#     return rsp

@app.route('/register', methods=['POST', 'GET'])
def register():
    rsp = make_response(render_template('register.html'))

    return rsp


@app.route('/login', methods=['POST', 'GET'])
def login():
    # rsp = make_response(render_template("index.html"))
    # rsp = make_response(render_template("gridtemp.html"))
    img_path = "static/images/kitten.jpg"
    path = os.path.abspath(img_path)
    print(path)
    rsp = make_response(render_template("login.html", img_path=img_path))
    return rsp


@app.route('/')
def index():
    rsp = make_response(render_template("index.html"))
    return rsp


if __name__ == '__main__':
    app.run(debug=True)
