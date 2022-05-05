# -*- coding: utf-8 -*-
"""
Created on Tue May  3 17:53:02 2022

@author: abdul
"""
#%% Imports

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%% Reading and Cleaning

# Reading the pickled datasets

accidents = pd.read_pickle('mvaccidents_pkl.zip')
accidentsall = pd.read_pickle('mvaccidents_pkl_overall.zip') 
violations = pd.read_pickle('trafficviolations_pkl.zip')

# Resetting index and dropping the extra index columns

accidents = accidents.reset_index().drop(columns=["index"])
accidentsall = accidentsall.reset_index().drop(columns=["index"])
violations = violations.reset_index().drop(columns=["index"])

#Converting the Year column to string type to be able to use later

violations["YEAR"] = violations["Violation Year"].astype(str)

#%% Checking Trend Lines of Total Fatalities & Injuries in NYC (2012-2021)

# By Month

injuriestotal=accidentsall.groupby(['YEAR_MONTH'])['TOTAL INJURIES'].sum()
fatalitiestotal=accidentsall.groupby(['YEAR_MONTH'])['TOTAL FATALITIES'].sum()

fig1,(ax1,ax2)=plt.subplots(2,dpi=300)                 
fig1.suptitle("Traffic Injuries & Fatalities in NYC, By Month, (2012 - 2022)")       
injuriestotal.plot(ax=ax1, color="#2AC0A2")                       
ax1.set_xlabel("Date")                         
ax1.set_ylabel("Injuries") 
ax1.axvline(x="2015", color='#124686', ls='--', label='Zero Vision Initiative')
fatalitiestotal.plot(ax=ax2, color="#CF355D")                       
ax2.set_xlabel("Date")                         
ax2.set_ylabel("Fatalities")
ax2.axvline(x="2015", color='#124686', ls='--', label='Zero Vision Initiative')

fig1.savefig('Injuries_Fatalities_Overall_ByMonth.png')  

# By Year

injuriestotalannual=accidentsall.groupby(['YEAR'])['TOTAL INJURIES'].sum()
fatalitiestotalannual=accidentsall.groupby(['YEAR'])['TOTAL FATALITIES'].sum()

fig2,(ax1,ax2)=plt.subplots(2,dpi=300)                 
fig2.suptitle("Traffic Injuries & Fatalities in NYC, Annual (2012 - 2022)")       
injuriestotalannual.plot(ax=ax1, color="#2AC0A2")                       
ax1.set_xlabel("Date")                         
ax1.set_ylabel("Injuries") 
fatalitiestotalannual.plot(ax=ax2, color="#CF355D")                       
ax2.set_xlabel("Date")                         
ax2.set_ylabel("Fatalities")

fig2.savefig('Injuries_Fatalities_Overall_ByYear.png')  

#%% Diving Deeper: Checking Trend Lines of Fatalities & Injuries for each NYC Borough (2012-2021)

# By Year

injuriesannual = accidents.groupby(['BOROUGH','YEAR'])['TOTAL INJURIES'].sum()
injuriesannual = injuriesannual.unstack('BOROUGH')

fatalitiesannual = accidents.groupby(['BOROUGH','YEAR'])['TOTAL FATALITIES'].sum()
fatalitiesannual = fatalitiesannual.unstack('BOROUGH')

fig3,(ax1,ax2)=plt.subplots(2,dpi=300)                 
fig3.suptitle("Traffic Injuries & Fatalities in NYC Boroughs, Annual (2012 - 2022)")       
injuriesannual.plot(ax=ax1)                       
ax1.set_xlabel("Date")                         
ax1.set_ylabel("Injuries") 
ax1.legend(bbox_to_anchor=(1.04,1),loc=2, fontsize='xx-small')
ax1.axvline(x=2015, color='#124686', ls='--', label='Zero Vision Initiative')
fatalitiesannual.plot(ax=ax2)                       
ax2.set_xlabel("Date")                         
ax2.set_ylabel("Fatalities")
ax2.legend(bbox_to_anchor=(1.04,1),loc=2, fontsize='xx-small')
ax2.axvline(x=2015, color='#124686', ls='--', label='Zero Vision Initiative')

