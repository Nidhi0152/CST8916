# Real-time Monitoring System for Rideau Canal Skateway

## Scenario Description

The **Rideau Canal Skateway**, located in Ottawa, Canada, is one of the world’s largest outdoor skating rinks. Given its historical and iconic status, ensuring the safety of skaters is of utmost importance. The ice conditions and weather factors such as temperature and snow accumulation must be monitored regularly to ensure that the skateway remains safe for users.

To address this, I have designed a **real-time monitoring system** that simulates IoT sensors deployed at key locations along the Rideau Canal (Dow’s Lake, Fifth Avenue, NAC). These sensors collect data about the following every 10 seconds:

- **Ice Thickness (in cm)**: Critical for determining whether the ice is thick enough to support skaters.
- **Surface Temperature (in °C)**: Helps identify the potential for ice melting, which could be dangerous for skaters.
- **Snow Accumulation (in cm)**: Impacts the strength and usability of the ice surface.
- **External Temperature (in °C)**: Provides weather context and indicates whether external weather conditions might be a risk.

This system continuously monitors the data from these sensors and processes it in real-time to detect unsafe conditions. The data is then stored in **Azure Blob Storage** for further analysis.

The key challenge that this system addresses is the **real-time monitoring and detection of unsafe ice conditions**, which helps to take timely actions to ensure safety along the Rideau Canal Skateway.

## System Architecture

