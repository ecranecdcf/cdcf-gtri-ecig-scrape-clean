class MergeData:
    def __init__(self, path):
        self.path = path
        self.dirs = os.listdir(path)
        self.final = ""
        
        conversions = {}
        for row in reader:
            key = row[0].strip()
            if key in conversions:
                # implement your duplicate row handling here
                pass
            conversions[key] = [x.strip() for x in row[1].split(',')]
        self.conversions = conversions
        
    
    def concat(self, source, targetCsvFile, product_type=""):
        print(source)
        df = pd.read_csv(targetCsvFile)
        for col in df.columns:
            name = col.lower()
            df.rename(columns={col : name}, inplace=True)

        df["product_type"] = product_type
        df["source"] = source

        if isinstance(self.final, str):
            self.final = df
        else:
            self.final = pd.concat([self.final, df], axis=0, ignore_index=True)

    def explore_dir(self, source, curr_path):
        #Items in a source folder are either csv files or files representing the type of product
        for item in os.listdir(curr_path):
            item_in_source_path = os.path.join(curr_path, item)

            #If item is not ipynb and it is not a file aka it is a directory
            if not os.path.isfile(item_in_source_path) and ".ipynb" not in item_in_source_path:
                product_type = item
                path_to_files_in_product = item_in_source_path

                products = os.listdir(path_to_files_in_product)
                for product in products:
                    #convert here and check item is not a jupyter checkpoint
                    if ".ipynb" not in product:
                        concat(source, os.path.join(path_to_files_in_product, product), product_type=product_type)
            else:
                #This means the items in the source folder are files and we should convert them
                #convert here
                if ".ipynb" not in item:
                    concat(source, os.path.join(curr_path,item))
    
    def join(self):
        #Top level, finds the source of what each individual thing looks for
        for source in tqdm(self.dirs):
            curr_path = os.path.join(path, source)

            if ".ipynb" not in curr_path:
                if not os.path.isfile(curr_path):
                    explore_dir(source, curr_path)
                    print()

    def clean_item(self, cell):
        if cell is np.nan:
            return np.nan

        try:
            cell = literal_eval(cell)

            if isinstance(cell, list):
                return cell
        except:
            pass

        if isinstance(cell, str):
            #print(cell.split(","))
            return cell.split(",")
        else:
            return list(cell)

    def flatten(self, cell):
        if isinstance(cell, list):
            new_list = []

            for item in cell:
                if isinstance(item, list):
                    for i in item:
                        if i is not np.nan and i != "nan":
                            new_list.append(i)
                else:
                    if item is not np.nan and item != "nan":
                        new_list.append(item)
            return new_list
        else:
            return cell

    def replace_list_nan(self, cell):
        if isinstance(cell, list):
            all_nan = True
            for item in cell:
                if item is not np.nan:
                    all_nan = False
                    break
            if all_nan:
                return np.nan
            else:
                return cell
        else:
            return cell