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

# --- Labels Test Samples ---
print("--- Labels Tests ---")

# Get All Labels
print("\nFetching all labels...")
labels = api.get_all_labels()
print(labels)

# Get a Specific Label by ID
# IMPORTANT: Replace 'YOUR_LABEL_ID' with a real Label ID from your Homebox instance
# Example fake ID for reference: 'a1b2c3d4-e5f6-7890-1234-567890abcdef'
label_id = 'YOUR_LABEL_ID' # Replace this placeholder

if label_id == 'YOUR_LABEL_ID':
    print(f"\nSkipping Get Label test: Please replace 'YOUR_LABEL_ID' with a real ID (e.g., '{fake_uuid()}')")
else:
    print(f"\nFetching label with ID: {label_id}")
    label_obj = api.request("GET", f"labels/{label_id}")
    print(label_obj)

# Print Empty Labels
print("\nFinding empty labels...")
empty_labels = api.get_empty_labels()
# The api.get_empty_labels() method already prints the results
# print(empty_labels) # Uncomment this line if you want to print the returned list explicitly

# Note: The delete_label and find_and_delete_empty_labels methods are also in homebox_api.py
# but are not included as uncommented samples here to prevent accidental deletion.
# Users can call them explicitly if needed, e.g., api.delete_label('some-id', 'some-name')
# or api.find_and_delete_empty_labels()