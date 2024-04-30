import numpy as np
from scipy.io.wavfile import read
from scipy import signal
from fft_just_do_it import *

def create_constellation(audio, Fs, chunk_size=1000):
    window_length_seconds = 0.05
    window_length_samples = int(window_length_seconds * Fs)
    window_length_samples += window_length_samples % 2
    num_peaks = 15

    constellation_map = []

    for start in range(0, len(audio), chunk_size):
        end = start + chunk_size
        chunk = audio[start:end]

        amount_to_pad = window_length_samples - chunk.size % window_length_samples
        padded_chunk = np.pad(chunk, (0, amount_to_pad))

        nperseg = min(window_length_samples, len(padded_chunk))

        frequencies, times, stft_result = stft(
            padded_chunk, Fs, nperseg=nperseg, nfft=nperseg, return_onesided=True
        )

        a = False

        for time_idx, window in enumerate(stft_result.T):
            spectrum = abs(window)
            spectrum = np.squeeze(spectrum).ravel()
            peaks, props = signal.find_peaks(spectrum, prominence=0)

            n_peaks = min(num_peaks, len(peaks))
            largest_peaks = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]
            for peak in peaks[largest_peaks]:
                frequency = frequencies[peak%len(frequencies)]
                constellation_map.append([time_idx + start, frequency])
                if len(constellation_map) >= len(peaks[largest_peaks]):
                    a = True
                    break
            if a == True:
                break
        if a == True:
            break


    return constellation_map

if __name__ == "__main__":
    Fs, audio_input = read("data/Rain Over Me.wav")
    constellation = create_constellation(audio_input, Fs)
    print(constellation)