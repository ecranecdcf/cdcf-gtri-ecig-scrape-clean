import re
import pandas as pd

# Function to extract nicotine levels from text
def find_nicotine_levels(text):
    text = str(text)

    pattern_percent = r'(\d*\.?\d+)\s*(?:%|percent)'
    pattern_mg = r'(\d+\.?\d*)\s*(?:mg)'
    zero_nicotine_pattern = r"\bZero Nicotine\b"

    percent_matches = set(re.findall(pattern_percent, text, re.IGNORECASE))
    mg_matches = set(re.findall(pattern_mg, text, re.IGNORECASE))

    if re.search(zero_nicotine_pattern, text, re.IGNORECASE):
        percent_matches.add('0.0')

    percent_list = sorted({float(m) for m in percent_matches if m.replace('.', '').isdigit()})
    mg_list = sorted({float(m) for m in mg_matches if m.replace('.', '').isdigit()})

    mg_list = [mg for mg in mg_list if not any(abs(mg - pct * 10) < 1e-6 for pct in percent_list)]

    percent_list = [pct for pct in percent_list if pct <= 7.0]
    mg_list = [mg for mg in mg_list if mg <= 70.0]

    if len(percent_list) == 1 and not mg_list:
        return (str(percent_list[0]) + ' PERCENT', None)

    if len(mg_list) == 1 and not percent_list:
        return (str(int(mg_list[0])) + ' MG', None)

    if not mg_list and not percent_list:
        return 'UNKNOWN', None

    all_values = []

    while percent_list or mg_list:
        if percent_list and (not mg_list or percent_list[0] < mg_list[0] / 10):
            all_values.append(str(percent_list.pop(0)) + ' PERCENT')
        elif mg_list:
            all_values.append(str(int(mg_list.pop(0))) + ' MG')

    return 'LEVELS', all_values

# Function to extract e-liquid values from text
def find_eliquid_contents(text):
    text = str(text)
    pattern_ml = r'(\d+\.?\d*)\s*(?:ml)'
    matches = set(re.findall(pattern_ml, text, re.IGNORECASE))
    values = [float(m) for m in matches]

    if not values:
        return None

    return f"{values[0]} mL"

# Function to populate nicotine and e-liquid values
def populate_nicotine_and_eliquid(df):
    if 'FINAL_Nicotine_Levels' not in df.columns:
        df['FINAL_Nicotine_Levels'] = pd.NA

    if 'FINAL_E-liquid contents' not in df.columns:
        df['FINAL_E-liquid contents'] = pd.NA

    product_text = (
        df.get('product_name', pd.Series('', index=df.index)).astype(str).fillna('') + ' ' +
        df.get('description', pd.Series('', index=df.index)).astype(str).fillna('')
    )

    for idx, row in df.iterrows():
        text = product_text.loc[idx]

        nic_lvl, values = find_nicotine_levels(text)

        if values:
            df.at[idx, 'FINAL_Nicotine_Levels'] = nic_lvl
            for i, val in enumerate(values):
                df.at[idx, f'FINAL_Nic_level_{i+1}'] = val
        else:
            df.at[idx, 'FINAL_Nicotine_Levels'] = nic_lvl

        if pd.isnull(row['FINAL_E-liquid contents']):
            df.at[idx, 'FINAL_E-liquid contents'] = find_eliquid_contents(text)

    return df

# Function to determine nicotine-free status
def find_nic_free(row):
    lvl = row['FINAL_Nicotine_Levels']

    if lvl == 'LEVELS':
        return '0*' if row.get('FINAL_Nic_level_1') in ['0 PERCENT', '0 MG'] else 0

    if lvl in ['0 PERCENT', '0 MG']:
        return 1

    if lvl == 'UNKNOWN':
        return 'UNKNOWN'

    return 0

# Function to populate nicotine-free values
def populate_nic_free(df):
    df['FINAL_Nic_Free'] = df.apply(find_nic_free, axis=1)
    return df
