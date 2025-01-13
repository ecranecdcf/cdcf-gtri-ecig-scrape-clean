#######
VLM usage guide - screens and iced flavor detection
#######

This repository utilizes a Vision-Language model to classify vapes based on multi-modal data. 
We applied this to the screens variable and the iced variables as features that signify these 
selling points can occur in the image, text description, or both.

To start, make sure your have run the webscraping scripts provided and note where it placed your 
images and text.

*****
Step 1: Vape detection
*****

First, choose one of the pre-traied YOLO models we provided from the box site that you would 
like to use. Then, in the ZeroShot directory open the find_vapes.py file and edit the text_paths 
and image_paths variables to reflect your directory structure. Finally, run the script as so:
``python find_vapes.py <PATH TO YOLO>``
This will output a pickle file in the directory that includes all information needed for the next step.

****
Step 2: VLM Querying
****
For this step, we will utilize LLava 1.5 to determine the answer to the question of interest. 
LLava is a vision language model that is capable of answering general queries about images and 
text similar to ChatGPT. It also displays very impressive zero-shot performance on many unseen tasks.
I evaluated its performance personally on ~1000 data points and found an accuracy of about 95%.
To use it, simply run:
``python vlm.py --topic <Screen or Iced> -b <Batch size>``
This will produce a pickle file that can then be converted into a csv via:
``python prepare_csv.py`` 
The files prepare_csv, find_vapes, and utils all require the paths to your text and/or image directories. Make sure to update these and keep them in the same format in order for this to work.

At this point, you should be good. Additionally, you can modify these files to look for arbitrary 
image-text features. Simply add a new prompt into the "topics" variable in the utils.py 
file and you should be able to prompt the VLM into solving for  most variables you would like. 
Just note that VLMs tend to struggle with very low-level features like shapes, so it will 
likely struggle with things of this nature. However, they are very versatile and can solve most 
tasks with a little prompt engineering.

----
Aside: Model Fine-tuning
----
We experimented a bit with using the data provided by LLaVA (with a little cleaning) and training a 
smaller VLM to perform the same task. We found a little success, but after many experiments struggled 
to surpass the accuracy LLaVA achieved. However, I have provided the model and a way to query it 
nonetheless.

First, download the FLAVA_Final.ckpt file from Box into the Finetuning directory.
Then, if you haven't already, run the find_vapes.py script as mentione above.

These are the only steps required for this portion to function. Once you have done so, simply run
``python inference.py`` 
and a csv file will be produced that contains all of the predictions.
We found that performance was roughly comparable to LLaVA but was much faster. However, this comes at a 
cost - these models must be fine-tuned to specific tasks. We did not find the performance improvement
to be worth this cost as finetuning is an intensive process, but we included our best model regardless.

