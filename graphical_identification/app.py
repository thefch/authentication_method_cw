import os

from flask import Flask, render_template, make_response, request, url_for, redirect, session, flash
from flask_session import Session
from werkzeug.utils import secure_filename

from src.Database import Database
from controller import validate_keyword, set_combination, check_default_images, get_default_images

app = Flask(__name__)

app.secret_key = "sg34oiufn23498fgh3kvjnslkjvn"
DEFAULT_IMAGES_PATH = 'static/images/default/'
UPLOAD_FOLDER = 'static/images/users/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # prevents uploading a file larger than 16mb

app.config['DEFAULT_IMAGES_PATH'] = DEFAULT_IMAGES_PATH
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SELECTED_IMAGE_PATH'] = None

DEFAULT_IMAGES = get_default_images(DEFAULT_IMAGES_PATH)


database = Database()


#   TODO
#       * check validation for / and range of values
#       * rearrange submit button in register page

@app.route('/validate_register', methods=['POST'])
def validate_register():

    username = ''
    image_path = ''
    try:
        username = request.form['username_box']
    except Exception as e:
        print(e)

    try:
        image_path = request.form['image_path']
    except Exception as e:
        print(e)

    print('username:', username)
    print('image_path:', image_path)

    if image_path.strip() is '' or username.strip() is '':
        msg = 'Account creation failed. Make sure to add a username and points on the image!'
        # rsp = make_response(redirect(url_for('register', msg=msg)))
        rsp = make_response(redirect(url_for('register', msg=msg,images_paths=DEFAULT_IMAGES)))

    else:
        #create_account(username,image_path)

        msg='Account created successful: {}'.format(username)
        rsp = make_response(redirect(url_for('register', msg=msg,images_paths=DEFAULT_IMAGES)))


    return rsp


@app.route('/register_pattern')
def register_pattern():
    img_path = app.config['SELECTED_IMAGE_PATH']
    app.config['SELECTED_IMAGE_PATH'] = None

    # if img_path is not None:
    rsp = make_response(render_template('register_pattern.html', image_path=img_path))
    # else:
    #     msg = 'No image found, please select one!'
    #     print(msg)
    #     rsp = make_response(redirect(url_for('index', msg=msg)))

    return rsp


# only when registering
# it should be used only when no account is in session
@app.route('/choose_image', methods=['POST', 'GET'])
def choose_image():
    img = None
    # user selection from default images
    try:
        img = request.args.get('img')
        print('SELECTED IMAGE from default:', img)
    except Exception as e:
        print("The selected image is not from the default images -- check for imported image")
        # print(e)
        img = None

    # import another image
    if img is None:
        try:
            # if 'imported_image' in request.files:
            img = request.form['import_image']
            print('IMPORTED IMAGE:', img)
            img.save(secure_filename(img.filename))
            # img.save(os.path.join(app.config['UPLOAD_FOLDER'], img.filename))
            # if img:
            #     print('IMPORTED IMAGE:', img)
            #
            # else:
            #     flash('No selected file')
            #     img = None
        except Exception as e:
            print("Error selecting imported image")
            img = None
    # if account is not in session:
    #  else: exit page

    if img is not None:
        app.config['SELECTED_IMAGE_PATH'] = img
        rsp = make_response(redirect(url_for('register_pattern')))

    else:
        rsp = make_response(redirect(url_for('register')))

    return rsp


# rename to validate_login if is used just for login
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


@app.route('/register', methods=['POST', 'GET'])
def register():
    try:
        msg = request.args['msg']
        print('Message found from register request:',msg)
        rsp = make_response(render_template('register.html', images_paths=DEFAULT_IMAGES,msg=msg))

    except Exception as e:
        print('No msg found from register request')
        rsp = make_response(render_template('register.html', images_paths=DEFAULT_IMAGES))

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
    check_default_images(DEFAULT_IMAGES, DEFAULT_IMAGES_PATH)

    rsp = make_response(render_template("index.html"))
    return rsp


if __name__ == '__main__':
    app.run(debug=True)
