import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import cv2
import os
from PIL import Image, ImageTk

class VideoEditor:
    def __init__(self, window):
        self.window = window
        self.window.title("Video Editor")
        self.window.attributes('-fullscreen', True)

        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        self.window.geometry("{0}x{1}+0+0".format(self.width,self.height))

        self.cap = None
        self.playing = False
        self.current_frame = 0
        self.current_video_index = 0
        self.video_files = []
        self.output_dir = None

        self.create_widgets()
        self.bind_events()

    def create_widgets(self):
        # Image display
        self.canvas_width = int(self.width * 7/8)
        self.canvas_height = int(self.height * 6/7)
        self.canvas = tk.Canvas(self.window, width= self.canvas_width , height= self.canvas_height)
        self.canvas.pack(pady=10)

        # Slider
        self.slider = ttk.Scale(self.window, from_=0, to=100, orient="horizontal", length=750)
        self.slider.pack(pady=10)
        self.slider.bind("<ButtonRelease-1>", self.slider_moved)

        # Buttons
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=10)

        self.play_pause_btn = ttk.Button(button_frame, text="Play", command=self.play_pause)
        self.play_pause_btn.grid(row=0, column=0, padx=5)

        self.prev_frame_btn = ttk.Button(button_frame, text="Previous Frame", command=self.prev_frame)
        self.prev_frame_btn.grid(row=0, column=1, padx=5)

        self.next_frame_btn = ttk.Button(button_frame, text="Next Frame", command=self.next_frame)
        self.next_frame_btn.grid(row=0, column=2, padx=5)

        self.save_frame_btn = ttk.Button(button_frame, text="Save Frame", command=self.save_frame)
        self.save_frame_btn.grid(row=0, column=3, padx=5)

        self.open_dir_btn = ttk.Button(button_frame, text="Open Directory", command=self.open_directory)
        self.open_dir_btn.grid(row=0, column=4, padx=5)

        self.output_dir_btn = ttk.Button(button_frame, text="Output Directory", command=self.output_directory)
        self.output_dir_btn.grid(row=0, column=5, padx=5)

    def bind_events(self):
        self.window.bind('<Left>', lambda e: self.prev_frame())
        self.window.bind('<Right>', lambda e: self.next_frame())
        self.window.bind('s', lambda e: self.save_frame())

    def open_directory(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.video_files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) 
                                if f.lower().endswith(('.mov', '.mp4'))]
            if self.video_files:
                self.current_video_index = 0
                self.current_video = self.video_files[self.current_video_index]
                self.load_video(self.current_video)
            else:
                print("No video files found in the selected directory.")
    
    def output_directory(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.output_dir = dir_path
            print(f"Output directory set to: {self.output_dir}")

    def load_video(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        self.current_frame = 0
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.slider.config(to=total_frames - 1)
        self.update_frame()

    def update_frame(self):
        if self.cap is None:
            return

        ret, frame = self.cap.read()
        if ret:
            self.current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1
            self.slider.set(self.current_frame)
            self.display_frame(frame)
            if self.playing:
                self.window.after(33, self.update_frame)  # Approximately 30 fps
        else:
            self.playing = False
            self.play_pause_btn.config(text="Play")
            self.next_video()

    def display_frame(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_image = cv2.resize(rgb_image, (self.canvas_width, self.canvas_height))
        pil_image = Image.fromarray(rgb_image)
        photo = ImageTk.PhotoImage(image=pil_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo  # Keep a reference to prevent garbage collection

    def play_pause(self):
        if self.cap is None:
            return

        if self.playing:
            self.playing = False
            self.play_pause_btn.config(text="Play")
        else:
            self.playing = True
            self.play_pause_btn.config(text="Pause")
            self.update_frame()

    def prev_frame(self):
        if self.cap is None:
            return

        self.current_frame = max(0, self.current_frame - 1)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        self.update_frame()

    def next_frame(self):
        if self.cap is None:
            return

        self.current_frame += 1
        if self.current_frame >= int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)):
            self.next_video()
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
            self.update_frame()

    def next_video(self):
        if self.current_video_index < len(self.video_files) - 1:
            self.current_video_index += 1
            self.load_video(self.video_files[self.current_video_index])
        else:
            print("All videos have been played.")

    def save_frame(self):
        if self.cap is None:
            return
        
        if self.output_dir is None:
            messagebox.showerror("Error", "Output directory not set.")
            return
        file_path = os.path.join(self.output_dir, f"{self.current_video.split("/")[-1].split(".")[0]}_{self.current_frame}.jpg")
        if file_path:
            ret, frame = self.cap.read()
            if ret:
                cv2.imwrite(file_path, frame)
                print(f"Frame saved to {file_path}")
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)

    def slider_moved(self, event):
        if self.cap is None:
            return

        frame_pos = int(self.slider.get())
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
        self.update_frame()

if __name__ == '__main__':
    root = tk.Tk()
    editor = VideoEditor(root)
    root.mainloop()