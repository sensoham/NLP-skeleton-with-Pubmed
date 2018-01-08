import pandas as pd

df = pd.read_csv('Term_details_complete.csv', names = ['TERM', 'OCCUR', 'PMID', 'month', 'year'], sep =',')

def compare(list1, term, dfx):
    term = term.lower()
    for t in list1:
        if t.lower() == term:
            df_term = dfx.loc[dfx['TERM'].isin([t]) & dfx['TERM'].isin([t.upper()])][:1]        #stemmer condition can be added here
            df1 = dfx[dfx['TERM'] != t]
            df1.append(df_term)
    return df1


df_f = pd.DataFrame()
for ids in df['PMID'].unique():
    df_temp = df.loc[df['PMID'].isin([ids])]
    for trm in df_temp['TERM'].unique():
        dfx = compare(list(df_temp['TERM'].unique()), trm, df_temp)
        df_f = df_f.append(dfx)


            
df_f = df_f.drop_duplicates()

df_f['TERM'] = df_f['TERM'].astype(str)
mask = (df_f['TERM'].str.len() > 2)
df_f = df_f.loc[mask]

eq_lst = []
for t1 in df_f['TERM']:
    for t2 in df_f['TERM']:
        if t1 in t2 and abs(len(t2)-len(t1))==1:
            eq_lst.append(t2)

for t in set(eq_lst):
    df_f = df_f[~df_f['TERM'].isin([t])]




df_1 = df_f[~df_f['TERM'].str.contains('%')]
df_2 = df_1[~df_1['TERM'].str.contains('=')]
df_3 = df_2[~df_2['TERM'].str.contains('#')]
df_4 = df_3[~df_3['TERM'].str.contains('\+')]
df_5 = df_4[~df_4['TERM'].str.contains('/')]
df_6 = df_5[~df_5['TERM'].str.contains('<')]
df_7 = df_6[~df_6['TERM'].str.contains('\.')]
df_8 = df_7[~df_6['TERM'].str.contains(r'^-')]  
df_8.to_csv('Term_details_clean.csv', sep =',')

