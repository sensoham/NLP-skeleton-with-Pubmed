# -*- coding: utf-8 -*-
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.charts import HeatMap, bins, output_file, show



df = pd.read_csv('heat_data.csv', header = 'infer', sep = ',')
data_plot = df.sort_values(df.columns[2], ascending = False)[:200]
data_plot.columns = ['term1','term2','occurence']
p = data_plot.pivot(index = 'term1', columns = 'term2', values = 'occurence')
p.to_csv('corr_mat.csv', sep = ',')
fig = plt.figure()
ax = sns.heatmap(p, xticklabels = p.columns, yticklabels = p.index)
ax.figure.subplots_adjust(bottom = 0.35)
ax.figure.subplots_adjust(left = 0.35)
fig = plt.gcf()
fig.set_size_inches(30, 30)
fig.savefig('test_heat.png', dpi=300)
plt.close(fig)
