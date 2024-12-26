import os
import argparse

def rename_images_and_labels(folder_path, prefix):
    # Lấy danh sách file trong folder
    files = os.listdir(folder_path)
    images = [f for f in files if f.lower().endswith('.jpg')]
    labels = [f for f in files if f.lower().endswith('.txt')]

    images.sort()
    labels.sort()

    # Kiểm tra số lượng file ảnh và label có khớp nhau không
    if len(images) != len(labels):
        print("Số lượng ảnh và label không khớp. Kiểm tra lại folder.")
        return

    # Đổi tên file ảnh và label
    for idx, (img, lbl) in enumerate(zip(images, labels)):
        new_name = f"{prefix}_{idx:04d}"  # Định dạng tên mới
        img_ext = os.path.splitext(img)[1]
        lbl_ext = os.path.splitext(lbl)[1]

        # Đổi tên file
        os.rename(os.path.join(folder_path, img), os.path.join(folder_path, new_name + img_ext))
        os.rename(os.path.join(folder_path, lbl), os.path.join(folder_path, new_name + lbl_ext))

    print(f"Đã đổi tên {len(images)} cặp ảnh và label trong folder {folder_path}.")

# Sử dụng hàm
folder_path = "/Users/kaiser/Documents/SOICT/remove/blur_remove_day"
prefix = "blur_remove_day"
rename_images_and_labels(folder_path, prefix)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename for dataset format prefix_xxx")
    parser.add_argument("--input", type=str, help="Path to the input data folder")
    parser.add_argument("--prefix", type=str, help="New name for dataset augmentation")
    args = parser.parse_args()

    dataset_folder = args.input
    prefix = args.prefix
    rename_images_and_labels(dataset_folder, prefix)
