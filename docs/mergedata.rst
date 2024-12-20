.. "CDCF ecig Documentation Page"

Merging Data
===========================

Scrapped data is put into several different folders, each with their own unique variables and formating types. To aid in future data anlysis, manipulation and additions, a script has be written to combine all csv files of data located in the data folder of the merge data subfolder. Additionally, future scrapped data and any additional cleaning and formatting needed can be added with ease.

Relevant Files and Folders
------------------
* data folder contains all the csv files that we want to merge together
    - This folder is organized by the source of the data. You can put as many csvs in one source folder as you want
    - Folders must be named what you want the source to appear as in the merged dataset
    - Do not nest csvs within folders. Leave them as is
* Concat.ipynb is where the functionalities and implementation code exists
    - Running the notebook from start to finish will output a merged_data.csv file
    - Notebook is modified into a few different sections for clarity and organization. You can add more to these sections as needed by adding more cells to each section or by adding more code to a cell
* conversions.xlsx and conversions.csv
    - the xlsx file is editable and will contain a mapping of current columns that exist to columns desired in the final output. You should add on to this file as you add more scrapped data.
    - The csv file is what Concat.ipynb uses to  merge dataframe columns together. This file should be overwritten every time the xlsx counterpart is changed. You can do this by using the save as option in excel
    - MergeData.py is a WIP script that houses all the functionalities of Concat which will make using functions and readbility better in the future
    
Steps for adding new data
------------------
1) In the data folder, create a new folder and name it after where the data came from
2) Put all relevant csv files in the newly created source folder
3) Go into conversions.xlsx and add new mappings or add to existing mappings of desired columns to columns you have in the newly added data
4) Convert the xlsx file into a csv file
5) Run Concat.ipynb from start to finish
6) Optionally add any additionaly cleaning that applies to newly added variables or adjusted variables


All Columns and What they Mean
------------------
* - Variable Name
    - Description of Variable
* - tag
    - For NLP and CV parts of the project, we need to link the product to the images. This tag is the id that lets us pair data points to images
* - image_urls
    - Image urls are the downloadable links we scrap off the different sources so we can access the pictures at any time without need to rescrap data
* - compare_price
    - Some sources have a comparative price between what they sell at versus what other vendors sell their products at
* - stock_status
    - This tells us whether a product is in stock or not
* - description
    - This is the raw description data we base many of our other variables off from certain sources. This is here to prevent the need for rescrapping
* - package_contents_description
    - Products are sometime sold in multiples or singles. Most commonly, you will see 1x or 5x to represent how many count of each item is present in the product being sold
* - disposable_description
    - A description of the dispoasable product. Recorded so we do not have to rescrap certain sites.
* - innovation_description
    - A description of how a productive is better or an improvement upon other products. To prevent rescrapping
* - preference_description
    - A description of what kind of person this product would appeal to. To prevent rescrapping
* - enjoyment_description
    - A description of the highlight features of the product To prevent rescrapping
* - compatibility_description
    - A description of what kinds of other products can be used with the current one. To prevent rescrapping
* - coil_description
    - A wordy description of the type of coil the product has. To prevent rescrapping
* - battery_description
    - A wordy description of the type of battery the product has. To prevent rescrapping
* - nicotine_description
    - A wordy description of the nicotine contents of the product. To prevent rescrapping
* - e_liquid_description
    - If the product is an eqliquid, this is the raw description of the item in question. To prevent rescrapping
* - prefilled_description
    - Raw details of whether a vape is prefilled. To prevent rescrapping
* - devices_description
    - Raw details of the device and its features. To prevent rescrapping
* - screen_description
    - Raw details concerning the device and any existing LED screens. To prevent rescrapping
* - product_type
    - Is the product a disposable, eqliquid or neither
* - source
    - Which website/dataset does the current item come from
* - brand
    - Brand name of the product
* - skunumber
    - Skunumber of the product
* - price
    - price of the product. Some will have two due to sales or comparing prices
* - full_led_screen
    - Does the item in question have a full led screen in yes or no
* - operation
    - How can the product be used
* - url
    - The original web link to the product
