import numpy as np
import matplotlib.pyplot as plt
from fft_just_do_it import stft, find_peaks, fftfreq
import signal
from scipy.io.wavfile import read

# Зчитуємо аудіофайл та встановлюємо параметри
Fs, input = read("Rain Over Me.wav")
time_to_plot = np.arange(Fs * 1, Fs * 1.5, dtype=int)

# Відображення сигналу в часовій області
plt.plot(time_to_plot, input[time_to_plot])
plt.title("Sound Signal")
plt.xlabel("Time Index")
plt.ylabel("Magnitude")

# Встановлюємо параметри для короткочасного перетворення Фур'є (STFT)
window_length_seconds = 2
window_length_samples = int(window_length_seconds * Fs)
window_length_samples += window_length_samples % 2
num_peaks = 7

# Доповнюємо вхідний сигнал
amount_to_pad = window_length_samples - input.size % window_length_samples
song_input = np.pad(input, (0, amount_to_pad))

# Обчислюємо короткочасне перетворення Фур'є
stft_result = stft(song_input, window_length_samples, window_length_samples)

# Вибираємо середнє вікно з STFT та його спектр
window = stft_result[stft_result.shape[0] // 2 + 5, :]
frequencies = fftfreq(window_length_samples, 1/Fs)

# Відображення спектру поточного вікна
plt.figure()
plt.plot(frequencies, abs(window) ** 2)
plt.title("Power Spectrum of Window")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power")

# Логарифмуємо та фільтруємо спектр
spectrum = np.log(abs(window) ** 2)
filter_freq = 0.005
b, a = signal.butter(3, filter_freq, "low")
filtered = signal.filtfilt(b, a, spectrum)

# Знаходимо та відображаємо піки
peaks = find_peaks(abs(window), prominence=0, distance=500)
n_peaks = min(num_peaks, len(peaks))
largest_peaks = np.argpartition(peaks["prominences"], -n_peaks)[-n_peaks:]
astrological_map = []
for peak in peaks[largest_peaks]:
    astrological_map.append([frequencies[peak], abs(window)[peak]])

# Відображення фільтрованого спектру та піків
plt.figure()
plt.plot(frequencies, abs(window), label="Filtered Power Spectrum")
plt.scatter(*zip(*astrological_map), color="r", zorder=10, label="Peaks")
plt.legend()
plt.title("Filtered Log Power Spectrum of Window")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Log Power")
plt.show()
