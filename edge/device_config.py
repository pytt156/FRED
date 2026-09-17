# FRED device deployment configuration

# "local" - Connect to the local Docker Compose MQTT broker
# "azure" - Connect to the Azure MQTT broker
DEPLOYMENT = "local"

LOCAL_MQTT_HOST = "192.168.1.10"
LOCAL_MQTT_PORT = 1883

AZURE_MQTT_HOST = ""
AZURE_MQTT_PORT = 8883