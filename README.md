# Filaments-EBUS

Code used for the data analysis and figures of the paper "A satellite-based estimate of the contribution of filamentary structures to lateral carbon transport in the Pacific and Atlantic Upwelling systems".

![big_california_example](https://github.com/user-attachments/assets/d3195d68-3d65-46c9-9091-4f35384650bc)

## What is in this folder

This directory contains the scripts, configs, notebooks, and outputs used to reproduce the paper workflow. The main processing steps are:

1. preprocess chlorophyll and SST anomalies
2. cluster the joint anomaly space
3. detect filament pixels
4. compute filament, shelf, and offshore carbon content
5. assemble the transport estimates and paper figures


## Set up an experiment folder

Create one folder per experiment and place the configuration files there. The scripts expect to run from inside that folder. 


### `glob_config.yaml`

Use a configuration file similar to the one below:

```yaml
data_path: '/path/to/your/data/' 
ref_depth: -1000
c_to_chl_ratio: 50
n_clusters: 4
time_period:
  start: '2003-01-01'
  end: '2012-12-31'
```

See below for expected data structure.

### `regions.input`

Define the regional boxes in a `regions.input` file. It is structured as a dictionary with the dynamical region name (e.g. California Current system) and a list of tuples defining the boxes limits. The coordinates inside the tuples have to be specified as `(lon_min, lon_max, lat_min, lat_max)`. For example:

```python
{
    'California Current System': [(-134, -124, 43, 53),
                                  (-130, -120, 33, 43),
                                  (-123, -113, 23, 33)],
    'Central America': [(-115, -105, 13, 23),
                        (-105, -95, 9, 19),
                        (-95, -85, 6, 16),
                        (-85, -75, -1, 9)],
    'Humboldt Current System': [(-88, -78, -11, -1),
                                (-80, -70, -21, -11),
                                (-79, -69, -31, -21),
                                (-81, -71, -41, -31),
                                (-82, -72, -51, -41)],
}
```

### Data structure

`data_path` folder should be structured as follows:

```
data_folder/
    chl/
        box_1.nc
        ...
    eudepth/
        box_1.nc
        ...
    sst/
        box_1.nc
        ...
    bathymetry/
        box_1.nc
        ...
```

## Processing workflow

Run the scripts in the following order:

```bash
python preprocess_data.py
python run_clustering.py
python create_filaments_masks_dask.py
```

Then compute the different carbon content diagnostics:

```bash
python filament_content_timeseries.py
python compute_off_shelf_content_map.py
python compute_off_shelf_content_timeseries.py
python compute_shelf_content_map.py
python compute_shelf_content_timeseries.py
```

`compute_off_shelf_content_map.py` and `compute_shelf_content_map.py` create the gridded content maps, while the corresponding `*_timeseries.py` scripts integrate them over longitude and latitude.

## Resulting folder structure 

The resulting folder structure after running the scripts should be as follows

```
project/
    outputs/
        train_data/ # Csv data used for fitting clustering
            California Current System.csv
            ...
                train_data/
        models/ # K-means clustering fitted model
            California Current System.joblib
            ...
        labels/ # .npy labels of each entry inside training data
            California Current System.npy
        filament_masks/ # (n_time, lon, lat) time series of binary filament masks
            box_1.nc
            ...
        filament_content_timeseries/ # (n_time,) time series of daily filament content
            box_1.nc
            ...
        off_shelf_content_map/ # (n_time, lon, lat) time series of off-shelf carbon content
            box_1.nc
            ...
        off_shelf_content_timeseries/ # (n_time,) time series of daily off-shelf content (integrated over lon, lat)
            box_1.nc
            ...
        oshelf_content_map/ # (n_time, lon, lat) time series of in-shelf carbon content
            box_1.nc
            ...
        shelf_content_timeseries/ # (n_time,) time series of in-shelf carbon content (integrated over lon, lat)
            box_1.nc
            ...
```

## Transport estimates

The transport estimates shown in the paper are assembled in the notebooks under `notebooks/`, especially `notebooks/paper_figures_and_transport_estimates.ipynb`.



