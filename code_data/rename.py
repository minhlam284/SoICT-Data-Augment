import os
import argparse

def rename_files_in_place(folder_path, prefix="file", start_index=1):
    # Lấy danh sách các file trong thư mục
    files = os.listdir(folder_path)
    
    # Sắp xếp các file để đảm bảo thứ tự nếu cần
    files.sort()

    # Đổi tên từng file theo format mới
    for index, filename in enumerate(files, start=start_index):
        # Tách đuôi file
        file_name = os.path.splitext(filename)[0]
        file_extension = os.path.splitext(filename)[1]
        
        # Tạo tên file mới theo format
        new_name = f"{prefix}_{file_name}{file_extension}"
        
        # Đường dẫn đầy đủ của file cũ và file mới
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)

        # Đổi tên file nếu tên mới chưa tồn tại (để tránh lỗi ghi đè)
        if not os.path.exists(new_path):
            os.rename(old_path, new_path)
            print(f"Đã đổi tên: {filename} -> {new_name}")
        else:
            print(f"Tên file {new_name} đã tồn tại, bỏ qua.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Rename data augmentation")
    parser.add_argument('--input', type=str, help="Path to the input data folder")
    parser.add_argument('--prefix', type = str, help="New name for data augmentation")
    args = parser.parse_args()

    dataset_folder = args.input
    prefix = args.prefix
    rename_files_in_place(dataset_folder, prefix, start_index=1)
