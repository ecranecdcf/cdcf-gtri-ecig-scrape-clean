.. "CDCF ecig Documentation Page"

Computer Vision
===============

YOLO V8 Code
_____________

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