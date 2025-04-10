# Guss The FCC BDC API 

This Python package provides an easy-to-use interface for interacting with the Federal 
Communications Commission (FCC) Broadband Data Collection (BDC) API. It allows users to
programmatically download fixed and mobile broadband service coverage data, including availability, speeds,
providers, and other relevant information for various states in the United States.

## Features

- Retrieve broadband availability data
- Access broadband service details by state
- Query broadband speeds, technologies, and providers
- Fetch data as GIS geopackage or SHP format
- Easy-to-use functions to interact with the FCC's BDC API

## Requirements

- Python 3.6 or higher
- Requests library 
- Pandas
- python-dotenv
  
## Installation

### 1. Download Guss
Pull Guss repository or download and extract the zip folder to your desired project directory

### 2. Create a Virtual Environment
Navigate to your project directory in your terminal. Then, run the following command to create a new virtual environment:

```
python -m venv venv
```
- venv is the name of the virtual environment folder. You can replace it with any name you prefer, but venv is commonly used.
- This command will create a folder called venv in your project directory containing the Python environment.

### 3. Activate the Virtual Environment
After creating the virtual environment, you need to activate it:

#### On macOS/Linux:
```
source venv/bin/activate
```
#### On Windows:
```
venv\Scripts\activate
```
Once activated, you’ll notice the environment name (e.g., (venv)) appears in the terminal prompt, indicating that the virtual environment is active.

### 4. Install Dependencies from requirements.txt
Now, with the virtual environment activated, you can install the required dependencies listed in your requirements.txt file.

Ensure that you have a requirements.txt file in your project folder, and that it contains the necessary dependencies

To install the dependencies, run:

```
pip install -r requirements.txt
```

## Usage

### create a .env file in the project root directory
In the root directory of your project, create a new file named .env.

### Add the following content to the .env file:
This file will store your credentials and configuration settings, such as the API credentials and base URL. 
To get your API credentials please visit: https://bdc.fcc.gov/ register to create an account to get your
username and hash code (api key) which you can copy and paste in the .env file using the structure provided below:
```

credentials = {'USERNAME':'your.email@domain.com', 'HASH_VALUE':'your registerd api ke'}
BASE_URL = 'https://broadbandmap.fcc.gov'
```
---

### Running `main.py` in VSCode Interpreter

Follow these steps to run a `main.py` Python file using the Visual Studio Code (VSCode) interpreter or any python 
interpreter of you choice. Example below is for Vscode only

#### 1. **Open VSCode**

Launch Visual Studio Code.

---

#### 2. **Install the Python Extension for VSCode**

If you haven't already installed the Python extension, follow these steps:

1. In the Activity Bar on the left side of the window, click on the **Extensions** icon (or press `Ctrl+Shift+X`).
2. In the search box, type **Python**.
3. Click the **Install** button for the extension provided by Microsoft.
   
---

#### 3. **Open Your Project Folder**

To open your project folder in VSCode:

1. Click on **File** in the top menu.
2. Select **Open Folder...**.
3. Navigate to the folder where your `main.py` file is located and select it.

---

#### 4. **Select the Python Interpreter**

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) to open the Command Palette.
2. Type **Python: Select Interpreter** and select it.
3. Choose the Python interpreter you want to use (make sure it’s the one where your dependencies are installed,
   such as your virtual environment or global Python installation).

---

#### 5. **Open `main.py`**

1. In the **Explorer** pane on the left side of VSCode, navigate to the folder where your `main.py` file is located.
2. Click on the `main.py` file to open it in the editor.
3. Make adjustments to the query parameters

---

#### 6. **Run the `main.py` File**

You have several options to run your Python file:

##### Option 1: Using the Play Button

1. After opening `main.py`, you should see a **Run** icon (a green triangle) in the top-right corner of the VSCode editor.
2. Click the **Run** button to execute the script. The output will be shown in the **Terminal** section at the bottom.

##### Option 2: Using the Integrated Terminal

1. Open the integrated terminal in VSCode by clicking **Terminal** in the top menu and selecting **New Terminal**,
   or press `` Ctrl + ` `` (backtick).
2. In the terminal, type the following command:

   ```bash
   python main.py

# main.py Usage Instructions

The function accepts various parameters to customize the query, enabling flexibility and control over the data retrieved.

### Parameters

- **`run`**: `bool`
  - **Description**: A boolean flag that indicates whether the function should run or not.
  - **Values**:
    - `True`: Run the function.
    - `False`: Dry run (for testing or simulation purposes).
  
- **`as_of_date`**: `string`
  - **Description**: A required date parameter that specifies the reference date for the data in `YYYY-MM-DD` format.
  - **Example**: `"2024-12-01"`

