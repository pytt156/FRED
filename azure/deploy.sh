#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# FRED Azure deployment
# ============================================================

RESOURCE_GROUP="FRED"
LOCATION="polandcentral"

ENVIRONMENT="fred-env"

VNET_NAME="fred-vnet"
VNET_CIDR="10.20.0.0/16"

SUBNET_NAME="fred-containerapps-subnet"
SUBNET_CIDR="10.20.0.0/23"

MOSQUITTO_APP="fred-mosquitto"
TIMESCALE_APP="fred-timescaledb"
GRAFANA_APP="fred-grafana"
CONSUMER_APP="fred-consumer"
MLFLOW_APP="fred-mlflow"

MOSQUITTO_IMAGE="ghcr.io/omeraytug/fred-mosquitto:demo"
TIMESCALE_IMAGE="ghcr.io/omeraytug/fred-timescaledb:demo"
GRAFANA_IMAGE="ghcr.io/omeraytug/fred-grafana:demo"
CONSUMER_IMAGE="ghcr.io/omeraytug/fred-consumer:demo"
MLFLOW_IMAGE="ghcr.io/mlflow/mlflow:v3.16.1"

CERT_DIR="azure/certs"
CA_KEY="${CERT_DIR}/fred-ca.key"
CA_CERT="${CERT_DIR}/fred-ca.crt"

SERVER_KEY="${CERT_DIR}/mqtt-server.key"
SERVER_CSR="${CERT_DIR}/mqtt-server.csr"
SERVER_CERT="${CERT_DIR}/mqtt-server.crt"
SERVER_EXT="${CERT_DIR}/mqtt-server.ext"

MLFLOW_YAML="$(mktemp "${TMPDIR:-/tmp}/fred-mlflow.XXXXXX.yaml")"

# ============================================================
# Cleanup
# ============================================================

cleanup() {
    unset MQTT_PASSWORD || true
    unset POSTGRES_PASSWORD || true
    unset GRAFANA_PASSWORD || true
    unset OPENAI_API_KEY || true
    unset OPENROUTER_API_KEY || true

    unset MQTT_CA_CERT_B64 || true
    unset MQTT_SERVER_CERT_B64 || true
    unset MQTT_SERVER_KEY_B64 || true

    rm -f "$MLFLOW_YAML" || true
}

trap cleanup EXIT

# ============================================================
# Preconditions
# ============================================================

echo
echo "========================================"
echo " FRED Azure Deployment"
echo "========================================"
echo

if ! command -v az >/dev/null 2>&1; then
    echo "ERROR: Azure CLI is not installed."
    exit 1
fi

if ! command -v openssl >/dev/null 2>&1; then
    echo "ERROR: OpenSSL is not installed."
    exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: Python 3 is not installed."
    exit 1
fi

if [[ ! -f "$CA_KEY" || ! -f "$CA_CERT" ]]; then
    echo "ERROR: FRED CA was not found."
    echo
    echo "Expected:"
    echo "  $CA_KEY"
    echo "  $CA_CERT"
    exit 1
fi

# ============================================================
# Secrets
# ============================================================

read -r -p "MQTT username [fred]: " MQTT_USERNAME
MQTT_USERNAME="${MQTT_USERNAME:-fred}"

read -r -s -p "MQTT password: " MQTT_PASSWORD
echo

read -r -s -p "PostgreSQL password: " POSTGRES_PASSWORD
echo

read -r -s -p "Grafana admin password: " GRAFANA_PASSWORD
echo

if [[ -z "$MQTT_PASSWORD" ||
      -z "$POSTGRES_PASSWORD" ||
      -z "$GRAFANA_PASSWORD" ]]; then
    echo "ERROR: passwords cannot be empty."
    exit 1
fi

echo
read -r -p "Model mode for the consumer (openai/free) [openai]: " MODEL_MODE
MODEL_MODE="${MODEL_MODE:-openai}"

