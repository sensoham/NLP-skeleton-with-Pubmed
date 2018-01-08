import pandas as pd

df = pd.read_csv('Term_details_cleaner.csv', header = 'infer', sep = ',')

lf = df[df['OCCUR'] < 3 ]
mf = df[(df['OCCUR'] >2) & (df['OCCUR'] < 7)]
hf = df[df['OCCUR'] >= 7]

perc_hf = float(len(hf)) / len(df)
perc_mf = float(len(mf)) / len(df)
perc_lf = float(len(lf)) / len(df)

terms = df['TERM'].unique()
lengths = [len(t) for t in terms]
max_len = (max(lengths))

scored_df = pd.DataFrame()
for term in df['TERM'].unique():
    df_temp = df.loc[df['TERM'].isin([term])]
    for lgt in df_temp['OCCUR'].unique():
        df_temp2 = df_temp.loc[df_temp['OCCUR'].isin([lgt])]
        if lgt >= 7:
            scr = (float(len(term))/ max_len) / perc_hf
        elif (lgt >2) & (lgt <7):
            scr = (float(len(term))/ max_len) / perc_mf
        else:
            scr = (float(len(term))/ max_len) / perc_lf
        df_temp2['value'] = scr
        scored_df = scored_df.append(df_temp2)


scored_df = scored_df.sort_values(['value'], ascending = False)

scored_df.to_csv('Terms_det_prior.csv', sep = ',')
