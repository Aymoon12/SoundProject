# main.py
import tkinter as tk
from tkinter import filedialog
import os
import pydub
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from model import AudioModel
from view import AudioView


class AudioController:
    def __init__(self, master):
        self.model = AudioModel()
        self.view = AudioView(master, self)
        self.current_plot = 'low'
        self.current_rt60_plot = 'low'  # low, mid, high
        self.rt60_data = {}

    def load_sample_file(self):
        file_path = filedialog.askopenfilename(title="Select Sample File",
                                               filetypes=[("Audio Files", "*.wav;*.mp3;*.aac")])
        if file_path:
            success = self.model.load_sample_file(file_path)
            if success:
                self.view.show_message(f"Sample File Loaded: {file_path}")
                self.process_audio_file()
            else:
                self.view.show_message("Failed to load file. Unsupported file type or corrupted file.")
        else:
            self.view.show_message("No file was selected.")

    def process_audio_file(self):
        self.model.convert_to_wav()
        self.model.remove_metadata()
        self.model.convert_to_mono()
        self.display_rt60_analysis()
        self.view.show_waveform(self.model.audio_data.get_array_of_samples())
        self.display_text_output()

    def display_highest_resonance_frequency(self):
        highest_resonance_freq = self.model.get_highest_resonance_frequency()
        self.view.show_message(f"Highest Resonance Frequency: {highest_resonance_freq:.2f} Hz")

    def display_rt60_analysis(self):
        rt60_results = self.model.calculate_all_rt60()
        for band, (rt60, time_slice, decibel_slice) in rt60_results.items():
            self.view.show_rt60_plot(f"{band.capitalize()} Frequency Band", time_slice, decibel_slice)
        self.rt60_data = self.model.calculate_all_rt60()
        self.display_rt60_plot()





    def display_rt60_plot(self):
        # Fetch the data for the current plot and display it
        rt60_info = self.rt60_data[self.current_rt60_plot]
        self.view.show_rt60_plot(f"{self.current_rt60_plot.capitalize()} Frequency Band",
                                 rt60_info[1], rt60_info[2])
    def switch_rt60_plot(self):
        # Cycle through the RT60 plots
        if self.current_rt60_plot == 'low':
            self.current_rt60_plot = 'mid'
        elif self.current_rt60_plot == 'mid':
            self.current_rt60_plot = 'high'
        else:
            self.current_rt60_plot = 'low'
        self.display_rt60_plot()

    def combine_rt60_plots(self):
        fig = plt.figure(figsize=(10, 6))

        # Combine the RT60 plot data
        for band, (rt60, time_slice, decibel_slice) in self.rt60_data.items():
            plt.plot(time_slice, decibel_slice, label=f"{band.capitalize()} Frequencies")

        plt.xlabel('Time (s)')
        plt.ylabel('Decibels (dB)')
        plt.title('Combined RT60 Plot for All Frequency Bands')
        plt.legend()

        self.view.create_matplotlib_canvas(fig)

    def display_text_output(self):
        duration = len(self.model.audio_data) / 1000.0
        rt60_results = self.model.calculate_all_rt60()
        rt60_low = rt60_results['low'][0]
        rt60_mid = rt60_results['mid'][0]
        rt60_high = rt60_results['high'][0]
        average_rt60 = (rt60_low + rt60_mid + rt60_high) / 3
        rt60_difference = average_rt60 - 0.5
        highest_resonance = self.model.get_highest_resonance_frequency()

        text_output = (
            f"Time in seconds: {duration}\n"
            f"Average RT60: {average_rt60:.2f} seconds\n"
            f"RT60 difference from 0.5 sec: {rt60_difference:.2f} seconds\n"
            f"Highest Resonance Frequency: {highest_resonance:.2f} Hz"

        )
        self.view.show_message(text_output)

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioController(root)
    root.mainloop()
