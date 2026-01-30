<<<<<<< HEAD
# Make the directories

Create the data directory in your preferred path

mkdir data
mkdir data/CHL
mkdir data/KD
mkdir data/SST

# CHL and KD data
=======
# CHL and KD490 data
>>>>>>> 53257a52fb6507726a63bc69dd46dc62d30e784b

1. Run the get_chl_files and get_kd_files .py scripts
2. These scripts will save data_urls.txt files with the links to download the data in the respective CHL/KD folders
3. Move into the data/CHL or data/KD folders:
    cd data/CHL
3. Run wget -i data_urls.txt  > log.txt to download the data

# SST data

1. Create the .urs_cookies file by following this guide:

https://oceancolor.gsfc.nasa.gov/data/download_methods/

2. Create the file list:

https://oceandata.sci.gsfc.nasa.gov/api/file_search/

3. Move to data/SST

4. Copy and paste this command:

wget -q --post-data="results_as_file=1&sensor_id=7&dtid=1052&sdate=2003-01-01 00:00:00&edate=2023-12-31 23:59:59&subType=1&period=DAY" -O - https://oceandata.sci.gsfc.nasa.gov/api/file_search 
| grep "4km" > file_list.txt

5. Then run the following command to add the full link to the data for the wget:

sed -i s#^#https://oceandata.sci.gsfc.nasa.gov/ob/getfile/# file_list.txt

6. Finally, the wget command:

wget --load-cookies ../.urs_cookies --save-cookies ../.urs_cookies --auth-no-challenge=on --content-disposition -i file_list.txt 


# GEBCO bathymetry

Download from official GEBCO distribution:

https://www.bodc.ac.uk/data/open_download/gebco/gebco_2024/zip/


