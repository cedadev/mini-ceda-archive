#!/usr/bin/env python

"""
generate-ukcp18.py
==================

Generates subsets from UKCP18 data.

"""

import os
import glob
import shutil
import subprocess as sp
import time


source_files = """/badc/ukcp18/data/land-cpm/uk/2.2km/rcp85/01/rss/day/latest/rss_rcp85_land-cpm_uk_2.2km_01_day_20671201-20681130.nc
/badc/ukcp18/data/land-cpm/uk/2.2km/rcp85/08/rss/day/latest/rss_rcp85_land-cpm_uk_2.2km_08_day_20671201-20681130.nc

/group_workspaces/jasmin2/ukcp18/incoming-astephen/ukcordex-example/tasmax_rcp85_land-rcm_uk_12km_EC-EARTH_r12i1p1_HIRHAM5_day_19801201-19901130.nc
/gws/nopw/j04/cmip6_prep_vol1/ukcp18/data/land-prob/v20211110/uk/25km/rcp85/sample/b8110/30y/cltAnom/mon/v20211110/cltAnom_rcp85_land-prob_uk_25km_sample_b8110_30y_mon_20091201-20991130.nc""".split()

mini_archive = './archive'
mini_gws = './group_workspace'


def create_dir(dr):
    if not os.path.isdir(dr):
        os.makedirs(dr)


def create_subset_file(fpath):

    print(f'[INFO] Creating subset file')
    print(f'[INFO] INPUT: {fpath}')
    dr, fname = os.path.split(fpath)

    if fpath.startswith("/g"):
        mini_dir = mini_gws + dr
        step = 6
        extra = f'-d projection_y_coordinate,,,{step} -d projection_x_coordinate,,,{step}'
        if "sample" in fpath: 
            extra += ' -d sample,,,25'
    else: 
        mini_dir = mini_archive + dr
        step = 50
        extra = f'-d grid_longitude,,,{step} -d grid_latitude,,,{step}'

    create_dir(mini_dir)

    output_path = os.path.join(mini_dir, fname)
    
    time_selector = ''
    input_path = fpath

    cmd = f'ncks {extra} {time_selector} {input_path} {output_path}'
    print(f'[INFO] Running: {cmd}')
    sp.call(cmd, shell=True)

    print(f'[INFO] OUTPUT: {output_path}')


def main():

    for fpath in source_files:
        print(f'[INFO] Working on: {fpath}')
        create_subset_file(fpath)


if __name__ == '__main__':

    main()
