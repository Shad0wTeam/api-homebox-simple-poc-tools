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

# --- Items Test Samples ---
print("--- Items Tests ---")

# Get Item by Asset ID
# IMPORTANT: Replace 'YOUR_ASSET_ID' with a real Asset ID from your Homebox instance
asset = "YOUR_ASSET_ID" # Example: "ITEM-123"

if asset == 'YOUR_ASSET_ID':
     print(f"\nSkipping Get Item by Asset ID test: Please replace 'YOUR_ASSET_ID' with a real ID (e.g., 'ITEM-123')")
else:
    print(f"\nFetching item with Asset ID: {asset}")
    item_asset = api.request("GET", f"assets/{asset}")
    print(item_asset)

# Query All Items
print("\nFetching all items...")
all_items = api.get_all_items()
print(f"Fetched {len(all_items)} items.") # Print count instead of all data
# print(all_items) # Uncomment this line to print all item data

# Get All Custom Field Names
print("\nFetching custom field names...")
custom_fields = api.request("GET", "items/fields")
print(custom_fields)

# Get All Custom Field Values (⚠️ API Error 500 Observed Previously - May vary by Homebox version)
print("\nFetching custom field values (expecting potential API Error 500)...")
custom_values = api.request("GET", "items/fields/values")
print(custom_values)

# Get Item by Item ID
# IMPORTANT: Replace 'YOUR_ITEM_ID_1' with a real Item ID from your Homebox instance
# Example fake ID for reference: 'b2c3d4e5-f6a1-0123-4567-890abcdef123'
item_id1 = "YOUR_ITEM_ID_1" # Replace this placeholder

if item_id1 == 'YOUR_ITEM_ID_1':
    print(f"\nSkipping Get Item by ID test: Please replace 'YOUR_ITEM_ID_1' with a real ID (e.g., '{fake_uuid()}')")
else:
    print(f"\nFetching item with ID: {item_id1}")
    item_OBJ = api.get_item(item_id1)
    print(item_OBJ)

# Get All Archived Items
print("\nFetching all archived items...")
item_archived = api.get_archived_items()
print(f"Fetched {len(item_archived)} archived items.") # Print count instead of all data
# print(item_archived) # Uncomment this line to print all archived item data


# Get the full path of an item
# IMPORTANT: Replace 'YOUR_ITEM_ID_2' with a real Item ID from your Homebox instance
# Example fake ID for reference: 'c3d4e5f6-a1b2-1234-5678-90abcdef1234'
item_id2 = "YOUR_ITEM_ID_2" # Replace this placeholder

if item_id2 == 'YOUR_ITEM_ID_2':
     print(f"\nSkipping Get Item Path test: Please replace 'YOUR_ITEM_ID_2' with a real ID (e.g., '{fake_uuid()}')")
else:
    print(f"\nFetching path for item with ID: {item_id2}")
    item_path = api.request("GET", f"items/{item_id2}/path")
    print(item_path)

# Get Asset label (⚠️ API Error 404 Observed Previously - May vary by Homebox version)
# IMPORTANT: Replace 'YOUR_ASSET_ID_2' with a real Asset ID from your Homebox instance
asset_no = "YOUR_ASSET_ID_2" # Example: "ASSET-XYZ"

if asset_no == 'YOUR_ASSET_ID_2':
     print(f"\nSkipping Get Asset Label test: Please replace 'YOUR_ASSET_ID_2' with a real ID (e.g., 'ASSET-XYZ')")
else:
    print(f"\nFetching label for Asset: {asset_no} (expecting potential API Error 404)...")
    asset_label = api.request("GET", f"labelmaker/assets/{asset_no}")
    print(asset_label)


# Get Item label (⚠️ JSONDecodeError Observed Previously - May vary by Homebox version)
# IMPORTANT: Replace 'YOUR_ITEM_ID_3' with a real Item ID from your Homebox instance
# Example fake ID for reference: 'd4e5f6a1-b2c3-2345-6789-0abcdef12345'
item_id3 = "YOUR_ITEM_ID_3" # Replace this placeholder

if item_id3 == 'YOUR_ITEM_ID_3':
    print(f"\nSkipping Get Item Label test: Please replace 'YOUR_ITEM_ID_3' with a real ID (e.g., '{fake_uuid()}')")
else:
    print(f"\nFetching label for Item ID: {item_id3} (expecting potential JSONDecodeError)...")
    item_label = api.request("GET", f"labelmaker/item/{item_id3}")
    print(item_label)

# Get All Items label
show_all = True # Set to False to avoid Querying all labels

if show_all:
    print(f"\nPrinting all Items in the Database\n{'=' * 80}\n")
    all_items = api.get_all_items()
    print(all_items)