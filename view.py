
import numpy as np
import matplotlib.pyplot as plt


def create_sine_wave():
    frequency = 5
    amplitude = 1
    duration = 10
    sampling_rate = 1000
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    y = amplitude * np.sin(2 * np.pi * frequency * t)

    # Plot the sine wave
    plt.plot(t, y)
    plt.title('Sine Wave')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.show()

if __name__ == "__main__":
    create_sine_wave()
