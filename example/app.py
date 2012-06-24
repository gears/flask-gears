import os
from flask import Flask, render_template
from flask_gears import Gears


NODE_PATH = os.path.join(os.path.dirname(__file__), 'node_modules')
NODE_PATH = os.path.normpath(os.path.abspath(NODE_PATH))
os.environ['NODE_PATH'] = NODE_PATH


app = Flask(__name__)

gears = Gears()
gears.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
