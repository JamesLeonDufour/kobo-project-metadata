import json
import requests
import pandas as pd
import time

def load_config(config_file='config.json'):
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading config file: {e}")
        return None

def fetch_all_assets(api_url, headers):
    assets = []
    while api_url:
        try:
            print(f"Fetching data from: {api_url}")
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()

            # Collect assets
            batch = data.get('results', [])
            assets.extend(batch)
            print(f"Retrieved {len(batch)} assets. Total so far: {len(assets)}")

            # Get the next page
            api_url = data.get('next')
            time.sleep(0.5)  # Pause between requests
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            break
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break
    return assets

def flatten_asset(asset):
    flat_asset = {}

    def flatten_dict(d, parent_key=''):
        for k, v in d.items():
            new_key = f"{parent_key}_{k}" if parent_key else k
            if isinstance(v, dict):
                flatten_dict(v, new_key)
            elif isinstance(v, list):
                if all(isinstance(item, dict) for item in v):
                    for i, item in enumerate(v):
                        flatten_dict(item, f"{new_key}_{i}")
                else:
                    flat_asset[new_key] = ', '.join(map(str, v)) if v else None
            else:
                flat_asset[new_key] = v

    flatten_dict(asset)
    return flat_asset

def main():
    # ============================
    # == Load Configuration File ==
    # ============================
    config = load_config('config.json')
    if not config:
        print("Configuration load failed. Exiting.")
        return

    # Retrieve the API token, base URL, and project view UID from config
    api_token = config.get('KOBO_API_TOKEN')
    base_url = config.get('BASE_URL')
    project_view_uid = config.get('PROJECT_VIEW_UID')

    if not all([api_token, base_url, project_view_uid]):
        print("Missing required configuration values. Please check your config.json file.")
        return

    # ============================
    # == Configuration Section ==
    # ============================


    initial_api_url = f"{base_url}/api/v2/project-views/{project_view_uid}/assets/"

    # Set up the headers with the API token
    headers = {
        'Authorization': f'Token {api_token}',
        'Accept': 'application/json',
    }

    # ============================
    # == Data Fetching Section ==
    # ============================

    # Fetch all assets
    assets = fetch_all_assets(initial_api_url, headers)

    if not assets:
        print("No assets retrieved. Exiting.")
        return

    # ================================
    # == Data Processing Section ==
    # ================================

    # Flatten each asset
    print("Flattening asset data...")
    flattened_assets = [flatten_asset(asset) for asset in assets]

    # Create a DataFrame
    print("Creating DataFrame...")
    try:
        df = pd.DataFrame(flattened_assets)
    except Exception as e:
        print(f"Failed to create DataFrame: {e}")
        return

    # ================================
    # == Excel Export Section ==
    # ================================

    # Export to Excel
    output_file = "project_metadata.xlsx"
    print(f"Exporting data to {output_file}...")
    try:
        df.to_excel(output_file, index=False, engine='openpyxl')
        print("Export completed successfully!")
    except Exception as e:
        print(f"Failed to export data to Excel: {e}")

if __name__ == "__main__":
    main()
