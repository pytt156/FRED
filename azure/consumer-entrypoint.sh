#!/bin/sh
set -eu

if [ "${MQTT_TLS:-false}" = "true" ]; then
    : "${MQTT_CA_CERT_B64:?MQTT_CA_CERT_B64 is required when MQTT_TLS=true}"

    printf '%s' "$MQTT_CA_CERT_B64" \
        | base64 -d \
        > /tmp/fred-ca.crt

    chmod 600 /tmp/fred-ca.crt
fi

exec uv run python -u backend/consumer.py