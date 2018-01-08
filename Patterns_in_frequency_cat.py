import pandas as pd

df = pd.read_csv('Term_categories_clean.csv', header = 'infer', sep = ',')
pmids = df['PMID'].unique()
df_low = df.loc[df['OCCUR'].isin(['LOW FREQUENCY'])]
df_med = df.loc[df['OCCUR'].isin(['MEDIUM FREQUENCY'])]
df_hig = df.loc[df['OCCUR'].isin(['HIGH FREQUENCY'])]
probably_useless = []
# Rule 1
for term in df_low['TERM']:
    df_term_temp = df_low.loc[df_low['TERM'].isin([term])]
    if len(df_term_temp['PMID'].unique()) > 15:
        probably_useless.append(term)

df_rem = df
for t in probably_useless:
    df_rem = df_rem[~df_rem['TERM'].isin([t])]


df_rem.to_csv('Term_categories_cleaner.csv', sep = ',')