if [[ "$MODEL_MODE" == "openai" ]]; then
    read -r -s -p "OpenAI API key: " OPENAI_API_KEY
    echo

    if [[ -z "$OPENAI_API_KEY" ]]; then
        echo "ERROR: OpenAI API key cannot be empty."
        exit 1
    fi

elif [[ "$MODEL_MODE" == "free" ]]; then
    read -r -s -p "OpenRouter API key: " OPENROUTER_API_KEY
    echo

    if [[ -z "$OPENROUTER_API_KEY" ]]; then
        echo "ERROR: OpenRouter API key cannot be empty."
        exit 1
    fi

    read -r -p "OpenRouter model [openrouter/free]: " OPENROUTER_MODEL
    OPENROUTER_MODEL="${OPENROUTER_MODEL:-openrouter/free}"

else
    echo "ERROR: Model mode must be 'openai' or 'free'."
    exit 1
fi

# ============================================================
# Resource Group
# ============================================================

echo
echo "Creating/updating resource group..."

az group create \
    --name "$RESOURCE_GROUP" \
    --location "$LOCATION" \
    --output none

# ============================================================
# VNet
# ============================================================

echo "Creating VNet..."

if ! az network vnet show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$VNET_NAME" \
    >/dev/null 2>&1; then

    az network vnet create \
        --resource-group "$RESOURCE_GROUP" \
        --name "$VNET_NAME" \
        --location "$LOCATION" \
        --address-prefixes "$VNET_CIDR" \
        --output none
else
    echo "VNet already exists."
fi

# ============================================================
# Container Apps subnet
# ============================================================

echo "Creating Container Apps subnet..."

if ! az network vnet subnet show \
    --resource-group "$RESOURCE_GROUP" \
    --vnet-name "$VNET_NAME" \
    --name "$SUBNET_NAME" \
    >/dev/null 2>&1; then

    az network vnet subnet create \
        --resource-group "$RESOURCE_GROUP" \
        --vnet-name "$VNET_NAME" \
        --name "$SUBNET_NAME" \
        --address-prefixes "$SUBNET_CIDR" \
        --delegations Microsoft.App/environments \
        --output none
else
    echo "Subnet already exists."
fi

SUBNET_ID=$(
    az network vnet subnet show \
        --resource-group "$RESOURCE_GROUP" \
        --vnet-name "$VNET_NAME" \
        --name "$SUBNET_NAME" \
        --query id \
        --output tsv
)

# ============================================================
# Container Apps environment
# ============================================================

echo "Creating Container Apps environment..."

if ! az containerapp env show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$ENVIRONMENT" \
    >/dev/null 2>&1; then

    az containerapp env create \
        --resource-group "$RESOURCE_GROUP" \
        --name "$ENVIRONMENT" \
        --location "$LOCATION" \
        --infrastructure-subnet-resource-id "$SUBNET_ID" \
        --logs-destination none \
        --enable-workload-profiles false \
        --output none
else
    echo "Container Apps environment already exists."
fi

ENV_STATE=$(
    az containerapp env show \
        --resource-group "$RESOURCE_GROUP" \
        --name "$ENVIRONMENT" \
        --query properties.provisioningState \
        --output tsv
)

echo "Container Apps environment: $ENV_STATE"

if [[ "$ENV_STATE" != "Succeeded" ]]; then
    echo "ERROR: Container Apps environment is not ready."
    exit 1
fi

DEFAULT_DOMAIN=$(
    az containerapp env show \
        --resource-group "$RESOURCE_GROUP" \
        --name "$ENVIRONMENT" \
        --query properties.defaultDomain \
        --output tsv
)

MQTT_HOST="${MOSQUITTO_APP}.${DEFAULT_DOMAIN}"

echo "MQTT hostname: $MQTT_HOST"

# ============================================================
# Generate deployment-specific MQTT certificate
# ============================================================

