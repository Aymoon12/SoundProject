import tkinter as tk
from tkinter import filedialog
import os
import pydub
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from model import AudioModel
from view import AudioView
from scipy.fft import fft


class AudioController:
    def __init__(self, master):
        self.model = AudioModel()
        self.view = AudioView(master, self)

    def load_sample_file(self):
        file_path = filedialog.askopenfilename(title="Select Sample File",
                                               filetypes=[("Audio Files", "*.wav;*.mp3;*.aac")])
        if file_path:
            self.model.load_sample_file(file_path)
            self.view.show_message(f"Sample File Loaded: {self.model.sample_file_path}")

            # Additional logic to handle audio file processing
            self.process_audio_file()

    def process_audio_file(self):
        # Check file format and convert to wav if necessary
        self.model.convert_to_wav()

        # Remove metadata (tags)
        self.model.remove_metadata()

        # Handle multi-channel or convert to one channel
        self.model.convert_to_mono()

        # Display waveform
        self.view.show_waveform(self.model.audio_data.get_array_of_samples())

        # Plot waveform and RT60 for Low, Mid, High frequencies, and an additional plot
        self.plot_waveform_and_rt60()

        # Display text output
        self.display_text_output()

    def plot_waveform_and_rt60(self):
        # Plot waveform
        plt.figure(figsize=(10, 6))
        samples = self.model.audio_data.get_array_of_samples()
        plt.plot(samples)
        plt.xlabel('Sample')
        plt.ylabel('Amplitude')
        plt.title('Waveform')

        # Plot RT60 for Low, Mid, High frequencies, and an additional plot
        # Add your specific logic for RT60 calculation based on frequency ranges
        frequencies = ["Low", "Mid", "High", "Additional"]
        rt60_values = [self.model.calculate_rt60() for _ in range(len(frequencies))]

        plt.figure(figsize=(10, 6))
        plt.bar(frequencies, rt60_values)
        plt.xlabel('Frequency Range')
        plt.ylabel('RT60')
        plt.title('RT60 for Different Frequency Ranges')

        # Display the plots in the Tkinter window
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.view.master)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def display_text_output(self):
        # Display text output
        duration = len(self.model.audio_data) / 1000.0  # Duration in seconds
        samples = self.model.audio_data.get_array_of_samples()
        frequency_of_greatest_amplitude = np.argmax(samples)  # Find the index of the maximum value

        # Add your specific logic for calculating RT60 differences in seconds
        rt60_low = self.calculate_rt60_difference("Low")
        rt60_mid = self.calculate_rt60_difference("Mid")
        rt60_high = self.calculate_rt60_difference("High")
        rt60_additional = self.calculate_rt60_difference("Additional")

        text_output = (
            f"Time in seconds: {duration}\n"
            f"Highest resonance display frequency: {frequency_of_greatest_amplitude}\n"
            f"RT60 differences: Low: {rt60_low}, Mid: {rt60_mid}, High: {rt60_high}, Additional: {rt60_additional}"
        )

        self.view.show_message(text_output)

    def calculate_rt60_difference(self, frequency_range):
        # Example: Calculate RT60 difference for a specific frequency range
        rt60_range = self.model.calculate_rt60()  # Replace with your specific RT60 calculation logic
        return rt60_range





if __name__ == "__main__":
    root = tk.Tk()
    app = AudioController(root)
    root.mainloop()
