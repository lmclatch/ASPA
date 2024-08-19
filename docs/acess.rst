Acessing the Data
====================

Introduction
------------
A guide to accessing the processsed data 

Accessible Tables
-----------------
There are multiple .CSVs availible for download. Followed are high-level descirptions.


Final Aggregated Data
----------------------
This is the main table with the required water use data
FinalAggregatedData.csv

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



The following tables are specified metadata tables used to support the main data table. 
Accompaned by a decsiption of American Samoan specific example of what each field corresponds too.

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


Water Sources
--------------
WaterSources.csv


WaterSourceTypeCV: the high level description of the water source type 

Example: Groundwater

URL ~



