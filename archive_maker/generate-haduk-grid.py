#!/usr/bin/env python

"""
generate-haduk-grid.py
======================

Generates subsets from HadUK-Grid Met Office data.

Example data/info:

```
/badc/ukmo-hadobs/data/insitu/MOHC/HadOBS/HadUK-Grid/v1.0.3.0/1km/
vars: snowLying & groundfrost
Freq: mon

/badc/ukmo-hadobs/data/insitu/MOHC/HadOBS/HadUK-Grid/v1.0.3.0/1km/snowLying/mon/v20210712/snowLying_hadukgrid_uk_1km_mon_{year}01-{year}12.nc 
where {year} is 1971..2019
```
"""

import os
import glob
import shutil
import subprocess as sp
import time


datasets = {
  "v1.0.3.0": [
    "/badc/ukmo-hadobs/data/insitu/MOHC/HadOBS/HadUK-Grid/v1.0.3.0/1km/groundfrost/mon/v20210712/groundfrost_hadukgrid_uk_1km_mon_196101-196112.nc",
    "/badc/ukmo-hadobs/data/insitu/MOHC/HadOBS/HadUK-Grid/v1.0.3.0/1km/snowLying/mon/v20210712/snowLying_hadukgrid_uk_1km_mon_197101-197112.nc"
  ],
  "v1.0.2.1": [
    "/badc/ukmo-hadobs/data/insitu/MOHC/HadOBS/HadUK-Grid/v1.0.2.1/1km/snowLying/mon/v20200731/snowLying_hadukgrid_uk_1km_mon_197101-197112.nc"
  ]
}

mini_archive = './archive'


def create_dir(dr):
    if not os.path.isdir(dr):
        os.makedirs(dr)


def create_subset_file(fpath):

    print(f'[INFO] Creating subset file')
    print(f'[INFO] INPUT: {fpath}')
    dr, fname = os.path.split(fpath)

    mini_dir = mini_archive + dr
    create_dir(mini_dir)

    output_path = os.path.join(mini_dir, fname)
    
    var_id = fname.split("_")[0]
    time_selector = '-d time,,,12'
    extra = '-d projection_x_coordinate,,,10 -d projection_y_coordinate,,,10'

    input_path = fpath

    cmd = f'ncks {extra} {time_selector} --variable {var_id} {input_path} {output_path}'
    print(f'[INFO] Running: {cmd}')
    sp.call(cmd, shell=True)

    print(f'[INFO] OUTPUT: {output_path}')


def main():

    for version, ncpaths in datasets.items():

        for fpath in ncpaths:
            print(f'[INFO] Working on: {fpath}')
            create_subset_file(fpath)


if __name__ == '__main__':

    main()
