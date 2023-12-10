# view.py
import tkinter as tk
import tkinter.messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AudioView:
    def __init__(self, master, controller):
        self.master = master
        self.controller = controller
        self.load_file_button = tk.Button(self.master, text="Load Sound File", command=self.controller.load_sample_file)
        self.load_file_button.pack()
        self.canvas = None




        self.switch_rt60_plot_button = tk.Button(self.master, text="Switch RT60 Plot",
                                                 command=self.controller.switch_rt60_plot)
        self.switch_rt60_plot_button.pack()

        # Button to combine RT60 plots
        self.combine_rt60_button = tk.Button(self.master, text="Combine RT60 Plots",
                                             command=self.controller.combine_rt60_plots)
        self.combine_rt60_button.pack()

        self.canvas = None

    def show_message(self, message):
        print(message)
        tk.messagebox.showinfo("Information", message)

    def create_matplotlib_canvas(self, fig):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def show_waveform(self, samples):
        fig = Figure(figsize=(10, 6))
        subplot = fig.add_subplot(1, 1, 1)
        subplot.plot(samples)
        subplot.set_xlabel('Sample')
        subplot.set_ylabel('Amplitude')
        subplot.set_title('Waveform')
        self.create_matplotlib_canvas(fig)

    def show_rt60_plot(self, title, time_slice, decibel_slice):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        fig = Figure(figsize=(10, 4))
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(time_slice, decibel_slice)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Decibels (dB)')
        ax.set_title(title)
        ax.grid()

        self.canvas = FigureCanvasTkAgg(fig, self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
