# Edge

### Code and resources for FRED's physical edge device.

This directory is intended for things such as:

- MicroPython / device code
- sensor integrations
- physical input
- display logic
- Wi-Fi setup
- MQTT communication
- device health and network checks

**Example structure:**
```
edge/
├── main.py
├── sensors/
├── display/
├── network/
├── mqtt/
├── config.example.py
└── README.md
```

The exact structure may change as the hardware and implementation are decided.

**Note on Azure mode:** to point the device at an Azure deployment instead of local Docker Compose, set `DEPLOYMENT = "azure"` in `device_config.py` with the current `AZURE_MQTT_HOST` (printed by `azure/deploy.sh` as "MQTT hostname"), copy `mqtt_azure_creds_example.py` to `mqtt_azure_creds.py` and fill in the real credentials, and upload `azure/certs/fred-ca.crt` to the device's filesystem root as `fred-ca.crt`. All three must be present on the device itself, not just in the repo checkout.