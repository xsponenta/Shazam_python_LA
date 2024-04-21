import numpy as np
from scipy import signal
from scipy.io.wavfile import read
from fft_just_do_it import stft, fftfreq, find_peaks


def create_constellation(audio, Fs, chunk_size=10000):
    window_length_seconds = 0.5
    window_length_samples = int(window_length_seconds * Fs)
    window_length_samples += window_length_samples % 2
    num_peaks = 15

    constellation_map = []

    for start in range(0, len(audio), chunk_size):
        end = start + chunk_size
        chunk = audio[start:end]
        amount_to_pad = window_length_samples - chunk.size % window_length_samples
        padded_chunk = np.pad(chunk, (0, amount_to_pad))
        stft_result = stft(padded_chunk, window_length_samples, window_length_samples)
        frequencies = fftfreq(window_length_samples, 1/Fs)

        for time_idx, window in enumerate(stft_result.T):
            spectrum = abs(window)
            peak_results = find_peaks(spectrum, prominence=0, distance=200)
            peaks = peak_results['peaks']
            props = {'prominences': peak_results['prominences']}
            n_peaks = min(num_peaks, len(peaks))
            largest_peaks = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]
            for peak in peaks[largest_peaks]:
                frequency = frequencies[peak]
                constellation_map.append([time_idx + start, frequency])

    return constellation_map

Fs, input = read("Rain Over Me.wav")
constellation_map = create_constellation(input, Fs)
