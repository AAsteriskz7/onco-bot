import googlemaps
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('APIKEY')
gmaps = googlemaps.Client(key=API_KEY)

def get_nearest_hospitals(address):
    # Geocode the address to get latitude and longitude
    geocode_result = gmaps.geocode(address)
    
    if not geocode_result:
        return "Address not found"
    
    # Extract the lat/lng from the geocode result
    location = geocode_result[0]['geometry']['location']
    lat = location['lat']
    lng = location['lng']
    
    # Search for nearby hospitals
    places_result = gmaps.places_nearby(
        location=(lat, lng), 
        radius=5000,  # Search within 5 kilometers
        type='hospital'  # Searching specifically for hospitals
    )
    
    # Extract hospital names and their addresses (only the closest 5)
    hospitals = []
    for place in places_result['results'][:5]:  # Limit to 5 results
        name = place['name']
        address = place['vicinity']
        hospitals.append({'name': name, 'address': address})
    
    return hospitals

address_input = "1600 Amphitheatre Parkway, Mountain View, CA"
hospitals = get_nearest_hospitals(address_input)

# if hospitals:
#     for i, hospital in enumerate(hospitals, start=1):
#         print(f"{i}. {hospital['name']} - {hospital['address']}")
# else:
#     print("No hospitals found.")