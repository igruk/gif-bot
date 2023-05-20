import os
from typing import List

import cv2
from skimage.metrics import structural_similarity as ssim


def split_video(input_path: str, similarity_threshold: float = 0.25) -> List[str]:
    """
    Split video into non-similar frames using OpenCV and Scikit-Image.
    Return list of saved frames.

    similarity_threshold is a value between 0 and 1, where 0 indicates no similarity and 1 indicates identical images.
    """
    # Extract the input video filename
    video_filename = os.path.basename(input_path)
    video_name = os.path.splitext(video_filename)[0]

    # Create the output folder
    output_folder = f"frames/{video_name}"
    os.makedirs(output_folder, exist_ok=True)

    # Open the video file
    video = cv2.VideoCapture(input_path)
    frame_count = 0
    prev_frame = None
    list_frames = []

    # Loop through the video frames
    while video.isOpened():
        # Read the next frame
        ret, frame = video.read()

        # Check if the frame was successfully read
        if not ret:
            break

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Compare the frame with the previous frame
        if prev_frame is not None:
            similarity = ssim(prev_frame, gray_frame)
            if similarity >= similarity_threshold:
                continue

        # Save the frame as an image
        frame_count += 1
        frame_name = f"frame_{frame_count}.jpg"
        frame_path = os.path.join(output_folder, frame_name)
        list_frames.append(frame_path)
        cv2.imwrite(frame_path, frame)

        # Update the previous frame
        prev_frame = gray_frame.copy()

    # Release the video file and close any open windows
    video.release()
    cv2.destroyAllWindows()

    return list_frames