fig3.tight_layout()

fig3.savefig('Injuries_Fatalities_Boroughs_ByYear.png')  

# Looks Like there is a sudden rise in fatalities in Brooklyn & Queens between 2016 to 2019
# We'll further check these variations through a Zip Code level progression of fatalities in these two boroughs
# This will be done through GIS

#%% Preparing Data for Geospatial Analysis

filtered = accidents[(accidents["YEAR"] == 2016) | (accidents["YEAR"] == 2017) | (accidents["YEAR"] == 2018) | (accidents["YEAR"] == 2019)]
filtered2 = filtered[(filtered["BOROUGH"] == "QUEENS") | (filtered["BOROUGH"] == "BROOKLYN")]
filteredg = filtered2.groupby(["ZIP CODE","YEAR"])["TOTAL FATALITIES"].sum()
filteredg = filteredg.unstack("YEAR")
filteredg=filteredg.reset_index()

filteredg.to_csv("Brooklyn&Queens Fatalities.csv")

#%% Checking the Top Known Reasons for Traffic Accidents

print(accidents["PRIMARY CONTRIBUTING FACTOR"].value_counts())

# Dropping Unspecified Cases

selectedaccidents = accidents[accidents["PRIMARY CONTRIBUTING FACTOR"] != 'Unspecified']

print(selectedaccidents["PRIMARY CONTRIBUTING FACTOR"].value_counts())

# Identifying the Top Reasons for Accidents every year (2014-2021)
# I am appending only the Top 5 cases from each year to the final dataframe to simplify the final visualization

year = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
col = 'YEAR'
group = 'PRIMARY CONTRIBUTING FACTOR'
topfactors = pd.DataFrame()

for y in year:
    x = selectedaccidents[selectedaccidents[col] == y]
    x = x.groupby([group,col])["COLLISION_ID"].count().reset_index().sort_values(by=["COLLISION_ID"], ascending=False).iloc[0:5]
    x = x.rename(columns={'COLLISION_ID':'Count'})
    topfactors = pd.concat([topfactors,x])

# Creating a Heatmap

fig6, ax1 = plt.subplots()
sns.set_theme(style="white")
hm = topfactors.pivot("PRIMARY CONTRIBUTING FACTOR", "YEAR", "Count")
ax1=sns.heatmap(hm, cmap="flare")
ax1.set_title("Heatmap of Top Reasons for Accidents")

fig6.subplots_adjust(left=0.5, right=1.5)

fig6.savefig('Heatmap of Top Reasons for Accidents.png',bbox_inches='tight') 

# Looks like "Driver Distraction is by far the most common reason
# It might be useful to check other reasons except Driver Distraction, to be able to better track their progression through the heatmap 

#%% Top Reasons without the top most reason (Driver Distraction)

print(selectedaccidents["PRIMARY CONTRIBUTING FACTOR"].value_counts())

# Dropping 'Driver Inattention/Distraction' Cases

selectedaccidents2 = selectedaccidents[selectedaccidents["PRIMARY CONTRIBUTING FACTOR"] != 'Driver Inattention/Distraction']

print(selectedaccidents2["PRIMARY CONTRIBUTING FACTOR"].value_counts())

# Identifying the Rest of the Top Reasons for Accidents every year (2014-2021)

year = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
col = 'YEAR'
group = 'PRIMARY CONTRIBUTING FACTOR'
topfactors2 = pd.DataFrame()

for y in year:
    x = selectedaccidents2[selectedaccidents2[col] == y]
    x = x.groupby([group, col])["COLLISION_ID"].count().reset_index().sort_values(by=["COLLISION_ID"], ascending=False).iloc[0:5]
    x = x.rename(columns={'COLLISION_ID':'Count'})
    topfactors2 = pd.concat([topfactors2,x])

