import requests
import random
import time

API_URL = "http://127.0.0.1:8000/ingest"

# Simulating different scenarios
scenarios = [
    {"soil_moisture": 25.0, "temperature": 32.0, "humidity": 40.0}, # Drought + Heat
    {"soil_moisture": 60.0, "temperature": 24.0, "humidity": 55.0}, # Perfect Conditions
    {"soil_moisture": 85.0, "temperature": 20.0, "humidity": 80.0}, # Overwatering
]

def send_data():
    print("🌱 Simulating IoT Sensors...")
    for data in scenarios:
        try:
            response = requests.post(API_URL, json=data)
            if response.status_code == 201:
                print(f"✅ Data Sent: {data} -> Saved ID: {response.json()['id']}")
            else:
                print(f"❌ Error: {response.text}")
        except Exception as e:
            print(f"⚠️ Connection failed: {e}")
        
        # Pause briefly between sends so they have different timestamps
        time.sleep(1) 

if __name__ == "__main__":
    send_data()