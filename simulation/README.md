# Simulation

### Tools for simulating room and device data during development and demo.

This directory is intended for things such as:

- simulated sensor values
- simulated network conditions
- MQTT event publishers
- repeatable demo scenarios

**Example structure:**

```
simulation/
├── sensor_simulator.py
├── network_simulator.py
├── scenarios/
└── README.md
```

Simulation should make it possible to develop and test FRED without requiring all physical hardware to be available.