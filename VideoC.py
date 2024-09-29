import cv2
import os
import numpy as np

def create_video_from_images(image_folder, output_video_path, fps=30):
    # Get list of image files
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg") or img.endswith(".png")]
    images.sort()  # Ensure images are in order

    # Read the first image to get dimensions
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Iterate through images and add to video
    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)

    # Release the video writer
    video.release()

    print(f"Video created successfully: {output_video_path}")

if __name__ == "__main__":
    image_folder = "output"  # Folder containing images
    output_video = "videooutput/output_video.mp4"  # Output video file name
    create_video_from_images(image_folder, output_video)
