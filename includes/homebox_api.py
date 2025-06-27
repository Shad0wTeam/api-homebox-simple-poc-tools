"""
╔════════════════════════════════════════════════════════════════════════════╗
║                        🌐 API COMMUNICATION MODULE                         ║
║                     ── HOMEBOX SERVER INTERFACE LOGIC ──                   ║
╚════════════════════════════════════════════════════════════════════════════╝

Overview:
    This module defines the HomeboxAPI class, which encapsulates all logic for 
    communicating with the Homebox server API. It provides centralized handling 
    of credentials, request dispatching, and error logging for all supported 
    HTTP operations (GET, POST, PATCH, PUT, DELETE).

Contents:
    - Base URL and authentication token management
    - Generic request and response handling with logging
    - Convenience methods for resource-specific interactions (items, attachments, etc.)
    - Support for query parameters, JSON payloads, and raw byte streaming
    - Extensible structure for future endpoints or custom integrations

══════════════════════════════════════════════════════════════════════════════
"""

import mimetypes
import os
import platform
import re

import getpass
import keyring
import requests
import configparser

class HomeboxAPI:
    API_BASE_URL = None
    SERVICE_NAME = None  # Used for storing credentials
    _TOKEN = None      # Cached token

    def __init__(self, config_path='config.ini'):
        """Initialize the HomeboxAPI and load configuration."""
        config = configparser.ConfigParser()
        # Construct the full path to config.ini in the same directory as this file
        config_file_path = os.path.join(os.path.dirname(__file__), config_path)
        config.read(config_file_path)

        if 'API' in config:
            HomeboxAPI.API_BASE_URL = config['API'].get('base_url')
            HomeboxAPI.SERVICE_NAME = config['API'].get('service_name', 'TestHomeboxAPI') # Default if not found
        else:
            raise ValueError(f"Missing '[API]' section in configuration file: {config_file_path}")

        if not HomeboxAPI.API_BASE_URL:
            raise ValueError("API base URL not configured.")

        if not HomeboxAPI.SERVICE_NAME:
            HomeboxAPI.SERVICE_NAME = "TestHomeboxAPI" # Default service name if not in config

        print(f"⚙️ API Base URL loaded: {HomeboxAPI.API_BASE_URL}")
        print(f"⚙️ Service Name loaded: {HomeboxAPI.SERVICE_NAME}")

    # ---------------- CREDENTIALS ----------------
    @classmethod
    def store_credentials(cls, username, password):
        """Manually store credentials in keyring."""
        # keyring.set_password(cls.SERVICE_NAME, "username", username) # Original comment
        keyring.set_password(cls.SERVICE_NAME, username, password)
        print("✅ Credentials stored securely.")

    @classmethod
    def get_credentials(cls, new_creds=False):
        """Retrieve or prompt for username and password, storing them securely."""
        # First, attempt to retrieve existing credentials from the keyring
        cred = keyring.get_credential(cls.SERVICE_NAME, "") # Try to get any credential for the service

        # If no credentials exist or new_creds flag is set, ask for new credentials
        if cred is None or new_creds:
            username = input("Enter your Homebox username: ")
            password = getpass.getpass("Enter your Homebox password: ")

            # Check if the credentials already exist for this username
            existing_cred = keyring.get_credential(cls.SERVICE_NAME, username)

            if existing_cred is not None:
                # If credentials exist and new_creds is True, ask if user wants to overwrite
                overwrite = input(f"Credentials for username '{username}' already exist. Do you want to overwrite them? (y/n): ")
                if overwrite.lower() != 'y':
                    print("Using existing credentials.")
                    # Attempt to get the specific credential for the entered username if not overwriting
                    existing_cred_specific = keyring.get_credential(cls.SERVICE_NAME, username)
                    if existing_cred_specific:
                        return existing_cred_specific.username, existing_cred_specific.password
                    else:
                         # Fallback if getting specific cred fails after prompt
                         print("❌ Could not retrieve existing credentials for that username.")
                         return None, None # Indicate failure

            # Store the new credentials securely
            cls.store_credentials(username, password)
            # Retrieve the newly stored credentials to ensure they were saved correctly
            cred = keyring.get_credential(cls.SERVICE_NAME, username)
            if cred:
                 return cred.username, cred.password
            else:
                 print("❌ Failed to retrieve newly stored credentials.")
                 return None, None # Indicate failure

        # Return the retrieved or newly stored credentials
        # If cred was not None initially, return it
        if cred:
            return cred.username, cred.password
        else:
            # This case should ideally not be reached if initial get_credential worked
            print("❌ Could not retrieve credentials.")
            return None, None # Indicate failure

    @classmethod
    def clear_stored_credentials(cls, username):
        """Clear stored credentials from keyring."""
        # keyring.delete_password requires both service name and username
        try:
            keyring.delete_password(cls.SERVICE_NAME, username)
            print(f"🔒 Credentials for username '{username}' removed from keyring.")
        except keyring.errors.NoEntryError:
             print(f"❌ No credentials found for username '{username}'.")
        except Exception as e:
             print(f"❌ An error occurred while trying to remove credentials: {e}")

    # ---------------- LOGIN & TOKEN CREATION ----------------
    @classmethod
    def login(cls):
        """Authenticate and return a session token."""
        if cls._TOKEN:
            return cls._TOKEN  # Use cached token

        username, password = cls.get_credentials()
        # Check if get_credentials returned valid data
        if not username or not password:
             raise ValueError("❌ Login failed: Could not retrieve valid credentials.")

        url = f"{cls.API_BASE_URL}/users/login"
        data = {"username": username, "password": password, "stayLoggedIn": True}

        try:
            response = requests.post(url, headers={"Accept": "application/json", "Content-Type": "application/json"}, json=data)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

            if response.status_code == 200:
                token = response.json().get("token")
                if token:
                    cls._TOKEN = token.replace("Bearer ", "").strip()  # Ensure token is clean
                    print("✅ Login successful")
                    return cls._TOKEN
                else:
                    raise ValueError("❌ Login failed: No token received in response.")
            # The raise_for_status() above handles other error codes, but keeping this for clarity
            # else:
            #     raise ValueError(f"❌ Login failed: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
             raise ConnectionError(f"❌ Login failed: Unable to connect to Homebox API at {url}. Error: {e}") from e
        except ValueError as e:
             raise ValueError(f"❌ Login failed: {e}") from e
        except Exception as e:
             raise RuntimeError(f"❌ An unexpected error occurred during login: {e}") from e

    @classmethod
    def get_headers(cls):
        """Returns cached headers with authentication token."""
        if not cls._TOKEN:
            cls._TOKEN = cls.login()  # Fetch a new token if not cached

        """Return headers with the authentication token."""
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {cls._TOKEN}"
        }
    
    # ---------------- API REQUEST HANDLING ----------------
    @classmethod
    def request(cls, method, endpoint, json=None):
        """Handles API requests with automatic token refresh."""
        url = f"{cls.API_BASE_URL}/{endpoint}"
        headers = cls.get_headers()

        method_function = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "PATCH": requests.patch,
            "DELETE": requests.delete
        }.get(method.upper()) # Use .upper() to make method matching case-insensitive

        if not method_function:
            raise ValueError(f"Unsupported HTTP method: {method}")

        try:
            response = method_function(url, headers=headers, json=json)
            response.raise_for_status() # Raise HTTPError for bad responses

            if response.status_code in (200, 201):
                return response.json()
            elif response.status_code == 204:
                return True  # Successful delete/no content
            else:
                 # This else might be redundant due to raise_for_status, but good as a fallback
                 print(f"⚠️ API Warning: Unexpected status code {response.status_code} for URL {url}")
                 return None # Or raise an exception depending on desired behavior

        except requests.exceptions.HTTPError as e:
            # Handle specific HTTP errors
            if e.response.status_code == 401:
                print("🔄 Token expired or invalid, attempting refresh...")
                cls._TOKEN = None  # Force token refresh
                try:
                     headers = cls.get_headers() # This will call login() again
                     response = method_function(url, headers=headers, json=json)
                     response.raise_for_status() # Check again after refresh
                     if response.status_code in (200, 201):
                          return response.json()
                     elif response.status_code == 204:
                          return True
                     else:
                          print(f"⚠️ API Warning after refresh: Unexpected status code {response.status_code} for URL {url}")
                          return None

                except requests.exceptions.RequestException as refresh_e:
                     print(f"❌ API Error after refresh: Failed to reconnect or request failed again. Error: {refresh_e}")
                     return None
            else:
                 # Handle other HTTP errors (400, 404, 500, etc.)
                 print(f"❌ API Error {e.response.status_code} for {method} {url}: {e.response.text}")
                 return None

        except requests.exceptions.RequestException as e:
             print(f"❌ API Request Failed for {method} {url}. Error: {e}")
             return None
        except Exception as e:
             print(f"❌ An unexpected error occurred during API request: {e}")
             return None

     # ---------------- LABEL OPERATIONS ----------------
    @classmethod
    def get_all_labels(cls):
        """Fetch all labels."""
        return cls.request("GET", "labels") or [] # Return empty list if request fails

    @classmethod
    def delete_label(cls, label_id, label_name):
        """Delete a label by ID."""
        success = cls.request("DELETE", f"labels/{label_id}")
        # The request method returns True for 204 or the JSON response for success, None/False on error
        if success is True: # Check specifically for the success indicator for DELETE
            print(f"🗑️ Deleted label: {label_name} (ID: {label_id})")
            return True
        else:
             print(f"❌ Failed to delete label: {label_name} (ID: {label_id}). Response: {success}")
             return False


     # ---------------- ITEM OPERATIONS ----------------
    @classmethod
    def get_all_items(cls):
        """Fetch all items in the database."""
        response = cls.request("GET", "items")
        # API response for items is often a dictionary with an 'items' key
        if isinstance(response, dict) and 'items' in response:
            return response['items']
        elif isinstance(response, list): # Handle case where API might just return a list
             return response
        else:
            print("⚠️ Could not fetch items or received unexpected format.")
            return [] # Return empty list on failure or unexpected format
    
    @classmethod
    def get_item(cls, item_id):
        """Fetch the an item by its ID."""
        return cls.request("GET", f"items/{item_id}") or []
    
    @classmethod
    def get_archived_items(cls):
        """Fetch all items that are archived."""
        response = cls.get_all_items()  # Fetch all items from the API
        # print(response)
        
        if response: # Check if get_all_items returned a non-empty list
             # Filter the list to include only items with 'archived' set to True
             # Assuming each item in the list is a dictionary
             archived_items = [item for item in response if isinstance(item, dict) and item.get('archived', False)] # Default to False if 'archived' key is missing
             return archived_items
        else:
             print("⚠️ No items found or failed to retrieve all items. Cannot filter archived items.")
             return []

    
    # ---------------- ITEM ATTACHMENT OPERATIONS ----------------
    @classmethod
    def get_default_download_path(cls):
        """Returns the default download path based on the OS."""
        if platform.system() == "Windows":
            # For Windows, use the default "Downloads" directory
            download_dir = os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "Downloads")
        elif platform.system() == "Darwin":  # macOS
            # For macOS, use the default "Downloads" directory
            download_dir = os.path.join(os.environ.get("HOME", os.path.expanduser("~")), "Downloads")
        else:
            # Default to the current working directory if the OS is not recognized or on Linux
             download_dir = os.path.join(os.environ.get("HOME", os.path.expanduser("~")), "Downloads") # Common for Linux
             if not os.path.exists(download_dir):
                 download_dir = os.getcwd() # Fallback if Downloads dir doesn't exist

        # Ensure the path exists
        os.makedirs(download_dir, exist_ok=True)
        return download_dir
    
    @staticmethod
    def sanitize_filename(name):
        """Removes illegal characters from filenames."""
        # Replace invalid characters with underscores
        name = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", name)
        # Remove leading/trailing whitespace and periods (common on Windows)
        name = name.strip().rstrip('. ')
        # Limit filename length (common limit is 255, but some OS have less)
        return name[:250] # Use 250 to be safe
    
    @classmethod
    def get_attachments(cls, item_id):
        """Retrieve all attachments for a specific item by checking the item's attachments field."""
        item = cls.get_item(item_id)

        if isinstance(item, dict) and "attachments" in item and isinstance(item["attachments"], list):
            return item["attachments"]  # Return the list of attachments
        else:
            print("⚠️ No attachments found or failed to retrieve item/invalid item format.")
            return []
    
    @classmethod
    def download_attachment_by_id(cls, item_id, attachment_id, save_to_disk=True, download_path=None):
        """Retrieve a specific attachment, determine its type, and download it."""
        attachments = cls.get_attachments(item_id)

        # Find the attachment with the matching ID
        attachment = next((att for att in attachments if att.get("id") == attachment_id), None)
        if not attachment:
            print(f"❌ Attachment with ID {attachment_id} not found.")
            return None

        attachment_type = attachment.get("type", "unknown")
        document = attachment.get("document", {})

        # Determine filename
        raw_title = document.get("title", attachment_id)  # Use title if available, else ID
        clean_title = cls.sanitize_filename(os.path.splitext(raw_title)[0])  # Remove extensions

        if attachment_type in ["photo", "attachment"]:  # Image files
            file_extension = os.path.splitext(document.get("path", ""))[-1] if "path" in document else ".png"
        else:  # Manuals, receipts, etc. (assume PDF if unknown)
            file_extension = ".pdf"

        file_name = f"{clean_title}{file_extension}"

        # Fetch the attachment data (binary)
        url = f"{cls.API_BASE_URL}/items/{item_id}/attachments/{attachment_id}"
        response = requests.get(url, headers=cls.get_headers(), stream=True)

        if response.status_code == 200:
            if save_to_disk:
                if not download_path:
                    download_path = cls.get_default_download_path()

                os.makedirs(download_path, exist_ok=True)
                file_path = os.path.join(download_path, file_name)

                with open(file_path, "wb") as f:
                    f.write(response.content)

                print(f"✅ Attachment saved to {file_path}")
            else:
                print("✅ Attachment fetched successfully (binary data).")
                return response.content  # Return binary data
        else:
            print(f"❌ Failed to download attachment: {response.status_code} - {response.text}")
            return None
    
    @classmethod
    def download_attachment_raw(cls, item_id, attachment_id):
        """Download attachment bytes directly, bypassing internal request parsing logic."""
        url = f"{cls.API_BASE_URL}/items/{item_id}/attachments/{attachment_id}"
        headers = cls.get_headers()

        try:
            response = requests.get(url, headers=headers, stream=True, timeout=60)
            if response.status_code == 200:
                return response.content  # Always return raw bytes
            else:
                print(f"❌ Attachment download failed: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error during attachment download: {e}")
            return None

    @classmethod    
    def download_raw(cls, resource_type, item_id=None, subresource_id=None, stream=True, timeout=60):
        """
        Generic raw downloader for any subresource (attachments, labels, etc.).

        Args:
            resource_type (str): Base API path like 'items', 'items/labels', or 'items/attachments'.
            item_id (str, optional): ID of the parent item.
            subresource_id (str, optional): ID of the subresource (e.g. attachment_id, label_id).
            stream (bool): Whether to stream the response.
            timeout (int): Timeout in seconds.

        Returns:
            bytes or None: Raw response content if successful, else None.
        """
        endpoint = resource_type
        if item_id:
            endpoint += f"/{item_id}"
        if subresource_id:
            endpoint += f"/{subresource_id}"

        url = f"{cls.API_BASE_URL}/{endpoint}"
        headers = cls._get_headers()

        try:
            response = requests.get(url, headers=headers, stream=stream, timeout=timeout)
            if response.status_code == 200:
                return response.content
            else:
                print(f"❌ Download failed: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error during download: {e}")
            return None

    @classmethod
    def upload_attachment(cls, item_id, file_path, file_type, file_name):
        """Uploads an attachment to a specific item."""
        url = f"{cls.API_BASE_URL}/items/{item_id}/attachments"

        # Ensure the file exists
        if not os.path.exists(file_path):
            print(f"❌ upload_attachment failed: Local file not found at path: {file_path}")
            return None

        # Determine the MIME type using mimetypes.guess_type()
        # guess_type returns a tuple (type, encoding). We only need the type.
        # If it can't guess, 'mime_type' will be None.
        guessed_mime_type, _ = mimetypes.guess_type(file_name)

        # Use the guessed MIME type, or default to "application/octet-stream" if None
        mime_type = guessed_mime_type if guessed_mime_type else "application/octet-stream"

        try:
            # Supported formats: ".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff", ".pdf"
            with open(file_path, "rb") as file:
                files = {
                    "file": (file_name, file, mime_type),
                }
                data = {
                    "type": file_type,
                    "name": file_name,
                }
                print(f"Attempting upload for '{file_name}' (MIME: '{mime_type}', Type: '{file_type}') for item {item_id}.")
                response = requests.post(url, headers={"Authorization": f"Bearer {cls.login()}"}, files=files, data=data)

            if response.status_code == 201:
                print(f"✅ Attachment '{file_name}' uploaded successfully.")
                return response.json()
            else:
                print(f"❌ Failed to upload attachment: {response.status_code} - {response.text}")
                return None
        except FileNotFoundError:
            print(f"❌ File not found at path: {file_path} during upload attempt.")
            return None
        except Exception as e:
            print(f"❌ An unexpected error occurred during upload_attachment for '{file_name}': {e}")
            return None

    @classmethod
    def delete_attachment(cls, item_id, attachment_id):
        """Delete an attachment for a specific item."""

        # Construct the URL for the DELETE request
        url = f"items/{item_id}/attachments/{attachment_id}"

        # Send the DELETE request
        response = cls.request("DELETE", url)

         # If response is boolean (True = success, False = failure)
        if isinstance(response, bool):
            if response:
                print(f"✅ Attachment {attachment_id} deleted successfully.")
                return True
            else:
                print(f"❌ Failed to delete attachment {attachment_id}.")
                return False
        else:
            # If the response is not a boolean, print error message
            print(f"❌ Invalid response received from the API: {response}")
            return False
        
    @classmethod
    def update_attachment(cls, item_id, attachment_id, new_type=None, new_name=None, new_primary=None):
        """Update the attachment of a specific item."""
        
        # Prepare data to be sent, but only include fields that are changed
        data = {}
        
        # Validate and update the type if specified
        if new_type:
            valid_types = ["manual", "photo", "receipt", "attachment", "warranty"]  # Define valid types
            if new_type not in valid_types:
                print(f"⚠️ Invalid type specified: {new_type}. Valid types are: {valid_types}")
                return None
            data["type"] = new_type  # Only update if valid

        # If new name is provided, update the name and title
        if new_name:
            data["name"] = new_name
            data["title"] = new_name  # Keep the title the same as the name

        # If new primary is provided, update the primary flag
        if new_primary is not None:
            data["primary"] = new_primary

        # If neither new_type, new_name, nor new_primary is provided, we don't need to update
        if not data:
            print("⚠️ No updates to apply. Skipping update.")
            return None

        # Construct URL
        url = f"items/{item_id}/attachments/{attachment_id}"
        
        # Log URL for debugging
        print(f"🔹 URL: {url}")

        # Send the PUT request with the data
        response = cls.request("PUT", url, json=data)

        # Check for response content (since it's a dictionary)
        if response and isinstance(response, dict):
            if 'error' in response:  # If an error is returned in the response
                print(f"❌ Failed to update attachment {attachment_id}: {response['error']}")
            else:
                print(f"✅ Attachment {attachment_id} updated successfully.")
                return response
        else:
            print("❌ No response received from the API or invalid response format.")
            return None



    # ---------------- CLEANUP PROCESS ----------------
    @classmethod
    def get_empty_labels(cls):
        """Find and print labels that are not used."""
        print("🔍 Fetching labels and items...")
        all_labels = cls.get_all_labels()
        all_items = cls.get_all_items()

        if not all_labels:
            print("⚠️ No labels found.")
            return
        if not all_items:
            print("⚠️ No items found. Assuming all labels are unused.")
            return

        # Extract all used label IDs from items
        used_label_ids = set()
        for item in all_items:
            if isinstance(item, dict):  # Check if the item is a dictionary
                labels = item.get("labels", [])
                if isinstance(labels, list):  # Ensure labels is a list
                    for label in labels:
                        if isinstance(label, dict) and "id" in label:  # Ensure label is a dict with "id"
                            used_label_ids.add(label["id"])
                        else:
                            print(f"⚠️ Warning: Invalid label format in item: {item.get('id', 'unknown')}. Label: {label}")
                else:
                    print(f"⚠️ Warning: 'labels' field is not a list in item: {item.get('id', 'unknown')}. Value: {labels}")
            else:
                print(f"⚠️ Warning: Unexpected item format (not a dictionary): {item}")

        # Find unused labels
        unused_labels = [label for label in all_labels if label["id"] not in used_label_ids]

        if not unused_labels:
            print("✅ No empty labels found.")
            return

        print(f"📝 Found {len(unused_labels)} empty labels. Listing them...")

        # Print unused labels
        for label in unused_labels:
            print(f"Label Name: {label['name']} (ID: {label['id']})")

        return unused_labels
    
    @classmethod
    def find_and_delete_empty_labels(cls):
        """Find labels that are unused and delete them."""
        print("🔍 Fetching labels and items...")
        all_labels = cls.get_all_labels()
        all_items = cls.get_all_items()

        if not all_labels:
            print("⚠️ No labels found. Skipping deletion.")
            return
        if not all_items:
            print("⚠️ No items found. Assuming all labels are unused.")

        # Extract all used label IDs from items
        used_label_ids = {label["id"] for item in all_items for label in item.get("labels", [])}

        # Find unused labels
        unused_labels = [label for label in all_labels if label["id"] not in used_label_ids]

        if not unused_labels:
            print("✅ No empty labels found.")
            return

        print(f"🗑️ Found {len(unused_labels)} empty labels. Deleting...")

        # Delete unused labels
        for label in unused_labels:
            cls.delete_label(label["id"], label["name"])

        print("✅ Cleanup complete.")
