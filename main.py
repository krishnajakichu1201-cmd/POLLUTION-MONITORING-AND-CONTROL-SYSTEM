import pandas as pd
import json
import os

def process_data():
    print("Processing cleaned data...")
    
    air_df = pd.read_csv('outputs/airpollution.csv')
    soil_df = pd.read_csv('outputs/soilpollution.csv')
    water_df = pd.read_csv('outputs/waterpollution.csv')
    
    # Process Air Data
    air_data = air_df.to_dict(orient='records')
    
    # Process Soil Data
    soil_data = soil_df.to_dict(orient='records')
    
    # Process Water Data
    water_data = water_df.to_dict(orient='records')
    
    # Extract unique values for filters
    cities = sorted(air_df['City'].unique().tolist())
    rivers = sorted(water_df['River'].unique().tolist())
    districts = sorted(soil_df['District'].unique().tolist())
    
    # Summary Statistics
    summary = {
        "avg_aqi": round(air_df['AQI'].mean(), 1),
        "max_aqi": int(air_df['AQI'].max()),
        "total_cities": len(cities),
        "total_rivers": len(rivers),
        "water_safe_percentage": round((water_df['Water_Quality_Class'].apply(lambda x: 'Good' in x or 'Satisfactory' in x).mean() * 100), 1),
        "soil_contaminated_percentage": round((soil_df['Soil_Quality_Class'].str.contains('Contaminated').mean() * 100), 1)
    }
    
    dashboard_data = {
        "air": air_data,
        "soil": soil_data,
        "water": water_data,
        "cities": cities,
        "rivers": rivers,
        "districts": districts,
        "summary": summary
    }
    
    # Ensure dashboard directory exists
    if not os.path.exists('dashboard/src'):
        os.makedirs('dashboard/src', exist_ok=True)
        
    with open('dashboard/src/dashboard_data.json', 'w') as f:
        json.dump(dashboard_data, f, indent=2)
    
    print("Data processed and saved to dashboard/src/dashboard_data.json")

if __name__ == "__main__":
    process_data()