# Creating a Heatmap

fig7, ax1 = plt.subplots()
sns.set_theme(style="white")
hm = topfactors2.pivot("PRIMARY CONTRIBUTING FACTOR", "YEAR", "Count")
ax1=sns.heatmap(hm, cmap="flare")
ax1.set_title("Heatmap of Top Reasons for Accidents(without topmost reason)")

fig7.subplots_adjust(left=0.5, right=1.5)

fig7.savefig('Heatmap of Top Reasons for Accidents2.png',bbox_inches='tight') 

# Looks like most of the top reasons do not actually lead to deaths. It could be that these are all relatively minor accidents.
# I am interested to look into the causes behind major accidents leading to fatalities

#%% Biggest Causes behind deaths

# Selecting only those cases that led to fatalities

onlydeaths = selectedaccidents[selectedaccidents["TOTAL FATALITIES"] != 0]

print(onlydeaths["PRIMARY CONTRIBUTING FACTOR"].value_counts())

# Identifying the Top Reasons for Accidents every year (2014-2021)

year = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
col = 'YEAR'
group = 'PRIMARY CONTRIBUTING FACTOR'
topdeathfactors = pd.DataFrame()

# Here I am using the sum of Fatalities instead of the count, as we have one group of fatalities data, compared to the two groups of fatalities and injuries data earlier. 

for y in year:
    x = onlydeaths[onlydeaths[col] == y]
    x = x.groupby([group,'YEAR'])["TOTAL FATALITIES"].sum().reset_index().sort_values(by=["TOTAL FATALITIES"], ascending=False).iloc[0:5]
    topdeathfactors = pd.concat([topdeathfactors,x])

# Creating a Heatmap

fig12, ax1 = plt.subplots()
sns.set_theme(style="white")
hmd = topdeathfactors.pivot("PRIMARY CONTRIBUTING FACTOR", "YEAR", "TOTAL FATALITIES")
ax1=sns.heatmap(hmd, cmap="coolwarm")
ax1.set_title("Heatmap of Top Reasons for Deaths")

fig12.subplots_adjust(left=0.5, right=1.5)

fig12.savefig('Heatmap of Top Reasons for Traffic Deaths.png',bbox_inches='tight') 

#%% Top Vehicles Involved in Accidents every year

counts = accidents["PRIMARY VEHICLE TYPE"].value_counts()

# Merging similar categories

change = {'SPORT UTILITY / STATION WAGON':'Station Wagon/Sport Utility Vehicle',
     'TAXI':'Taxi',
     '4 dr sedan':'Sedan',
     'BUS':'Bus'}

for c in change.keys():
    accidents["PRIMARY VEHICLE TYPE"] = accidents["PRIMARY VEHICLE TYPE"].str.replace(c,change[c])

counts = accidents["PRIMARY VEHICLE TYPE"].value_counts()

# Identifying the Top Vehicles Involved in Accidents every year (2014-2021)

year = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
col = 'YEAR'
group = 'PRIMARY VEHICLE TYPE'
topvehicles = pd.DataFrame()

for y in year:
    x = accidents[accidents[col] == y]
    x = x.groupby([group,'YEAR'])["COLLISION_ID"].count().reset_index().sort_values(by=["COLLISION_ID"], ascending=False).iloc[0:5]
    x = x.rename(columns={'COLLISION_ID':'Count'})
    topvehicles = pd.concat([topvehicles,x])

# Creating a Heatmap

fig8, ax1 = plt.subplots()
sns.set_theme(style="white")
hm2 = topvehicles.pivot("PRIMARY VEHICLE TYPE", "YEAR", "Count")
ax1=sns.heatmap(hm2, cmap="crest")
ax1.set_title("Heatmap of Top Vehicles Involved in Accidents")

fig8.savefig('Heatmap of Top Vehicles Involved in Accidents.png') 

#%% Trend Lines of Traffic Violations in NYC

# Performing additional analysis on the traffic violations in NYC to check for any trend/correlation with Traffic Accidents

