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

# --- Item Maintenance Test Samples ---
print("--- Item Maintenance Tests ---")

# Get Maintenance Log for an Item
# IMPORTANT: Replace 'YOUR_ITEM_ID_7' with a real Item ID from your Homebox instance that has maintenance logs
# Example fake ID for reference: 'b2c3d4e5-f6a1-6789-0abc-def123456789'
item_id7 = "YOUR_ITEM_ID_7" # Replace this placeholder

if item_id7 == 'YOUR_ITEM_ID_7':
    print(f"\nSkipping Get Item Maintenance Log test: Please replace 'YOUR_ITEM_ID_7' with a real ID (e.g., '{fake_uuid()}')")
else:
    print(f"\nFetching maintenance logs for item ID: {item_id7}")
    item_maintenance = api.request("GET", f"items/{item_id7}/maintenance")
    print(item_maintenance)

# Note: Other maintenance related operations (like adding logs) would need POST requests,
# which are not included as simple GET samples here.