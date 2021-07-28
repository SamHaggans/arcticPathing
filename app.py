import os

from flask import Flask, render_template, request, send_file

from arcticpathing import main, display


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # starting information form
    @app.route('/', methods=['GET'])
    def form():
        return render_template("form.html")

    # receive form inputs (starting/ending coords)
    @app.route('/submit', methods=['POST'])
    def submit_form():
        if request.method == 'POST':
            information = request.form
            lat1 = float(information['lat_start'])
            lon1 = float(information['lon_start'])
            lat2 = float(information['lat_end'])
            lon2 = float(information['lon_end'])
            path = main.get_path(lat1, lon1, lat2, lon2)
            plot_file = display.save_path_plot(path['path'], 0, 500)
            return render_template("path.html", path_info=path, plot=f'/plots/{plot_file}')

    @app.route('/plots/<path:filename>', methods=['GET'])
    def plot_route(filename):
        return send_file(f'plots/{filename}')
    return app
