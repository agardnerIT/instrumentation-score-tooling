# instrumentation-score-tooling
Tooling to leverage https://github.com/instrumentation-score/spec

## Quick Start

```
git clone https://github.com/agardnerit/instrumentation-score-tooling
cd instrumentation-score-tooling
python -m venv .
source bin/activate .
pip install -r requirements.txt
python app.py --file samples/all-signals.output --debug true
```

## Generating Custom Telemetry (optional)

1. Start a collector which is configured to listen for incoming telemetry and save it to a file

```
/path/to/otelcol-contrib --config=collector/config.yaml
```

1. Send telemetry eg. using telemetrygen

```
// Send a single trace
docker run --add-host=host.docker.internal:host-gateway ghcr.io/open-telemetry/opentelemetry-collector-contrib/telemetrygen:latest traces --otlp-insecure --otlp-endpoint host.docker.internal:4317 --traces 1

// Send a single log
docker run --add-host=host.docker.internal:host-gateway ghcr.io/open-telemetry/opentelemetry-collector-contrib/telemetrygen:latest logs --otlp-insecure --otlp-endpoint host.docker.internal:4317 --logs 1

// Send a single metric
docker run --add-host=host.docker.internal:host-gateway ghcr.io/open-telemetry/opentelemetry-collector-contrib/telemetrygen:latest metrics --otlp-insecure --otlp-endpoint host.docker.internal:4317 --metrics 1
```