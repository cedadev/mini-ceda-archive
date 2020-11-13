import pandas as pd

import sys
fpath = sys.argv[1]


df = pd.read_csv(fpath, header=None, skipinitialspace=True)
fout = fpath + '.new'

df_jan = df[df[0].str.replace('201.-', '').str.replace('-.*', '').astype(int) == 1]
df_jan_start = df_jan[df_jan[0].str.replace('201.-..-', '').str.replace(' .+', '').astype(int) < 4]
sorted_src_ids = sorted(list(df_jan_start[6]))[:]

df_jan_start[6] = sorted_src_ids

df_jan_start.to_csv(fout, index=False, header=None)

import time
time.sleep(1)

lines = open(fout).readlines()

with open(fout, 'w') as writer:
    for line in lines:
        writer.write(line.replace(',', ', '))

print(f'Wrote: {fout}')
