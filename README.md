# Corporate Database Builder

## Description

Impact Radar is a corporate database builder which is built in Python to automate the creation and management of corporate databases.  Utilizing tools like Selenium, it streamlines data collection and organization processes, making it efficient for users to build comprehensive corporate databases.​

### Features:

- Automated data collection using Selenium.​
- Structured organization of corporate data.​
- Easy setup with a virtual environment.​

## Commit History (Latest Major Updates)

- **c6848c0** [UPDATE 8.32.3] Extracting the liquidator of a global business company from the corporate registry.
- **696a009** [UPDATE 8.32.2] Extracting the data from the portable document file version of the corporate registry based on the status of the file generation as well as on the dataset for a foreign domestic company.
- **9a691f9** [UPDATE 8.31.3] Extracting the affidavits of the liquidator of a global business company from the corporate registry.
- **04b3f11** [UPDATE 8.31.2] Extracting the data for the financial summaries from the result set.
- **5274595** [UPDATE 8.31.1] Checking if the date is in the correct format.
- **9e8f144** [UPDATE 8.26.3] Curating and sanitizing the names of office bearers by filtering out invalid names and formatting valid ones.
- **6ef3f97** [UPDATE 8.26.2] This module provides the Database_Handler class, which is responsible for handling database operations such as retrieving, inserting, updating, and deleting data in a MySQL database.
- **1919017** [UPDATE 8.26.1] Standardizing the formatting of office bearer positions.
- **e6912c2** [UPDATE 8.25.2] Assuring that the environment is deactivated after processing data
- **af1097d** [UPDATE 8.24.5] Replacing placeholder business names with their corresponding company names.

For a full list of updates, check the [commit history](https://github.com/DONALDBZR/Corporate_Dabase_Builder/commits).


## Installation & Setup

### Prerequisites:

Ensure you have the following installed on your system:

- Python 3.10
- pip (Python package installer)​
- Google Chrome + ChromeDriver
- Git

### Setup Steps:

1. Clone the repository:​

```bash
git clone https://github.com/DONALDBZR/Corporate_Dabase_Builder.git
cd Corporate_Dabase_Builder
```

2. Create a virtual environment:​

```bash
python3 -m venv ./venv
```

3. Activate the virtual environment:​

```bash
source ./venv/bin/activate
```

4. Install required dependencies:​

```bash
pip3 install -r requirements.txt
```

5. Configure the required ENV file for the application to be able to communicate efficiently.

## Usage

After setting up the environment and installing dependencies, you can run the application to start building your corporate database.​  The data extraction pipeline is divided into four shell scripts, each handling a specific step of the corporate data processing workflow.  Execute them sequentially from the `Auto/` directory:

1. **Index registered companies**  

```bash
./fincorp_module1.sh
```

This script indexes all companies registered by fetching available corporate entries.

2. **Download corporate registries**

```bash
./fincorp_module2.sh
```

Downloads the official registry documents for each indexed company.

3. **Extract data from registries**

```bash
./fincorp_module3.sh
```

Parses the downloaded documents to extract structured data.

4. **Curate and clean extracted data**

```bash
./fincorp.data_curation.sh
```

Cleans, formats, and consolidates the extracted data for final use.

## Dependencies

This project requires the following Python packages:

- **mysql-connector-python** – to connect and interact with MySQL databases.
- **selenium** – for automating browser interactions during data collection.
- **webdriver-manager** – to manage browser drivers automatically for Selenium.
- **pdfminer.six** – for extracting data from PDF-based corporate registries.
- **msal** – Microsoft's Authentication Library for secure access via OAuth2.

Install all dependencies using:

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the **CeCILL License**.  You are free to use, modify, and distribute the code, but you must ensure that any derivative works:

- Clearly differ in name, branding, and user-facing identity.
- Do not replicate the original project's look, behavior, or branding.

For full details, see the [LICENSE](LICENSE) file in this repository.

> The CeCILL License is designed to comply with French law and is similar to the GNU GPL but adapted for legal compatibility.

## Contact

For issues, suggestions, or collaboration inquiries, please reach out via the following channels:

- GitHub Issues: [https://github.com/DONALDBZR/Corporate_Dabase_Builder/issues](https://github.com/DONALDBZR/Corporate_Dabase_Builder/issues)
- Email: andygaspard@hotmail.com
- LinkedIn: [https://www.linkedin.com/in/andy-gaspard/](https://www.linkedin.com/in/andy-gaspard/)

For more information, please refer to the GitHub repository.
