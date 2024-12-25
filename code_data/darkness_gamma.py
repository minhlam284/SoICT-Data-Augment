import os
import shutil
import numpy as np
import cv2
from PIL import Image
import torchvision.transforms.functional as F
import argparse

def adjust_gamma(image_path, gamma):
    image = Image.open(image_path).convert('RGB')
    adjust_image = F.adjust_gamma(image, gamma=gamma, gain=1.0)
    return np.array(adjust_image)


def process_images_gamma(image_folder, target_folder):
    os.makedirs(target_folder, exist_ok=True)
    for filename in os.listdir(image_folder):
        if filename.endswith('.jpg'):
            image_path = os.path.join(image_folder, filename)
            
            # Xử lý theo quy tắc tên file
            if filename.startswith('cam_03'):
                bright_image = adjust_gamma(image_path, gamma=2.0)
            elif filename.startswith('cam_05'):
                bright_image = adjust_gamma(image_path, gamma=1.7)
            else:
                bright_image = adjust_gamma(image_path, gamma=1.8)
            
            # Lưu ảnh kết quả
            final_path = os.path.join(target_folder, filename)
            bright_image_rgb = cv2.cvtColor(bright_image, cv2.COLOR_BGR2RGB)

# Lưu ảnh dạng RGB
            cv2.imwrite(final_path, bright_image_rgb)
        
        elif filename.endswith('.txt'):
            txt_path = os.path.join(image_folder, filename)
            final_path = os.path.join(target_folder, filename)
            
            # Sao chép file nhãn
            if os.path.isfile(txt_path):
                shutil.copy(txt_path, final_path)

input_path = '/Users/kaiser/Documents/SOICT/remove/remove_data'
output_path = '/Users/kaiser/Documents/SOICT/test_gamma'
process_images_gamma(input_path, output_path)