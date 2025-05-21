import sys
import os
import uuid # Import uuid for generating fake example IDs

# --- Path Setup (Adjust if your structure is different) ---
# Get the directory where the current script is located (e.g., .../API.HomeBox_V1/examples)
script_dir = os.path.dirname(__file__)
# Get the directory containing the 'examples' and 'includes' folders (e.g., .../API.HomeBox_V1)
# This is the directory one level up from the script directory
api_homebox_v1_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
# Add the directory containing the 'includes' package to sys.path
sys.path.append(api_homebox_v1_dir)


# --- Import the HomeboxAPI class from the includes package ---
try:
    # Now import from the 'includes' package
    from includes.homebox_api import HomeboxAPI
except ImportError:
    print("Error: Could not import HomeboxAPI.")
    print(f"Please ensure that:")
    print(f"1. Your '{os.path.basename(api_homebox_v1_dir)}' directory is structured correctly (containing 'includes' and 'examples').")
    print(f"2. 'homebox_api.py' is located inside the 'includes' directory.")
    print(f"Attempted to add '{api_homebox_v1_dir}' to sys.path.")
    print(f"Current sys.path: {sys.path}")
    sys.exit(1)

# --- Initialize the API client ---
api = HomeboxAPI()

# Helper function to generate a fake UUID string for examples
def fake_uuid():
    return str(uuid.uuid4())

# --- Locations Test Samples ---
print("--- Locations Tests ---")

# Get Location label (⚠️ JSONDecodeError Observed Previously - May vary by Homebox version)
# IMPORTANT: Replace 'YOUR_LOCATION_ID_1' with a real Location ID from your Homebox instance
# Example fake ID for reference: 'c3d4e5f6-a1b2-7890-12de-f1234567890a'
loc_id1 = "YOUR_LOCATION_ID_1" # Replace this placeholder

if loc_id1 == 'YOUR_LOCATION_ID_1':
    print(f"\nSkipping Get Location Label test: Please replace 'YOUR_LOCATION_ID_1' with a real ID (e.g., '{fake_uuid()}')")
else:
    print(f"\nFetching label for Location ID: {loc_id1} (expecting potential JSONDecodeError)...")
    loc_label = api.request("GET", f"labelmaker/location/{loc_id1}")
    print(loc_label)

# Get All Locations
print("\nFetching all locations...")
all_location = api.request("GET", f"locations")
print(f"Fetched {len(all_location)} locations.") # Print count instead of all data
# print(all_location) # Uncomment this line to print all location data


# Get Locations Tree
print("\nFetching locations tree...")
location_trees = api.request("GET", f"locations/tree")
print(location_trees)

# Get Location by ID
# IMPORTANT: Replace 'YOUR_LOCATION_ID_2' with a real Location ID from your Homebox instance
# Example fake ID for reference: 'd4e5f6a1-b2c3-8901-23ef-1234567890ab'
loc_id2 = "YOUR_LOCATION_ID_2" # Replace this placeholder

if loc_id2 == 'YOUR_LOCATION_ID_2':
     print(f"\nSkipping Get Location by ID test: Please replace 'YOUR_LOCATION_ID_2' with a real ID (e.g., '{fake_uuid()}')")
else:
    print(f"\nFetching location with ID: {loc_id2}")
    location_obj= api.request("GET", f"locations/{loc_id2}")
    print(location_obj)