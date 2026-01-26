import os
import xarray as xr
import numpy as np
import pickle 
import scripts.preprocessing as proc
from scripts.globals import where_to_find_data

def compute_available_pct(region_folder, years_list, ref_depth):

    regions = proc.read_region_input_files(f'configs/{region_folder}_regions.input')
    groups = proc.obtain_boxes_grouping(regions)


    # Compute number of pixels that are not available because of bathymetry filter
    bathymetry = xr.open_dataarray('/data01/benassi/export-biomass/data/processed/bathymetry.nc')

    # Number of removed points because of bathymetry for each 10x10 square (total possible available in shelf)

    
    in_shelf_tot = [[
                    (
                      (proc.crop_square(bathymetry, box) >= ref_depth) #& 
                      #(proc.crop_square(bathymetry, box) <= 0)  
                    )\
                      .sum() 
                      for box in region] for region in regions.values()]
    

    off_shelf_dict = {}
    in_shelf_dict = {}
    tot_dict = {}
    for region, group, masks in zip(regions, groups, in_shelf_tot):
        
        # binary boxes with mapped cloud cover have already been generated. True = isnan = unavailable
        # in this way we import data where True = notnan
        boxes = [~xr.open_dataset(f'data_availability/{region_folder}/box_{n_box}.nc') for n_box in group]

        off_shelf_pct = []
        in_shelf_pct = []
        tot_pct = []

        for year_slice in years_list:
            # Select the year slice used for training
            train_set = [box.sel(time = year_slice) for box in boxes]
            
            # Compute the number of points that are marked as non nans
            # and take the minimum between sst, eudepth and chl (which is what drives the estimation)
            tot_available_points = [box.sum(dim = ['longitude', 'latitude']).to_array().min(axis = 0) for box in train_set]

            # Number of available in-shelf data per day
            path = where_to_find_data(region_folder)[abs(ref_depth)]

            # This comes from a bug in the generation of shelf_content. Non-shelf is simply put to zero, not to nan
            in_shelf = [
                (xr.open_dataarray(os.path.join(path, 'outputs', f'shelf_content/box_{box}.nc'))\
                    .sel(time = year_slice) > 0.) \
                    .sum(dim = ['longitude', 'latitude']) 
                    for box in group
                ]

            # Everything else available that is not in-shelf is off-shelf
            off_shelf = [(tot - in_sh).values for tot, in_sh in zip(tot_available_points, in_shelf)]

            # Total count (57600 in our case) is the total number of points
            tot_avails = [(box['chl'].count(dim = ['longitude', 'latitude'])).values for box in boxes]

            # This is the total possible number of off-shelf data
            off_shelf_tot = [(box - mask) for box, mask in zip(tot_avails, masks)]

            # Obtain a single number over the whole dynamical region for chl, sst and eudepth
            off_shelf_pct.append(
                np.array(off_shelf) / np.array(off_shelf_tot)
            )

            in_shelf_pct.append(
                np.array(in_shelf) / np.array(masks).reshape(-1,1)
            )

            tot_pct.append(
                np.array(tot_available_points) / np.array(tot_avails)
            )

        in_shelf_dict[region] = in_shelf_pct
        off_shelf_dict[region] = off_shelf_pct
        tot_dict[region] = tot_pct

    return in_shelf_dict, off_shelf_dict, tot_dict

def main():

    os.makedirs('pct_available', exist_ok = True)
    os.makedirs('pct_available/in_shelf', exist_ok = True)
    os.makedirs('pct_available/off_shelf', exist_ok = True)
    os.makedirs('pct_available/tot', exist_ok = True)

    for ref_depth in [250,500,1000,1500,2000]:
        for ebu in ['pacific', 'atlantic']:
            print(f'Preprocessing {ref_depth} m for {ebu}')
            in_shelf_dict, off_shelf_dict, tot_dict = compute_available_pct(ebu, [slice('2003-01-01', '2023-12-31')], -ref_depth)
            for name, dicti in zip(['in_shelf', 'off_shelf', 'tot'], [in_shelf_dict, off_shelf_dict, tot_dict]):
                filename = f'{ebu}_{ref_depth}.pkl'
                path = os.path.join('pct_available', name, filename)
                with open(path, 'wb') as f:
                    pickle.dump(dicti, f)
                    print(f'Saved {path}')


if __name__ == '__main__':
    main()
    