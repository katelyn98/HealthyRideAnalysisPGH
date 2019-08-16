from pathlib import Path

import pandas as pd


data_dir = Path('.') / 'data'
output_dir = Path('.') / 'output'

if not (data_dir.exists() or data_dir.is_dir()):
    exit(-1)

if not output_dir.exists():
    output_dir.mkdir()

dataframes = []
data_files = data_dir.glob('*.csv')


def clean_df(pd_df):
    columns_rename = {}
    for col in list(pd_df.columns):
        renamed_column = col.lower().replace(' ', '_')
        columns_rename[col] = renamed_column

    new_df = pd_df.rename(columns=columns_rename)
    df_filtered = new_df[new_df.from_station_id.notnull()]
    df_filtered = df_filtered[new_df.to_station_id.notnull()]
    return df_filtered

for file in data_files:
    df = pd.read_csv(str(file))
    df = clean_df(df)
    dataframes.append(df)
    df.to_csv(str(output_dir / file.name), index=False)


df = pd.concat(dataframes)
df.to_csv(str(output_dir / 'final.csv'), index=False)