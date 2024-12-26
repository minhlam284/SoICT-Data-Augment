import cv2
import numpy as np
import os
from skimage.exposure import match_histograms
import shutil

# Hàm tạo nhiễu Gaussian
def generate_gaussian_noise(image, mean, sigma):
    row, col, ch = image.shape
    gauss = np.random.normal(mean, sigma, (row, col, ch))
    noisy = np.clip(image + gauss, 0, 255).astype(np.uint8)
    return noisy

# Hàm áp dụng histogram matching và làm mờ cho toàn bộ ảnh
def apply_histogram_matching_and_blur(image_path, reference_image, output_image_path):
    # Đọc ảnh gốc
    img = cv2.imread(image_path)
    
    # Chuyển ảnh từ BGR sang RGB (OpenCV mặc định BGR, matplotlib yêu cầu RGB)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Áp dụng histogram matching cho toàn bộ ảnh
    matched_img = match_histograms(img_rgb, reference_image)

    # Đảm bảo rằng ảnh có giá trị trong phạm vi [0, 255]
    matched_img = np.clip(matched_img, 0, 255).astype(np.uint8)

    # Thêm hiệu ứng làm mờ (Gaussian Blur)
    blurred_img = cv2.GaussianBlur(matched_img, (5, 5), 0)

    # Chuyển ảnh về BGR trước khi lưu
    blurred_img_bgr = cv2.cvtColor(blurred_img, cv2.COLOR_RGB2BGR)

    # Lưu ảnh đã chỉnh sửa vào thư mục mới
    cv2.imwrite(output_image_path, blurred_img_bgr)

