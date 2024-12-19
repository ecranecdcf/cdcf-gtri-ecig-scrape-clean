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
     - 
     - 
     - 
     - 
   * - Screens
     - A regular-expression based script to detect various screen features: display_type, color_display, touch_screen, curved_screen, battery_indicator, eliquid_indicator, smart_display, digital_display, hd_display, animated,backlit
     - `nlp/screens.py`
     - `nlp/screens_sample_data`
     - Does not capture all aspects of 'gaming' features, which will be part of another script.
   * - Product Type
     - 
     - 
     - 
     - 
   * - Iced/Menthol
     - 
     - 
     - 
     - 
   * - Total Ounces/mL
     - 
     - 
     - 
     - 
   * - Nicotine Level
     - 
     - 
     - 
     - 
   * - Synthetic Nicotine
     - 
     - 
     - 
     - 
   * - Nicotine Free
     - 
     - 
     - 
     - 





