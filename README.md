# Exploratory-Analysis-of-Traffic-Accidents-in-NYC_dev

# Purpose:

There has been a recent uptick in Traffic Accidents in New York City, particularly after the pandemic. Experts have cited reasons such as worsening mental health issues and drug abuse in a post pandemic world. The mayor of NYC have also recalled the past success of the 2014 Vision Zero initiative, that included a host of legislative, technological, and educational transformations to reduce accidents in NYC.

The analysis was done to assess how Traffic accidents and fatality cases have changed before and after the Zero Vision Initiative, as well as after the pandemic. In particular, the analysis would try to find if the policy was indeed successful. If not, what might be the core reasons? It will also try to fund out how drastic the impact of the pandemic might have been. Are the recent upticks only a return to pre-pandemic levels, or are cases higher than pre-pandemic levels. 

# Datasets:

The datasets that have been used are:
The datasets have been exported as csv files from the links provided.

1) NYC Open Data Motor Vehicle Collisions – Crashes (2012 – 2022)
https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95

2) NYS Traffic Tickets Issued (2018-2022)
https://data.ny.gov/Transportation/Traffic-Tickets-Issued-Four-Year-Window/q4hy-kbtf

# Scripts:

There are three scripts that have been created. The scripts should be run in the order mentioned below:

1) Traffic Accidents.py

This script cleans the NYC Traffic Accidents dataset and creates a pickled filed that is used for analysis and visualizations in another script. The dataset includes records of all cases of injuries and fatalities in NYC between 2012 to February 2022. The dataset has been cleaned to remove the columns that will not be required, and removed for missing values in certain columns. The output includes two pickled files -  one with missing values for the 'Borough" and "Zip Code", and the other without the missing values. The data that includes missing values will be used to provide the aggregrate analysis for the full city. The data excluding the missing values will be used for Borough and Zip Code level analysis

2) Traffic Tickets.py

The script cleans the Traffic Tickets dataset and creates a pickled file. It includes all cases of traffic violation in New York State that led to traffic tickets being issues between 2018-2021. The dataset was filtered for only those cases within New York City. It also cleans the Court column to identify the corresponding Boroughs. The irrelevant columns are dropped as well. The dataset contains information about the age of each violator, which doe not exist for the other accident dataset. We use this age data later to make an inference about the trend of accidents. 

3) Analysis.py

The dataset performs the analysis and creates the charts and visualiations. 

First we look into the total fatalities and injuries across the state every year from 2012-2021. We create two trend lines, one by month, and another by year. The monthly data shows a seasonal variation in the number of cases, with cases at their lowest during the winter months, and highest during the middle of the year in summer. Most importantly, cases of injuries show an observable increase after the Zero Vision Initiative was launched in 2015. In addition, although the pandemic brought a sharp reduction, cases have increased sharply, but yet to reurn to pre-pandemic levels. 

We then look into the same data for each of the boroughs in NYC. It seems that the number of cases correspond to the population of each borough. However, there is a sudden uptick of fatalities in Brooklyn and Queens from 2016 to 2019. So, we took a further look into these two Boroughs at Zip Code Level. 

First we filtered the datasets for the two boroughs and the years from 2016 to 2019. We saved it into a nee csv "Brooklyn & Queens". The csv was loaded into a GIS software and the Zip Code level heatmap was generated for each year. The heatmaps are saved in the "Brooklyn & Queens" PowerPoint document. The heatmaps show that the cases initially concentrated mostly at the intersecting borders of the two boroughs, and simply worsened all across the boroughs as time progresses. This warrants a further dive into other variables during that period. 

We then moved onto the known reasons behind the traffic accidents. We draw a heatmap for the top 5 reasons in each year. It seems "Driver Distraction" is by far the most common reason. It might be useful to check other reasons except Driver Distraction, to be able to better track their progression through the heatmap. So, we remove the Drive Distraction cases, and create another heatmap. Now we can see that there has been a steady increase in all the top reasons until the pandemic. The top reasons included Failure to yield right-of-way, Following Too CLosely, Backing Unsafely, Passing too CLosely, and Improper Lane Usage. 

It seemed that most of these reasons might cause injuries but not fatalities. So, we look into the top reasons that led to deaths. Although aforementioned reasons remained among the top, we now see more variations, with factors such as Alcohol Involvement, Speeding, Disregarding Traffic Control becoming important reasons. It was also intreseting to note that speeding became the most common reason leading to fatalities after the pandemic. 

We also looked into the other dataset of traffic violations to catch any trend. But it did not yield any discernable results that can be matched with traffic accidents data. However, the dataset did have data on age, which the traffic accident dataset does not have. So we tried to check how the age of traffic law violators distributed. This may also give us an idea of the age distribution of the perpetrators of traffic accidents. The age hve been divided into 10 bins between the ages 16 to 95. While we expect young people between the ages 16 to 23 to be one of the highest violators, it was interesting to note that most violations were caused by drivers between the ages 29 to 33, when drivers are expected to be more mature. They have been consistently the largest group across the years. In addition, the number of violations drastically reduced after pandemic, not showing any signs of returning to pre-pandemic levels. 


# Other files

A PowerPoint file is added in the repository that summarizes the aforementioned analysis.

# Moving Forward

The analysis is only a preliminary dive into the impact of the Zero Policy Initiative and the pandemic on the Traffic Accidents in New York City. There is indeed much more that can be done. For instance, the data can b e normalized to traffic volumes, to have a better idea about the progression. However, it is quite evident that the Initiative did not have the desired impact. 





