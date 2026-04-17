"""
This is a code that uploads the .png on the cloud radar dedicated bucket.
it works that it reads the files on the folder and the files on the bucket, and then 
uploads the files that are in the folder but not in the bucket.
author: Claudia Acquistapace
date: 16 Aprile 2026
email: claudia.acquistapace-at-unipd.it

how to run the code:
activate the venv and run the script with python3 -m process.upload_ch_ncdf_to_bucket

"""
import os
from glob import glob
from readers.data_buckets_funcs import init_s3, list_files_bucket, upload_to_bucket
import pdb

def main():

    # reading list of files from folder
    png_path = "/Users/claudia/Documents/Data/cloud_radar_Lampedusa/plots/samples/"
    # data bucket names
    bucket_name = "cloud-radar-ml-samples"

    # list all files in the folder (these are the files with 32 bits floating point data)  
    file_list = sorted(glob(os.path.join(png_path, "*.png")))
    print(f"number of files in the folder {png_path}: {len(file_list)}")
    print("******************************************************") 

    for file in file_list:

        print(file)
        print("******************************************************")
        # read list of files on the bucket
        s3 = init_s3()
        files_on_bucket = list_files_bucket(s3, bucket_name)
        print('files on bucket', files_on_bucket)
        pdb.set_trace()

        # read only filename from the path and check if it is already on bucket. skip if yes    
        filename = file.split("/")[-1]
        file_path = os.path.dirname(file)
        
        print(f"processing file {filename} to upload on bucket {bucket_name}")

        # check if file is in files_on_bucket. skip if yes
        if filename in files_on_bucket:
            print(f"file {filename} already on bucket {bucket_name}. skipping")
            continue
        else:               
            # reading filename full path
            filename = os.path.basename(file)
            
            # add prefix of site to the filename to avoid overwriting files with the same name from different sites
            filename = filename
            print(f"moving file {filename} on bucket {bucket_name}")
            print("******************************************************")
            check = upload_to_bucket(file_path, filename, bucket_name)
            if check:
                print(f"file {filename} moved on bucket {bucket_name}")
            else:
                print(f"file {filename} not moved on bucket {bucket_name}")
            print("******************************************************")
            print("******************************************************")


if __name__ == "__main__":
    main()