# Hàm xử lý tất cả ảnh trong thư mục
def process_images_in_folder(input_folder, output_folder):
    # Tạo thư mục đầu ra nếu chưa có
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Duyệt qua tất cả các file trong thư mục
    for filename in os.listdir(input_folder):
        # Kiểm tra nếu là file ảnh (jpg, png, v.v.)
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            # Đường dẫn đầy đủ đến file ảnh
            image_path = os.path.join(input_folder, filename)

            # Đọc ảnh và tạo ảnh nhiễu làm ảnh tham chiếu
            img = cv2.imread(image_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Đọc ảnh và chuyển sang RGB
            
            # Tạo ảnh tham chiếu với nhiễu Gaussian khác nhau cho mỗi loại ảnh
            if filename.startswith('cam_03'):
                reference_img_rgb = generate_gaussian_noise(img_rgb, mean=135, sigma=30)
            elif filename.startswith('cam_05'):
                reference_img_rgb = generate_gaussian_noise(img_rgb, mean=70, sigma=25)
            else:
                reference_img_rgb = generate_gaussian_noise(img_rgb, mean=100, sigma=14)
            
            # Tạo đường dẫn lưu ảnh đã chỉnh sửa
            output_image_path = os.path.join(output_folder, filename)
            
            # Áp dụng histogram matching và làm mờ cho ảnh, rồi lưu vào thư mục mới
            apply_histogram_matching_and_blur(image_path, reference_img_rgb, output_image_path)
            
            # Cũng cần chuyển file label (nếu có)
            # label_path = os.path.splitext(image_path)[0] + '.txt'
            # if os.path.exists(label_path):
            #     output_label_path = os.path.join(output_folder, os.path.basename(label_path))
            #     # Chuyển file label sang thư mục mới
            #     os.rename(label_path, output_label_path)
            #     print(f"Đã chuyển file label: {label_path} -> {output_label_path}")

            label_path = os.path.splitext(image_path)[0] + '.txt'
            if os.path.exists(label_path): 
                output_label_path = os.path.join(output_folder, os.path.basename(label_path))
                # Sao chép file label sang thư mục mới
                shutil.copy(label_path, output_label_path)
                print(f"Đã sao chép file label: {label_path} -> {output_label_path}")

# Đường dẫn đến thư mục chứa ảnh và thư mục đầu ra
input_folder = '/Users/kaiser/Documents/SOICT/remove/remove_raw'
output_folder = '/Users/kaiser/Documents/SOICT/remove/blur_remove'

# Xử lý tất cả ảnh trong thư mục
process_images_in_folder(input_folder, output_folder)


# import cv2
# import numpy as np
# import os
# import random
# from skimage.exposure import match_histograms

# # Hàm tạo nhiễu Gaussian
# def generate_gaussian_noise(image, mean, sigma):
#     row, col, ch = image.shape
#     gauss = np.random.normal(mean, sigma, (row, col, ch))
#     noisy = np.clip(image + gauss, 0, 255).astype(np.uint8)
#     return noisy

# # Hàm áp dụng histogram matching và làm mờ cho toàn bộ ảnh
# def apply_histogram_matching_and_blur(image_path, reference_image, output_image_path):
#     # Đọc ảnh gốc
#     img = cv2.imread(image_path)
    
#     # Chuyển ảnh từ BGR sang RGB (OpenCV mặc định BGR, matplotlib yêu cầu RGB)
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#     # Chuyển ảnh về float và chuẩn hóa giá trị ảnh trong phạm vi [0, 1]
#     img_rgb = img_rgb.astype(np.float32) / 255.0
#     reference_image = reference_image.astype(np.float32) / 255.0

#     # Áp dụng histogram matching cho toàn bộ ảnh
#     matched_img = match_histograms(img_rgb, reference_image)

#     # Đảm bảo rằng ảnh có giá trị trong phạm vi [0, 255] và chuyển về kiểu uint8
#     matched_img = np.clip(matched_img * 255.0, 0, 255).astype(np.uint8)

#     # Thêm hiệu ứng làm mờ (Gaussian Blur)
#     blurred_img = cv2.GaussianBlur(matched_img, (5, 5), 0)

#     # Chuyển ảnh về BGR trước khi lưu
#     blurred_img_bgr = cv2.cvtColor(blurred_img, cv2.COLOR_RGB2BGR)

#     # Lưu ảnh đã chỉnh sửa vào thư mục mới
#     cv2.imwrite(output_image_path, blurred_img_bgr)

# # Hàm chọn ngẫu nhiên ảnh bắt đầu với 'cam' từ thư mục tham chiếu
# def get_random_reference_image(reference_folder):
#     # Lọc các file có tên bắt đầu bằng 'cam' trong thư mục tham chiếu
#     all_files = [f for f in os.listdir(reference_folder) if f.endswith(('.jpg', '.png', '.jpeg')) and f.startswith('cam_13')]
    
#     # Chọn ngẫu nhiên một ảnh
#     if all_files:
#         random_image = random.choice(all_files)
        
#         # Đọc ảnh và chuyển sang RGB
#         reference_image_path = os.path.join(reference_folder, random_image)
#         reference_img = cv2.imread(reference_image_path)
#         reference_img_rgb = cv2.cvtColor(reference_img, cv2.COLOR_BGR2RGB)
        
#         return reference_img_rgb
#     else:
#         raise ValueError("Không có ảnh nào bắt đầu với 'cam' trong thư mục tham chiếu")

# # Hàm xử lý tất cả ảnh trong thư mục
# def process_images_in_folder(input_folder, output_folder, reference_folder):
#     # Tạo thư mục đầu ra nếu chưa có
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     # Duyệt qua tất cả các file trong thư mục
#     for filename in os.listdir(input_folder):
#         # Kiểm tra nếu là file ảnh (jpg, png, v.v.)
#         if filename.endswith(('.jpg', '.png', '.jpeg')):
#             # Đường dẫn đầy đủ đến file ảnh
#             image_path = os.path.join(input_folder, filename)

#             # Lấy ảnh tham chiếu ngẫu nhiên từ thư mục tham chiếu
#             try:
#                 reference_img_rgb = get_random_reference_image(reference_folder)
#             except ValueError as e:
#                 print(e)
#                 continue  # Nếu không tìm thấy ảnh 'cam', tiếp tục với ảnh tiếp theo
            
#             # Tạo đường dẫn lưu ảnh đã chỉnh sửa
#             output_image_path = os.path.join(output_folder, filename)
            
#             # Áp dụng histogram matching và làm mờ cho ảnh, rồi lưu vào thư mục mới
#             apply_histogram_matching_and_blur(image_path, reference_img_rgb, output_image_path)
            
#             # Cũng cần chuyển file label (nếu có)
#             label_path = os.path.splitext(image_path)[0] + '.txt'
#             if os.path.exists(label_path):
#                 output_label_path = os.path.join(output_folder, os.path.basename(label_path))
#                 # Chuyển file label sang thư mục mới
#                 os.rename(label_path, output_label_path)
#                 print(f"Đã chuyển file label: {label_path} -> {output_label_path}")

# # Đường dẫn đến thư mục chứa ảnh, thư mục tham chiếu và thư mục đầu ra
# input_folder = '/Users/kaiser/Documents/SOICT/remove/remove_data'
# output_folder = '/Users/kaiser/Documents/SOICT/remove/blur_remove'
# reference_folder = '/Users/kaiser/Documents/SOICT/data/private test'  # Đặt đường dẫn đến thư mục tham chiếu

# # Xử lý tất cả ảnh trong thư mục
# process_images_in_folder(input_folder, output_folder, reference_folder)