![image](https://github.com/user-attachments/assets/d0d6d836-f8b3-44e4-a000-11a44202f170)

The architecture of the **Real-time Monitoring System for Rideau Canal Skateway** consists of the following components:

1. **Simulated IoT Sensors**: Deployed at Dow’s Lake, Fifth Avenue, and NAC. They collect real-time data (ice thickness, surface temperature, snow accumulation, and external temperature) every 10 seconds.

2. **Azure IoT Hub**: Acts as a central hub, receiving data from the sensors and streaming it in real-time to Azure Stream Analytics.

3. **Azure Stream Analytics**: Processes data in 5-minute tumbling windows to calculate:
   - Average ice thickness
   - Maximum snow accumulation
   Aggregates are grouped by location.

4. **Azure Blob Storage**: Stores the processed output, organized by location and timestamp for easy access and analysis.

### Data Flow

1. Sensors → Azure IoT Hub  
2. IoT Hub → Azure Stream Analytics  
3. Stream Analytics → Azure Blob Storage  

## Implementation Details

### 1. IoT Sensor Simulation

The simulated IoT sensors generate data for three key locations along the Rideau Canal Skateway: **Dow's Lake**, **Fifth Avenue**, and **National Arts Centre (NAC)**. These sensors collect the following Data:
- **Ice Thickness** (in cm)
- **Surface Temperature** (in °C)
- **Snow Accumulation** (in cm)
- **External Temperature** (in °C)

The data is generated every **10 seconds** and sent to **Azure IoT Hub** in a JSON format. Each simulated sensor randomly generates values for these parameters within realistic ranges.

#### JSON Payload Structure

Here’s the structure of the JSON payload sent by the simulated sensors:
```
e.g Dow'sLake Sensor
{
    "location": "Dow's Lake",
    "iceThickness": 33,
    "surfaceTemperature": 3,
    "snowAccumulation": 8,
    "externalTemperature": 0,
    "timestamp": "2025-04-04T16: 51: 00.745122Z"
}
```
Python scripts (`DowsLake_Simulator.py,FifthAvenue_Simulator.py,NAC_Simulator.py`) is used to randomly generate realistic sensor values.

### 2. IoT Hub Configuration:

1. **Create IoT Hub**
   - Create IoT hub.
     - Resource group: cst8916
     - Name: RidueIoTHub
     - Region: Canada Central
     - Tier: Free

![RidueIoThub](https://github.com/user-attachments/assets/fbbc466f-378a-4e45-bbdf-af65f914622b)
2. **Register a Device**
   -  Navigate to Device managmnet > Device. Create 3 devices(sensors) Dow'slake, FifthAvenue,NAC.   
![DowsLake_Senosor](https://github.com/user-attachments/assets/32f28271-5521-4fd8-9057-72f0467510c8)
![FifthAvenueSensor](https://github.com/user-attachments/assets/cedfc58d-3f55-4a14-b09d-3c793bb5c412)
![NACSensor](https://github.com/user-attachments/assets/6611b308-c6f7-4e37-a6ea-df81e879e8a4)

 3. **IoT Hub endpoints:**
![RidueIoThub_Overview](https://github.com/user-attachments/assets/7ec20617-eded-486f-ac7a-f81ca973a369)

### 3. Azure Stream Analytics Job

**Job**: Azure Stream Analytics processes the incoming data from Azure IoT Hub and aggregates the data based on specified queries.

- Adding IoT hub as input
![CreatingInput1](https://github.com/user-attachments/assets/86f8f62d-1ca0-4973-af42-113bdb3284c5)
![CreatingInput](https://github.com/user-attachments/assets/564654ba-a4a3-4fe8-b94d-c2244c0446e1)
- Adding Blob storage as output
 ![CreatingOutput1](https://github.com/user-attachments/assets/22317509-56fd-4013-85b5-e9b13c60844f)
![CreatingOutput](https://github.com/user-attachments/assets/04878678-5c1f-42d9-a8e7-639167e6872d)
- Query used:
Below query groups incoming data every 5 minutes per location and aggregates:Average Ice Thickness and Maximum Snow Accumulation
```SELECT
    location,
    AVG(iceThickness) AS avgIceThickness,
    MAX(snowAccumulation) AS maxSnowAccumulation,
    System.Timestamp AS timestamp
INTO
    ridueoutput
FROM
    ridueinput
GROUP BY
    location,
    TumblingWindow(minute, 5)
```


### 4. Azure Blob Storage

- Created Container (e.g., `riduecontaineroutput`)
![CreatingContainer](https://github.com/user-attachments/assets/88572690-cde1-4ff6-bca4-c49ac96ef065)
![container](https://github.com/user-attachments/assets/1cac32fe-8974-456d-b479-b6e045894b92)
- After running qurey, output file is stored in container in JSON foramt
![StoredData_Container](https://github.com/user-attachments/assets/3c9f24a5-06d8-4414-97fe-52810d5ceea3)
![JSONFile](https://github.com/user-attachments/assets/2dfff3d2-a3b2-4b85-9863-c1e8d769930a)

## Usage Instructions
### Running the IoT Sensor Simulation:
1. Intall python
2. Generate python scripts for three sensors (DowsLake_Simulator.py,FifthAvenue_Simulator.py,NAC_Simulato.py)
3. Define **requirement.txt** and put **azure.iot.device** module in it.
4. Copy **Primary Connection String** for each device from IoT hub and replace in each python script.
```CONNECTION_STRING = "HostName=RidueIoTHub.azure-devices.net;DeviceId=Dow'sLake;SharedAccessKey=mQRuBBxABqxiPwuZ4YjvJLlvwTqjbakYMM3MUfwo2Po="
device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
```
5.Run each python scripts in diffrent terminals by creating virtual enviornment and select **requirement.txt** to install required modules.

### Configuring Azure Services:
1. Create Iot Hub (e.g RidueIoTHub)
2. Register three sensors for three location in **Device** under **Device mangment**.(e.g Dow'sLake, FifthAvenue, NAC)
3. Copy **Primary Connection String** for each sensors for python script
4.Create Stream Analytics (RidueProcessor):
  - Under Job Topology under Input add IoT Hub input (e.g. ridueinput)
  - Under Job Topology under Output add Blob Storage output (e.g.ridueoutput)
  - Under Job Topology under Query insert query, save it and run
   ```SELECT
    location,
    AVG(iceThickness) AS avgIceThickness,
    MAX(snowAccumulation) AS maxSnowAccumulation,
    System.Timestamp AS timestamp
INTO
    ridueoutput
FROM
    ridueinput
GROUP BY
    location,
    TumblingWindow(minute, 5)
```

### Accessing Stored Data:
1. Navigate to Storageaccount and select conatiner (e.g. riduecontaineroutput)
2. After running qurey above find json file in this container
   
## Result
In container(e.g. riduecontaineroutput) json file stores the aggregated sensor data every 5 minutes.
```
{"location":"Dow's
Lake","avgIceThickness":28.862068965517242,"maxSnowAccumulation":15.0,"timestamp":"2025-04-04T16:40:00.0000000Z"}
{"location":"NAC","avgIceThickness":28.93103448275862,"maxSnowAccumulation":13.0,"timestamp":"2025-04-04T16:40:00.0000000Z"}
{"location":"Fifth Avenue","avgIceThickness":29.551724137931036,"maxSnowAccumulation":15.0,"timestamp":"2025-04-04T16:40:00.0000000Z"}
```
## Reflection
1. Initially, I had trouble running the Python scripts in a virtual environment because the **requirements.txt** file wasn't properly selected, and dependencies were missing. As a result, the scripts failed to run. Then I followed a video tutorial to correctly set up the virtual environment and install the dependencies from the requirements.txt file. After that, I was able to successfully run the simulation scripts.
2. This assignment helped me explore Azure IoT services and real-time data processing. I learned how to simulate sensor data, work with Stream Analytics.
