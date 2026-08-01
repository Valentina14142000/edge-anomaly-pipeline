import asyncio
import random
import httpx

CLOUD_ENDPOINT = "http://127.0.0.1:8000/telemetry"


async def generate_telemetry():
  print("--- Edge Sensor Simulator Started ---")
  async with httpx.AsyncClient() as client:
    while True:
      # Simulate normal operating parameters or rare structural anomaly
      is_anomaly = random.random() < 0.15  # 15% chance of anomaly

      if is_anomaly:
        temperature = round(random.uniform(95.0, 115.0), 2)  # High risk
        pressure = round(random.uniform(80.0, 95.0), 2)
        vibration = round(random.uniform(4.5, 7.0), 2)  # High vibration
        print(f"--- [EDGE] Injecting Anomaly Telemetry ---")
      else:
        temperature = round(random.uniform(60.0, 75.0), 2)
        pressure = round(random.uniform(45.0, 55.0), 2)
        vibration = round(random.uniform(0.5, 1.5), 2)

      payload = {
          "device_id": "uae-industrial-sensor-01",
          "temperature": temperature,
          "pressure": pressure,
          "vibration": vibration,
      }

      try:
        response = await client.post(CLOUD_ENDPOINT, json=payload)
        print(f"Sent: {payload} | Response: {response.json()}")
      except Exception as e:
        print(f"Failed to reach cloud processor: {e}")

      await asyncio.sleep(3)


if __name__ == "__main__":
  asyncio.run(generate_telemetry())