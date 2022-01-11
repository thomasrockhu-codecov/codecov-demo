from datetime import datetime

from flask import (
    Flask,
    render_template,
)

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry import trace

from utils.time import format_time

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

app = Flask(
    __name__,
    static_url_path='',
    static_folder='',
    template_folder='templates',
)
FlaskInstrumentor().instrument_app(app)

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
