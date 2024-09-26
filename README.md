# kobo-project-metadata

This project fetches metadata of all projects from a project views given to specific users and exports it to an Excel file.

### Files

- **config.json**: Contains the API configuration details such as the token, base URL, and project view UID.
- **metadata.py**: The main script that fetches and processes the project metadata.
- **requirements.txt**: Lists the Python dependencies required to run the project.

## Setup Instructions

1. **Clone the repository**:

    ```bash
    git clone https://github.com/JamesLeonDufour/kobo-project-metadata.git
    ```

2. **Navigate to the project directory**:

    ```bash
    cd repository-name
    ```

3. **Install dependencies**:

    Install the required Python packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the config file**:

    In `config.json`, provide your API token, base URL, and project view UID:

    ```json
    {
      "KOBO_API_TOKEN": "YOURTOKENHERE",
      "BASE_URL": "https://kobo.XXXX.org/",
      "PROJECT_VIEW_UID": "PROJECT_VIEW_UID"
    }
    ```

## Running the Script

To fetch the metadata and export it to an Excel file:

```bash
python metadata.py
