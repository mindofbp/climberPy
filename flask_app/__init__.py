from io import BytesIO
import os
from zipfile import ZipFile, ZIP_DEFLATED

from flask import Flask, make_response, request, send_file

from classes import *
import identifiers
import parsers


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello", methods=["POST", "GET"])
    def hello():
        try:
            filename = "upper_lake_loop.fit"
            if request.method == "POST":
                req_data = request.get_json()
                if "filename" in req_data.keys() and req_data["filename"] != None:
                    filename = req_data["filename"]
            files = []
            points = parsers.parse_fit_file(filename)
            climbs = identifiers.ClimbIdentifier(points).identify_climbs()
            for index, segment in enumerate(climbs):
                if segment.distance >= 1000:
                    # If distance is less than 2k then we wil plot in 400m segments
                    # If the distance is betwen 2k and 5k then we will plot in 800m segments
                    # If the distance is greater than 5k then we will plot in 1k segments
                    if segment.distance < 2000:
                        files.append(segment.plot_segment(400, index))
                    elif segment.distance < 5000:
                        files.append(segment.plot_segment(800, index))
                    else:
                        files.append(segment.plot_segment(1000, index))

            mem_file = BytesIO()

            with ZipFile(mem_file, mode="w") as zip:
                for file in files:
                    zip.write(file, os.path.basename(file), compress_type=ZIP_DEFLATED)

            mem_file.seek(0)

            return send_file(
                mem_file,
                as_attachment=True,
                mimetype="application/zip",
                download_name="climbs.zip",
            )
        except Exception as e:
            print(e)
            return make_response({"error": "An error occurred"}, 500)
        finally:
            for file in files:
                os.remove(file)

    return app
