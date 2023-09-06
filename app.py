from flask import Flask, request, render_template
import json

app = Flask(__name__)


# for running tests
@app.route('/', methods=['POST'])
def index():
    data = request.json  # This reads JSON data from the POST request
    return render_template('render_template.html', data=data)


# for running locally
# @app.route('/')
# def index():
#     data = {
#         "isActive": True,
#         "isMarried": False,
#         "children": None,
#         "numberOfCars": 2
#     }
#     return render_template('render_template.html', data=data)



if __name__ == '__main__':
    app.run(debug=True)