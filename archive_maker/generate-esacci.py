#!/usr/bin/env python

"""
generate-esacci.py
==================

Generates subsets from ESA CCI data.

"""

import os
import glob
import shutil
import subprocess as sp
import time


source_files = """/gws/nopw/j04/esacci_portal/fire/SYN/FireCCIS310/Grid/20190101-ESACCI-L4_FIRE-BA-SYN-fv1.0.nc 
/neodc/esacci/sea_ice/data/sea_ice_thickness/L3C/envisat/v2.0/SH/2012/ESACCI-SEAICE-L3C-SITHICK-RA2_ENVISAT-SH50KMEASE2-201202-fv2.0.nc""".split()

mini_archive = './archive'
mini_gws = './group_workspace'


def create_dir(dr):
    if not os.path.isdir(dr):
        os.makedirs(dr)


def create_subset_file(fpath):

    print(f'[INFO] Creating subset file')
    print(f'[INFO] INPUT: {fpath}')
    dr, fname = os.path.split(fpath)

    step = 25

    if fpath.startswith("/g"):
        mini_dir = mini_gws + dr
        extra = f'-d lat,,,{step} -d lon,,,{step}'
    else: 
        mini_dir = mini_archive + dr
        extra = f'-d yc,,,{step} -d xc,,,{step}'

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
