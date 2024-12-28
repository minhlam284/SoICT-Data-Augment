import cv2
import numpy as np
import os

def yolo_to_bbox(yolo_bbox, img_width, img_height):
    class_id, x_center, y_center, bbox_width, bbox_height = yolo_bbox
    x_center *= img_width
    y_center *= img_height
    bbox_width *= img_width
    bbox_height *= img_height

    x1 = int(x_center - bbox_width / 2)
    y1 = int(y_center - bbox_height / 2)
    x2 = int(x_center + bbox_width / 2)
    y2 = int(y_center + bbox_height / 2)
    
    return class_id, x1, y1, x2, y2

def bbox_to_yolo(class_id, x1, y1, x2, y2, img_width, img_height):
    x_center = (x1 + x2) / 2 / img_width
    y_center = (y1 + y2) / 2 / img_height
    bbox_width = (x2 - x1) / img_width
    bbox_height = (y2 - y1) / img_height
    return f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}"

def expand_bbox(x1, y1, x2, y2, scale, img_width, img_height):
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2
    
    width = (x2 - x1) * scale
    height = (y2 - y1) * scale
    
    x1_new = int(max(0, x_center - width / 2))
    y1_new = int(max(0, y_center - height / 2))
    x2_new = int(min(img_width, x_center + width / 2))
    y2_new = int(min(img_height, y_center + height / 2))
    
    return x1_new, y1_new, x2_new, y2_new

# Tỉ lệ mở rộng box
scale = 1.05 

def remove(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if not filename.endswith(('.jpg', '.png')):
            continue

        image_path = os.path.join(input_folder, filename)
        label_path = os.path.join(input_folder, filename.replace('.jpg', '.txt'))
        output_image_path = os.path.join(output_folder, filename)
        output_label_path = os.path.join(output_folder, filename.replace('.jpg', '.txt'))

        image = cv2.imread(image_path)
        if image is None:
            print(f"Không thể đọc ảnh: {filename}")
            continue
        img_height, img_width = image.shape[:2]

        if not os.path.exists(label_path):
            print(f"Không tìm thấy file nhãn cho: {filename}")
            continue

        with open(label_path, 'r') as f:
            bboxes = [list(map(float, line.strip().split())) for line in f.readlines()]

        updated_bboxes = []

        for bbox in bboxes:
            class_id, x1, y1, x2, y2 = yolo_to_bbox(bbox, img_width, img_height)
            
            # Mở rộng bbox
            x1_expanded, y1_expanded, x2_expanded, y2_expanded = expand_bbox(x1, y1, x2, y2, scale, img_width, img_height)
            
            # Lưu bbox mở rộng vào YOLO format
            updated_bbox = bbox_to_yolo(int(class_id), x1_expanded, y1_expanded, x2_expanded, y2_expanded, img_width, img_height)
            updated_bboxes.append(updated_bbox)

        # Lưu ảnh không thay đổi
        cv2.imwrite(output_image_path, image)
        print(f"Đã lưu ảnh không thay đổi: {filename}")

        # Lưu nhãn kết quả
        with open(output_label_path, 'w') as f:
            f.write("\n".join(updated_bboxes))
        print(f"Đã lưu nhãn mở rộng: {filename.replace('.jpg', '.txt')}")

# Thư mục đầu vào và đầu ra
input_data = '/Users/kaiser/Documents/SOICT/data/train_20241023/nighttime'
output_data = '/Users/kaiser/Documents/SOICT/final/expand'
os.makedirs(output_data, exist_ok=True)
remove(input_data, output_data)
