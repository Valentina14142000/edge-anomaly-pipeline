from fastapi import FastAPI
import numpy as np
from pydantic import BaseModel
from sklearn.ensemble import IsolationForest

app = FastAPI(
    title="Edge-to-Cloud Anomaly Detection Pipeline",
    description=(
        "Real-time industrial IoT telemetry ingestion and machine learning"
        " anomaly detection"
    ),
    version="1.0.0",
)

# Initialize and pre-fit Isolation Forest on baseline normal operational bounds
# Features: [temperature, pressure, vibration]
X_train = np.array([
    [65.0, 50.0, 1.0],
    [70.0, 52.0, 1.2],
    [62.0, 48.0, 0.8],
    [72.0, 55.0, 1.5],
    [68.0, 49.0, 1.1],
])

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X_train)


class TelemetryPayload(BaseModel):
  device_id: str
  temperature: float
  pressure: float
  vibration: float


@app.post("/telemetry")
async def ingest_telemetry(data: TelemetryPayload):
  features = np.array(
      [[data.temperature, data.pressure, data.vibration]]
  )

  # Predict: 1 = Normal, -1 = Anomaly
  prediction = model.predict(features)[0]
  is_anomaly = bool(prediction == -1)

  status = "CRITICAL_ANOMALY" if is_anomaly else "NORMAL"

  if is_anomaly:
    print(
        f"🚨 ALERT: Anomaly detected on {data.device_id}! Metrics:"
        f" {data.dict()}"
    )

  return {
      "device_id": data.device_id,
      "status": status,
      "anomaly_score": float(model.decision_function(features)[0]),
  }