echo
echo "Generating MQTT TLS certificate..."

rm -f \
    "$SERVER_KEY" \
    "$SERVER_CSR" \
    "$SERVER_CERT" \
    "$SERVER_EXT"

openssl genrsa \
    -out "$SERVER_KEY" \
    2048

openssl req \
    -new \
    -key "$SERVER_KEY" \
    -out "$SERVER_CSR" \
    -subj "/CN=FRED MQTT Server"

cat > "$SERVER_EXT" <<EOF
subjectAltName=DNS:${MQTT_HOST}
keyUsage=digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
EOF

openssl x509 \
    -req \
    -in "$SERVER_CSR" \
    -CA "$CA_CERT" \
    -CAkey "$CA_KEY" \
    -CAcreateserial \
    -out "$SERVER_CERT" \
    -days 365 \
    -sha256 \
    -extfile "$SERVER_EXT"

chmod 600 "$SERVER_KEY"

echo "Verifying MQTT certificate..."

openssl verify \
    -CAfile "$CA_CERT" \
    "$SERVER_CERT"

openssl x509 \
    -in "$SERVER_CERT" \
    -noout \
    -checkhost "$MQTT_HOST"

# ============================================================
# Encode certificates for Container App secrets
# ============================================================

MQTT_CA_CERT_B64=$(
    openssl base64 -A -in "$CA_CERT"
)

MQTT_SERVER_CERT_B64=$(
    openssl base64 -A -in "$SERVER_CERT"
)

MQTT_SERVER_KEY_B64=$(
    openssl base64 -A -in "$SERVER_KEY"
)

# ============================================================
# Mosquitto
# ============================================================

echo
echo "Deploying Mosquitto with TLS..."

if az containerapp show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$MOSQUITTO_APP" \
    >/dev/null 2>&1; then

    echo "$MOSQUITTO_APP already exists, skipping creation."
    echo "(To rotate its TLS cert/credentials, delete it first and re-run this script.)"
else
    az containerapp create \
        --name "$MOSQUITTO_APP" \
        --resource-group "$RESOURCE_GROUP" \
        --environment "$ENVIRONMENT" \
        --image "$MOSQUITTO_IMAGE" \
        --cpu 0.25 \
        --memory 0.5Gi \
        --min-replicas 1 \
        --max-replicas 1 \
        --secrets \
            mqtt-password="$MQTT_PASSWORD" \
            mqtt-ca-cert-b64="$MQTT_CA_CERT_B64" \
            mqtt-server-cert-b64="$MQTT_SERVER_CERT_B64" \
            mqtt-server-key-b64="$MQTT_SERVER_KEY_B64" \
        --env-vars \
            MQTT_USERNAME="$MQTT_USERNAME" \
            MQTT_PASSWORD=secretref:mqtt-password \
            MQTT_CA_CERT_B64=secretref:mqtt-ca-cert-b64 \
            MQTT_SERVER_CERT_B64=secretref:mqtt-server-cert-b64 \
            MQTT_SERVER_KEY_B64=secretref:mqtt-server-key-b64 \
        --ingress external \
        --transport tcp \
        --target-port 8883 \
        --exposed-port 8883 \
        --output none
fi

# ============================================================
# TimescaleDB
# ============================================================

echo "Deploying TimescaleDB..."

if az containerapp show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$TIMESCALE_APP" \
    >/dev/null 2>&1; then

    echo "$TIMESCALE_APP already exists, skipping creation."
else
    az containerapp create \
        --name "$TIMESCALE_APP" \
        --resource-group "$RESOURCE_GROUP" \
        --environment "$ENVIRONMENT" \
        --image "$TIMESCALE_IMAGE" \
        --cpu 0.5 \
        --memory 1Gi \
        --min-replicas 1 \
        --max-replicas 1 \
        --secrets \
            postgres-password="$POSTGRES_PASSWORD" \
        --env-vars \
            POSTGRES_DB=fred \
            POSTGRES_USER=fred \
            POSTGRES_PASSWORD=secretref:postgres-password \
        --ingress internal \
        --transport tcp \
        --target-port 5432 \
        --exposed-port 5432 \
        --output none
fi

# ============================================================
# Grafana
# ============================================================

echo "Deploying Grafana..."

if az containerapp show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$GRAFANA_APP" \
    >/dev/null 2>&1; then

    echo "$GRAFANA_APP already exists, skipping creation."
else
    az containerapp create \
        --name "$GRAFANA_APP" \
        --resource-group "$RESOURCE_GROUP" \
        --environment "$ENVIRONMENT" \
        --image "$GRAFANA_IMAGE" \
        --cpu 0.25 \
        --memory 0.5Gi \
        --min-replicas 1 \
        --max-replicas 1 \
        --secrets \
            postgres-password="$POSTGRES_PASSWORD" \
            grafana-password="$GRAFANA_PASSWORD" \
        --env-vars \
            POSTGRES_HOST="$TIMESCALE_APP" \
            POSTGRES_PORT=5432 \
            POSTGRES_DB=fred \
            POSTGRES_USER=fred \
            POSTGRES_PASSWORD=secretref:postgres-password \
            GF_SECURITY_ADMIN_USER=admin \
            GF_SECURITY_ADMIN_PASSWORD=secretref:grafana-password \
        --ingress external \
        --target-port 3000 \
        --transport auto \
        --output none
fi

# ============================================================
# MLflow
# ============================================================

echo "Deploying MLflow..."

if az containerapp show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$MLFLOW_APP" \
    >/dev/null 2>&1; then

    echo "$MLFLOW_APP already exists, skipping creation."
else
    az containerapp create \
        --name "$MLFLOW_APP" \
        --resource-group "$RESOURCE_GROUP" \
        --environment "$ENVIRONMENT" \
        --image "$MLFLOW_IMAGE" \
        --cpu 1 \
        --memory 2Gi \
        --min-replicas 1 \
        --max-replicas 1 \
        --ingress external \
        --target-port 5000 \
        --transport auto \
        --output none

    MLFLOW_FQDN=$(
        az containerapp show \
            --name "$MLFLOW_APP" \
            --resource-group "$RESOURCE_GROUP" \
            --query properties.configuration.ingress.fqdn \
            --output tsv
    )

    if [[ -z "$MLFLOW_FQDN" ]]; then
        echo "ERROR: Could not determine MLflow public FQDN."
        exit 1
    fi

    echo "MLflow public hostname: $MLFLOW_FQDN"

    echo "Configuring MLflow startup command..."

    az containerapp show \
        --name "$MLFLOW_APP" \
        --resource-group "$RESOURCE_GROUP" \
        --output yaml \
        > "$MLFLOW_YAML"

    MLFLOW_INTERNAL_FQDN="${MLFLOW_APP}.internal.${DEFAULT_DOMAIN}"
    MLFLOW_ALLOWED_HOSTS="${MLFLOW_APP}:5000,${MLFLOW_INTERNAL_FQDN},${MLFLOW_FQDN}"
    MLFLOW_ALLOWED_ORIGIN="https://${MLFLOW_FQDN}"
    export MLFLOW_ALLOWED_HOSTS MLFLOW_ALLOWED_ORIGIN

    python3 - "$MLFLOW_YAML" <<'PYMLFLOW'
from pathlib import Path
import os
import sys

path = Path(sys.argv[1])
text = path.read_text()
image_marker = "    - image: ghcr.io/mlflow/mlflow:v3.16.1"

if text.count(image_marker) != 1:
    raise SystemExit("ERROR: Expected exactly one MLflow container image in exported YAML.")

