# CDCF Web Scraping Vape Products Project

## Data Scrapers

See `scraping` directory. For now these are in Jupyter notebooks and probably require some cleanup, but for the time being the notebooks are available for the following sites. 

- CS Vape
- Get Pop
- My Vapor Store
- Perfect Vape
- Vape.com
- Vape Sourcing
- Vape WH
- Vaping.com

Some of the original regular expression functios developed as a demo are available here, but we expect them to all eventually be replaced and/or migrated to the NLP code section.

## Data Model 

Eventually, all output will be mapped to this format. This is a work a in progress.

| Column Name             | Data Type    | Description                                                                                   |
|-------------------------|--------------|-----------------------------------------------------------------------------------------------|
| Brand                   | String       | Brand name of the product (from the dataset).                                          |
| Product                 | String       | Specific product name.                                                                        |
| SkuNumber               | Integer      | SKU identifier number for tracking and inventory.                                             |
| Price                   | String       | Price of the product, formatted as currency.                                                  |
| Description             | String       | Short description of the product, including flavor profile or unique attributes.              |
| E-liquid contents       | String       | Volume of e-liquid in the product, typically measured in ml.                                  |
| Puffs per Device        | Integer      | Number of puffs the device can provide.                                                       |
| Flavor                  | String       | Flavor profile or variety information for the product.                                        |
| Coil                    | String       | Type of coil used in the product, e.g., "Mesh Coil".                                          |
| Nic_level_1             | String       | Primary nicotine level designation, often in mg or percent.                                   |
| Nic_level_2             | String       | Secondary nicotine level designation if multiple strengths are offered.                       |
| Nic_level_3             | String       | Tertiary nicotine level designation if applicable.                                            |
| Iced_Variable           | Boolean      | Indicator if the flavor includes a menthol or "iced" variant.                                 |
| Nic_Free                | Integer      | Binary indicator (0 or 1) indicating if the product is nicotine-free.                         |
| TFN                     | Integer      | Binary indicator (0 or 1) if the product contains tobacco-free nicotine.                      |
| Product_Type            | String       | Classification of the product type, e.g., "Disposable System".                                |
| Internal_Features       | String       | Additional internal features of the device, if available.                                     |
| External_Features       | String       | Additional external features or specifications of the device.                                 |
| Country_of_Assembly     | String       | Country where the product was assembled or manufactured.                                      |


## Data Cleaning

TODO

## NLP

Currently a combo of regular expressions and LLMs. All under the `nlp/llm_code` folder.

- This contains a `datasets` folder with scraped data sets, in addition to some labeled data sets loaded for the fine-tuned model, the output sample data sets are also contained here. Notably, CS Vape and Vape WH are availble as sample outputs.
- Most functions can be executed through `nlp/llm_code/llama_vape_csvape_test.ipynb`

    - Some NLP functions are successfully loaded through regex functions in the `regex_functions.py` file. These include e-liquid contents and nicotine levels.
    - Other functions that use the LLM code, including prompts are available in `llm_functions.py`. Currently the LLM code uses a fine-tuned version of Meta's `Llama-3.1-8B-Instruct` model. Instructions for setting up this model are found under `doc/Instructions for downloading LLaMA LLM model.docx`.
    - An output viewer for a better understanding the NLP output is available in `output_explorer.ipynb`.
    
    
## Image Processing

TODO 

### Pre-processing

TODO

### VLM Code

TODO

#### Iced

TODO

#### Screens

TODO
