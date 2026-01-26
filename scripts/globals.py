COLORS = {'California Current System': '#1b9e77',
          'Central America': '#d95f02',
          'Humboldt Current System': '#7570b3',
          'Canary Current System': '#e7298a',
          'Central Africa': '#66a61e',
          'Benguela Current System': '#e6ab02'}

def where_to_find_data(region):

    return {250 : f'../estimate_250m/{region}',
            500 : f'../estimate_500m/{region}',
            1000 : f'../estimate_1000m/{region}',
            1500 : f'../estimate_1500m/{region}',
            2000 : f'../estimate_2000m/{region}'}