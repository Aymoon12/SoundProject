# model.py
import os
import pydub
import numpy as np
import scipy.signal
from scipy.io import wavfile
from pydub import AudioSegment


class AudioModel:
    def __init__(self):
        self.sample_file_path = None
        self.audio_data = None

    def load_sample_file(self, file_path):
        # Handles loading of WAV, MP3, and AAC files
        self.sample_file_path = file_path
        file_extension = os.path.splitext(file_path)[1].lower()
        # Load file using pydub, which supports multiple formats
        try:
            if file_extension in ['.mp3', '.aac']:
                self.audio_data = AudioSegment.from_file(file_path, file_extension[1:])
            elif file_extension == '.wav':
                self.audio_data = AudioSegment.from_wav(file_path)
            else:
                return False  # or raise an exception for unsupported format
            return True
        except:
            return False  # or handle / log exception as per your program's requirements


    def convert_to_wav(self):
        # Converts to WAV if it's not already a WAV file
        _, file_extension = os.path.splitext(self.sample_file_path)
        if file_extension.lower() != '.wav':
            wav_file_path = self.sample_file_path.replace(file_extension, '.wav')
            self.audio_data.export(wav_file_path, format='wav')
            self.audio_data = AudioSegment.from_wav(wav_file_path)
            self.sample_file_path = wav_file_path

    def remove_metadata(self):
        self.sample_file_path = self.sample_file_path.replace(".wav", "_cleaned.wav")
        self.audio_data.export(self.sample_file_path, format="wav", tags={})

    def convert_to_mono(self):
        if self.audio_data.channels > 1:
            self.audio_data = self.audio_data.set_channels(1)
            self.sample_file_path = self.sample_file_path.replace(".wav", "_mono.wav")
            self.audio_data.export(self.sample_file_path, format="wav")

    def get_duration_seconds(self):
        return len(self.audio_data) / 1000.0

    def get_highest_resonance_frequency(self):
        sample_rate = self.audio_data.frame_rate
        samples = np.array(self.audio_data.get_array_of_samples())
        frequencies, times, Sxx = scipy.signal.spectrogram(samples, fs=sample_rate, nperseg=1024)
        Sxx_sum = Sxx.sum(axis=1)
        highest_resonance_idx = np.argmax(Sxx_sum)
        highest_resonance_frequency = frequencies[highest_resonance_idx]
        return highest_resonance_frequency

    def calculate_rt60_for_frequency(self, frequency):
        # Get the data and sample rate from the audio segment
        samples = np.array(self.audio_data.get_array_of_samples())
        sample_rate = self.audio_data.frame_rate
        # Calculate the spectrogram
        f, t, Sxx = scipy.signal.spectrogram(samples, fs=sample_rate, nfft=1024)
        Sxx_dB = 10 * np.log10(Sxx)

        # Find the index of the frequency
        idx = (np.abs(f - frequency)).argmin()

        # Get the power for the specific frequency
        freq_power = Sxx_dB[idx]
        # Slice the data starting from the maximum value
        max_idx = np.argmax(freq_power)
        data_slice = freq_power[max_idx:]

        # Define reverberation time estimation logic
        # max - 5dB
        ref_value = np.max(data_slice) - 5
        ref_idx = (np.abs(data_slice - ref_value)).argmin() + max_idx
        # max - 25dB (or 20 for RT20)
        end_value = np.max(data_slice) - 25
        end_idx = (np.abs(data_slice - end_value)).argmin() + max_idx
        # Calculate RT20 or RT60
        rt60 = (t[end_idx] - t[ref_idx]) * 3

        # The time slice and decibel levels for plotting
        time_slice = t[max_idx:end_idx]
        decibel_slice = data_slice[:end_idx - max_idx]

        return rt60, time_slice, decibel_slice

    def calculate_all_rt60(self):
        # Define low, mid, and high frequency ranges
        low_freq = 125
        mid_freq = 500
        high_freq = 2000

        # Calculate RT60 for each band
        rt60_low, time_slice_low, decibel_slice_low = self.calculate_rt60_for_frequency(low_freq)
        rt60_mid, time_slice_mid, decibel_slice_mid = self.calculate_rt60_for_frequency(mid_freq)
        rt60_high, time_slice_high, decibel_slice_high = self.calculate_rt60_for_frequency(high_freq)

        return {
            "low": (rt60_low, time_slice_low, decibel_slice_low),
            "mid": (rt60_mid, time_slice_mid, decibel_slice_mid),
            "high": (rt60_high, time_slice_high, decibel_slice_high),
        }

    def calculate_spectrum(self, low_freq, high_freq):
        sample_rate = self.audio_data.frame_rate
        samples = np.array(self.audio_data.get_array_of_samples())
        frequencies, times, Sxx = scipy.signal.spectrogram(samples, fs=sample_rate)
        power_db = 10 * np.log10(Sxx)
        freq_indices = np.where((frequencies >= low_freq) & (frequencies <= high_freq))
        return times, frequencies[freq_indices], power_db[freq_indices]