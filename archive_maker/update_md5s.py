import os


for (dr, _, files) in os.walk('./archive'):

    for fname in files:
        fpath = os.path.join(dr, fname)
        md5name = os.path.join(dr, fname + '.md5')
        os.system(f'md5sum {fpath} > {md5name}')
        print(f'Wrote: {md5name}')

