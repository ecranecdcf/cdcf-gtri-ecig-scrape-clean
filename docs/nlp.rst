.. "CDCF ecig Documentation Page"

Natural Language Processing
===========================

Setup
-----

Currently a combination of regular expressions and LLMs. 

Regex Setup
~~~~~~~~~~~

Most regular expressions are straightforward and can be executed as Python code in the Features table described below.

LLM Setup
~~~~~~~~~

Download :download:`InstructionsForDownloadingLLaMALLMmodel.docx <./InstructionsForDownloadingLLaMALLMmodel.docx>`

Under the ``nlp/llm_code`` folder:

- This contains a ``datasets`` folder with scraped datasets, in addition to some labeled datasets loaded for the fine-tuned model. The output sample datasets are also contained here. Notably, CS Vape and Vape WH are available as sample outputs.
- Most functions can be executed through ``nlp/llm_code/llama_vape_csvape_test.ipynb``.

  - Some NLP functions are successfully loaded through regex functions in the ``regex_functions.py`` file. These include e-liquid contents and nicotine levels.
  - Other functions that use the LLM code, including prompts, are available in ``llm_functions.py``. Currently, the LLM code uses a fine-tuned version of Meta's ``Llama-3.1-8B-Instruct`` model. Instructions for setting up this model are found under ``doc/Instructions for downloading LLaMA LLM model.docx``.
  - An output viewer for a better understanding of the NLP output is available in ``output_explorer.ipynb``.


NLP Features
------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 30 30 40

   * - Feature Name
     - Description
     - Code Location
     - Sample Data
     - Notes
   * - Flavors
     - Currently, flavors is captured using regex and completed for common patterns in vape.com and vapewh. We are in the process of implementing LLM prompting to extract the flavors. Flavors currently are stored in a dictionary data structure, with the key being the flavor name and value being the description.
     - `nlp/llm_code/regex_functions/extract_flavors_with_descriptions`
     - `nlp/llm_code/datasets/output/processed_output`
     - Since data is not consistent across different sources, we are working to standardize it. LLM will assist in standardizing the data for easier parsing and storage.
   * - Screens
     - A regular-expression-based script to detect various screen features: display_type, color_display, touch_screen, curved_screen, battery_indicator, eliquid_indicator, smart_display, digital_display, hd_display, animated, backlit.
     - `nlp/screens.py`
     - `nlp/screens_sample_data`
     - Does not capture all aspects of "gaming" features, which will be part of another script.
   * - Product Type
     - Product type is captured using LLaMA-based classification. Categories include Closed Refills, Closed System, Disposable System, E-liquid, and Accessories. Further information can be found in `doc/Vape_Product_Categories.docx`.
     - `nlp/llm_code/llm_functions/classify_product`
     - `nlp/llm_code/datasets/output/processed_output`
     - Requires consistent labeling of categories and may need LLM fine-tuning for specific outliers or new product types. csvape and vapewh have labeled datasets for reference (`nlp/llm_code/datasets/labeled`).
   * - Iced/Menthol
     - This is in progress--we will continue work on this following completion of flavor parsing. This may be completed either using regex or LLaMA-based classification pending additional investigation.
     - TBD
     - TBD
     - 
   * - Total Ounces/mL
     - Captured via regex to extract volume values (e.g., ounces or mL) from product descriptions.
     - `nlp/llm_code/regex_functions/find_eliquid_contents`
     - `nlp/llm_code/datasets/output/processed_output`
     - Multiple volumes may be available for some products. Additional work can be done to handle this similar to nicotine levels.
   * - Nicotine Level
     - Captured via regex patterns to extract nicotine levels (e.g., 0mg, 3mg). Multiple levels are stored in separate columns.
     - `nlp/llm_code/regex_functions/find_nicotine_levels`
     - `nlp/llm_code/datasets/output/processed_output`
     - 
   * - Synthetic Nicotine
     - Synthetic nicotine is detected using LLaMA-based classification to identify key terms (e.g., "tobacco-free nicotine").
     - `nlp/llm_code/llm_functions/classify_tfn`
     - `nlp/llm_code/datasets/output/processed_output`
     - LLM captures most of the edge cases--may need additional prompting if any new verbiage is found. csvape and vapewh have labeled datasets for reference (`nlp/llm_code/datasets/labeled`).
   * - Nicotine Free
     - Uses Nicotine Level to indicate if the product is nicotine free or not alongside relevant verbiage.
     - `nlp/llm_code/regex_functions/find_nic_free`
     - `nlp/llm_code/datasets/output/processed_output`
     - Additional edge cases may warrant LLM use. csvape and vapewh have labeled datasets for reference (`nlp/llm_code/datasets/labeled`).
   * - CBD/THC
     - CBD/THC is detected using LLaMA-based classification. Zero-shot learning (no examples or additional training) has been successful in classifying CBD for products available.
     - `nlp/llm_code/llm_functions/classify_cbd`
     - `nlp/llm_code/datasets/output/processed_output`
     - Larger test dataset may be useful to obtain a more robust accuracy metric. csvape and vapewh have labeled datasets for reference (`nlp/llm_code/datasets/labeled`).


