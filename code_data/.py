import cv2
import os

# Define paths
image_folder = "/Users/kaiser/Documents/SOICT/data/private test"  # Folder containing images
annotation_file = "/Users/kaiser/Downloads/predict_ult.txt"  # YOLO-formatted annotation file
# annotation_file = "/home/vdotmint/SOICT/IAI_SOICT_VecDet/yolo_smooth.txt"  # YOLO-formatted annotation file

CLASS_COLORS = {
    0: (0, 0, 255),    # Red
    1: (0, 255, 0),    # Green
    2: (255, 0, 0),    # Blue
    3: (0, 255, 255)   # Yellow
}

# Load annotations into a dictionary with file names as keys
annotations = {}
with open(annotation_file, 'r') as f:
    for line in f:
        parts = line.strip().split()
        file_name, cls, x, y, w, h, conf = parts[0], int(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]), float(parts[5]), float(parts[6])
        if file_name not in annotations:
            annotations[file_name] = []
        annotations[file_name].append((cls, x, y, w, h, conf))

# Get sorted list of image files
image_files = sorted([img for img in os.listdir(image_folder) if img.endswith(('.jpg', '.png', '.jpeg'))])
index = 0

def draw_bounding_boxes(img, file_name):
    h, w, _ = img.shape
    if file_name in annotations:
        for (cls, x, y, box_w, box_h, conf) in annotations[file_name]:
            # Convert normalized coordinates to pixel coordinates
            x1 = int((x - box_w / 2) * w)
            y1 = int((y - box_h / 2) * h)
            x2 = int((x + box_w / 2) * w)
            y2 = int((y + box_h / 2) * h)

            cls = int(cls)
            
            # Draw bounding box and label
            cv2.rectangle(img, (x1, y1), (x2, y2), CLASS_COLORS[cls], 1)
            cv2.putText(img, f"{conf:.03}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, CLASS_COLORS[cls], 2)

    cv2.putText(img, file_name, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 0), 2)
    
    return img

while True:
    # Load image and draw bounding boxes
    file_name = image_files[index]
    img_path = os.path.join(image_folder, file_name)
    img = cv2.imread(img_path)
    if img is None:
        print(f"Image {file_name} not found.")
        break
    img = draw_bounding_boxes(img, file_name)
    
    # Show image
    cv2.imshow("Image Viewer", img)
    key = cv2.waitKey(0)
    
    # Handle key press
    if key == 27 or key == ord('q'):  # Esc key to exit
        break
    elif key == ord('a') or key == 81:  # Left arrow or 'a' for previous image
        index = (index - 1) % len(image_files)
    elif key == ord('d') or key == 83:  # Right arrow or 'd' for next image
        index = (index + 1) % len(image_files)

cv2.destroyAllWindows()
