# Rideau Canal Sensor Simulation

## Overview
This project is a simple Python sensor simulator for the Rideau Canal Skateway. It mimics three IoT devices (Dow’s Lake, Fifth Avenue, NAC) and sends fake ice and weather data to an Azure IoT Hub every 10 seconds. The data can be processed by Azure Stream Analytics and used by a dashboard.

## Technologies
- Python
- Azure IoT Device SDK for Python (`azure-iot-device`)
- `python-dotenv` for loading environment variables

## Prerequisites
- Python 3.11+ and `pip` installed
- An existing Azure IoT Hub
- Three IoT devices created in the IoT Hub with device connection strings:
  - `dows-lake-device`
  - `fifth-avenue-device`
  - `nac-device`

## Installation
1. Clone the repository.
2. Open a terminal in the project folder.
4. Install dependencies: `pip install -r requirements.txt`

## Configuration
Create a `.env` file in the project folder containing the device connection strings:

```
DOWS_LAKE_CONNECTION_STRING=HostName=...;DeviceId=dows-lake-device;SharedAccessKey=...
FIFTH_AVENUE_CONNECTION_STRING=HostName=...;DeviceId=fifth-avenue-device;SharedAccessKey=...
NAC_CONNECTION_STRING=HostName=...;DeviceId=nac-device;SharedAccessKey=...
```

- Replace the `...` portions with the actual values from the Azure Portal.
- Ensure `.env` is listed in `.gitignore` so secrets are not committed.

## Usage
1. Verify `.env` is configured.
2. Run the simulator from the project folder:

```
python sensor_simulator.py
```

3. You should see log lines every 10 seconds for each location with the current random values.
4. Press `Ctrl+C` to stop the simulator.

## Code Structure
- `sensor_simulator.py`: main script that loads environment variables, creates one IoT Hub client per device, generates random sensor readings, and sends JSON messages to IoT Hub in a loop.

Key pieces:
- Device setup: builds three clients using the three connection strings.
- Telemetry generation: creates fake data for ice thickness, surface temperature, snow, and external temperature.
- Send loop: every 10 seconds, sends one JSON message per location to the IoT Hub.

Representative functions:
- `create_clients()`: sets up IoT Hub clients for each device.
- `generate_telemetry(meta)`: returns a dictionary with random values for one location.
- `main()`: runs the infinite loop that sends messages and prints them.

## Sensor Data Format
Each JSON payload sent to IoT Hub follows this schema:

- `deviceId`: string, the IoT device id (e.g., `dows-lake-device`)
- `location`: string, the logical location name (e.g., `DowsLake`)
- `timestamp`: ISO 8601 timestamp in UTC
- `iceThickness`: number, ice thickness in cm
- `surfaceTemperature`: number, ice surface temperature in °C
- `snowAccumulation`: number, snow depth on the ice in cm
- `externalTemperature`: number, air temperature in °C

Example JSON:

```json
{
  "deviceId": "dows-lake-device",
  "location": "DowsLake",
  "timestamp": "2025-12-08T21:40:00.123456+00:00",
  "iceThickness": 32.5,
  "surfaceTemperature": -4.8,
  "snowAccumulation": 6.2,
  "externalTemperature": -10.3
}
```

## Troubleshooting
- Module not found (e.g., `No module named 'azure'`):
  - Run `pip install -r requirements.txt` in the correct environment.
  - Confirm you are using the Python version that has the packages installed.
- Missing environment variable or startup errors:
  - Verify `DOWS_LAKE_CONNECTION_STRING`, `FIFTH_AVENUE_CONNECTION_STRING`, `NAC_CONNECTION_STRING`.
  - Ensure `load_dotenv()` is called and `.env` is in the same folder as `sensor_simulator.py`.
  - Confirm `.env` is present and not empty.
- IoT Hub not receiving messages:
  - Confirm devices in Azure are enabled.
  - Use device connection strings, not the IoT Hub connection string.
  - Check your internet connection.
  - In IoT Hub metrics, inspect “Device to cloud messages” to see if the count rises while the simulator runs.
