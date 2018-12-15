import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

#Collecting all files in one df_list
files = glob.glob('state*.csv')
df_list = []
for file in files:
  data = pd.read_csv(file)
  df_list.append(data)
#Concatenating all the files in one DF
us_census = pd.concat(df_list)

#Income to numeric
us_census['Income'] = us_census['Income'].str.replace('[\$,]','',regex=True)
us_census['Income'] = pd.to_numeric(us_census['Income'])

#Separating GenderPop into two columns: Men and Women
gender_pop_split_list = us_census['GenderPop'].str.split('_')
#Making 2 new columns from this list
us_census['Men'] = gender_pop_split_list.str.get(0)
us_census['Women'] = gender_pop_split_list.str.get(1)
#Dropping GenderPop column
us_census.drop('GenderPop', axis=1, inplace=True)
#Replacing M and F symbols from new columns
split_df = us_census['Men'].str.split('(\d+)', expand=True)
us_census['Men'] = pd.to_numeric(split_df[1])
split_df = us_census['Women'].str.split('(\d+)', expand=True)
us_census['Women'] = pd.to_numeric(split_df[1])
#print(us_census.isna().any())
us_census = us_census.fillna(value={'Women':us_census['TotalPop']-us_census['Men']})
#Removing duplicates
duplicates = us_census.duplicated()
#print(duplicates.value_counts())
us_census = us_census.drop_duplicates()
duplicates = us_census.duplicated()
#print(duplicates.value_counts())
#Cleaning nationality columns to make them suitable for histograms
columns_to_clear = ['Hispanic', 'White', 'Black', 'Native', 'Asian', 'Pacific']
for column in columns_to_clear:
  us_census[column] = us_census[column].str.replace('[\%,]','',regex=True)
  us_census[column] = pd.to_numeric(us_census[column])
#Removing nan values from them
us_census = us_census.fillna(value=0)
#Removing duplicates
duplicates = us_census.duplicated()
#print(duplicates.value_counts())
us_census = us_census.drop_duplicates()

print(us_census.columns)
print(us_census.dtypes)
print(us_census.isna().any())
print(us_census.head())

#Making scatter plot of women column
plt.scatter(us_census["Women"], us_census["Income"])
plt.title("Woman population income")
plt.xlabel("Women population")
plt.ylabel("Income value")
plt.show()

#Histograms of different population in states
ax = plt.subplot()
for column in columns_to_clear:
  plt.hist(us_census[column])
  plt.title('%s population in states' %(column))
  plt.xlabel("Value 0-100%")
  plt.ylabel('State')
  plt.show()

us_census['Unnamed: 0'] = range(len(us_census))
us_census = us_census.set_index('Unnamed: 0')
us_census.to_csv('Us_census.csv')