command_block = f"""      command:
      - /bin/sh
      args:
      - -c
      - mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri sqlite:////mlflow/mlflow.db --artifacts-destination /mlflow/artifacts --allowed-hosts \"{os.environ['MLFLOW_ALLOWED_HOSTS']}\" --cors-allowed-origins \"{os.environ['MLFLOW_ALLOWED_ORIGIN']}\" --workers 1
"""

# The exported Azure YAML lists the image first, followed by the other
# properties of the same container. Insert the command INSIDE that container.
text = text.replace(image_marker, image_marker + "\n" + command_block.rstrip("\n"), 1)
path.write_text(text)
PYMLFLOW

    az containerapp update \
        --name "$MLFLOW_APP" \
        --resource-group "$RESOURCE_GROUP" \
        --yaml "$MLFLOW_YAML" \
        --output none

    echo "Waiting for MLflow revision to become ready..."
    MLFLOW_READY=false
    for attempt in $(seq 1 60); do
        LATEST_REVISION=$(az containerapp show --name "$MLFLOW_APP" --resource-group "$RESOURCE_GROUP" --query properties.latestRevisionName --output tsv)
        READY_REVISION=$(az containerapp show --name "$MLFLOW_APP" --resource-group "$RESOURCE_GROUP" --query properties.latestReadyRevisionName --output tsv)
        if [[ -n "$LATEST_REVISION" && "$LATEST_REVISION" == "$READY_REVISION" ]]; then
            MLFLOW_READY=true
            break
        fi
        sleep 5
    done
    if [[ "$MLFLOW_READY" != true ]]; then
        echo "ERROR: MLflow revision did not become ready; inspect Azure revision logs."
        exit 1
    fi
fi

# Resolve MLflow endpoints unconditionally — needed by the Consumer below
# whether MLflow was just created or already existed.
MLFLOW_FQDN=$(
    az containerapp show \
        --name "$MLFLOW_APP" \
        --resource-group "$RESOURCE_GROUP" \
        --query properties.configuration.ingress.fqdn \
        --output tsv
)
MLFLOW_INTERNAL_FQDN="${MLFLOW_APP}.internal.${DEFAULT_DOMAIN}"
MLFLOW_TRACKING_URI="https://${MLFLOW_INTERNAL_FQDN}"
MLFLOW_PUBLIC_URL="https://${MLFLOW_FQDN}"

echo "MLflow internal tracking URI: $MLFLOW_TRACKING_URI"

# ============================================================
# Consumer
# ============================================================

echo "Deploying Consumer with MQTT TLS..."
echo "Model mode: $MODEL_MODE"

CONSUMER_SECRETS=(
    mqtt-password="$MQTT_PASSWORD"
    mqtt-ca-cert-b64="$MQTT_CA_CERT_B64"
    postgres-password="$POSTGRES_PASSWORD"
)

CONSUMER_ENV_VARS=(
    MQTT_HOST="$MQTT_HOST"
    MQTT_PORT=8883
    MQTT_USERNAME="$MQTT_USERNAME"
    MQTT_PASSWORD=secretref:mqtt-password
    MQTT_TLS=true
    MQTT_CA_CERT=/tmp/fred-ca.crt
    MQTT_CA_CERT_B64=secretref:mqtt-ca-cert-b64
    POSTGRES_HOST="$TIMESCALE_APP"
    POSTGRES_PORT=5432
    POSTGRES_DB=fred
    POSTGRES_USER=fred
    POSTGRES_PASSWORD=secretref:postgres-password
    MODEL_MODE="$MODEL_MODE"
    MLFLOW_TRACKING_URI="$MLFLOW_TRACKING_URI"
)

if [[ "$MODEL_MODE" == "openai" ]]; then
    CONSUMER_SECRETS+=(openai-api-key="$OPENAI_API_KEY")
    CONSUMER_ENV_VARS+=(
        OPENAI_API_KEY=secretref:openai-api-key
        OPENAI_MODEL=gpt-5.6-luna
        OPENAI_TTS_MODEL=gpt-4o-mini-tts
        OPENAI_TTS_VOICE=ash
    )
