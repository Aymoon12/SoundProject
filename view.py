import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class AudioView:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller

        # Create and pack GUI components
        self.load_file_button = tk.Button(self.master, text="Load Sound File", command=self.controller.load_sample_file)
        self.load_file_button.pack()

        # Additional GUI components for displaying messages, plots, etc. (as needed)
        self.canvas = None  # Canvas to display plots
        #
    def show_message(self, message):
        # Example: Display messages to the user
        print(message)

    def show_waveform(self, samples):
        # Display waveform
        plt.figure(figsize=(10, 6))
        plt.plot(samples)
        plt.xlabel('Sample')
        plt.ylabel('Amplitude')
        plt.title('Waveform')

        # Display the waveform in the Tkinter window
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def show_frequency_plot(self, frequencies, amplitudes):
        # Display frequencies plot
        plt.figure(figsize=(10, 6))
        plt.bar(frequencies, amplitudes)
        plt.xlabel('Frequency Range')
        plt.ylabel('Amplitude')
        plt.title('Frequency Ranges')

        # Display the frequencies plot in the Tkinter window
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)