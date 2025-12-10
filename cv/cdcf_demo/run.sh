#!/bin/bash

#example usage
python yolo_detections.py -f vapingdotcom_images
python google_gemini_predictions.py -f vapingdotcom_images -k KEY -s 0 -e 10
