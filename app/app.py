from flask import Flask, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQ_COUNT = Counter(
    'http_requests_total', 'Total HTTP requests',
    ['method', 'endpoint', 'status']
)
REQ_LATENCY = Histogram(
    'http_request_duration_seconds', 'HTTP request latency'
)


@app.before_request
def start_timer():
    from flask import g
    g.start = time.time()


@app.after_request
def record_metrics(response):
    from flask import g, request
    latency = time.time() - g.start
    REQ_LATENCY.observe(latency)
    REQ_COUNT.labels(request.method, request.path, response.status_code).inc()
    return response


@app.route('/')
def index():
    return jsonify({'message': 'DevOps Project API', 'status': 'ok'})


@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200


@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route('/version')
def version():
    import os
    return jsonify({'version': os.getenv('APP_VERSION', 'dev')})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)  # nosec B104
