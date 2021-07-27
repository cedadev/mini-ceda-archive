import os
import glob
import shutil
import subprocess as sp
import time


data_dir_4_04 = '/badc/cru/data/cru_ts/cru_ts_4.04/data'
data_dir_4_05 = '/badc/cru/data/cru_ts/cru_ts_4.05/data'
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

    if fpath.endswith(".gz"):
        tmp_gzip = os.path.join(mini_dir, 'temp.nc.gz')
        print(f'[INFO] Gunzipping to temporary file: {tmp_gzip}')
        shutil.copy(fpath, tmp_gzip)

        sp.call(f'gunzip {tmp_gzip}', shell=True)

        nc_gz_path = output_path
        input_path = os.path.splitext(tmp_gzip)[0]
        output_path = os.path.splitext(output_path)[0]
    else:
        input_path = fpath

    cmd = f'ncks {extra} {lat_selector} {lon_selector} --variable {var_id} {input_path} {output_path}'
    print(f'[INFO] Running: {cmd}')
    sp.call(cmd, shell=True)

    if fpath.endswith(".gz"):
        print(f'[INFO] Removing: {input_path}')
        os.remove(input_path)

        print(f'[INFO] Gzipping: {output_path}')
        sp.call(f'gzip {output_path}', shell=True)
        output_path = nc_gz_path

    print(f'[INFO] OUTPUT: {output_path}')


def process_var(var_dir):
    
    # Try: "*.nc" and then "*.nc.gz" if no "*.nc" files
    files = glob.glob(f'{var_dir}/*.nc') or glob.glob(f'{var_dir}/*.1901.2*.nc.gz')

    if len(files) != 1:
        raise Exception(f'Expected one data file in directory, but found: {files}')

    fpath = files[0]
    create_subset_file(fpath)


def main():

    dir_var_map = {
        #data_dir_4_04: os.listdir(data_dir_4_04),
        data_dir_4_05: ["wet"]
    } 

    for dr in dir_var_map:
        print(f'[INFO] Working on: {dr}')
        var_ids = dir_var_map[dr]

        for var_id in var_ids:
            print(f'[INFO] Working on: {var_id}')

            var_dir = os.path.join(dr, var_id)
            process_var(var_dir)


if __name__ == '__main__':

    main()
