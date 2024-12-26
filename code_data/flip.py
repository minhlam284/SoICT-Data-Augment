import os
from PIL import Image
import argparse

def flip_image_and_labels(image_path, label_path, output_folder):
    # Đọc ảnh
    image = Image.open(image_path).convert("RGB")
    
    # Lật ảnh từ phải sang trái
    flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
    
    # Đường dẫn lưu ảnh lật trong thư mục đầu ra
    output_image_path = os.path.join(output_folder, os.path.basename(image_path))
    flipped_image.save(output_image_path)
    
    # Đọc file nhãn
    with open(label_path, 'r') as f:
        labels = f.readlines()

    # Cập nhật nhãn
    new_labels = []
    for label in labels:
        class_id, x_center, y_center, width, height = map(float, label.split())
        
        # Cập nhật tọa độ x_center sau khi lật
        x_center = 1.0 - x_center
        
        # Tạo dòng nhãn mới
        new_label = f"{int(class_id)} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n"
        new_labels.append(new_label)

    # Đường dẫn lưu file nhãn
    output_label_path = os.path.join(output_folder, os.path.basename(label_path))
    
    # Ghi file nhãn mới
    with open(output_label_path, 'w') as f:
        f.writelines(new_labels)

def process_folder(input_folder, output_folder):
    # Tạo thư mục đầu ra nếu chưa tồn tại
    os.makedirs(output_folder, exist_ok=True)
    
    # Lặp qua tất cả các file trong thư mục đầu vào
    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg'):
            image_path = os.path.join(input_folder, filename)
            label_path = os.path.join(input_folder, filename.replace('.jpg', '.txt'))
            
            # Kiểm tra nếu file nhãn tồn tại
            if os.path.isfile(label_path):
                flip_image_and_labels(image_path, label_path, output_folder)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Flip image in dataset")
    parser.add_argument('--input', type = str, help = "Path to input dataset folder")
    parser.add_argument('--output', type = str, help = "Path to output folder")
    args = parser.parse_args()

    dataset_folder = args.input
    output_folder = args.output

    process_folder(dataset_folder, output_folder)
