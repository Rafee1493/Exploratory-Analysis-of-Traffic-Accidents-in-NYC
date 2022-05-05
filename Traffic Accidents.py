# -*- coding: utf-8 -*-
"""
Created on Tue May  3 15:28:32 2022

@author: abdul
"""

#%% Imports

import pandas as pd


#%% Cleaning & Pickling Traffic Accident Dataset from 2012-2021

pd.set_option('display.max_columns',None)           

# Reading the NYC Motor Vehicles Collision Data

raw = pd.read_csv("Motor_Vehicle_Collisions_-_Crashes.csv")   

# Checking Column Names
      
list(raw.columns)

# Dropping Columns that won't be required for analysis

selected = raw.drop(columns=['CRASH TIME',
                             'LATITUDE',
                             'LONGITUDE',
                             'LOCATION',
                             'ON STREET NAME',
                             'CROSS STREET NAME',
                             'OFF STREET NAME', 
                             'CONTRIBUTING FACTOR VEHICLE 2',
                             'CONTRIBUTING FACTOR VEHICLE 3',
                             'CONTRIBUTING FACTOR VEHICLE 4',
                             'CONTRIBUTING FACTOR VEHICLE 5',
                             'VEHICLE TYPE CODE 2',
                             'VEHICLE TYPE CODE 3',
                             'VEHICLE TYPE CODE 4',
                             'VEHICLE TYPE CODE 5'])
# Checking Data Types

selected.dtypes

# Converting Zip Codes to str and removing the additional character that is irrelevant

selected['ZIP CODE'] = selected['ZIP CODE'].astype(str)
selected['ZIP CODE'] = selected['ZIP CODE'].str.strip('.0')

# Checking the number of missing values in Boroughs and Zip Codes

print(selected['BOROUGH'].value_counts(dropna=False))
print(selected['ZIP CODE'].value_counts(dropna=False))

# Cleaning the Date column and extracting the year, month, and a year-month column together

selected['CRASH DATE'] = selected['CRASH DATE'].str.replace(r'\D|\s','',regex=True)
selectedymd = pd.to_datetime(selected['CRASH DATE'], format="%m%d%Y")
selected['YEAR'] = selectedymd.dt.year
selected['MONTH'] = selectedymd.dt.month
selected['YEAR_MONTH'] = selectedymd.dt.to_period("M")

# Dropping the date column

selected = selected.drop(columns=['CRASH DATE'])

# Renaming columns for simplicity

selected = selected.rename(columns={'CONTRIBUTING FACTOR VEHICLE 1':'PRIMARY CONTRIBUTING FACTOR'})
selected = selected.rename(columns={'VEHICLE TYPE CODE 1' : 'PRIMARY VEHICLE TYPE'})

# Calculating total injuries and fatalities from an accident

selected['TOTAL INJURIES'] = selected['NUMBER OF PERSONS INJURED'] + selected['NUMBER OF PEDESTRIANS INJURED'] + selected['NUMBER OF CYCLIST INJURED'] + selected['NUMBER OF MOTORIST INJURED'] 
selected['TOTAL FATALITIES'] = selected['NUMBER OF PERSONS KILLED'] + selected['NUMBER OF PEDESTRIANS KILLED'] + selected['NUMBER OF CYCLIST KILLED'] + selected['NUMBER OF MOTORIST KILLED'] 

# Dropping NAN for Boroughs and Zip Codes for the Borough-wise and Zip Code wise analysis

mvaccidents = selected[selected['BOROUGH'].notna()]
mvaccidents = mvaccidents[mvaccidents['ZIP CODE'].notna()]

#Checking for NaN values

print(mvaccidents['BOROUGH'].value_counts(dropna=False))
print(mvaccidents['ZIP CODE'].value_counts(dropna=False))

# Converting to Pickle files, one with nan, and the other without nan
# The pickle file is required to make it easier to work with this large dataset. The dataset with missing values will be used for overall analysis, and the one without missing values for Borough and Zip code wise analysis

mvaccidents.to_pickle("mvaccidents_pkl.zip")
selected.to_pickle("mvaccidents_pkl_overall.zip")
