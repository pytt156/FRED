# FRED device deployment configuration

# "local" - Connect to the local Docker Compose MQTT broker
# "azure" - Connect to the Azure MQTT broker
DEPLOYMENT = "azure"

LOCAL_MQTT_HOST = "192.168.1.10"
LOCAL_MQTT_PORT = 1883

AZURE_MQTT_HOST = "fred-mosquitto.bravebay-c1aaf610.polandcentral.azurecontainerapps.io"
AZURE_MQTT_PORT = 8883