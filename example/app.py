from flask import Flask, render_template
from flask_gears import Gears
from gears_stylus import StylusCompiler


app = Flask(__name__)

gears = Gears()
gears.init_app(app)

env = gears.get_environment(app)
env.compilers.register('.styl', StylusCompiler.as_handler())


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
