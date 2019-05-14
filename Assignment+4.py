
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[13]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import csv


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[14]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

    
GDP0=pd.read_excel('gdplev.xls',skiprows=4)
GDP0.drop(['Unnamed: 0','Unnamed: 1','Unnamed: 2','Unnamed: 3','Unnamed: 5','Unnamed: 7'], axis=1,inplace=True)

GDP=GDP0[215:]
GDP=GDP.rename(columns={'Unnamed: 4':'quater','Unnamed: 6':'2009 dollars'})
GDP.reset_index(inplace=True)
GDP.drop(['index'],axis=1,inplace=True)

GDP


# In[15]:


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    
    university_towns=pd.read_csv('university_towns.txt',delimiter='\t',header=None,names=['StaReg'])
    
    university_towns['StaReg']=university_towns['StaReg'].str.split('(').str[0].str.rstrip()
    
    
    for i in university_towns.index:
        if '[' in university_towns.loc[i,'StaReg']:
            university_towns.loc[i,'State']=university_towns.loc[i,'StaReg'].split('[')[0]
            
      
    university_towns.fillna(method='ffill',inplace=True)
    
    for i in university_towns.index:
        if '[' in university_towns.loc[i,'StaReg']:
            university_towns.drop(i,inplace=True)
            
    university_towns['RegionName']=university_towns['StaReg'] 
    university_towns.drop('StaReg',axis=1, inplace=True)
    
    return university_towns

get_list_of_university_towns()


# In[16]:


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''

    for i in (GDP.index):
        if ((GDP['2009 dollars'].iloc[i]>GDP['2009 dollars'].iloc[i+1])&(GDP['2009 dollars'].iloc[i+1]>GDP['2009 dollars'].iloc[i+2])):
            #print('i=',i,'quater=',GDP['quater'].iloc[i],'GPD=',GDP['2009 dollars'].iloc[i])
            break
            
    
    return GDP['quater'].iloc[i+1]

get_recession_start()


# In[17]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    j=GDP[GDP['quater']==get_recession_start()].index[0]
    #print('j=',j)
    for i in (GDP.index[j+2:]-2):
        #print('i+2=',i,'quater=',GDP['quater'].iloc[i+2],'GPD=',GDP['2009 dollars'].iloc[i+2])
        if ((GDP['2009 dollars'].iloc[i+2]>GDP['2009 dollars'].iloc[i+1])&(GDP['2009 dollars'].iloc[i+1]>GDP['2009 dollars'].iloc[i])):
            #print('i=',i,'quater=',GDP['quater'].iloc[i],'GPD=',GDP['2009 dollars'].iloc[i])
            break
            
    
    return GDP['quater'].iloc[i+2]

get_recession_end()


# In[18]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    S1=GDP[GDP['quater']==get_recession_start()].index[0]
    E1=GDP[GDP['quater']==get_recession_end()].index[0]
    Min1=GDP['2009 dollars'].iloc[S1:E1].min()
    
    IndMin=(GDP[GDP['2009 dollars']==Min1].index[0])
  
        
    return (GDP['quater'].iloc[IndMin])

get_recession_bottom()


# In[19]:


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    AllHomes1=pd.read_csv('City_Zhvi_AllHomes.csv')
    AllHomes1.sort(['State','RegionName'],inplace=True)
    AllHomes1.set_index(['State','RegionName'],inplace=True)
    
    for col in AllHomes1.columns:
        if ((col[-3:]=='-01')|(col[-3:]=='-02')|(col[-3:]=='-03')):
            AllHomes1.rename(columns={col:col[0:4]+'q1'},inplace=True)
            
        if ((col[-3:]=='-04')|(col[-3:]=='-05')|(col[-3:]=='-06')):
            AllHomes1.rename(columns={col:col[0:4]+'q2'},inplace=True)
            
        if ((col[-3:]=='-07')|(col[-3:]=='-08')|(col[-3:]=='-09')):
            AllHomes1.rename(columns={col:col[0:4]+'q3'},inplace=True)
            
        if ((col[-3:]=='-10')|(col[-3:]=='-11')|(col[-3:]=='-12')):
            AllHomes1.rename(columns={col:col[0:4]+'q4'},inplace=True)
    
    
    AllHomesT=AllHomes1.T
    AllHomesT.reset_index(inplace=True)
    AllHomesT.drop(AllHomesT.index[0:49],inplace=True)
    AllHomesT.set_index(['index'],inplace=True)
    
    AllHomes=AllHomesT.astype(float).groupby(AllHomesT.index).mean()
    
    AllHomes.rename(columns=states,inplace=True)
    
    return AllHomes.T


convert_housing_data_to_quarters()


# In[20]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).
    
    From top  of the page: Run a t-test to compare the ratio of the mean price of houses in university towns
    the quarter before the recession starts compared to the recession bottom. 
    (price_ratio=quarter_before_recession/recession_bottom)
    
    '''
    university_towns=get_list_of_university_towns().set_index(['State','RegionName'])
    AllHomes=convert_housing_data_to_quarters()[['2008q2',get_recession_bottom(),get_recession_end()]]
    
    #(price_ratio=quarter_before_recession/recession_bottom)
    AllHomes['price_ratio']=AllHomes['2008q2']/AllHomes['2009q2']
    AllHomes.dropna(inplace=True)
    
    
    TF=AllHomes.index.isin(university_towns.index)
    
    uni=AllHomes.loc[TF==True]
    non_uni=AllHomes.loc[TF==False]
    
    #print('uni_mean=',uni['price_ratio'].mean(),'  non_uni_mean=',non_uni['price_ratio'].mean())

    Test=ttest_ind(uni['price_ratio'],non_uni['price_ratio'])
    different = True if Test[1]<0.01 else False
    better='university town' if (uni['price_ratio'].mean()<non_uni['price_ratio'].mean()) else 'non-university town'
    
   
    return (different,Test[1],better)

run_ttest()
 


# In[ ]:





# In[ ]:




