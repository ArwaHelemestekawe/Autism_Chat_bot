from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time

# Define Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total",          # Metric name
    "Total HTTP Requests",          # Help text (description)
    ["method", "endpoint", "status"]  # Labels
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",  # Metric name
    "HTTP Request Latency",           # Help text (description)
    ["method", "endpoint"]            # Labels
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Process the request
        response = await call_next(request)  # call next contain function code in end point

        # Record metrics after request is processed
        duration = time.time() - start_time
        endpoint = request.url.path

        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(duration)

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=response.status_code
        ).inc()

        return response


def setup_metrics(app:FastAPI):
    app.add_middleware(PrometheusMiddleware)

    # Expose /metrics endpoint for Prometheus
    @app.get("/guessmetrics",include_in_schema=False)
    async def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
