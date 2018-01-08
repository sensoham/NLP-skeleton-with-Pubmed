import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text

df_rem = pd.read_csv(']Dict_match_titplusabs_flashtext.csv', names = ['TERM','Category','OCCUR','PMID','month','year'], sep = ',')
df_cln = df_rem[~df_rem['year'].isin(['No Date'])]
df_norm = pd.DataFrame()
df_total = pd.DataFrame()
for yr in df_cln['year'].unique():
    df_temp = df_cln.loc[df_cln['year'].isin([yr])]
    occ_all_terms_yr = df_temp['OCCUR'].sum()
    df_temp['Total_trm_occ_yr'] = occ_all_terms_yr
    df_total = df_total.append(df_temp)

for term in df_total['TERM'].unique():
    df_tempa = df_total.loc[df_total['TERM'].isin([term])]
    sum_term = 0
    for yr in df_tempa['year'].unique():
        df_tempb = df_tempa.loc[df_tempa['year'].isin([yr])]
        sum_term = sum_term + (df_tempb['OCCUR'].astype(float)/df_tempb['Total_trm_occ_yr'].astype(float))
        df_tempb['Cum_freq_norm'] = sum_term
        df_norm = df_norm.append(df_tempb)


df_date = pd.DataFrame()
for ids in df_norm['PMID'].unique():
    df_t = df_norm.loc[df_norm['PMID'].isin([ids])]
    for trm in df_t['TERM'].unique():
        df_t2 = df_t.loc[df_t['TERM'].isin([trm])]
        year = df_t2['year'].astype(float)
        month = df_t2['month'].astype(float)
        date = year + (month/12)
        df_t2['date'] = date
        df_date = df_date.append(df_t2)

df_sort = df_date.sort_values(['Cum_freq_norm', 'date'], ascending = False)
df_sort = df_sort.drop_duplicates(subset=['TERM'], keep = 'first')
new_plot_df = df_sort[['TERM', 'date', 'Cum_freq_norm']].copy()

sample_run_df = new_plot_df[:20]
text = sample_run_df['TERM']
udata = [text1.decode('utf-8') for text1 in text]
asciitext = [text2.encode('ascii', 'ignore') for text2 in udata]
x = sample_run_df['date']
x = [float(i) for i in x]
x = np.array(x)
y = sample_run_df['Cum_freq_norm']
y= np.array(y)
xy = np.vstack((x, y)).T

yers = sample_run_df['date'].unique()
if len(yers) == 1:
    maxyr = yers+50
    minyr = yers-50
    maxocc= max(sample_run_df['Cum_freq_norm'])+0.02

else:
    maxyr = max(yers) + 0.5
    minyrs =min(yers) - 0.5
    maxocc= max(sample_run_df['Cum_freq_norm'])+0.02

fig, ax = plt.subplots()
scat = ax.plot(x,y, 'bo')
texts = []
for (a,b),label in zip(xy,asciitext):
    texts.append(plt.text(a,b,label))

adjust_text(texts, x=x, y=y, force_points=0.1, arrowprops=dict(arrowstyle='->', 
color='red'))
ax.axis([minyrs,maxyr,0,maxocc])
ax.set_ylabel("Total occurance (normalized)")
ax.set_xlabel("Year")

figure = plt.gcf()
figure.set_size_inches(20,20)
plt.savefig("myplot1.png", dpi = 200)
plt.show()
plt.close()
