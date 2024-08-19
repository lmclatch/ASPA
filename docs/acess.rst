Acessing the Data
====================

Introduction
------------
A guide to accessing the processsed data 

Accessible Tables
-----------------
The multiple .CSVs availible for download

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

Example:


AmountUnitCV: Unit of the site-specific  amount.

Example:


AggregationIntervalUnitCV: The aggregation unit (e.g., day ,month, year).

Example: 



URL ~


Water Sources
--------------
WaterSources.csv