# By Month

violationsmonthtotal = violations.groupby(['YEAR_MONTH'])["Violation Description"].count()

fig9,ax1=plt.subplots(dpi=300)                 
fig9.suptitle("Traffic Violations in NYC, By Month (2018 - 2022)")       
violationsmonthtotal.plot(ax=ax1)                       
ax1.set_xlabel("Date")                         
ax1.set_ylabel("Traffic Violations") 

fig9.savefig('Traffic Violations in NYC Boroughs By Year (2018-2022).png')

#%% Checking for Trends in Traffic Violations in the NYC Boroughs (2018-2022)

# By Month

violationsannual = violations.groupby(['Borough','YEAR_MONTH'])["Violation Description"].count()
violationsannual = violationsannual.unstack('Borough')

fig4,ax1=plt.subplots(dpi=300)                 
fig4.suptitle("Traffic Violations in NYC Boroughs, By Month (2018 - 2022)")       
violationsannual.plot(ax=ax1)                       
ax1.set_xlabel("Date")                         
ax1.set_ylabel("Traffic Violations") 
ax1.legend(bbox_to_anchor=(1.04,1),loc=2, fontsize='xx-small')

fig4.tight_layout()

fig4.savefig('Traffic Violations in NYC Boroughs By Month (2018-2022).png')  

# By Year

violationstotal = violations.groupby(['Borough','YEAR'])["Violation Description"].count()
violationstotal = violationstotal.unstack('Borough')

fig5,ax1=plt.subplots(dpi=300)                 
fig5.suptitle("Traffic Violations in NYC Boroughs, By Year (2018 - 2022)")       
violationstotal.plot(ax=ax1)                       
ax1.set_xlabel("Date")                         
ax1.set_ylabel("Traffic Violations") 
ax1.legend(bbox_to_anchor=(1.04,1),loc=2, fontsize='xx-small')

fig5.tight_layout()

fig5.savefig('Traffic Violations in NYC Boroughs By Year (2018-2022).png')  


#%% Traffic Violation Type Heatmap

# Checking for the causes behind these Traffic Violations, to compare with the Traffic Accident causes

countsvio = violations["Violation Description"].value_counts()

# Identifying the Top Reasons every year

year = ['2018', '2019', '2020', '2021']
col = 'YEAR'
group = 'Violation Description'
violations = violations.reset_index()
topvio = pd.DataFrame()


for y in year:
    x = violations[violations[col] == y]
    x = x.groupby([group,col])["index"].count().reset_index().sort_values(by=["index"], ascending=False).iloc[0:5]
    x = x.rename(columns={'index':'Count'})
    topvio = pd.concat([topvio,x])

# Creating a Heatmap

fig10, ax1 = plt.subplots()
sns.set_theme(style="white")
hm3 = topvio.pivot("Violation Description", "YEAR", "Count")
ax1=sns.heatmap(hm3, cmap="flare")
ax1.set_title("Heatmap of Top Traffic Violations")

fig10.savefig('Heatmap of Top Traffic Violations.png') 

#%% Traffic Violator Age Heatmap

# I am now checking the ages of the violators of the traffic violations. This could potentially provide an idea of the ages of people that are engaged in traffic accidents.

countsvio = violations["Age at Violation"].value_counts()

# Dividing the ages into 10 bins

violations['age_bin']=pd.qcut(violations['Age at Violation'], q=10)

x = violations.groupby(['YEAR','age_bin'])["index"].count().reset_index()
x = x.rename(columns={'index':'Count'})

# Creating a Heatmap

fig11, ax1 = plt.subplots()
sns.set_theme(style="white")
hm4 = x.pivot("age_bin", "YEAR", "Count")
ax1=sns.heatmap(hm4, cmap="crest")
ax1.set_title("Traffic Violations by Age")

fig11.subplots_adjust(left=0.5, right=1.7)

fig11.savefig('Traffic Violations by Age.png', bbox_inches='tight')
