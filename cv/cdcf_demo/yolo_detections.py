from ultralytics import YOLO
import os
import cv2 as cv
import gc
import argparse
import shutil


#create argument parser to take in folder name
parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", type=str, help="Specify an input directory.")

args = parser.parse_args()

save_name = args.file + "_results_model_8"


#run pre-trained YOLO model on all the images in the folder passed in the command line
model = YOLO('model_8_medium_more_aug_200_epoch_all_MVS_CSVape_vape_juices/weights/best.pt')
model.predict(source=args.file, conf=0.50, project="results" ,name=save_name, save_txt=True, save_conf=True)
del model
gc.collect()


#setup save directory for images that the YOLO model said contained vape juices
label_directory = "results/" + args.file + "_results_model_8/labels"

label_list = os.listdir(label_directory)

image_dir = args.file

save_dir = args.file + "_clean"

os.makedirs(save_dir, exist_ok=True)


#process predictions and move jpg files with vape juices present
for file in label_list:
	if file.endswith(".txt"):

		label_file = open(os.path.join(label_directory, file))

		label_file_lines = label_file.readlines()

		for line in label_file_lines:

			if line.startswith("2"):
				
				try:
					source_ = os.path.join(image_dir, file.replace(".txt",".jpg"))
					dest_ = os.path.join(save_dir, file.replace(".txt",".jpg"))

					shutil.copy(source_, dest_)

					break

				except:
					xyz = 0


#process predictions and move png files with vape juices present
for file in label_list:
	if file.endswith(".txt"):

		label_file = open(os.path.join(label_directory, file))

		label_file_lines = label_file.readlines()

		for line in label_file_lines:

			if line.startswith("2"):
				
				try:
					source_ = os.path.join(image_dir, file.replace(".txt",".png"))
					dest_ = os.path.join(save_dir, file.replace(".txt",".png"))

					shutil.copy(source_, dest_)

					break

				except:
					xyz = 0


#process predictions and move webp files with vape juices present
for file in label_list:
	if file.endswith(".txt"):

		label_file = open(os.path.join(label_directory, file))

		label_file_lines = label_file.readlines()

		for line in label_file_lines:

			if line.startswith("2"):
				
				try:
					source_ = os.path.join(image_dir, file.replace(".txt",".webp"))
					dest_ = os.path.join(save_dir, file.replace(".txt",".webp"))

					shutil.copy(source_, dest_)

					break

				except:
					xyz = 0


