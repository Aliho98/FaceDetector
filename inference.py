import torch
from ultralytics import YOLO
import cv2
import numpy as np
import os
import concurrent.futures

# Load the YOLOv8 model
model = YOLO('yolov8l-face.pt')

# Function to perform face detection
def detect_faces(image_path):
    # Perform inference
    results = model(image_path)
    
    # Process and return the results
    faces = []
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        
        for box, confidence in zip(boxes, confidences):
            if confidence > 0.70:
                x1, y1, x2, y2 = box
                face = {
                    'bbox': [int(x1), int(y1), int(x2), int(y2)],
                    'confidence': float(confidence)
                }
                faces.append(face)
    
    return faces

# Function to visualize detected faces
def visualize_faces(image_path, detected_faces):
    # Read the image
    image = cv2.imread(image_path)
    
    # Define a list of colors for bounding boxes
    colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
    
    for i, face in enumerate(detected_faces):
        x1, y1, x2, y2 = face['bbox']
        color = colors[i % len(colors)]  # Cycle through colors if more faces than colors
        
        # Draw bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        
        # Add confidence score text
        confidence_text = f"Confidence: {face['confidence']:.2f}"
        cv2.putText(image, confidence_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    
    return image

# Function to process a single image
def process_image(image_file, image_folder, output_folder):
    image_path = os.path.join(image_folder, image_file)
    
    # Detect faces
    detected_faces = detect_faces(image_path)
    
    # Visualize faces
    output_image = visualize_faces(image_path, detected_faces)
    
    # Save the output image
    output_path = os.path.join(output_folder, f"detected_{image_file}")
    cv2.imwrite(output_path, output_image)
    
    return image_file, len(detected_faces)

# Example usage
if __name__ == "__main__":
    image_folder = "output_frames"  # Folder containing images
    output_folder = "output"  # Folder to save output images
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Get list of image files
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    # Process images in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_image, image_file, image_folder, output_folder) for image_file in image_files]
        
        for future in concurrent.futures.as_completed(futures):
            image_file, num_faces = future.result()
            print(f"Processed {image_file}: Detected {num_faces} faces")
    
    print("Processing complete. Check the output folder for results.")
