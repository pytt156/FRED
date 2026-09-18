# FRED device deployment configuration

# "local" - Connect to the local Docker Compose MQTT broker
# "azure" - Connect to the Azure MQTT broker
DEPLOYMENT = "local"

LOCAL_MQTT_HOST = "192.168.1.10"
LOCAL_MQTT_PORT = 1883

 # Leave empty until you deploy — azure/deploy.sh prints this as "MQTT hostname"
# (also visible via: az containerapp show --name fred-mosquitto --resource-group FRED --query properties.configuration.ingress.fqdn)
AZURE_MQTT_HOST = ""
AZURE_MQTT_PORT = 8883