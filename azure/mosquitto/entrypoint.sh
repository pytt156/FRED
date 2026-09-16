#!/bin/sh
set -eu

: "${MQTT_USERNAME:?MQTT_USERNAME is required}"
: "${MQTT_PASSWORD:?MQTT_PASSWORD is required}"

PASSWORD_FILE="/tmp/fred-mqtt-passwords"

umask 077

printf '%s:%s\n' "$MQTT_USERNAME" "$MQTT_PASSWORD" > "$PASSWORD_FILE"

mosquitto_passwd -U "$PASSWORD_FILE"

chmod 600 "$PASSWORD_FILE"

exec mosquitto -c /mosquitto/config/mosquitto.conf
