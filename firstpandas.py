import pandas as pd
import numpy as np
import os


# np.array and np.ndarray (n dimensional)
# pandas Series - data in single column
# pandas DataFrame - table like data

numpyArray = np.random.rand(3) # 3 random numbers in array
firstSeries = pd.Series(np.random.rand(3)) # 3 random number in series (1 column)
firstFrame = pd.DataFrame(np.random.rand(3, 2)) # 3x2 random table
indexSeries = pd.Series(np.random.rand(3), index=["First", "Second", "Third"]) # custom indexes

print(indexSeries.index) #displays index and datatype

array2d = np.random.rand(3, 2) #can access like array2d[0,0]
df = pd.DataFrame(array2d) #cant access df[0,0]

df.columns = ["First", "Second"] # indexes columns of df

print(df["Second"]) # prints 2nd column of df

# pandas can handle text, binary, relational databases, python structures
# text formats - csv, json, html

df = pd.read_csv('data/artworkdata.csv', nrows=5) #reads first 5 rows
df = pd.read_csv('data/artworkdata.csv', index_col='id', usecols=['id', 'artist']) #reads rows of id and artist based on id
usecols = ['id', 'artist', 'title', 'medium', 'year', 'acquisitionYear', 'height', 'width', 'units']
df = pd.read_csv('data/artworkdata.csv', index_col='id', usecols=usecols) #reads rows of specified columns based on id
#df.to_pickle('data/dataFrame.pickle')

artists = df['artist'] #gets just specified column, avoid using df.artist

# find number of unique artists:
uniqueArtists = len(pd.unique(artists)) # use the unique parameter to get list of unique values, length to find number

#find number of works by francis bacon
dfBacon = df['artist'] == 'Bacon, Francis' #creates column of true/false whether the artist is Francis Bacon
numBacon = dfBacon.value_counts() #identifies the amount of true values in column

artistCounts = df['artist'].value_counts() #creates structure of number of works by every artist

#iloc represents index of row/column as integer, loc represents index of row/column based on row/column names
example = df.loc[1035, 'artist'] #returns single value
example2 = df.loc[df['artist'] == 'Bacon, Francis', :] #returns all values that FB is artist
ilocExample = df.iloc[100:300, [0,1,4]] #all values in rows 100-300 and the information from 3 of those columns

#find biggest artwork in dataset
#input data not perfect -> needs to be converted to address missing data
numWidths = pd.to_numeric(df['width'], errors='coerce') #may not always work unless errors=coerce added, then all invalid data becomes NaN
#modify original dataframe to address issues
df.loc[:, 'width'] = pd.to_numeric(df['width'], errors='coerce')
df.loc[:, 'height'] = pd.to_numeric(df['height'], errors='coerce')
#can now find area 
area = df['height'] * df['width']
#add new column to dataframe
df = df.assign(area=area)
#find max
df['area'].max() #finds max value
df['area'].idxmax() #finds location of max value
final = df.loc[df['area'].idxmax(), :] #full entry of max area


# Groups
# Find first year for each artist - split data into groups based on artist (aggregation)
# Fill unknown medium values based on most common medium for the artist (transformation)
# Dropping groups - filtering
for name, group in df.groupby('artist'):
    #name is the name and group is all of the data associated with that artist
    #find minimum year for each group
    minYear = group['acquisitionYear'].min()

def fillValues(series):
    values = series.value_counts()
    if values.empty:
        return series
    mostFreq = values.index[0]
    #replace nonexistent values with most frequent
    newSeries = series.fillna(mostFreq)
    return newSeries

def transform(original):
    groups = []
    #for each artists, identify most common medium and replace nonexisting data with most common
    for name, group in df.groupby('artist'):
        filled = group.copy()
        filled.loc[:, 'medium'] = fillValues(group['medium'])
        groups.append(filled)
    new = pd.concat(groups)
    return new

#cleanedMediums = transform(df)

#***OR***
#gathers data just from medium column after its grouped by artist
groupedMedium = df.groupby('artist')['medium']
#replaces column in dataframe by transforming the data using the indicated function
df.loc[:, 'medium'] = groupedMedium.transform(fillValues)

#group year based on artist
groupedYear = df.groupby('artist')['acquisitionYear']
#identify min of each group
minYears = groupedYear.agg(np.min)

#group by titles
groupedTitles = df.groupby('title')
#sort new data by length of group
titleCounts = groupedTitles.size().sort_values(ascending=False)

condition = lambda x: len(x.index) > 1
dupTitles = groupedTitles.filter(condition)
dupTitles.sort_values('title', inplace=True)

df.to_pickle('data/dataFrame.pickle')

