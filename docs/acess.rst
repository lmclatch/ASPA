Accessing the Data
====================

Introduction
------------
A guide to accessing the processed data. The tables are posted to an object endpoint space through Digital Ocean and are publically accessible.

Data Endpoint URLs ~

https://try-test.sfo3.digitaloceanspaces.com/Final_Aggregated_Data.csv

https://try-test.sfo3.digitaloceanspaces.com/WaterSources.csv

https://try-test.sfo3.digitaloceanspaces.com/Sites.csv 

https://try-test.sfo3.digitaloceanspaces.com/Variables.csv 

https://try-test.sfo3.digitaloceanspaces.com/Organization.csv 
 


Required Libraries
------------------

To access the endpoints within Python, you'll need this Python library

- **Requests**: A simple and elegant HTTP library for Python, perfect for making HTTP requests to your endpoints.

You can install the `requests` library using pip:

bash
pip install requests

Here is a basic GET request code snippet:

import requests

url = "https://your-endpoint-space-url.com/api/resource"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("Data retrieved:", data)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")



Accessible Tables
-----------------
There are multiple .CSVs available for download. Following are high-level descriptions.


Final Aggregated Data
----------------------
This is the main table with the required water use data
Final_Aggregated_Data.csv

SiteNativeID: Unique identifier code / ID used by the data provider to distinguish the data site in the source data set.

Example: Aasu		


BeneficialUseCategory: The use category for which the water is being allocated to

Example: Commercial

			
TimeframeStart: The datetime start of the recorded usage

Example: 2021-12-01


TimeframeEnd: The datetime end of the recorded usage

Example: 2021-12-31


Amount: Usage of water reported for the specific time frame, village, and use.

Example: 5008.0


VariableCV: This is a high-level variable used for site-specific water data.

Example: Consumptive Use


ReportYear: Year associated with data
	
Example: 2021


URL ~

https://try-test.sfo3.digitaloceanspaces.com/Final_Aggregated_Data.csv





The following tables are specified metadata tables used to support the main data table. 
Accompanied by a description of American Samoan specific examples of what each field corresponds to.

Sites
-------------
Sites.csv

SiteNativeID: Unique identifier code / ID used by the data provider to distinguish the data site in the source data set.

Example: Pago Pago Village


Latitude: Latitude coordinate of the data site.

Example: -14.274006


Longitude: Longitude coordinate of the data site.

Example: -170.70403


SiteTypeCV: The high level description of the site type recognized by the data provider 

Example: Village (aggregation of individual water meter use within each village boundary) 


URL ~ 

https://try-test.sfo3.digitaloceanspaces.com/Sites.csv

Note: This also contains site-specific well data.

Organization
------------
Organization.csv

OrganizationName: Name corresponding to unique organization and the organization ID

Example: American Samoa Power Authority



OrganizationContactEmail: Email information for organization contact person.

Example: wei@aspower.com


OrganizationContactName: Name of the contact person

Example: Wei Hua-Hsien


OrganizationPhoneNumber: The organization's phone number for general information

Example: 1 (684) 699-1234


OrganizationWebsite: A hyperlink back to the organization's website

Example: https://www.aspower.com

StateCV:Two digit state abbreviation where the organization is

Example: AS


OrganizationPurview: A description of the purview of the agency (i.e. water rights, consumptive use, etc.)

Example: water utility, production, delivery, consumptive use 


URL ~

https://try-test.sfo3.digitaloceanspaces.com/Organization.csv

Variables
----------
Variables.csv

VariableCV: This is a high-level variable used for site-specific water data.

Example: Consumptive Use


AmountUnitCV: Unit of the site-specific  amount.

Example: Gallons


AggregationIntervalUnitCV: The aggregation unit (e.g., day ,month, year).

Example: Month



URL ~

https://try-test.sfo3.digitaloceanspaces.com/Variables.csv

Water Sources
--------------
WaterSources.csv


WaterSourceTypeCV: the high level description of the water source type 

Example: Groundwater

URL ~


https://try-test.sfo3.digitaloceanspaces.com/WaterSources.csv