- **`provider_id_list`**: `list`
  - **Description**: A list of unique identifiers for the service provider(s) you wish to query.
  - If querying all providers, use `["ALL"]` to select all/any providers.
  - **Example**: `["130077", "130403"]` or `["ALL"]`
    

- **`state_fips_list`**: `list`
  - **Description**: A list of 2-digit FIPS codes for the states or territories you want to include in the query. The FIPS code should be included with a leading zero. 
  - **Options**:
    - If querying specific states/territories, provide the list of FIPS codes (e.g., `["01", "06"]` for Alabama and California).
    - If querying all FIPS codes, use `["ALL"]` to select all states/territories.
  - **Example**: `["01", "06"] or ["ALL"]`

- **`technology_list`**: `list`
  - **Description**: A list of technology codes used by the service provider to report service availability. Each code corresponds to a specific technology.
  - **Options**:
    - `300`: 3G
    - `400`: LTE
    - `500`: 5G-NR
  - **Example**: `[300, 400, 500]`

- **`technology_type`**: `string`
  - **Description**: The type of technology being queried. The available options are:
    - `'Mobile Broadband'`
    - `'Mobile Voice'`
  - **Example**: `"Mobile Broadband"`

- **`subcategory`**: `string`
  - **Description**: A string to specify the subcategory of coverage data. Valid options are:
    - `'Hexagon Coverage'`
    - `'Raw Coverage'`
  - **Example**: `"Hexagon Coverage"`

- **`FiveG_speed_tier_list`**: `list`
  - **Description**: A list of 5G speed tiers to filter the data. The format is `"download_speed/upload_speed"`.
  - **Example**: `["35/3", "7/1"]`

- **`gis_type`**: `string`
  - **Description**: The type of GIS file format in which the data should be returned. Valid options are:
    - `"SHP"`: Shapefile format.
    - `"GPKG"`: GeoPackage format.
  - **Example**: `"SHP"`

---

### Example Usage in main.py

```python

from bin.download_mb_coverage import download_provider_state_coverage_data
from bin.download_fixed_coverage import download_location_fixed_coverage_by_state
from bin.download_challenge_data import download_challenge_data
from guss.gussErrors import GussExceptions





if __name__ == '__main__':

    try:

        # hexagon coverage shp
        download_provider_state_coverage_data(run=True, 
                                              as_of_date="2024-06-30",
                                              provider_id_list=['all'],
                                              state_fips_list=["11"],
                                              technology_list=[400, 300, 500],
                                              technology_type="Mobile Broadband",
                                              subcategory='Hexagon Coverage',
                                              fiveG_speed_tier_list=['7/1', '35/3'],
                                              gis_type="shp")

        # raw coverage gpkg
        download_provider_state_coverage_data(run=False, 
                                              as_of_date="2024-06-30",
                                              provider_id_list=['130077', '130403',
                                                                '131425', '131310'],
                                              state_fips_list=["11"],
                                              technology_list=[400, 300, 500],
                                              technology_type="Mobile Broadband",
                                              subcategory='Raw Coverage',
                                              fiveG_speed_tier_list=['7/1', '35/3'],
                                              gis_type="gpkg")

        # fixed coverage csv
        download_location_fixed_coverage_by_state(run=True,
                                                  as_of_date='2024-06-30',
                                                  provider_id_list=['all'],
                                                  state_fips_list=['11'],
                                                  technology_list=[10,40,50,60,61,70,71,72,0]
                                                  )

        download_challenge_data(run=True,
                               as_of_date='2024-06-30',
                               category='Mobile Challenge - Resolved',
                               state_fips_list=["all"])



    except GussExceptions as e:
        print(f"error: {e}")

```
#### The code above will download 3 different broadband coverage files for any providers serving in Washington D.C.

1. Mobile broadband coverage in Washington D.C. represented as h3 hexagon in a shapefile format.
2. Raw mobile broadband coverage in Washington D.C. in a GeoPackage (gpkg) format.
3. Fixed broadband coverage in Washington D.C. which is always outputed as CSV.


The output files will be outputed in the ~/data/output/{file_format_type} folder.

---
### Notes
- Ensure that the as_of_date is correctly formatted as 'YYYY-MM-DD' to avoid errors. There are only two 2 annually filings per year. so please indicate either June 30 or December 31 for a given year. 
- The state_fips_list or provider_id can include ["ALL"] if you need data for all U.S. states and territories or provider ids. **Do not include 'ALL'** if individual states are desired. Same **Rule** applies to provider_id_list parameter.
- The FiveG_speed_tier_list is used for filtering 5G data based on download/upload speeds. Provide the values in the format "download_speed/upload_speed".
- The gis_type option allows you to choose between Shapefile (SHP) or GeoPackage (GPKG) formats for geographic data
