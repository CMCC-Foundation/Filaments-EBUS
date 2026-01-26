def plot_export_values_with_errorbar(exports, errors, ax, c, l):
    max_exports = exports + errors
    min_exports = exports - errors
    y = [[1, max_exports.iloc[0]], [2, max_exports.iloc[1]], [5, max_exports.iloc[2]], [10, max_exports.iloc[3]], [15, max_exports.iloc[4]],
         [15, min_exports.iloc[4]], [10, min_exports.iloc[3]], [5, min_exports.iloc[2]], [2, min_exports.iloc[1]], [1, min_exports.iloc[0]]]
    
    
    polygon = mpatches.Polygon(y, alpha = 0.2, color = c)
    ax.add_patch(polygon)

    ax.plot([1, 2, 5, 10, 15], exports, label = l, color = c, marker = 'o')

    #ax.legend()

    return ax

def prepare_export_errors_data(ebu):

    cols = ['1year', '2years', '5years', '10years', '15years']

    export_files = [f'{ebu}/{col}/outputs/carbon_exports.csv' for col in cols]

    regions = read_region_input_files(f'{ebu}/2years/regions.input')

    groups = obtain_boxes_grouping(regions)

    export_dataset = pd.DataFrame(index = regions.keys(), columns = cols)
    errors_dataset = pd.DataFrame(index = regions.keys(), columns = cols)

    for file, c in zip(export_files, ['1year', '2years', '5years', '10years', '15years']):
        export = pd.read_csv(file, index_col = 0)
        export_dataset[c] = [export.loc[g]['export'].sum().T for g in groups]
        errors_dataset[c] = [export.loc[g]['error'].sum().T for g in groups]

    return export_dataset, errors_dataset

def plot_sensitivity_export(ax, region, colors):

    export_dataset, errors_dataset = prepare_export_errors_data(region)
    for d, l, c  in zip(export_dataset.index, export_dataset.index, colors):
        plot_export_values_with_errorbar(export_dataset.loc[d], errors_dataset.loc[d], ax, c, l)

    #ax.legend()
    ax.set_xlabel('Clustering years', fontsize = 15)
    ax.set_title('Export value [TgC yr$^{-1}$]', fontsize = 15)
    ax.set_xticks([1, 2, 5, 10, 15])
    ax.grid()

    return ax

def plot_num_streamers(ax, region, colors):

    dataset = compute_number_streamers(region)
    for l, c  in zip(dataset.index, colors):
        ax.plot([1, 2, 5, 10, 15], dataset.loc[l], label = l, color = c, marker = 'o')

    #ax.legend()
    ax.set_xlabel('Clustering years', fontsize = 15)
    ax.set_title('Number of pixels labelled as streamers', fontsize = 15)
    ax.set_xticks([1, 2, 5, 10, 15])
    ax.grid()

    return ax
    
def compute_number_streamers(ebu):

    cols = ['1year', '2years', '5years', '10years', '15years']

    mask_path = [f'sensitivity_test_years/{ebu}/{col}/outputs/streamers_masks/' for col in cols]

    regions = read_region_input_files(f'configs/{ebu}_regions.input')

    groups = obtain_boxes_grouping(regions)

    dataset = pd.DataFrame(index = regions.keys(), columns = cols)
    
    for file, c in zip(mask_path, ['1year', '2years', '5years', '10years', '15years']):
        
        dataset[c] = [np.sum([xr.open_dataarray(os.path.join(file, f"box_{box}.nc")).sum() for box in group]) for group in groups]

    return dataset
    
    