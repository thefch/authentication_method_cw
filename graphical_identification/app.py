import os

from flask import Flask, render_template, make_response, request

app = Flask(__name__)
app.debug = True

from src.Database import database


def update_image():
    pass

#
#   TODO
#       * SPLIT KEYWORDS
#
@app.route('/check_login', methods=['POST'])
def check_login():
    try:
        grid_keyword = request.form["grid_keyword"]
        print(grid_keyword)
    except Exception as e:
        raise e

    img_path = "static/images/kitten.jpg"
    path = os.path.abspath(img_path)
    rsp = make_response(render_template("gridv2.html", img_path=img_path))

    return rsp


@app.route('/')
def index():
    # rsp = make_response(render_template("index.html"))
    # rsp = make_response(render_template("gridtemp.html"))
    img_path = "static/images/kitten.jpg"
    path = os.path.abspath(img_path)
    print(path)
    rsp = make_response(render_template("gridv2.html", img_path=img_path))
    return rsp


if __name__ == '__main__':
    app.run(debug=True)
