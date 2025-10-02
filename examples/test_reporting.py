import sys
import os

# --- Path Setup (Adjust if your structure is different) ---
# Get the directory where the current script is located
script_dir = os.path.dirname(__file__)
# Get the directory containing the 'examples' and 'includes' folders
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

# --- Reporting Test Samples ---
print("--- Reporting Tests ---")

# Get Bill of Materials
print("\nFetching Bill of Materials...")
bill_of_material = api.request("GET", f"reporting/bill-of-materials")
print(bill_of_material)