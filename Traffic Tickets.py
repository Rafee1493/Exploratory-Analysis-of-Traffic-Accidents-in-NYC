# -*- coding: utf-8 -*-
"""
Created on Tue May  3 16:54:27 2022

@author: abdul
"""

#%% Imports

import pandas as pd


#%% Cleaning & Pickling

pd.set_option('display.max_columns',None)           

# Reading the NYC Motor Vehicles Collision Data

raw2 = pd.read_csv("Traffic_Tickets_Issued__Four_Year_Window.csv")   

# Checking Column Names
      
list(raw2.columns)
print(raw2['Police Agency'].value_counts(dropna=False))
print(raw2['Court'].value_counts(dropna=False))

# Dropping Columns that won't be required for analysis

selected2 = raw2.drop(columns= ['Violation Day of Week',
                               'State of License', 
                               'Source'])

# Selected data from only NYC
selected2 = selected2.rename(columns={'Police Agency' : 'PoliceAgency'})
selected2 = selected2.query("PoliceAgency=='NYC POLICE DEPT'")

# Checking the value counts

print(selected2['PoliceAgency'].value_counts(dropna=False))
v = selected2['Court'].value_counts(dropna=False)

# Identifying the Boroughs

split = selected2['Court'].str.split(' ', 1, expand = True)
violations = selected2.join(split)
violations = violations.drop(columns = ['Court',1])
violations = violations.rename(columns={0 : 'Borough'})

# Renaming the Richmond court as Staten Island as it corresponds to that borough
violations['Borough'] = violations['Borough'].str.replace('RICHMOND', 'STATEN ISLAND')

# Selecting data from the 5 Boroughs in NYC
violations = violations.query("Borough == 'MANHATTAN' or Borough=='BROOKLYN' or Borough=='QUEENS' or Borough=='BRONX' or Borough=='STATEN ISLAND'")

v = violations['Borough'].value_counts(dropna=False)

# Converting to Year-Month Date Time Format
violations['DATE']=violations['Violation Year'].astype(str) + violations['Violation Month'].astype(str).str.zfill(2)
ymd = pd.to_datetime(violations['DATE'], format="%Y%m")
violations['YEAR_MONTH'] = ymd.dt.to_period("M")



# Converting to Pickle files
violations.to_pickle("trafficviolations_pkl.zip")





