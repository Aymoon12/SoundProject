import os
from tkinter import Tk, filedialog, Button, Label
from pydub import AudioSegment
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import PhotoImage
from PIL import ImageTk


class AudioProcessor:
    def __init__(self, root):
        self.root = root
        self.file_path = None
        self.waveform_image = None  # Store the reference to prevent garbage collection

        # GUI components
        self.load_button = Button(root, text="Load Audio File", command=self.load_file)
        self.load_button.pack()

        self.file_label = Label(root, text="")
        self.file_label.pack()

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3;*.aac")])

        if self.file_path:
            self.process_audio()

    def process_audio(self):
        # Check if the file is WAV, MP3, or AAC
        _, file_extension = os.path.splitext(self.file_path)
        if file_extension.lower() != '.wav':
            # Convert to WAV
            self.file_path = self.convert_to_wav()

        # Check for metadata and remove if present
        audio = AudioSegment.from_file(self.file_path, format="wav")

        # Check for tags in the audio file
        if hasattr(audio, 'info') and audio.info.get('tags'):
            audio = audio.remove_tags()

        # Check for multi-channel and convert to mono if necessary
        if audio.channels > 1:
            audio = audio.set_channels(1)

        # Display time value of WAV in seconds
        duration_seconds = len(audio) / 1000.0
        print(f"Duration: {duration_seconds} seconds")

        # Display the waveform in Tkinter
        self.display_waveform_tkinter(audio)

    def convert_to_wav(self):
        # Convert to WAV using pydub
        audio = AudioSegment.from_file(self.file_path)
        new_file_path = os.path.splitext(self.file_path)[0] + ".wav"
        audio.export(new_file_path, format="wav")
        return new_file_path

    def display_waveform_tkinter(self, audio):
        # Generate waveform image
        waveform_image = self.generate_waveform_image(audio)

        # Display waveform in Tkinter window
        if not hasattr(self, 'label'):
            # Create a Label if it doesn't exist
            self.label = Label(self.root)
            self.label.pack()

        # Set the image reference to the instance variable
        self.waveform_image = waveform_image
        self.label.configure(image=self.waveform_image)

    def generate_waveform_image(self, audio):
        samples = np.array(audio.get_array_of_samples())
        time = np.arange(0, len(samples)) / audio.frame_rate

        fig, ax = plt.subplots(figsize=(5, 2), dpi=100)
        ax.plot(time, samples)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.set_title("Waveform")

        # Convert the Matplotlib figure to a Tkinter-compatible format
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        pil_image = Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
        tk_image = ImageTk.PhotoImage(pil_image)

        return tk_image


if __name__ == "__main__":
    root = Tk()
    root.title("Audio Processor")
    audio_processor = AudioProcessor(root)
    root.mainloop()