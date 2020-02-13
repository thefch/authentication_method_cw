from flask import Flask, render_template, make_response

app = Flask(__name__)
app.debug = True



@app.route('/')
def index():
    rsp = make_response(render_template("index.html"))


    return rsp


if __name__ == '__main__':
    app.run(debug=True)
