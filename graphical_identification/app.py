import os

from flask import Flask, render_template, make_response, request, url_for, redirect, session, flash
from flask_session import Session
from werkzeug.utils import secure_filename

from controller import validate_keyword, set_combination, check_default_images, get_default_images, check_image_size, \
    create_account

app = Flask(__name__)

app.secret_key = "sg34oiufn23498fgh3kvjnslkjvn"
DEFAULT_IMAGES_PATH = 'static/images/default/'
UPLOAD_FOLDER = 'static/images/users/'
ALLOWED_EXTENSIONS = ['jpg', 'jpeg']
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # prevents uploading a file larger than 16mb

app.config['DEFAULT_IMAGES_PATH'] = DEFAULT_IMAGES_PATH
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SELECTED_IMAGE_PATH'] = None

DEFAULT_IMAGES = get_default_images(DEFAULT_IMAGES_PATH)




#   TODO
#       * check validation for / and range of values
#       * rearrange submit button in register page

def check_file_extension(file) -> [bool, str]:
    parts = file.filename.split('.')
    ext = parts[-1]

    valid = False
    if ext in ALLOWED_EXTENSIONS:
        valid = True
    return valid, ext


@app.route('/validate_register', methods=['POST'])
def validate_register():
    username = ''
    image_path = ''
    keyword = None
    try:
        username = request.form['username_box']
    except Exception as e:
        print(e)

    try:
        image_path = request.form['image_path']
    except Exception as e:
        print(e)

    try:
        keyword = ''
    except Exception as e:
        print(e)

    print('username:', username)
    print('image_path:', image_path)

    if image_path.strip() is '' or username.strip() is '':
        msg = 'Account creation failed. Make sure to add a username and points on the image!'
        rsp = make_response(redirect(url_for('register', msg=msg, images_paths=DEFAULT_IMAGES)))
    elif keyword is None:
        msg = 'Account creation failed. Something went wrong with the keyword!'
        rsp = make_response(redirect(url_for('register', msg=msg, images_paths=DEFAULT_IMAGES)))
    else:
        # validation is successful

        create_account(username, keyword, image_path)
        msg = 'Account created successful: {}'.format(username)
        rsp = make_response(redirect(url_for('register', msg=msg, images_paths=DEFAULT_IMAGES)))

    return rsp


@app.route('/register_pattern')
def register_pattern():
    img_path = app.config['SELECTED_IMAGE_PATH']
    app.config['SELECTED_IMAGE_PATH'] = None

    if img_path is not None:
        rsp = make_response(render_template('register_pattern.html', image_path=img_path))
    else:
         msg = 'No image found, please select one!'
         print(msg)
         rsp = make_response(redirect(url_for('index', msg=msg)))

    return rsp


# used when uploading an image
# checks for EXTENSIONS and verifies the image
@app.route('/upload', methods=['POST'])
def upload():
    if 'import_image' not in request.files:
        print('No file part')
        msg = "There was an error with the uploaded image. Try again!"
        resp = redirect(url_for('register', msg=msg))
    else:
        file = request.files['import_image']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename.strip() is not '':
            valid, ext = check_file_extension(file)
            print(file)
            if valid:
                fname_ = file.filename
                filename = secure_filename(file.filename)

                # print(filename)
                # fname_ = 'register_temp_img.' + ext
                path = app.config['UPLOAD_FOLDER'] + fname_
                # if os.path.exists(path):
                #     os.remove(path)

                #   TODO:
                #       save the image with a temporary name instead
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname_))

                print(fname_)
                # set the path of the selected image when registering
                app.config['SELECTED_IMAGE_PATH'] = path

                print('saved')
                print(path)

                checked = check_image_size(app.config['UPLOAD_FOLDER'], fname_)
                # for debugging the image size
                # if checked:
                #     print('image resized:',fname_)
                # else:
                #     print('Error when resizing image')

                resp = make_response(redirect(url_for('register_pattern', image_path=path)))
            else:
                msg = "Image is not supported, choose a different one!"
                resp = redirect(url_for('register', msg=msg))
        else:
            print('No selected file')
            msg = 'No image was uploaded. Try again!'
            resp = redirect(url_for('register', msg=msg))
    return resp


# only when registering
# it should be used only when no account is in session
# and when the user selects one of the default images
@app.route('/choose_image', methods=['GET'])
def choose_image():
    img = None
    # user selection from default images
    try:
        img = request.args.get('img')
        print('SELECTED IMAGE from default:', img)

        # set the path of the selected image when registering
        app.config['SELECTED_IMAGE_PATH'] = img
        rsp = make_response(redirect(url_for('register_pattern')))
    except Exception as e:
        msg = "The selected image is not from the default images -- check for imported image"
        print(msg)
        img = None
        rsp = make_response(redirect(url_for('register', msg=msg)))

    # if account is not in session:
    #  else: exit page

    return rsp


# rename to validate_login if is used just for login
@app.route('/validate', methods=['POST'])
def validate():
    grid_keyword = ''
    keydown_keyword = ''
    entered_keyword = ''
    username = ''
    image_path = ''
    keyword = None
    try:
        grid_keyword = request.form["grid_keyword"]
        keydown_keyword = request.form["keydown_keyword"]
        entered_keyword = request.form["entered_keyword"]
        print('grid kwrd:',grid_keyword)
        print('keydown kwrd:',keydown_keyword)
        print('entered kwrd:',entered_keyword)
    except Exception as e:
        print(e)

    try:
        username = request.form['username_box']
    except Exception as e:
        print(e)

    try:
        image_path = request.form['image_path']
    except Exception as e:
        print(e)

    is_valid, combination, keys, clicks = validate_keyword(entered_keyword, keydown_keyword, grid_keyword)
    if is_valid and username.strip() != '' and image_path.strip() != '':
        final_combination = set_combination(combination, keys, clicks)
        keyword_info={
            'grid_keyword':grid_keyword,
            'keydown_keyword':keydown_keyword,
            'entered_keyword':entered_keyword,
            'final_combination':final_combination}
        create_account(username,keyword_info,image_path)
    else:
        # throw an error massage
        pass


    img_path = "static/images/kitten.jpg"
    path = os.path.abspath(img_path)
    rsp = make_response(render_template("login.html", img_path=img_path))

    return rsp


@app.route('/register', methods=['POST', 'GET'])
def register():
    try:
        msg = request.args['msg']
        print('Message found from register request:', msg)

        rsp = make_response(render_template('register.html', images_paths=DEFAULT_IMAGES, msg=msg))

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
