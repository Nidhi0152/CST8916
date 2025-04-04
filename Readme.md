# Real-time Monitoring System for Rideau Canal Skateway

## Scenario Description

The **Rideau Canal Skateway**, located in Ottawa, Canada, is one of the world’s largest outdoor skating rinks. Given its historical and iconic status, ensuring the safety of skaters is of utmost importance. The ice conditions and weather factors such as temperature and snow accumulation must be monitored regularly to ensure that the skateway remains safe for users.

To address this, we have designed a **real-time monitoring system** that simulates IoT sensors deployed at key locations along the Rideau Canal (Dow’s Lake, Fifth Avenue, NAC). These sensors collect data about the following parameters every 10 seconds:

- **Ice Thickness (in cm)**: Critical for determining whether the ice is thick enough to support skaters.
- **Surface Temperature (in °C)**: Helps identify the potential for ice melting, which could be dangerous for skaters.
- **Snow Accumulation (in cm)**: Impacts the strength and usability of the ice surface.
- **External Temperature (in °C)**: Provides weather context and indicates whether external weather conditions might be a risk.

This system continuously monitors the data from these sensors and processes it in real-time to detect unsafe conditions. The data is then stored in **Azure Blob Storage** for further analysis.

The key challenge that this system addresses is the **real-time monitoring and detection of unsafe ice conditions**, which helps authorities take timely actions to ensure skater safety along the Rideau Canal Skateway.

## System Architecture

The architecture of the **Real-time Monitoring System for Rideau Canal Skateway** consists of the following components:

1. **Simulated IoT Sensors**:
   - **Location**: Sensors are deployed at three key locations: Dow’s Lake, Fifth Avenue, and the National Arts Centre (NAC).
   - **Data Collection**: Sensors collect real-time data about ice thickness, surface temperature, snow accumulation, and external temperature every 10 seconds.

2. **Azure IoT Hub**:
   - **Data Ingestion**: The simulated IoT sensors send the collected data to **Azure IoT Hub**, which acts as a central data hub for all incoming sensor data.
   - **Real-time Data Stream**: The data is pushed into IoT Hub, where it is made available for processing by Azure Stream Analytics.

3. **Azure Stream Analytics**:
   - **Real-time Processing**: The data is processed by **Azure Stream Analytics**, which aggregates it over 5-minute intervals. The processing includes:
     - Calculating the **average ice thickness** for each 5-minute window.
     - Determining the **maximum snow accumulation** over the same 5-minute window.
   - **Data Aggregation**: The data is grouped by **location** (e.g., Dow’s Lake, Fifth Avenue, NAC) and aggregated using a **Tumbling Window**.

4. **Azure Blob Storage**:
   - **Data Storage**: The processed data, which contains aggregated ice conditions for each location, is stored in **Azure Blob Storage**.
   - **File Organization**: The output is stored in a structured manner by location and timestamp, making it easy to access and analyze later.

### Data Flow Diagram

Below is a diagram illustrating the data flow through the system:

1. **IoT Sensors** collect data from three locations on the Rideau Canal.
2. **Azure IoT Hub** receives the data in real-time from the sensors.
3. **Azure Stream Analytics** processes the data (aggregating ice thickness and snow accumulation) in real-time.
4. The **processed data** is stored in **Azure Blob Storage** for further analysis.

> **[Insert Data Flow Diagram Here]**

### Diagram Explanation:
- The **IoT sensors** at Dow's Lake, Fifth Avenue, and NAC send data (ice thickness, snow accumulation, surface temperature, external temperature) to **Azure IoT Hub** every 10 seconds.
- **Azure Stream Analytics** processes this incoming data using a **Tumbling Window** to aggregate the values over 5-minute periods for each location.
- Finally, the processed data (average ice thickness and maximum snow accumulation) is stored in **Azure Blob Storage** for future analysis.
  
## Implementation Details

### 1.IoT Sensor Simulation

The simulated IoT sensors generate data for three key locations along the Rideau Canal Skateway: **Dow's Lake**, **Fifth Avenue**, and **National Arts Centre (NAC)**. These sensors collect the following parameters:

- **Ice Thickness** (in cm)
- **Surface Temperature** (in °C)
- **Snow Accumulation** (in cm)
- **External Temperature** (in °C)

The data is generated every **10 seconds** and sent to **Azure IoT Hub** in a JSON format. Each simulated sensor randomly generates values for these parameters within realistic ranges.

#### JSON Payload Structure

Here’s the structure of the JSON payload sent by the simulated Dow'sLake sensors:
```
{
    "location": "Dow's Lake",
    "iceThickness": 33,
    "surfaceTemperature": 3,
    "snowAccumulation": 8,
    "externalTemperature": 0,
    "timestamp": "2025-04-04T16: 51: 00.745122Z"
}
```