else
    CONSUMER_SECRETS+=(openrouter-api-key="$OPENROUTER_API_KEY")
    CONSUMER_ENV_VARS+=(
        OPENROUTER_API_KEY=secretref:openrouter-api-key
        OPENROUTER_MODEL="$OPENROUTER_MODEL"
        PIPER_VOICE_PATH=backend/voices/en_US-hfc_male-medium.onnx
    )
fi

CONSUMER_EXISTS=false

if az containerapp show \
    --resource-group "$RESOURCE_GROUP" \
    --name "$CONSUMER_APP" \
    >/dev/null 2>&1; then

    CONSUMER_EXISTS=true
    CONSUMER_STATE=$(
        az containerapp show \
            --name "$CONSUMER_APP" \
            --resource-group "$RESOURCE_GROUP" \
            --query properties.provisioningState \
            --output tsv
    )

    # A container app whose first revision never provisioned successfully
    # gets stuck in 'Failed' and rejects normal updates — it has to be
    # deleted and recreated instead.
    if [[ "$CONSUMER_STATE" == "Failed" ]]; then
        echo "$CONSUMER_APP exists but never provisioned successfully (state: Failed) — deleting so it can be recreated..."

        az containerapp delete \
            --name "$CONSUMER_APP" \
            --resource-group "$RESOURCE_GROUP" \
            --yes \
            --output none

        CONSUMER_EXISTS=false
    fi
fi

if [[ "$CONSUMER_EXISTS" == true ]]; then
    echo "$CONSUMER_APP already exists, updating image and configuration..."

    az containerapp secret set \
        --name "$CONSUMER_APP" \
        --resource-group "$RESOURCE_GROUP" \
        --secrets "${CONSUMER_SECRETS[@]}" \
        --output none

    # A mutable ":demo" tag can point at a new image without the declared
    # template string changing, so Container Apps won't always create a new
    # revision on its own. Force one explicitly so updates always apply.
    az containerapp update \
        --name "$CONSUMER_APP" \
        --resource-group "$RESOURCE_GROUP" \
        --image "$CONSUMER_IMAGE" \
        --set-env-vars "${CONSUMER_ENV_VARS[@]}" \
        --revision-suffix "deploy$(date +%s)" \
        --output none
else
    az containerapp create \
        --name "$CONSUMER_APP" \
        --resource-group "$RESOURCE_GROUP" \
        --environment "$ENVIRONMENT" \
        --image "$CONSUMER_IMAGE" \
        --cpu 0.25 \
        --memory 0.5Gi \
        --min-replicas 1 \
        --max-replicas 1 \
        --secrets "${CONSUMER_SECRETS[@]}" \
        --env-vars "${CONSUMER_ENV_VARS[@]}" \
        --output none
fi

# ============================================================
# Output endpoints
# ============================================================

GRAFANA_FQDN=$(
    az containerapp show \
        --name "$GRAFANA_APP" \
        --resource-group "$RESOURCE_GROUP" \
        --query properties.configuration.ingress.fqdn \
        --output tsv
)

echo
echo "========================================"
echo " FRED deployment complete"
echo "========================================"
echo
echo "Grafana:"
echo "https://${GRAFANA_FQDN}"
echo
echo "Secure MQTT:"
echo "${MQTT_HOST}:8883"
echo
echo "MQTT TLS:"
echo "Enabled"
echo
echo "MLflow:"
echo "${MLFLOW_PUBLIC_URL}"
echo
echo "Model mode:"
echo "${MODEL_MODE}"
echo
echo "Pico CA certificate:"
echo "${CA_CERT}"
echo
echo "IMPORTANT:"
echo "TimescaleDB and MLflow storage are currently ephemeral."
echo "Container replacement/recreation can destroy telemetry,"
echo "MLflow traces, registered prompts, and artifacts."