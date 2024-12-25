import cv2
import numpy as np
import os
import shutil

def add_gaussian_blur(patch, kernel_size=(5, 5)):
    blurred_patch = cv2.GaussianBlur(patch, kernel_size, 0)
    return blurred_patch

def process_blur(dataset_folder, output_folder):

    for filename in os.listdir(dataset_folder):
        if filename.endswith('.jpg'):
            img_path = os.path.join(dataset_folder, filename)
            image = cv2.imread(img_path)
            height, width, _ = image.shape

            label_path = os.path.join(dataset_folder, filename.replace('.jpg', '.txt'))
            if os.path.exists(label_path):
                with open(label_path, 'r') as file:
                    labels = file.readlines()
                for label in labels:
                    class_id, center_x, center_y, box_width, box_height = map(float, label.strip().split())
                    x1 = int((center_x - box_width / 2) * width)
                    y1 = int((center_y - box_height / 2) * height)
                    x2 = int((center_x + box_width / 2) * width)
                    y2 = int((center_y + box_height / 2) * height)
                    
                    patch = image[y1:y2, x1:x2]
                    blurred_patch = add_gaussian_blur(patch)
                    
                    image[y1:y2, x1:x2] = blurred_patch

                output_path = os.path.join(output_folder, f"blurred_{filename}")
                cv2.imwrite(output_path, image)

                output_label_path = os.path.join(output_folder, f"blurred_{filename.replace('.jpg', '.txt')}")
                shutil.copy(label_path, output_label_path)

dataset_folder = '/Users/kaiser/Documents/SOICT/add_car_flip_final'
output_folder = '/Users/kaiser/Documents/SOICT/data_aug/add_car_blur'
os.makedirs(output_folder, exist_ok=True)

process_blur(dataset_folder, output_folder)