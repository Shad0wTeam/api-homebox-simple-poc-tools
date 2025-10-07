# Homebox API Python Client

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI Version](https://img.shields.io/pypi/v/requests.svg)](https://pypi.org/project/requests/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python client library for interacting with the [Homebox](https://hay-kot.github.io/homebox/) inventory system API. This library provides a convenient way to authenticate and perform various operations on your Homebox data from Python scripts.

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [✨ Features](#-features)
- [📦 Installation](#installation)
- [⚙️ Setup](#setup)
- [💻 Usage](#usage)
- [📁 Project Structure](#project-structure)
- [🤝 Contributing](#contributing)
- [📄 License](#license)
- [🙏 Acknowledgements](#acknowledgements)

## 🚀 Quick Start

Get up and running with the Homebox API Python Client in minutes:

### 1. **Install Dependencies**
```bash
pip install requests>=2.32.0 keyring>=25.2.1
```

### 2. **Configure Your Homebox Instance**
Create a `config.ini` file in your `includes/` directory:
```ini
[API]
base_url = http://your-homebox-instance.com/api/v1
service_name = MyHomeboxApp
```

### 3. **Start Using the API**
```python
from includes.homebox_api import HomeboxAPI

# Initialize the client (will prompt for credentials on first run)
api = HomeboxAPI()

# Get all items
items = api.get_all_items()
print(f"Found {len(items)} items in your Homebox!")

# Get items by location
location_items = api.get_items_by_location("your-location-id")
print(f"Items in location: {location_items}")
```

That's it! 🎉 You're ready to integrate with your Homebox inventory system.

## ✨ Features

- 🔗 **Centralized API communication logic**
- 🔐 **Secure credential management** using `keyring`
- 🔄 **Automatic token handling and refresh**
- 🌐 **Support for common HTTP methods** (GET, POST, PATCH, PUT, DELETE)
- 📚 **Convenience methods for accessing various Homebox resources:**
  - 🏷️ Labels
  - 📦 Items (including by Asset ID, archived items)
  - 📎 Item Attachments (get, download, upload, delete, update)
  - 🔧 Item Maintenance Logs
  - 📍 Locations (including tree view)
  - 📋 General Maintenance Logs
  - 🔔 Notifiers
  - 📊 Reporting (Bill of Materials)
- 🛠️ **Helper functions** for file handling (default download path, filename sanitization)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    Create a `requirements.txt` file in the root of your repository with the following content:
    ```
    requests>=2.32.0
    keyring>=25.2.1
    ```
    Then install using pip:
    ```bash
    pip install -r requirements.txt
    ```

## Setup

1.  **Configure the Application using `config.ini`:**
    The application now uses a dedicated configuration file, `config.ini`, located in the same directory as the `includes/homebox_api.py` file. You need to create this file and populate it with your Homebox instance's API details.

    a.  **Create `config.ini`:** If it doesn't already exist, create a file named `config.ini` in the same directory as your `includes/homebox_api.py` file.

    b.  **Edit `config.ini`:** Open `config.ini` and add the following content, replacing the placeholder values with your actual Homebox API URL and a service name:

    ```ini
    [API]
    base_url = http://your_homebox_server_address/api/v1
    service_name = YourServiceName
    ```

    * **`base_url`**: Replace `http://your_homebox_server_address/api/v1` with the actual URL of your Homebox instance's API (e.g., `http://your_homebox.instance.com/api/v1` or `http://localhost:3100/api/v1`).
    * **`service_name`**: This is an optional field used for storing credentials. You can set a descriptive name for your application (e.g., `MyHomeboxApp`, `IntegrationTool`). If not provided, it defaults to `TestHomeboxAPI`.

    **Example `config.ini`:**

    ```ini
    [API]
    base_url = [http://homebox.example.com/api/v1](http://homebox.example.com/api/v1)
    service_name = MyAwesomeIntegration
    ```

2.  **Store Credentials:**
    The first time you run a script that requires authentication (like fetching data), the `get_credentials()` method will prompt you for your Homebox username and password. These credentials will be securely stored using the `keyring` library specific to your operating system.

    Alternatively, you can manually store credentials using the `store_credentials` class method (though prompting is usually preferred for first-time setup):
    ```python
    from includes.homebox_api import HomeboxAPI

    # This will prompt if not found or store directly
    HomeboxAPI.store_credentials("your_homebox_username", "your_homebox_password")
    print("Credentials stored.")
    ```

    You can clear stored credentials using `clear_stored_credentials`:
    ```python
    from includes.homebox_api import HomeboxAPI
    HomeboxAPI.clear_stored_credentials("your_homebox_username")
    print("Credentials cleared.")
    ```
    **Note:** The `clear_stored_credentials` method requires the username to know which credential to delete.

## Usage

1.  **Import and Initialize:**
    In any script where you want to use the API client, import the `HomeboxAPI` class and create an instance:

    ```python
    # Assuming your script is structured to find 'includes'
    import sys
    import os

    # Adjust path based on your project structure if needed
    current_dir = os.path.dirname(__file__)
    # Example assuming script is in 'examples/' and homebox_api.py is in 'includes/'
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    includes_dir = os.path.join(parent_dir, 'includes')
    sys.path.append(includes_dir)


    try:
        from homebox_api import HomeboxAPI
    except ImportError:
        print("Error: Could not import HomeboxAPI.")
        print(f"Please ensure 'homebox_api.py' is in {includes_dir} or adjust sys.path.")
        sys.exit(1)

    # Initialize the API client - this will handle login/token
    api = HomeboxAPI()

    # Now you can make API calls using the 'api' instance
    # items = api.get_all_items()
    # print(items)
    ```

2.  **Running Examples:**
    Navigate to the `examples/` directory. Each `.py` file in this directory demonstrates how to use specific parts of the API client.

    **Before running any example script:**
    * Open the file.
    * **Carefully read the comments** and replace the placeholder values like `YOUR_LABEL_ID`, `YOUR_ITEM_ID`, `YOUR_ASSET_ID`, `YOUR_ATTACHMENT_ID`, `YOUR_LOCATION_ID`, and `YOUR_LOCAL_DOWNLOAD_PATH` with actual valid identifiers and paths from your Homebox instance. Example fake IDs are provided in comments for format reference, but you need to use your own real data IDs.

    To run an example, open your terminal or command prompt, activate your virtual environment if you created one, and execute the script:
    ```bash
    cd examples/
    python test_labels.py
    python test_items.py
    # etc.
    ```

## Project Structure

-   `includes/`: Contains the main `homebox_api.py` class file.
-   `examples/`: Contains individual Python scripts demonstrating how to use the `HomeboxAPI` for different types of API calls.
-   `requirements.txt`: Lists the necessary Python libraries.
-   `README.md`: This file.

## Contributing

Contributions are welcome! If you find bugs, want to add features, or improve the documentation, feel free to open an issue or submit a pull request.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature`).
3.  Make your changes.
4.  Commit your changes (`git commit -am 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature`).
6.  Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. (Note: You should create a LICENSE file in your repository if you choose this license).

## Acknowledgements

-   Thanks to **Hayden Kot** (hay-kot) for creating the original [Homebox](https://github.com/hay-kot/homebox) project and the documentation at [hay-kot.github.io/homebox](https://hay-kot.github.io/homebox).
-   Thanks to **Sysadmins Media** (sysadminsmedia) for continuing the development of the project at [github.com/sysadminsmedia/homebox](https://github.com/sysadminsmedia/homebox).
-   Thanks to the authors of the `requests` and `keyring` Python libraries.