* - vg
    - Stands for vegetable glycerin. Usually is a percent of the amount
* - pg
    - Stands for propylene glycol. Also usually a precent of prescence in the product
* - formulation
    - A list of important and key ingredients in the product
* - made_in
    - The country the product was assembled in
* - vendor
    - Another word for brand
* - product_id
    - Some items have products ids from their respective websites
* - image_url
    - The shortened version of image_urls
* - image_url_zoom
    - Some products have multiple images. This is a url for a zoomed in look at the product
* - master case qty
    - How many items are present in each package of a product
* - vibration notifications
    - Boolean of whether a vape will vibrate or not based on notifications
* - display_description
    - Raw data on display features of a product. To prevent rescrapping data
* - adjustable_airflow
    - Data on feature that lets you control how much air mixes with vapor when you inhale
* - power_mode
    - Some products can be boosted. This is a description of different power settings besides the default
* - internal_features
    - A description of the inner workings of the product. To prevent rescrapping data
* - external_features
    - A description of the outside looks of a product. To prevent rescrapping
* - tfn
    - Boolean on whether product is tobacco free or not
* - product_name
    - What the product is called
* - product_code
    - Another version of the product id.
* - warnings
    - The text version of the warnings written on the image of the product or meantioned in the description of the product. 
* - puff_count
    - The amount of puffs contained in the product
* - features
    - Features include items that are included in the product
* - reward_points
    - Some sites allow users to earn points for buying the item
* - review_stars
    - Average review stars that customers have left for product
* - total_reviews
    - Total number of reviews left for product
* - links_description
    - Hyperlinks that are available on the page the product is displayed on
* - returns_description
    - Raw data of how customers can return products if they no longer want them
* - size_description
    - Raw data on the size of objects
* - wattage_description
    - Raw data on the wattage of chargeable products
* - reviews
    - Text data of reviews customers have left on products
* - wishlist
    - How many people have added a product to their wishlist
* - flavors
    - A list of flavors that a product might have
* - vgpg_ratio_description
    - Raw text description of vg and pg. To prevent rescrapping
* - power_mode_description
    - Detailed raw text data of how power modes function
* - sku
    - Similar to skunumber
* - image_alt_text
    - The hidden alt text attribute of images found on the product website
* - rating
    - Like average star level but in a different metric
* - raters
    - Number of people who have rated a product
* - variation
    - How much variety of each product there is
* - flavors_section
    - The raw text description of the flavors of a product
* - in_store_pickup
    - Whether a product is available to pick up in person
* - image2_url
    - Another image that exists for a product
* - image2_alt_text
    - The hidden alternative text that appears after hovering of a image of a product
* - sizes
    - The different volumes of products
* - nicotine_values
    - The varying levels of nicotine in a product
* - colors
    - The colors a product is available in
* - adjustable_airflow_bool
    - A boolean variable for whether a product has adjustable airflow
* - has_battery
    - A boolean for if a product is battery powered
* - bottle_capacity_ml
    - The amount of stuff a bottle of eliquid can hold in ml
* - coil_bool
    - A boolean value for whether or not a coil exists
* - display_bool
    - A boolean value for whether a screen exists
* - disposable_bool
    - A boolean value where true means the product is a disposable
* - dual_tank_bool
    - A boolean value where true means the product has dual tanks
* - flavor_description
    - Raw detailed text of description containing information on flavors
* - iced_bool
    - A boolean on whether a product is "iced" or has menthol
* - ingredients
    - Ingredients list for a product
* - key_features_desription
    - Raw detailed text data for key features for a product
* - has_led
    - Boolean value on whether a product has specifically an led screen
* - name_change
    - Previous version of the product's name
* - nic_free_bool
    - A boolean value where true means the product does not have nicotine
* - nic_levels
    - Like nicotine_values but is measured in percentages
* - online_availbility
    - Is the product available for shipping
* - rechargeable_bool
    - A boolean where true means the product can be recharged
* - smart_led_bool
    - A boolean where true means the product has a smart touchable led screen
* - usb_bool
    - A boolean where true means the product has a usb port

