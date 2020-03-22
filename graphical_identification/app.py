import os

from flask import Flask, render_template, make_response, request

from src.Database import Database
from controller import validate_keyword, set_combination,check_default_images

app = Flask(__name__)
app.debug = True

database = Database()
# DEFAULT_IMAGES_PATHS = ["static/images/default/kitten.jpg",
#                          "static/images/default/puppy.jpg",
#                          "static/images/default/sunflower.jpg",
#                          "static/images/default/bar.jpg"]

default_images_path = 'static/images/default/'
DEFAULT_IMAGES = os.listdir(default_images_path)

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


def get_default_images():
    return [ default_images_path+x for x in DEFAULT_IMAGES]



@app.route('/register', methods=['POST', 'GET'])
def register():
    DEFAULT_IMAGES_ = get_default_images()


    rsp = make_response(render_template('register.html',images_paths=DEFAULT_IMAGES_))

    return rsp


@app.route('/login', methods=['POST', 'GET'])
def login():

    # 789 x 770
    img_path = "static/images/default/bar.jpg"
    path = os.path.abspath(img_path)
    print(path)
    rsp = make_response(render_template("login.html", img_path=img_path))
    return rsp


@app.route('/')
def index():
    check_default_images(DEFAULT_IMAGES, default_images_path)


    rsp = make_response(render_template("index.html"))
    return rsp


if __name__ == '__main__':
    app.run(debug=True)
