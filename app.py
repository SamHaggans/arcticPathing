import io

from flask import (
    Flask,
    render_template,
    request,
    Response,
    jsonify
)

from arcticpathing import main, display, pathing


def create_app(test_config=None):
    app = Flask(__name__)

    # starting information form
    @app.route('/', methods=['GET'])
    def form():
        return render_template("form.html")

    # receive form inputs (starting/ending coords)
    @app.route('/submit', methods=['POST'])
    def submit_form():
        information = request.form
        lat1 = float(information['lat_start'])
        lon1 = float(information['lon_start'])
        lat2 = float(information['lat_end'])
        lon2 = float(information['lon_end'])
        path = main.get_path(lat1, lon1, lat2, lon2)
        if path:
            return render_template("path.html", path_info=path)
        else:
            return "500 Error: Path not found", 500

    # receive non-form inputs (starting/ending coords)
    @app.route('/route', methods=['GET'])
    def submit_request():
        lat1 = float(request.args.get('lat_start'))
        lon1 = float(request.args.get('lon_start'))
        lat2 = float(request.args.get('lat_end'))
        lon2 = float(request.args.get('lon_end'))
        path = main.get_path(lat1, lon1, lat2, lon2)
        if path:
            path = pathing.serialize_path(path)
            return jsonify(path)
        else:
            return jsonify({'error': "Path not found"}), 500

    # route the plot image request to generate the plot image
    @app.route('/plot', methods=['GET'])
    def plot_route():
        path_string = request.args.get('path')
        path = pathing.parse_request_path_string(path_string)
        output = io.BytesIO()
        plot = display.get_path_plot(path)
        plot.savefig(output)
        return Response(output.getvalue(), mimetype='image/png')
    return app
