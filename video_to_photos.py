import cv2
import os
import tkinter as tk
from tkinter import filedialog

def capture_frames(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Save the frame as an image in the output folder
        frame_filename = f"frame_{frame_count:05d}.jpg"
        frame_filepath = os.path.join(output_folder, frame_filename)
        cv2.imwrite(frame_filepath, frame)

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

def image_clarity(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clarity = cv2.Laplacian(gray, cv2.CV_64F).var()
    return clarity

def select_clearest_images(folder_path, num_images=5):
    image_files = os.listdir(folder_path)
    image_files = sorted(image_files)

    
    sorted_images = sorted(image_files, key=lambda x: image_clarity(os.path.join(folder_path, x)), reverse=True)

  
    selected_images = sorted_images[:num_images]

    return [os.path.join(folder_path, img) for img in selected_images]

def process_video():
    video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4")])
    if not video_path:
        return

    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if not output_folder:
        return

    capture_frames(video_path, output_folder)
    selected_images = select_clearest_images(output_folder)

    clearest_images_folder = os.path.join(output_folder, "clearest_images")
    os.makedirs(clearest_images_folder, exist_ok=True)

    for img_path in selected_images:
        _, img_filename = os.path.split(img_path)
        new_img_path = os.path.join(clearest_images_folder, img_filename)
        os.rename(img_path, new_img_path)

    status_label.config(text="Five Clearest Images have been saved to the 'clearest_images' folder.")

# GUI setup
root = tk.Tk()
root.title("Video to Photos")
root.geometry("400x200")

process_button = tk.Button(root, text="Process Video", command=process_video)
process_button.pack(pady=20)

status_label = tk.Label(root, text="", fg="green")
status_label.pack()

root.mainloop()

#AUTHOR : Kartikay Misra
