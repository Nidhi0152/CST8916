import random
import json
import time
import datetime
from azure.iot.device import IoTHubDeviceClient, Message

# Function to simulate Fifth Avenue sensor data
def generate_fifth_avenue_data():
    return {
        "location": "Fifth Avenue",
        "iceThickness": random.randint(20, 40),  # Ice thickness in cm
        "surfaceTemperature": random.randint(-5, 5),  # Surface temperature in °C
        "snowAccumulation": random.randint(0, 15),  # Snow accumulation in cm
        "externalTemperature": random.randint(-10, 0),  # External temperature in °C
        "timestamp": datetime.datetime.utcnow().isoformat() + 'Z'
    }

# Set up IoT Hub connection for Fifth Avenue
CONNECTION_STRING = "HostName=RidueIoTHub.azure-devices.net;DeviceId=FifthAvenue;SharedAccessKey=vuHRI42wPCxntuqPxx9RbCQKDZToJPEBXt5diunAxd8="
device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

# Main loop to simulate data every 10 seconds
while True:
    data = generate_fifth_avenue_data()
    message = Message(json.dumps(data))
    device_client.send_message(message)
    print(f"Fifth Avenue Data sent: {data}")
    time.sleep(10)  # Wait 10 seconds before sending next data point
