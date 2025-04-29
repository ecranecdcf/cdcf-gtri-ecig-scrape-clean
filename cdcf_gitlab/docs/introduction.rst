.. "CDCF ecig Documentation Page"

Introduction
============

Project Purpose
---------------

The Monitoring the E-cigarette Use Among Youth project, under the Monitoring the Global and Domestic Tobacco Epidemic program, is an initiative funded by Bloomberg Philanthropies to complement existing surveillance activities used to monitor e-cigarette use with innovative rapid response data collection strategies that allow for greater nimbleness, sub-national representativeness, and evaluation capacity in the United States. Included in these surveillance activities is the collaboration with purveyors of retail sales data to obtain real-time data for select states, communities, and control states and communities to enable the evaluation of the real-time impact of state- and community-level flavored tobacco policies on e-cigarette sales volume, market share, and product/brand consumption to generate scientifically defensible and rapidly available data on e-cigarette use among youth.

Approach
--------
This documentation outlines a multimodal approach to analyzing vape-related data by combining web scraping, data unification, natural language processing (NLP), and computer vision techniques. The process involves extracting data from online vaping websites, consolidating it into a unified format, applying NLP for text-based feature extraction, and using computer vision models for image-based analysis.

Data Scraping
^^^^^^^^^^^^^
The first step involves scraping data from online vaping websites to collect information about vape products, including product names, descriptions, pricing, and images. Tools like `BeautifulSoup`, or browser automation libraries such as `Selenium` can be used for scraping structured and unstructured data. The scraped data will typically consist of product metadata, text descriptions, and associated product images.

Data Unification
^^^^^^^^^^^^^^^^
After scraping, the data needs to be unified into a single, structured data model. This involves cleaning and normalizing text fields, standardizing units for numerical values (e.g., size, nicotine strength), and associating product images with their corresponding text records. Tools such as `pandas` for data frames and relational databases or JSON formats for storage can be used to ensure consistency and accessibility for downstream analysis.

Natural Language Processing
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Natural language processing techniques are applied to extract key features from the product text, such as product type, flavors, tobacco level, size, and the presence of iced or menthol properties. Regular expressions can be used for rule-based extraction of structured patterns, while large language models (LLMs), such as GPT, can parse complex and ambiguous text descriptions to identify additional attributes.

Computer Vision Models
^^^^^^^^^^^^^^^^^^^^^^
Computer vision models are deployed to analyze product images and extract visual features. Vision Language Models (VLMs) can identify text overlays and contextual elements in images, while object detection models like YOLOv8 can detect specific visual attributes, such as product screens, iced/menthol indicators, and branding elements. These models work in tandem with the NLP outputs to enhance feature extraction and provide a comprehensive understanding of the products.






