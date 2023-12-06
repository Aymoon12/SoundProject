from pydub import AudioSegment
import numpy as np


class AudioData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.audio = None
        self.sampling_rate = None
        self.samples = None

    def load_data(self):
        try:
            self.audio = AudioSegment.from_file(self.file_path)
            self.samples = np.array(self.audio.get_array_of_samples())
            self.sampling_rate = self.audio.frame_rate
            return True
        except Exception as e:
            print(f"Error loading audio file: {e}")
            return False

