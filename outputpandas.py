import pandas as pd
import os
import openpyxl
import xlsxwriter
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import rcParams

#read pickled data frame and gather a small section of it
df = pd.read_pickle('./data/dataFrame.pickle')
dfSegment = df.iloc[49980:50019, :].copy()
#dfSegment.to_excel('output/basic.xlsx') or not show index as seen below
dfSegment.to_excel('output/noIndex.xlsx', index=False)
#can also specify columns to use with columns=['artist', etc]

#use xlsx writer to have multiple sheets - ignores/overrides if already present
writer = pd.ExcelWriter('output/multipleSheets.xlsx', engine='xlsxwriter')
dfSegment.to_excel(writer, sheet_name='Preview', index=False)
df.to_excel(writer, sheet_name='Complete', index=False)
writer.save()

#create new sheet color coded artist count column as gradient
artistCounts = df['artist'].value_counts()
artistCounts.head()
writer = pd.ExcelWriter('output/colors.xlsx', engine = 'xlsxwriter')
artistCounts.to_excel(writer, sheet_name='Artist Counts')
sheet = writer.sheets['Artist Counts']
cellsRange = 'B2:B{}'.format(len(artistCounts.index))
sheet.conditional_format(cellsRange, {'type': '2_color_scale', 'min_value': '10', 'min_type': 'percentile', 'max_value': '99', 'max_type': 'percentile'})
writer.save()

#to_sql() also available

dfSegment.to_json('output/basic.json')
dfSegment.to_json('output/table.json', orient='table')

#plotting - uses matplotlib for visualization
acquisitionYears = df.groupby('acquisitionYear').size()
acquisitionYears.plot()
rcParams.update({'figure.autolayout': True, 'axes.titlepad': 20})
fig = plt.figure()
subplot = fig.add_subplot(1,1,1)
acquisitionYears.plot(ax=subplot, rot='45', logy=True, grid=True)
subplot.set_xlabel('Aquisition Year')
subplot.set_ylabel('Artworks Acquired')
subplot.locator_params(nbins=40, axis='x')
plt.savefig('output/graph.png')
plt.show()
