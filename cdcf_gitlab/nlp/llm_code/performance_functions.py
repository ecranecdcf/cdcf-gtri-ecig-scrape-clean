import pandas as pd

def performance_check(labeled_df_dir, output_df_dir, category):
    # Read in targeted csvs
    labeled_df = pd.read_csv(labeled_df_dir)
    output_df = pd.read_csv(output_df_dir)
    
    # Convert case to lower
    labeled_df.columns = labeled_df.columns.str.lower()   
    output_df.columns = output_df.columns.str.lower()
    
    # Extract relevant category column
    category_labeled = labeled_df[category]
    category_output = output_df[f"{category}_proc_llm"]
    
    ### JPJ: Change this in future iteration -- data format for TFN / CBD output should match labeled
    if category == 'tfn' or category == 'cbd':
        category_output = category_output.fillna("False -").str.contains("True").astype(int)
        
    matches = (category_labeled == category_output)
    matching_percentage = sum(matches) * 100 / len(matches)
    
    print(f"Matching percentage: {matching_percentage:.2f}%")
    
    
    
    
    
    