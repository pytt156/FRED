#!/bin/sh
set -eu

: "${MQTT_USERNAME:?MQTT_USERNAME is required}"
: "${MQTT_PASSWORD:?MQTT_PASSWORD is required}"
: "${MQTT_CA_CERT_B64:?MQTT_CA_CERT_B64 is required}"
: "${MQTT_SERVER_CERT_B64:?MQTT_SERVER_CERT_B64 is required}"
: "${MQTT_SERVER_KEY_B64:?MQTT_SERVER_KEY_B64 is required}"

PASSWORD_FILE="/tmp/fred-mqtt-passwords"
CERT_DIR="/tmp/fred-certs"

mkdir -p "$CERT_DIR"

umask 077

printf '%s:%s\n' \
    "$MQTT_USERNAME" \
    "$MQTT_PASSWORD" \
    > "$PASSWORD_FILE"

mosquitto_passwd -U "$PASSWORD_FILE"

printf '%s' "$MQTT_CA_CERT_B64" \
    | base64 -d \
    > "$CERT_DIR/ca.crt"

printf '%s' "$MQTT_SERVER_CERT_B64" \
    | base64 -d \
    > "$CERT_DIR/server.crt"

printf '%s' "$MQTT_SERVER_KEY_B64" \
    | base64 -d \
    > "$CERT_DIR/server.key"

chmod 600 \
    "$PASSWORD_FILE" \
    "$CERT_DIR/ca.crt" \
    "$CERT_DIR/server.crt" \
    "$CERT_DIR/server.key"

exec mosquitto \
    -c /mosquitto/config/mosquitto.conf#!/bin/sh
set -eu

: "${MQTT_USERNAME:?MQTT_USERNAME is required}"
: "${MQTT_PASSWORD:?MQTT_PASSWORD is required}"
: "${MQTT_CA_CERT_B64:?MQTT_CA_CERT_B64 is required}"
: "${MQTT_SERVER_CERT_B64:?MQTT_SERVER_CERT_B64 is required}"
: "${MQTT_SERVER_KEY_B64:?MQTT_SERVER_KEY_B64 is required}"

PASSWORD_FILE="/tmp/fred-mqtt-passwords"
CERT_DIR="/tmp/fred-certs"

mkdir -p "$CERT_DIR"

umask 077

printf '%s:%s\n' \
    "$MQTT_USERNAME" \
    "$MQTT_PASSWORD" \
    > "$PASSWORD_FILE"

mosquitto_passwd -U "$PASSWORD_FILE"

printf '%s' "$MQTT_CA_CERT_B64" \
    | base64 -d \
    > "$CERT_DIR/ca.crt"

printf '%s' "$MQTT_SERVER_CERT_B64" \
    | base64 -d \
    > "$CERT_DIR/server.crt"

printf '%s' "$MQTT_SERVER_KEY_B64" \
    | base64 -d \
    > "$CERT_DIR/server.key"

chmod 600 \
    "$PASSWORD_FILE" \
    "$CERT_DIR/ca.crt" \
    "$CERT_DIR/server.crt" \
    "$CERT_DIR/server.key"

exec mosquitto \
    -c /mosquitto/config/mosquitto.conf