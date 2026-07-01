from dask.distributed import Client
import xarray as xr
import pandas as pd
import ast
import os
import numpy as np
from tqdm import tqdm
from omegaconf import OmegaConf

import warnings
warnings.filterwarnings('ignore')

from scripts.preprocessing import *

"""
Preprocessing script for preparing delta time series of chlorophyll and SST data for specified regions. 
The script reads region definitions from an input file, processes the data in parallel using Dask, and saves the resulting anomaly data to CSV files.
"""

if __name__ == '__main__':

    print('Reading regions')
    # Reading the input regions with the boxes from the regions.input file
    regions = read_region_input_files('regions.input')
    print(f'Found regions: {regions.keys()}')

    # Global configurations are stored in the glob_config.yaml file
    cfg = OmegaConf.load('glob_config.yaml')
    print(f'Configuration loaded from glob_config.yaml: {cfg}')

    # Specifying the clustering time period
    time_period = cfg.time_period
    print(f'Preprocessing data in range {time_period["start"]} - {time_period["end"]}')

    # Dask client opening for code profiling
    client = Client()
    print(client.dashboard_link)

    print(f'Saving to {os.getcwd()}/outputs/train_data/')
    # The train_data folder is created in case it is not existing
    if not os.path.exists('outputs/train_data/'):
        print('train_data folder is missing. Creating it.')
        os.makedirs('outputs/train_data/')

    # Main loop start
    for label, boxes in regions.items():
            print(f'Preparing data for {label}')
            
            deltas = pd.DataFrame(columns = ['chl', 'sst'])
            if os.path.exists(f'outputs/train_data/{label}.csv'):
                print(f'File outputs/train_data/{label}.csv already exists. Skipping this region.')
                continue

            for i, box in enumerate(tqdm(boxes)):
                chl_path = os.path.join(cfg.data_path, 'chl', f'box_{i+1}.nc')
                sst_path = os.path.join(cfg.data_path, 'sst', f'box_{i+1}.nc')
                bathy_path = os.path.join(cfg.data_path, 'bathymetry', f'box_{i+1}.nc')

                deltas_box = prepare_training_data(box, chl_path, sst_path, bathy_path, cfg.ref_depth, time_period['start'], time_period['end'])

                deltas = pd.concat([deltas, deltas_box.compute()])

            print(f'Saving as outputs/train_data/{label}.csv')
            deltas.to_csv(f'outputs/train_data/{label}.csv')

    client.close()