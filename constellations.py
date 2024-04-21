import numpy as np
from scipy import signal
from scipy.io.wavfile import read
from fft_just_do_it import stft, fftfreq, find_peaks

def create_constellation(audio, Fs):
    window_length_seconds = 0.5
    window_length_samples = int(window_length_seconds * Fs)
    window_length_samples += window_length_samples % 2
    num_peaks = 15
    amount_to_pad = window_length_samples - audio.size % window_length_samples
    song_input = np.pad(audio, (0, amount_to_pad))
    stft_result = stft(song_input, window_length_samples, window_length_samples)
    frequencies = fftfreq(window_length_samples, 1/Fs)

    constellation_map = []

    for time_idx, window in enumerate(stft_result.T):
        spectrum = abs(window)
        peaks, props = find_peaks(spectrum, prominence=0, distance=200)
        n_peaks = min(num_peaks, len(peaks))
        largest_peaks = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]
        for peak in peaks[largest_peaks]:
            frequency = frequencies[peak]
            constellation_map.append([time_idx, frequency])

    return constellation_map


Fs, input = read("data/001. 24kgoldn - Mood (feat. iann dior).wav")
constellation_map = create_constellation(input, Fs)
