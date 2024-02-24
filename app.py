from flask import Flask, render_template, jsonify, request, redirect, url_for
import data
import collect
import threading
from chartkick.flask import chartkick_blueprint, LineChart
from datetime import datetime, timedelta

def web_func():
    app = Flask(__name__)
    app.register_blueprint(chartkick_blueprint)

    @app.route("/")
    def landing():
        return render_template("menu.html")

    @app.route("/station&location=<location>&hours=<hours>")
    def station(location: int, hours: str):
        chart = LineChart(
            data.get_values_from_position(location),
            xmin=str(datetime.now() - timedelta(hours=int(hours))),
            xmax=str(datetime.now()),
            width="100%",
            height="100%",
            download={'filename': data.get_location_name(location)},
            points=False,
        )
        all_loc = data.get_all_locations()
        print(all_loc)
        return render_template("index.html", chart=chart, location=location, hours=hours, all_locations=all_loc)

    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=8080, debug=True)

def collect_func():
    collect.main()

collecting = threading.Thread(target=collect_func)

collecting.start()
web_func()