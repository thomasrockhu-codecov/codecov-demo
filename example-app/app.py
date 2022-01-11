from datetime import datetime

from flask import (
    Flask,
    render_template,
)

from utils.time import format_time

app = Flask(
    __name__,
    static_url_path='',
    static_folder='',
    template_folder='templates',
)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/time')
def current_time():
    return render_template(
        'time.html',
        time=format_time(datetime.now()),
    )

app.run(host='0.0.0.0', port=8080)
