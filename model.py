# audio_model.py
import numpy as np
from scipy.io import wavfile
from scipy.signal import find_peaks
from pydub import AudioSegment

class AudioModel:
    def __init__(self):
        self.file_path = None
        self.rt60_low = None
        self.rt60_mid = None
        self.rt60_high = None
        self.peak_frequency = None
        self.duration_seconds = None

    def set_file_path(self, file_path):
        self.file_path = file_path
        # Check if the file is not in wav format and convert it if necessary
        if not self.file_path.endswith('.wav'):
            sound = AudioSegment.from_file(self.file_path)
            self.file_path = self.file_path.replace('.mp3', '.wav')
            sound.export(self.file_path, format="wav")

    def calculate_rt60(self, data, fs, f_low, f_high):
        n = len(data)
        yf = np.fft.fft(data)
        xf = np.fft.fftfreq(n, 1 / fs)

        mask = (xf >= f_low) & (xf <= f_high)

        # Zero out frequencies outside the specified range in the mask
        yf_filtered = yf.copy()
        yf_filtered[~mask] = 0

        peaks, _ = find_peaks(np.abs(yf_filtered), height=0)

        rt60 = -60 / (np.mean(np.diff(peaks)) / fs / np.log(0.001))

        return rt60
    def process_audio(self):
        fs, data = wavfile.read(self.file_path)

        self.rt60_low = self.calculate_rt60(data, fs, 20, 200)
        self.rt60_mid = self.calculate_rt60(data, fs, 200, 2000)
        self.rt60_high = self.calculate_rt60(data, fs, 2000, 20000)

        self.peak_frequency = self.find_peak_frequency(data, fs)

        # Additional info
        self.duration_seconds = len(data) / fs

    def find_peak_frequency(self, data, fs):
        # Calculate the frequency spectrum using FFT
        n = len(data)
        yf = np.fft.fft(data)
        xf = np.fft.fftfreq(n, 1/fs)[:n//2]

        # Find peaks in the frequency spectrum
        peaks, _ = find_peaks(np.abs(yf), height=0)

        # Get the frequency corresponding to the highest peak
        peak_freq = xf[peaks][np.argmax(np.abs(yf[peaks]))]

        return peak_freq

    def reduce_rt60(self, target_rt60=0.5):
        # Calculate the difference in RT60 time to reduce RT60 to the target value
        rt60_difference = target_rt60 - max(self.rt60_low, self.rt60_mid, self.rt60_high)
        return rt60_difference
