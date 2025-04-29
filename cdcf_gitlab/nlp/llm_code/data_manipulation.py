import pandas as pd

def random_sample(df, n=50):
    sampled_df = df.sample(n)
    return sampled_df

def merge_text(df, source):
    source_name = source.split('_')[0]
    columns_map = {
        'csvape': ['title', 'flavor_list', 'description', 'warning_description', 'ingredients_description', 
                   'key_features_description', 'flavors_description', 'why_description', 'nicotine_description', 'innovation_description', 'e_liquid_description', 'prefilled_description'],
        # 'getpop': ['title', 'flavor_list', 'description', 'warning_description', 'ingredients_description', 
        #            'key_features_description', 'flavors_description', 'why_description', 'nicotine_description'],
        # 'myvaporstore': ['title', 'flavor_list', 'description', 'warning_description', 'ingredients_description', 
        #                  'key_features_description', 'flavors_description', 'why_description', 'nicotine_description'],
        'vapedotcom': ['title', 'description', 'warning_description', 'ingredients_description', 
                        'key_features_description', 'flavors_description', 'nicotine_description'],
        # 'perfectvape': ['title', 'flavor_list', 'description', 'warning_description', 'ingredients_description', 
        #                 'key_features_description', 'flavors_description', 'why_description', 'nicotine_description'],
        'vapewh': ['title', 'flavors_section', 'specifications_section', 'description', 'key_features_description', 
                   'specifications_description', 'nicotine_description', 'e_liquid_description']
    }
    
    columns_to_merge = columns_map.get(source_name, [])
    
    if columns_to_merge:
        df['all_text'] = df[columns_to_merge].apply(lambda row: '\n'.join(row.dropna().astype(str).replace('', float('NaN')).dropna()), axis=1)
    
    return df

