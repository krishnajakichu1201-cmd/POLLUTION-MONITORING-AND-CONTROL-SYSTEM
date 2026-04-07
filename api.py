from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import random

app = FastAPI(title="EcoWatch Kerala API", description="Real-time Pollution Monitoring API")

# Enable CORS so the Vite/React frontend can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/data")
async def get_dashboard_data():
    try:
        # Load the base static processed data
        with open('dashboard/src/dashboard_data.json', 'r') as f:
            data = json.load(f)
            
        # Simulate real-time sensor fluctuation for demo purposes
        if "air" in data:
            sum_aqi = 0
            for item in data["air"]:
                if "AQI" in item:
                    # Fluctuate AQI slightly to mimic live updates (-5 to +5)
                    fluctuation = random.randint(-5, 5)
                    item["AQI"] = max(0, item["AQI"] + fluctuation)
                    
                    # Also fluctuate PM2.5 and PM10 to keep realistic proportions
                    try:
                        item["PM2.5(µg/m³)"] = round(max(0, float(item.get("PM2.5(µg/m³)", 0)) + random.uniform(-2, 2)), 1)
                        item["PM10(µg/m³)"] = round(max(0, float(item.get("PM10(µg/m³)", 0)) + random.uniform(-3, 3)), 1)
                    except:
                        pass
                sum_aqi += item.get("AQI", 0)
                
            # Update summary average AQI reflecting the real-time changes
            if len(data["air"]) > 0:
                data["summary"]["avg_aqi"] = round(sum_aqi / len(data["air"]), 1)
                
        return data
    except Exception as e:
        return {"error": str(e), "message": "Failed to load underlying data source. Make sure main.py has generated the JSON."}

@app.get("/api/health")
async def health_check():
    return {"status": "online", "service": "EcoWatch Real-time AI"}
