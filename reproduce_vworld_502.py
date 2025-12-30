
import os
import requests
from dotenv import load_dotenv
from api.vworld_api import VWorldGeocodingProvider
from api.vworld_wfs import get_building_polygon

load_dotenv()

api_key = os.getenv("VWORLD_API_KEY")
domain = os.getenv("VWORLD_DOMAIN")

print(f"API Key present: {bool(api_key)}")
print(f"Domain: {domain}")

if not api_key:
    print("Error: VWORLD_API_KEY not found in environment.")
    exit(1)

# Test Geocoding
try:
    print("\n[Testing Geocoding with VWorldGeocodingProvider]")
    provider = VWorldGeocodingProvider(api_key, domain=domain)
    # Using the failing address from screenshot
    address = "서울특별시 중구 세종대로 110" 
    result = provider.geocode(address)
    print(f"Geocoding Result: {result}")
    
    if result and result.point:
         # Test WFS
        print("\n[Testing WFS with get_building_polygon]")
        lat = result.point['lat']
        lon = result.point['lon']
        poly = get_building_polygon((lat, lon), api_key, domain=domain)
        print(f"WFS Result (Polygon points count): {len(poly) if poly else 'None'}")
    else:
        print("Skipping WFS test because geocoding failed.")

except Exception as e:
    print(f"FAILED with Exception: {e}")
