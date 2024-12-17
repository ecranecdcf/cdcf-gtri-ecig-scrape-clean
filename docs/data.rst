.. "CDCF ecig Documentation Page"

Data Model and Preparation
==========================

Proposed data model. This is a work in progress.

.. list-table:: Data Model
   :widths: 20 15 65
   :header-rows: 1

   * - Column Name
     - Data Type
     - Description
   * - Brand
     - String
     - Brand name of the product (from the dataset).
   * - Product
     - String
     - Specific product name.
   * - SkuNumber
     - Integer
     - SKU identifier number for tracking and inventory.
   * - Price
     - String
     - Price of the product, formatted as currency.
   * - Description
     - String
     - Short description of the product, including flavor profile or unique attributes.
   * - E-liquid contents
     - String
     - Volume of e-liquid in the product, typically measured in ml.
   * - Puffs per Device
     - Integer
     - Number of puffs the device can provide.
   * - Flavor
     - String
     - Flavor profile or variety information for the product.
   * - Coil
     - String
     - Type of coil used in the product, e.g., "Mesh Coil".
   * - Nic_level_1
     - String
     - Primary nicotine level designation, often in mg or percent.
   * - Nic_level_2
     - String
     - Secondary nicotine level designation if multiple strengths are offered.
   * - Nic_level_3
     - String
     - Tertiary nicotine level designation if applicable.
   * - Iced_Variable
     - Boolean
     - Indicator if the flavor includes a menthol or "iced" variant.
   * - Nic_Free
     - Integer
     - Binary indicator (0 or 1) indicating if the product is nicotine-free.
   * - TFN
     - Integer
     - Binary indicator (0 or 1) if the product contains tobacco-free nicotine.
   * - Product_Type
     - String
     - Classification of the product type, e.g., "Disposable System".
   * - Internal_Features
     - String
     - Additional internal features of the device, if available.
   * - External_Features
     - String
     - Additional external features or specifications of the device.
   * - Country_of_Assembly
     - String
     - Country where the product was assembled or manufactured.
