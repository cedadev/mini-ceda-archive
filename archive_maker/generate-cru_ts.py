import os
import glob
import subprocess as sp


data_dir = '/badc/cru/data/cru_ts/cru_ts_4.04/data'
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
    
    var_id = os.path.basename(dr)
    lat_selector = '-d lat,,,100'
    lon_selector = '-d lon,,,100'
    extra = ''

    cmd = f'ncks {extra} {lat_selector} {lon_selector} --variable {var_id} {fpath} {output_path}'
    print(f'[INFO] Running: {cmd}')

    sp.call(cmd, shell=True)

    print(f'[INFO] OUTPUT: {output_path}')


def process_var(var_dir):
    
    nc_files = glob.glob(f'{var_dir}/*.nc')
    if len(nc_files) != 1:
        raise Exception(f'Expected one file ".nc" file in directory, but found: {nc_files}')

    fpath = nc_files[0]
    create_subset_file(fpath)


def main(dr=data_dir):

    var_ids = os.listdir(data_dir)

    for var_id in var_ids:
        print(f'[INFO] Working on: {var_id}')

        var_dir = os.path.join(dr, var_id)
        process_var(var_dir)


if __name__ == '__main__':

    main()
