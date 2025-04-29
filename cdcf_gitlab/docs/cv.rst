.. "CDCF ecig Documentation Page"

Computer Vision
===============

Pre-processing (YOLO V8 Code)
_____________________________

**predict.py**

    This file has examples of running a pre-trained model on a set of webscraped images.
    The following is an example of a single prediction run:

    1. model = YOLO('runs/detect/model_8_medium_more_aug_200_epoch_all_MVS_CSVape_vape_juices/weights/best.pt')

    2. model.predict(source="/projects/frostbyte-1/cdcf_ecig_analysis/box_src/data_from_sites/csvape/csvape_images", conf=0.50, name="csvape_results", save_txt=True, save_conf=True)

    3. del model

    4. gc.collect()

    The first line calls the YOLO function to load a model with a given path

    The second line runs the predict function using the loaded model on a source which is a folder containing images, this function also takes a confidence level which is the minimum confidence for a prediction, the name of the folder to store the results, save_text=True to save the text files for the labels, and finally save_conf=True saves the model confidence per prediction in the text files.

    The third line deletes the model from memory (RAM)

    The fourth line collects the garbage from memory when removing the model from RAM

**Model Files**

    We trained many models during this project, they are all stored in the runs/detect directory

    Each model directory contains a weights file with weights for the last model and the best model according to the validation set

    Below is a description of how each model was trained and what it can detect:


    *model_1_small - trained using only the open source dataset found online for vapes vs cigarette detection, trained for 100 epochs with default augmentation and using the SMALL version of YOLO_V8*


    *model_2_medium - trained using only the open source dataset found online for vapes vs cigarette detection, trained for 100 epochs with default augmentation and using the MEDIUM version of YOLO_V8*


    *model_3_medium_more_aug - trained using only the open source dataset found online for vapes vs cigarette detection, trained for 100 epochs with EXTRA augmentation and using the MEDIUM version of YOLO_V8*


    *model_4_medium_more_aug_200_epoch - trained using only the open source dataset found online for vapes vs cigarette detection, trained for 200 epochs with EXTRA augmentation and using the MEDIUM version of YOLO_V8*


    *model_5_medium_more_aug_200_epoch_my_vape_store - trained using the open source dataset for vapes vs cigarette detection along with some of the my_vape_store data which was annotated by GTRI, trained for 200 epochs with EXTRA augmentation and using the MEDIUM version of YOLO_V8*


    *model_6_medium_more_aug_200_epoch_all_my_vape_store - trained using the open source dataset for vapes vs cigarette detection along with ALL of the my_vape_store data which was annotated by GTRI, trained for 200 epochs with EXTRA augmentation and using the MEDIUM version of YOLO_V8*


    *model_7_medium_more_aug_200_epoch_all_MVS_CSVape - trained using the open source dataset for vapes vs cigarette detection along with ALL of the my_vape_store data which was annotated by GTRI and ALL of the CSVape dataset that was annotated by GTRI, trained for 200 epochs with EXTRA augmentation and using the MEDIUM version of YOLO_V8*


    *model_8_medium_more_aug_200_epoch_all_MVS_CSVape_vape_juices - trained using the open source dataset for vapes vs cigarette detection along with ALL of the my_vape_store data which was annotated by GTRI and ALL of the CSVape dataset that was annotated by GTRI, trained for 200 epochs with EXTRA augmentation and using the MEDIUM version of YOLO_V8, this model includes labels for VAPE JUICES as an additional class*

**YOLO Data**

    The data is split into training and validation sets containing 6153 and 1222 images respectively. All images have a cooresponding label file which contains the bounding box information in the YOLO format to be used for training or validation. Each line of the label file cooresponds to a single bounding box, the line starts with a single number representing the class of the object, followed by four numbers, each representing one of the corners of the bounding box. Empty label files indicate the images contains no objects of interest. This dataset has three seperate classes, class 0 represents cigarettes, class 1 represents vapes, and class 2 represents vape juices. 



Vision Language Model (Screens and Iced Flavor Detection)
_____________________________

    This repository utilizes a Vision-Language model to classify vapes based on multi-modal data. 
    We applied this to the screens variable and the iced variables as features that signify these 
    selling points can occur in the image, text description, or both.

    To start, make sure your have run the webscraping scripts provided and note where it placed your 
    images and text.

**Step 1: Vape Detectionn**

    First, choose one of the pre-traied YOLO models we provided from the box site that you would 
    like to use. Then, in the ZeroShot directory open the find_vapes.py file and edit the text_paths 
    and image_paths variables to reflect your directory structure. Finally, run the script as so:
    ``python find_vapes.py <PATH TO YOLO>``
    This will output a pickle file in the directory that includes all information needed for the next step.

**Step 2: VLM Querying**

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

**Model Fine-tuning**

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
