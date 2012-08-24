from flask import Flask, render_template
from flask_gears import Gears

from gears_stylus import StylusCompiler
from gears_clean_css import CleanCSSCompressor


app = Flask(__name__)

gears = Gears(
    compilers={'.styl': StylusCompiler.as_handler()},
    compressors={'text/css': CleanCSSCompressor.as_handler()},
)
gears.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
