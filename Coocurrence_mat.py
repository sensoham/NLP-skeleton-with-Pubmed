import pandas as pd


dfx = pd.read_csv('Terms_det_prior.csv')
dfx = dfx.drop(dfx.columns[0], axis=1)
dfx = dfx.drop(dfx.columns[0], axis=1)

df_top = dfx.sort_values(['value'], ascending = False)[:400]
pmids = df_top['PMID'].unique()
data = pd.DataFrame([])
coocc = []
for ids in pmids:
    df_temp = df_top.loc[df_top['PMID'].isin([ids])]
    topterm = df_temp['TERM']
    for term1 in topterm:
        for term2 in topterm:
            if term1.lower() != term2.lower():
                occ = [term1, term2, 1]
                coocc.append(occ)
                data = data.append(pd.DataFrame({'TERM1': term1, 'TERM2': term2}, index=[0]), ignore_index=True)

data_df = data.groupby(['TERM1','TERM2']).size()
data_df.to_csv('heat_data.csv', sep = ',')

