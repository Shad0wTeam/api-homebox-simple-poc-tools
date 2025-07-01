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

# --- Item Attachment Test Samples ---
print("--- Item Attachment Tests ---")

# Get Item Attachments
# IMPORTANT: Replace 'YOUR_ITEM_ID_4' with a real Item ID from your Homebox instance that has attachments
# Example fake ID for reference: 'e5f6a1b2-c3d4-3456-7890-abcdef123456'
item_id4 = "YOUR_ITEM_ID_4" # Replace this placeholder

if item_id4 == 'YOUR_ITEM_ID_4':
     print(f"\nSkipping Get Item Attachments test: Please replace 'YOUR_ITEM_ID_4' with a real ID (e.g., '{fake_uuid()}')")
else:
    print(f"\nFetching attachments for item ID: {item_id4}")
    item_attachments = api.get_attachments(item_id4)
    print(item_attachments)

# Download a Specific Item Attachment
# IMPORTANT: Replace with real IDs and a valid local path
# Example fake IDs for reference:
# Item ID: 'f6a1b2c3-d4e5-4567-890a-bcdef1234567'
# Attachment ID: '01234567-890a-bcde-f123-456789abcdef'
item_id5 = "YOUR_ITEM_ID_5" # Replace this placeholder
attachment_id1 = "YOUR_ATTACHMENT_ID_1" # Replace this placeholder
# Replace 'YOUR_LOCAL_DOWNLOAD_PATH_1' with a local directory path where you want to save the file
download_path_1 = r"YOUR_LOCAL_DOWNLOAD_PATH_1" # Example Windows: r"C:\Users\YourUser\Downloads\Homebox"
                                               # Example Linux/macOS: "/home/youruser/downloads/homebox_files"


if item_id5 == 'YOUR_ITEM_ID_5' or attachment_id1 == 'YOUR_ATTACHMENT_ID_1' or download_path_1 == r"YOUR_LOCAL_DOWNLOAD_PATH_1":
     print(f"\nSkipping Download Attachment test: Please replace 'YOUR_ITEM_ID_5', 'YOUR_ATTACHMENT_ID_1', AND 'YOUR_LOCAL_DOWNLOAD_PATH_1' with real values (e.g., Item ID: '{fake_uuid()}', Attachment ID: '{fake_uuid()}', Path: '/path/to/download')")
else:
    print(f"\nDownloading attachment {attachment_id1} for item {item_id5} to {download_path_1}...")
    attachment_obj = api.download_attachment_by_id(item_id5, attachment_id1, save_to_disk=True, download_path=download_path_1)
    print(f"Download result: {attachment_obj}") # Prints the path where saved, or None


# Fetch Item Attachment Binary Data (Does not save to disk)
# IMPORTANT: Replace with real IDs
# Example fake IDs for reference:
# Item ID: 'a1b2c3d4-e5f6-5678-90ab-cdef12345678'
# Attachment ID: '12345678-90ab-cdef-1234-567890abcdef'
item_id6 = "YOUR_ITEM_ID_6" # Replace this placeholder
attachment_id2 = "YOUR_ATTACHMENT_ID_2" # Replace this placeholder

if item_id6 == 'YOUR_ITEM_ID_6' or attachment_id2 == 'YOUR_ATTACHMENT_ID_2':
    print(f"\nSkipping Fetch Attachment Binary test: Please replace 'YOUR_ITEM_ID_6' and 'YOUR_ATTACHMENT_ID_2' with real IDs (e.g., Item ID: '{fake_uuid()}', Attachment ID: '{fake_uuid()}')")
else:
    print(f"\nFetching binary data for attachment {attachment_id2} for item {item_id6}...")
    attachment_obj1 = api.download_attachment_by_id(item_id6, attachment_id2, save_to_disk=False) # download_path is ignored when save_to_disk is False
    # Note: Printing raw binary data might mess up your console
    # print(attachment_obj1) # Uncomment this line to print the binary content (use with caution)
    if attachment_obj1 is not None:
        print(f"Successfully fetched {len(attachment_obj1)} bytes of binary data.")
    else:
        print("Failed to fetch binary data.")

# Note: The upload_attachment and delete_attachment methods are also in homebox_api.py
# and can be called explicitly if needed.
# e.g., api.upload_attachment('item-id', 'path/to/file', 'photo', 'file-title)
# e.g., api.delete_attachment('item-id', 'attachment-id')