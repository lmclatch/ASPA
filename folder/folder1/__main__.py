#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 08:12:37 2024

@author: lizamclatchy
"""

import os
import re
import pandas as pd
import requests
import boto3
from io import BytesIO, StringIO

#####---------- READING GITHUB PRIV REPO ---- ######
def get_xlsx_files_from_repo(repo_url, token):
    headers = {
        'Authorization': f'token {token}'
    }
    response = requests.get(repo_url, headers=headers)
    if response.status_code == 200:
        items = response.json()
        xlsx_files = []
        for item in items:
            if item['type'] == 'file' and item['name'].endswith('.xlsx'):
                xlsx_files.append(item['download_url'])
            elif item['type'] == 'dir':
                xlsx_files += get_xlsx_files_from_repo(item['url'], token)
        return xlsx_files
    else:
        raise ValueError(f"Failed to fetch repository contents: {response.status_code}")


def read_xlsx_files(xlsx_files, token):
    headers = {
        'Authorization': f'token {token}'
    }
    dataframes = []
    for file_url in xlsx_files:
        response = requests.get(file_url, headers=headers)
        if response.status_code == 200:
            df = pd.read_excel(BytesIO(response.content))
            dataframes.append(df)
        else:
            raise ValueError(f"Failed to download file: {response.status_code}")
    return dataframes

#--------------------------------------------------------------------------------------------#
#MAKE DATAFRAMES/COMBINE
#--------------------------------------------------------------------------------------------#
# Combine all dataframes into one big dataframe
def combine_dataframes(dataframes):
    cs_data = pd.concat(dataframes, ignore_index=True)
    return cs_data

#--------------------------------------------------------------------------------------------#
#CLEAN DATA
#--------------------------------------------------------------------------------------------#
#data cleaning starts
def clean_data(cs_data):
    # Ensure column names are strings before stripping
    cs_data.columns = [str(col).strip() for col in cs_data.columns]
    cs_data = cs_data[cs_data['LOSADD'].notnull()]
    cs_data['Usage'] = cs_data['Usage'].astype(str).str.replace(" ", "")
    cs_data['Usage'] = cs_data['Usage'].str.replace("-", "0")
    cs_data['Usage'] = cs_data['Usage'].str.replace(",", "")
    cs_data['Usage'] = pd.to_numeric(cs_data['Usage'], errors='coerce')
    pattern = re.compile(r'ASPA:WATER\s*\d+')
    cs_data['SiteTypeCV'] = cs_data['NAME'].apply(lambda x: 'Production' if pattern.match(x) else 'Unspecified')
    return cs_data

def map_rsp_to_beneficial_use_category(cs_data):
    rsp_mapping = {
        'RES': 'Domestic',
        'IND': 'Industrial',
        'LGS': 'Industrial',
        'SGS': 'Commercial',
        'ASG': 'Commercial'
    }
    
    # Compile the pattern
    pattern = re.compile(r'ASPA:WATER\s*\d+')
    
    # Apply the mapping
    cs_data['BeneficialUseCategory'] = cs_data['RSP'].map(rsp_mapping)
    
    # Update the BeneficialUseCategory to 'Well' where the pattern matches
    cs_data['BeneficialUseCategory'] = cs_data.apply(
        lambda row: 'Production' if pattern.match(row['NAME']) else row['BeneficialUseCategory'],
        axis=1
    )
    
    return cs_data

#QA/QC DATA
def qa_qc_checks(cs_data):
    # Ensure TimeframeStart and Month columns exist in cs_data
    cs_data['TimeframeStart'] = pd.to_datetime(cs_data['Rdg Date']) - pd.to_timedelta(cs_data['Days of Usage'], unit='D')
    cs_data['Month'] = cs_data['TimeframeStart'].dt.to_period('M').astype(str)
    
    # Calculate the mean and standard deviation for each LOSADD and BeneficialUseCategory
    cs_data['Mean'] = cs_data.groupby(['LOSADD', 'BeneficialUseCategory'])['Usage'].transform('mean')
    cs_data['StdDev'] = cs_data.groupby(['LOSADD', 'BeneficialUseCategory'])['Usage'].transform('std')
    cs_data['UpperLimit'] = cs_data['Mean'] + 3 * cs_data['StdDev']
    cs_data['LowerLimit'] = cs_data['Mean'] - 3 * cs_data['StdDev']
    
    # Debugging
    print("QA Data with Limits Preview:")
    print(cs_data.head())
    cs_data.to_csv('cs_data_with_limits.csv', index=False)
    
    # Filtering data based on the limits
    initial_count = len(cs_data)
    filtered_data = cs_data[(cs_data['Usage'] >= cs_data['LowerLimit']) & (cs_data['Usage'] <= cs_data['UpperLimit'])]
    filtered_count = len(filtered_data)
    
    # Print the number of data points filtered out
    print(f"Filtered out {initial_count - filtered_count} data points out of {initial_count}")
    
    # Dropping columns used for QA/QC only if they exist
    columns_to_drop = ['Mean', 'StdDev', 'UpperLimit', 'LowerLimit']
    existing_columns = [col for col in columns_to_drop if col in filtered_data.columns]
    filtered_data = filtered_data.drop(columns=existing_columns)
    
    # Debugging
    print("Filtered Data Preview:")
    print(filtered_data.head())
    filtered_data.to_csv('filtered_data.csv', index=False)
    
    return filtered_data



village_key = {
    'AASU': "Aasu",
    'AASU FOU': 'Aasu',
    'AFAO': 'Afao',
    'AFONO': 'Afono',
    'AGUGULU': 'Agugulu',
    'ALAO': 'Alao',
    'ALEGA': 'Alega',
    'ALOFAU': 'Alofau',
    'AMALUIA': 'Amaluia',
    'AMANAVE': 'Amanave',
    'AMAUA': 'Amaua',
    'AMOULI': 'Amouli',
    'AOA': 'Aoa',
    'AOLOAU': 'Aoloau',
    'ASILI': 'Asili',
    'ATAULOMA': 'Afao',
    'ATUU': 'Atuu',
    'AUA': 'Aua',
    'AUASI': 'Auasi',
    'AUNUU': 'Aunuu',
    'AUTO': 'Auto',
    'AVAIO': 'Avaio',
    'FAGAALU': 'Fagaalu',
    'FAGAITUA': 'Fagaitua',
    'FAGALII': 'Fagalii',
    'FAGAMALO': 'Fagamalo',
    'FAGANEANEA': 'Faganeanea',
    'FAGASA': 'Fagasa',
    'FAGATOGO': 'Fagatogo',
    'FAILOLO': 'Failolo',
    'FALEASAO': 'Tau',
    'FALENIU': 'Faleniu',
    'FATUMAFUTI': 'Fatumafuti',
    'FITIUTA': 'Tau',
    'FOGAGOGO': 'Iliili', 
    'FUTIGA': 'Futiga',
    'Fagaalu': 'Fagaalu',
    'GATAIVAI': 'Utulei',
    'ILIILI': 'Iliili',
    'LAULII': 'Laulii',
    'LELOALOA': 'Leloaloa',
    'LEONE': 'Leone',
    'MALAEIMI': 'Malaeimi',
    'MALAELOA': 'Malaeloa',
    'MALALOA': 'Fagatogo',
    'MALOATA': 'Maloata',
    'MAPUSAGA': 'Mapusagafou',
    'MAPUSAGA FOU': 'Mapusagafou',
    'MASAUSI': 'Masausi',
    'MASEFAU': 'Masefau',
    'MATUU': 'Matuu',
    'MESEPA': 'Mesepa',
    'NUA': 'Nua',
    'NUUULI': 'Nuuuli',
    'OFU': 'Ofu',
    'OLOSEGA': 'Olosega',
    'ONENOA': 'Onenoa',
    'PAGAI': 'Pagai',
    'PAGO PAGO': 'Pago Pago',
    'PAVAIAI': 'Pavaiai',
    'POLOA': 'Poloa',
    'SAILELE': 'Sailele',
    'SATALA': 'Pago Pago',
    'SEETAGA': 'Seetaga',
    'TAFETA': 'Mapusagafou',
    'TAFUNA': 'Tafuna',
    'TAPUTIMU': 'Taputimu',
    'TAU': 'Tau',
    'TULA': 'Tula',
    'UTULEI': 'Utulei',
    'UTUMEA': 'Utumea West',
    'UTUMEA-SASAE': 'Utumea East',
    'UTUSIA': 'Fagaitua',
    'VAILOA': 'Vailoatai',
    'VAITOGI': 'Vaitogi',
    'VATIA': 'Vatia',
    'Vaitogi': 'Vaitogi'
}

def transform_to_site_specific_format(cs_data):
   
    
   transformed_data = pd.DataFrame(columns=['SiteNativeID','VariableSpecificUUID', 'Amount', 'BeneficialUseCategory', 'TimeframeStart', 'TimeframeEnd'])
    
   # Map the villages using SiteUUID
   transformed_data['SiteNativeID'] = cs_data['LOSADD'].map(village_key)
   transformed_data['VariableSpecificUUID'] = 'UTssps_V3'
   transformed_data['Amount'] = cs_data['Usage']
   transformed_data['BeneficialUseCategory'] = cs_data['BeneficialUseCategory']

   # Calculate TimeframeStart and TimeframeEnd
   transformed_data['TimeframeStart'] = pd.to_datetime(cs_data['Rdg Date']) - pd.to_timedelta(cs_data['Days of Usage'], unit='D')
   transformed_data['TimeframeEnd'] = pd.to_datetime(cs_data['Rdg Date'])
   
   transformed_data['Month'] = transformed_data['TimeframeStart'].dt.to_period('M')

   # Aggregate usage per month, village, and beneficial use category
   aggregated_data = transformed_data.groupby(['SiteNativeID', 'Month', 'BeneficialUseCategory'])['Amount'].sum().reset_index()

   # Convert 'Month' back to datetime and calculate TimeframeStart and TimeframeEnd for the final format
   aggregated_data['TimeframeStart'] = aggregated_data['Month'].dt.to_timestamp()
   aggregated_data['TimeframeEnd'] = aggregated_data['TimeframeStart'] + pd.offsets.MonthEnd(0)

   # Adjust the column names to match the example output
   aggregated_data = aggregated_data[['SiteNativeID', 'BeneficialUseCategory', 'TimeframeStart', 'TimeframeEnd', 'Amount']]
   aggregated_data['VariableCV'] = aggregated_data['BeneficialUseCategory'].apply(
    lambda x: 'Withdrawal' if x == 'Production' else 'Consumptive Use'
   )
   aggregated_data['ReportYear'] = aggregated_data['TimeframeStart'].dt.year

   # Sort the data for better readability
   aggregated_data = aggregated_data.sort_values(by=['SiteNativeID', 'TimeframeStart', 'BeneficialUseCategory'])
   
   return aggregated_data

#--------------------------------------------------------------------------------------------#
#WELL DATA 
#--------------------------------------------------------------------------------------------#
def well_data(well_data_url, cs_data, village_key):
    # Fetch the GitHub token from environment variables
    access_token = os.getenv('GITHUB_TOKEN')

    # Headers for GitHub API access
    headers = {'Authorization': f'token {access_token}'}

    # Fetch the well data from the GitHub URL
    response_well = requests.get(well_data_url, headers=headers)
    response_well.raise_for_status()  # Ensure we notice bad responses
    well_data = pd.read_csv(StringIO(response_well.text))
    
    # Define the pattern to match 'ASPA:WATER' followed by digits
    pattern = re.compile(r'ASPA:WATER\s*(\d+)')

    # Extract well numbers from 'NAME' in cs_data
    cs_data['Well_Number'] = cs_data['NAME'].apply(lambda x: pattern.findall(x)[0] if pattern.findall(x) else None)

    # Ensure Well_Number is of the same type for matching
    cs_data['Well_Number'] = cs_data['Well_Number'].astype(str)
    well_data['Well_Number'] = well_data['Well #'].astype(str)
    
    # Create well_data_frame containing the desired columns
    well_data_frame = well_data[['Village', 'Well_Number', 'Lat', 'Long']].dropna(subset=['Well_Number'])
    well_data_frame['SiteNativeID'] = well_data_frame.apply(lambda row: f"{row['Village']}_Well_{row['Well_Number']}", axis=1)
    well_data_frame['SiteTypeCV'] = 'Withdrawal'
    well_data_frame = well_data_frame.drop_duplicates()
    well_data_frame = well_data_frame.drop(columns=['Well_Number', 'Village'])

    # Calculate TimeframeStart and TimeframeEnd
    cs_data['TimeframeStart'] = pd.to_datetime(cs_data['Rdg Date']) - pd.to_timedelta(cs_data['Days of Usage'], unit='D')
    cs_data['TimeframeEnd'] = pd.to_datetime(cs_data['Rdg Date'])

    # Filter cs_data to include only matched wells
    matched_well_data = cs_data[cs_data['Well_Number'].isin(well_data['Well_Number'])]

    # Select the relevant columns for matched_well_data DataFrame
    matched_well_data = matched_well_data[['Well_Number', 'TimeframeStart', 'TimeframeEnd', 'Usage', 'NAME', 'BeneficialUseCategory', 'LOSADD']]

    # Map the villages using LOSADD
    matched_well_data['Village'] = matched_well_data['LOSADD'].map(village_key)
    
    # Assign SiteUUID to be the well name
    matched_well_data['SiteNativeID'] = matched_well_data.apply(lambda row: f"{row['Village']}_Well_{row['Well_Number']}", axis=1)
   
    
    # Create transformed_well_data similar to your workflow
    transformed_well_data = pd.DataFrame(columns=['SiteNativeID', 'VariableSpecificUUID', 'Amount', 'BeneficialUseCategory', 'TimeframeStart', 'TimeframeEnd'])
    transformed_well_data['SiteNativeID'] = matched_well_data['SiteNativeID']
    transformed_well_data['VariableSpecificUUID'] = 'UTssps_V3'
    transformed_well_data['Amount'] = matched_well_data['Usage']
    transformed_well_data['BeneficialUseCategory'] = matched_well_data['BeneficialUseCategory']
    transformed_well_data['TimeframeStart'] = matched_well_data['TimeframeStart']
    transformed_well_data['TimeframeEnd'] = matched_well_data['TimeframeEnd']

    # Aggregate usage per month and beneficial use category
    transformed_well_data['Month'] = transformed_well_data['TimeframeStart'].dt.to_period('M')
    # Filter out data points exceeding 17,520,000 gallons per month (max well is 400 gpm)
    max_threshold = 17520000
    filtered_out_count = transformed_well_data[transformed_well_data['Amount'] > max_threshold].shape[0]
    transformed_well_data = transformed_well_data[transformed_well_data['Amount'] <= max_threshold]

    # Print the number of filtered data points
    print(f"Filtered out {filtered_out_count} data points exceeding {max_threshold} gallons per month.")
    
    aggregated_well_data = transformed_well_data.groupby(['SiteNativeID', 'Month', 'BeneficialUseCategory'])['Amount'].sum().reset_index()

    # Convert 'Month' back to datetime and calculate TimeframeStart and TimeframeEnd for the final format
    aggregated_well_data['TimeframeStart'] = aggregated_well_data['Month'].dt.to_timestamp()
    aggregated_well_data['TimeframeEnd'] = aggregated_well_data['TimeframeStart'] + pd.offsets.MonthEnd(0)

    # Adjust the column names to match the example output
    aggregated_well_data = aggregated_well_data[['SiteNativeID', 'BeneficialUseCategory', 'TimeframeStart', 'TimeframeEnd', 'Amount']]
    aggregated_well_data['VariableCV'] = aggregated_well_data['BeneficialUseCategory'].apply(
        lambda x: 'Withdrawal' if x == 'Production' else 'Consumptive Use'
    )
    aggregated_well_data['ReportYear'] = aggregated_well_data['TimeframeStart'].dt.year

    # Sort the data for better readability
    aggregated_well_data = aggregated_well_data.sort_values(by=['SiteNativeID', 'TimeframeStart', 'BeneficialUseCategory'])

    return well_data_frame, aggregated_well_data
#--------------------------------------------------------------------------------------------#
#METADATA TABLE CREATIONS
#--------------------------------------------------------------------------------------------#
def organization_metadata():
    organizations_df = pd.DataFrame(columns=[
        'OrganizationName', 'OrganizationContactEmail', 'OrganizationContactName', 
        'OrganizationPhoneNumber', 'OrganizationWebsite', 'StateCV', 'OrganizationPurview'
    ])
    new_row = pd.DataFrame([{
        'OrganizationName': 'American Samoa Power Authority',
        'OrganizationContactEmail': 'wei@aspower.com',
        'OrganizationContactName': 'Wei Hua-Hsien',
        'OrganizationPhoneNumber': '1 (684) 699-1234',
        'OrganizationWebsite': 'https://www.aspower.com/',
        'StateCV': 'AS',
       ' OrganizationPurview' : 'water utility, production, delivery, consumptive use '


    }])
    organizations_df = pd.concat([organizations_df, new_row], ignore_index=True)
    return organizations_df

def variables_metadata():
    variables_df = pd.DataFrame(columns=[
        'VariableCV', 'AmountUnitCV', 'AggregationIntervalUnitCV'
    ])
    new_rows = pd.DataFrame([
        {'VariableCV': 'Consumptive Use', 'AmountUnitCV': 'Gallons', 'AggregationIntervalUnitCV': 'Month'},
        {'VariableCV': 'Withdrawal', 'AmountUnitCV': 'Gallons', 'AggregationIntervalUnitCV': 'Month'}
    ])
    variables_df = pd.concat([variables_df, new_rows], ignore_index=True)
    return variables_df

def watersources_metadata():
    watersources_df = pd.DataFrame(columns=['WaterSourceTypeCV'])
    new_row = pd.DataFrame([{'WaterSourceTypeCV': 'Groundwater'}])
    watersources_df = pd.concat([watersources_df, new_row], ignore_index=True)
    return watersources_df
    
def sites_metadata(cs_data, village_url, well_data_frame):
    # Pull from private GitHub repo
    access_token = os.getenv('GITHUB_TOKEN')
    if not access_token:
        raise ValueError("GitHub token not found in environment variables")
    
    headers = {'Authorization': f'token {access_token}'}
    
    # Load Village Data
    response_vill = requests.get(village_url, headers=headers)
    response_vill.raise_for_status()
    village_coordinates = pd.read_csv(StringIO(response_vill.text))
    
    # Transform Village Data
    village_data = pd.DataFrame()
    village_data['Lat'] = village_coordinates['Y']
    village_data['Long'] = village_coordinates['X']
    village_data['SiteNativeID'] = village_coordinates['VILLAGE']
    village_data['SiteTypeCV'] = ' Village (aggregation of individual water meter use within each village boundary) '

    
    sites_df = pd.concat([village_data, well_data_frame], ignore_index=True)
    
    return sites_df
#--------------------------------------------------------------------------------------------#
#UPLOAD TO DIGITALOCEAN SPACES
#--------------------------------------------------------------------------------------------#
def upload_to_digitalocean_spaces(file_path):
    spaces_key = os.getenv('SPACES_KEY')
    spaces_secret = os.getenv('SPACES_SECRET')
    space_name = os.getenv('SPACE_NAME')
    space_region = os.getenv('SPACE_REGION')

    if not all([spaces_key, spaces_secret, space_name, space_region]):
        raise ValueError("Missing DigitalOcean Spaces credentials or bucket information")
    
    # Configure the boto3 client
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name=space_region,
                            endpoint_url=f'https://{space_region}.digitaloceanspaces.com',
                            aws_access_key_id=spaces_key,
                            aws_secret_access_key=spaces_secret)

    # Upload the file
    with open(file_path, 'rb') as file:
        client.upload_fileobj(file, space_name, os.path.basename(file_path))

#--------------------------------------------------------------------------------------------#
#FORMAT OF DIGITALOCEAN FUNCTION
#--------------------------------------------------------------------------------------------#
def main(args):
    repo_url = args.get('repo_url', "https://api.github.com/repos/cshuler/ASPA_WUDR_Input_Files/contents/Data/2022")
    token = args.get('token', os.environ.get('GITHUB_TOKEN'))
    if not token:
        raise ValueError("GitHub token not found in environment variables or arguments")

    xlsx_files = get_xlsx_files_from_repo(repo_url, token)
    dataframes = read_xlsx_files(xlsx_files, token)
    cs_data = combine_dataframes(dataframes)
    cs_data = clean_data(cs_data)
    cs_data = map_rsp_to_beneficial_use_category(cs_data)
    cs_data = qa_qc_checks(cs_data)
    aggregated_data = transform_to_site_specific_format(cs_data)
    
    # Remove 'Well' entries from the first aggregated data
    aggregated_data = aggregated_data[aggregated_data['BeneficialUseCategory'] != 'Production']
    
    well_data_url = "https://raw.githubusercontent.com/cshuler/ASPA_WUDR_Input_Files/main/Well%20Info%20-%20Sheet1.csv"
    village_url = "https://raw.githubusercontent.com/cshuler/ASPA_WUDR_Input_Files/main/Village_Centroid_points%20-%20Sheet1.csv"
    
    well_data_frame, aggregated_well_data = well_data(well_data_url, cs_data, village_key)
    
    # Concatenate the two aggregated DataFrames
    final_aggregated_data = pd.concat([aggregated_data, aggregated_well_data], ignore_index=True)
    
    csv_file_paths = []
    
    final_aggregated_csv_path = '/tmp/Final_Aggregated_Data.csv'
    final_aggregated_data.to_csv(final_aggregated_csv_path, index=False)
    csv_file_paths.append(final_aggregated_csv_path)
    
    well_data_frame_csv_path = '/tmp/Well_Data.csv'
    well_data_frame.to_csv(well_data_frame_csv_path, index=False)
    csv_file_paths.append(well_data_frame_csv_path)
    
    sites_df = sites_metadata(cs_data, village_url, well_data_frame)
    sites_csv_path = '/tmp/Sites.csv'
    sites_df.to_csv(sites_csv_path, index=False)
    csv_file_paths.append(sites_csv_path)
    
    organizations_df = organization_metadata()
    organizations_csv_path = '/tmp/Organization.csv'
    organizations_df.to_csv(organizations_csv_path, index=False)
    csv_file_paths.append(organizations_csv_path)
    
    variables_df = variables_metadata()
    variables_csv_path = '/tmp/Variables.csv'
    variables_df.to_csv(variables_csv_path, index=False)
    csv_file_paths.append(variables_csv_path)
    
    watersources_df = watersources_metadata()
    watersources_csv_path = '/tmp/WaterSources.csv'
    watersources_df.to_csv(watersources_csv_path, index=False)
    csv_file_paths.append(watersources_csv_path)
    
    for file_path in csv_file_paths:
        upload_to_digitalocean_spaces(file_path)
    
    return {"csv_file_paths": csv_file_paths}
