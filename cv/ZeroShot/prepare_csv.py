import pandas as pd
import pickle
import os 

text_paths = {
    'csvape' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/csvape/csvape_scrape.csv',
    'getpop' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/getpop/getpop_ecig.csv',
    'mipod' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/mipod/product_type_mipod.csv',
    'myvaporstore': 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/myvaporstore/myvaporstore_scrape.csv',
    'perfect_vape' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/perfect_vape/perfectvape_scrape.csv',
    'vapedotcom' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/vapedotcom/vapedotcom_scrape.csv',
    'vapesourcing' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/vapesourcing/vapesourcing_scrape.csv',
    'vapewh' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/vapewh/vapewh_scrape.csv',
    'vapingdotcom' : 'projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/vapingdotcom/vapingdotcom_scrape.csv'
}
def find_site(path):
    for site in text_paths.keys():
        if site in path:
            return site
def get_descs(base_path):
    descs = {}
    for site in text_paths:
        descs[site] = {}
    for site in text_paths:
        text_data = pd.read_csv(base_path + text_paths[site])
        if  'mipod' in site:
            for i in text_data.index:
                name = text_data.loc[i, "Product"]
                desc = text_data.loc[i, "Description"]
                descs[site][name] = desc
        else:
            for i in text_data.index:
                name = text_data.loc[i, "tag"]
                desc = text_data.loc[i, "description"]
                descs[site][name] = desc
    return descs
def main():
    base_path = os.path.expanduser("~") + "/../../"
    descs = get_descs(base_path)
    
    with open("vapes.pkl", "rb") as file:
        positions = pickle.load(file)
    cropping = {}
    for eg in positions:
        cropping[eg[1]] = (eg[5],eg[4],eg[3],eg[2])
    with open("zeroshotscreen.pkl", "rb") as file:
        data = pickle.load(file)
    site = []
    path = []
    description = []
    label = []
    lower = []
    upper = []
    left = []
    right = []
    yes = ['Yes', 'Yes,', 'Yes.', 'yes', 'yes.','yes,']
    no = ['No', 'No,','No.' 'yes', 'yes.', 'yes,']
    print(len(data))
    for result in data:
        website = find_site(result[0])
        start_idx = result[1].find(':') + 2
        end_idx = result[1].find('Description')-1
        if end_idx == -2:
            vape = result[1][start_idx:]
        else:
            vape = result[1][start_idx: end_idx]
        if len(vape) == 0:
            print(result[1])
            continue
        if vape.find('image') != -1:
            new_end = vape.find('image')
            vape = vape[:new_end-1]
        if vape.find('imag') != -1:
            new_end = vape.find('imag')
            vape = vape[:new_end-1]
        if vape[-1] == '-':
            vape = vape[:-1]
        try:
            description.append(descs[website][vape])
            
        except KeyError:
            continue
            
        for res in result[2]:
            if res in yes:
                label.append(1)
                break
            if res in no:
                label.append(0)
                break
        
        path.append(result[0])
        site.append(website)
        lower.append(cropping[result[0]][0])
        upper.append(cropping[result[0]][1])
        left.append(cropping[result[0]][2])
        right.append(cropping[result[0]][3])
        
    data = {"site" : site, "path" : path, "description":description, "label":label, "lower":lower, "upper":upper, "left":left,"right":right}
    csv = pd.DataFrame(data)
    csv.to_csv("../Finetuning/res.csv", index = False)
if __name__ == "__main__":
    main()