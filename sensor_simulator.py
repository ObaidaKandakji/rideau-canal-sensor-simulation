import os
import time
import json
import random
from datetime import datetime, timezone

from azure.iot.device import IoTHubDeviceClient, Message
from dotenv import load_dotenv


load_dotenv()

SEND_INTERVAL_SECONDS = 10  # required by assignment

# Environment variables must contain the three device connection strings
DEVICES = [
    {
        "device_id": "dows-lake-device",
        "location": "DowsLake",
        "env_var": "DOWS_LAKE_CONNECTION_STRING",
    },
    {
        "device_id": "fifth-avenue-device",
        "location": "FifthAvenue",
        "env_var": "FIFTH_AVENUE_CONNECTION_STRING",
    },
    {
        "device_id": "nac-device",
        "location": "NAC",
        "env_var": "NAC_CONNECTION_STRING",
    },
]


def create_clients():
    clients = []
    for d in DEVICES:
        conn_str = os.getenv(d["env_var"])
        if not conn_str:
            raise RuntimeError(
                f"Missing environment variable {d['env_var']} for {d['location']}"
            )
        client = IoTHubDeviceClient.create_from_connection_string(conn_str)
        clients.append({"meta": d, "client": client})
    return clients


def generate_telemetry(meta):
    # Simple ranges chosen to sometimes hit safe/caution/unsafe conditions
    ice_thickness = random.uniform(15.0, 45.0)       # cm
    surface_temp = random.uniform(-10.0, 2.0)        # °C
    snow_acc = random.uniform(0.0, 20.0)             # cm
    external_temp = random.uniform(-25.0, 5.0)       # °C

    return {
        "deviceId": meta["device_id"],
        "location": meta["location"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "iceThickness": round(ice_thickness, 2),
        "surfaceTemperature": round(surface_temp, 2),
        "snowAccumulation": round(snow_acc, 2),
        "externalTemperature": round(external_temp, 2),
    }


def main():
    print("Starting Rideau Canal sensor simulation...")
    clients = create_clients()
    print(f"Initialized {len(clients)} devices. Sending every {SEND_INTERVAL_SECONDS}s.")

    try:
        while True:
            for item in clients:
                meta = item["meta"]
                client = item["client"]

                telemetry = generate_telemetry(meta)
                body = json.dumps(telemetry)
                message = Message(body)
                message.content_type = "application/json"
                message.content_encoding = "utf-8"

                client.send_message(message)
                print(
                    f"[{telemetry['timestamp']}] "
                    f"{telemetry['location']}: "
                    f"ice={telemetry['iceThickness']}cm, "
                    f"surface={telemetry['surfaceTemperature']}°C, "
                    f"snow={telemetry['snowAccumulation']}cm, "
                    f"external={telemetry['externalTemperature']}°C"
                )

            time.sleep(SEND_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("Stopping simulation.")
    finally:
        for item in clients:
            try:
                item["client"].disconnect()
            except Exception:
                pass
        print("Simulation stopped.")


if __name__ == "__main__":
    main()
