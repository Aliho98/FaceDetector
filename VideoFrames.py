import cv2
import os
import multiprocessing as mp

def extract_frame(args):
    frame_number, video_path, output_folder = args
    video = cv2.VideoCapture(video_path)
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    success, frame = video.read()
    if success:
        frame_filename = os.path.join(output_folder, f"frame_{frame_number:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
    video.release()
    return frame_number

def extract_frames(video_path, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Get the total number of frames in the video
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Release the video capture object
    video.release()

    # Create a pool of workers
    pool = mp.Pool(processes=mp.cpu_count())

    # Prepare arguments for each frame
    args = [(i, video_path, output_folder) for i in range(total_frames)]

    # Extract frames in parallel
    for i, _ in enumerate(pool.imap_unordered(extract_frame, args), 1):
        print(f"\rExtracted frame {i}/{total_frames}", end='')

    # Close the pool
    pool.close()
    pool.join()

    print(f"\nExtraction complete. {total_frames} frames saved to {output_folder}")

# Example usage
if __name__ == "__main__":
    name=input("enter the name of the video located in video input(with file extension):")
    video_path = "videoinput/"+name
    output_folder = "output_frames"
    extract_frames(video_path, output_folder)
