from geopy.geocoders import Nominatim
import pandas as pd

df = pd.read_csv('eth_cons_pp_clust.csv')
df=pd.DataFrame(df)[['lat_mod_dd','lon_mod_dd']]

# Initialize the Nominatim geocoder
geolocator = Nominatim(user_agent="geoapiExercises")

def reverse_geocode(lat, lon):
    location = geolocator.reverse((lat, lon), exactly_one=True)
    return location.address if location else None

# Example DataFrame with latitude and longitude

df = pd.DataFrame(df)

# Apply the reverse geocoding function to each row in the DataFrame
df['place_name'] = df.apply(lambda row: reverse_geocode(row['latitude'], row['longitude']), axis=1)

# Display the DataFrame with place names
print(df)