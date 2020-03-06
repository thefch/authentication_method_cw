from flask import Flask, render_template, make_response

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    # upper_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
    #                  'U', 'V', 'W', 'X', 'Y', 'Z']
    # lower_letters = [x.lower() for x in upper_letters]
    #
    # print("upper alphabet:", upper_letters)
    # print("lower alphabet:", lower_letters)

    rsp = make_response(render_template("index.html"))
    rsp = make_response(render_template("gridtemp.html"))
    rsp = make_response(render_template("gridv2.html"))
    return rsp


if __name__ == '__main__':
    app.run(debug=True)
