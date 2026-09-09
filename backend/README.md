# Backend

### Backend services and logic for FRED.

This directory is intended for things such as:

- MQTT subscriber/publisher
- room state
- pet state / state engine
- persistence
- PostgreSQL integration
- logging and observability

**Example structure:**

```
backend/
├── app/
│ ├── mqtt/
│ ├── state/
│ ├── database/
│ └── models/
├── tests/
├── pyproject.toml
└── README.md
```

The backend should be able to run and be tested independently from the physical device.