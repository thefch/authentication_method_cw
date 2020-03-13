from flask import Flask, render_template, make_response

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():

    # rsp = make_response(render_template("index.html"))
    # rsp = make_response(render_template("gridtemp.html"))

    img_path = "static/kitten.jpg"
    rsp = make_response(render_template("gridv2.html", img_path=img_path))
    return rsp


if __name__ == '__main__':
    app.run(debug=True)
