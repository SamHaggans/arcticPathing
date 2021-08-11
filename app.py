import os
import io

from flask import Flask, render_template, request, Response, jsonify

from arcticpathing import main, display, pathing


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
            if path:
                return render_template("path.html", path_info=path)
            else:
                return "No path found"

    # receive non-form inputs (starting/ending coords)
    @app.route('/route', methods=['GET'])
    def submit_request():
        lat1 = float(request.args.get('lat_start'))
        lon1 = float(request.args.get('lon_start'))
        lat2 = float(request.args.get('lat_end'))
        lon2 = float(request.args.get('lon_end'))
        path = main.get_path(lat1, lon1, lat2, lon2)
        if path:
            return jsonify(path)
        else:
            return "No path found"

    # route the plot image request to generate the plot image
    @app.route('/plot', methods=['GET'])
    def plot_route():
        path_string = request.args.get('path')
        path = pathing.parse_string(path_string, True)
        output = io.BytesIO()
        plot = display.get_path_plot(path)
        plot.savefig(output)
        return Response(output.getvalue(), mimetype='image/png')
    return app
