from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry import trace

from flask import Flask, request
import requests

from codecovopentelem import (
    CoverageSpanFilter,
    get_codecov_opentelemetry_instances,
)

token = 'e832b1f98c106abe1debd69b423fb341986dad1d'
current_version = '0.0.1'
current_env = 'test'
export_rate = 0

provider = TracerProvider()
generator, exporter = get_codecov_opentelemetry_instances(
        repository_token=token,
        version_identifier=current_version,
        sample_rate=export_rate,
        filters={
            CoverageSpanFilter.regex_name_filter: None,
            CoverageSpanFilter.span_kind_filter: [
                trace.SpanKind.SERVER,
                trace.SpanKind.CONSUMER,
            ],
        },
        code=f"{current_version}:{current_env}",
        untracked_export_rate=export_rate,
        environment=current_env,
)
provider.add_span_processor(generator)
provider.add_span_processor(BatchSpanProcessor(exporter))

trace.set_tracer_provider(provider)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

@app.route('/fib/<int:N>')
def index(N):
    response = requests.get(
        'http://localhost:6000/worker/fib/{}'.format(N)
    )
    return response.content


app.run(host='0.0.0.0', port=8080)
