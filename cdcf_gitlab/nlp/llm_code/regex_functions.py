import re
import pandas as pd

### Function to extract nicotine levels from text
def find_nicotine_levels(text):
    text = str(text)

    # Updated regular expressions for nicotine values to capture decimals without leading zeros
    pattern_percent = r'(\d*\.?\d+)\s*(?:%|percent)'
    pattern_mg = r'(\d+\.?\d*)\s*(?:mg)'
    
    ### special cases
    zero_nicotine_pattern = r"\bZero Nicotine\b"

    # Find all matches for percent and mg values
    percent_matches = set(re.findall(pattern_percent, text, re.IGNORECASE))
    mg_matches = set(re.findall(pattern_mg, text, re.IGNORECASE))

    # Check for "Zero Nicotine" and add 0% if found
    if re.search(zero_nicotine_pattern, text, re.IGNORECASE):
        percent_matches.add('0.0')

    # Convert matches to numbers (handling float if needed)
    percent_list = sorted({float(match) for match in percent_matches if match.replace('.', '').isdigit()})
    mg_list = sorted({float(match) for match in mg_matches if match.replace('.', '').isdigit()})

    # Remove mg values that correspond to percentages (mg = percent * 10)
    mg_list = [mg for mg in mg_list if not any(abs(mg - percent * 10) < 1e-6 for percent in percent_list)]
    
    # Remove values greater than 70mg or 7% to prevent brittleness for pattern matches. Currently have not seen anything greater than these.
    percent_list = [percent for percent in percent_list if percent <= 7.0]
    mg_list = [mg for mg in mg_list if mg <= 70.0]

    # Handle various cases for return
    if len(percent_list) == 1 and not mg_list:
        return (str(percent_list[0]) + ' PERCENT', None)
    
    if len(mg_list) == 1 and not percent_list:
        return (str(int(mg_list[0])) + ' MG', None)
    
    if not mg_list and not percent_list:
        return 'UNKNOWN', None

    # Sort and gather all values, ensuring uniqueness
    all_values = []

    while percent_list or mg_list:
        if percent_list and (not mg_list or percent_list[0] < mg_list[0] / 10):
            all_values.append(str(percent_list.pop(0)) + ' PERCENT')
        elif mg_list:
            all_values.append(str(int(mg_list.pop(0))) + ' MG')

    return 'LEVELS', all_values

### Function to extract e-liquid values from text
### JPJ: I haven't seen anything indicative of multiple eliquid amounts--could update this if that is ever at thing. Would need to figure out how to code this per CDC.
def find_eliquid_contents(text):
    text = str(text)
    pattern_ml = r'(\d+\.?\d*)\s*(?:ml)'

    ml_match = set(re.findall(pattern_ml, text, re.IGNORECASE))
    ml_list = [float(match) for match in ml_match]

    if not ml_list:
        return None
    else:
        return (str(ml_list[0]) + " mL")  

### Function to populate nicotine and e-liquid values
def populate_nicotine_and_eliquid(df):
    if 'FINAL_Nicotine_Levels' not in df.columns:
            df['FINAL_Nicotine_Levels'] = pd.NA
    if 'FINAL_E-liquid contents' not in df.columns:
            df['FINAL_E-liquid contents'] = pd.NA
    
    for idx, row in df.iterrows():     
        nic_lvl, values = find_nicotine_levels(row['all_text']) #if pd.isnull(row['FINAL_Nicotine_Levels']) else find_nicotine_levels(row['FINAL_Nicotine_Levels'])
        if values:
            df.at[idx, 'FINAL_Nicotine_Levels'] = nic_lvl
            for i in range(len(values)):
                df.at[idx, f'FINAL_Nic_level_{i+1}'] = values[i]
        else:
            df.at[idx, 'FINAL_Nicotine_Levels'] = nic_lvl

        # Search e-liquid contents across all description columns
        if pd.isnull(row['FINAL_E-liquid contents']):
            liq_cont = find_eliquid_contents(row['all_text'])
            df.at[idx, 'FINAL_E-liquid contents'] = liq_cont

    return df
 
### Regex for finding nicotine free by checking the different 
def find_nic_free(row):   
    if row['FINAL_Nicotine_Levels'] == 'LEVELS':
        if row['FINAL_Nic_level_1'] == '0 PERCENT' or row['FINAL_Nic_level_1'] == '0 MG':
            nic_free = '0*'
        else:
            nic_free = 0
    elif row['FINAL_Nicotine_Levels'] in ['0 PERCENT', '0 MG']:
        nic_free = 1
    elif row['FINAL_Nicotine_Levels'] == 'UNKNOWN':
        nic_free = 'UNKNOWN'
    else:
        nic_free = 0
    return nic_free

### Function to populate nicotine free 
def populate_nic_free(df):
    if 'FINAL_Nic_Free' not in df.columns:
        df['FINAL_Nic_Free'] = pd.NA 
    df['FINAL_Nic_Free'] = df.apply(find_nic_free, axis=1)
    return df

### Function to extract flavors and descriptions into a dictionary 
### JPJ: Currently only for vapedotcom
def extract_flavors_with_descriptions(dataset, text):
    # remove empty fields
    if not isinstance(text, str) or text == ':': 
        return {}
    # Split the input text into lines or separators 
    flavor_lines = re.split(r'\n|,', text)  
    flavor_dict = {}

    for line in flavor_lines:
        line = line.strip()
        if not line:
            continue
        
        ### vapedotcom - most common patterns
        if dataset == 'vapedotcom':
            match = re.match(r"^(.*?)(?:\s*â€“|\s*-\s*|\s*\|)\s*(.*)$", line)
            if match:
                flavor = match.group(1).strip()
                description = match.group(2).strip()
                flavor_dict[flavor] = description
            else:
                flavor_dict[line] = None
        ### vapewh - most common patterns
        elif dataset == 'vapewh':
            normalized_text = re.sub(r'\n(?![A-Za-z0-9 ]+[:\-])', ' ', text)
            match = re.findall(r'([A-Za-z0-9 *()]+)(?:\s*[:\-]\s*(.*?))?(?=(?:[A-Za-z0-9 *()]+[:\-])|$)', normalized_text, re.DOTALL)
            for flavor, description in flavor_lines:
                flavor = flavor.strip()
                description = description.strip() if description else None
                flavor_dict[flavor] = description
        
    return flavor_dict
