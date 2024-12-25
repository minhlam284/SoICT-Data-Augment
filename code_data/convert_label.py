import os
import shutil
import argparse
def modify_first_number_and_copy_files(input_folder, output_folder):
    # Tạo thư mục đầu ra nếu chưa tồn tại
    os.makedirs(output_folder, exist_ok=True)

    # Duyệt qua tất cả các file trong thư mục
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Kiểm tra nếu là file .txt
        if filename.endswith('.txt'):
            # Đọc nội dung của file nhãn
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Sửa số đầu tiên của mỗi dòng lùi đi 4 đơn vị
            modified_lines = []
            for line in lines:
                # Tách các phần của dòng để xử lý số đầu tiên
                parts = line.strip().split()
                if parts and parts[0].isdigit():  # Kiểm tra nếu phần đầu là số
                    parts[0] = str(int(parts[0]) - 4)  # Lùi đi 4 đơn vị
                modified_line = " ".join(parts) + "\n"  # Ghép lại các phần đã chỉnh sửa
                modified_lines.append(modified_line)

            # Ghi nội dung đã chỉnh sửa vào file trong thư mục mới
            with open(output_path, 'w') as file:
                file.writelines(modified_lines)
            print(f"Đã chỉnh sửa file nhãn: {filename}")

        # Nếu là file ảnh, sao chép sang thư mục mới
        elif filename.endswith(('.jpg', '.png')):
            shutil.copy(file_path, output_path)
            print(f"Đã sao chép file ảnh: {filename}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert label 4 ->0, 5->1, 6->2, 7->3")
    parser.add_argument('--input', type = str, help = "Path to the input data folder")
    parser.add_argument('--output', type = str, help = "Path to the output folder")
    args = parser.parse_args()

    dataset_folder = args.input
    output_folder = args.output

    modify_first_number_and_copy_files(dataset_folder, output_folder)