Code used for data analysis and plots of the paper "A satellite-based estimate of the contribution of filamentary structures to lateral carbon transport in the Pacific and Atlantic Upwelling systems"

![big_california_example](https://github.com/user-attachments/assets/d3195d68-3d65-46c9-9091-4f35384650bc)

# Setup experiment folder

- Create a folder for your experiment
- Inside this folder, create a configuration list named 'glob_config.yaml' with the following entries:

    data_path : '/path/to/your/data/pacific'
    ref_depth : -1000
    c_to_chl_ratio : 50
    n_clusters : 4
    time_period:
        start: '2003-01-01'
        end: '2012-12-31'

- Inside this folder, also create a 'regions.input' file with the boxes, similar as follows:

    {'California Current System' : [(-134, -124, 43, 53),
                                    (-130, -120, 33, 43),
                                    (-123, -113, 23, 33)],
    'Central America' : [(-115, -105, 13, 23),
                        (-105, -95, 9, 19),
                        (-95, -85, 6, 16),
                        (-85, -75, -1, 9)],
    'Humboldt Current System' : [(-88, -78, -11, -1),
                                (-80, -70, -21, -11),
                                (-79, -69, -31, -21),
                                (-81, -71, -41, -31),
                                (-82, -72, -51, -41)],
    }


# Run clustering and filament detection:

    python preprocess_data.py
    python run_clustering.py
    python create_filament_mask_dask.py

# Compute filament-area mass content

    python filament_content_timeseries.py # 

# Compute offshore-area mass content
    python compute_off_shelf_content_map.py # Creates filament content maps
    python compute_off_shelf_content_timeseries.py # Sums over longitude and latitude

# Compute in-shelf-area mass content
    python compute_shelf_content_map.py # Creates filament content maps
    python compute_shelf_content_timeseries.py # Sums over longitude and latitude

Transport estimates are provided inside the notebooks. Alternatively, you can use the following script:

