import numpy as np

def fft(signal, n=None):
    if n is None:
        n = len(signal)

    # Згортка сигналу з комплексною експонентою
    return np.sum(signal * np.exp(-2j * np.pi * np.arange(n) / n)[:, None], axis=0)


def stft(signal, window_length, hop_length):
    # Розмір сигналу
    signal_length = len(signal)

    # Кількість вікон STFT
    num_windows = 1 + (signal_length - window_length) // hop_length

    # Ініціалізуємо масив для збереження результату STFT
    stft_result = np.zeros((num_windows, window_length), dtype=signal.dtype)

    # Цикл по вікнам
    for i in range(num_windows):
        # Обчислюємо початок та кінець поточного вікна
        start = i * hop_length
        end = start + window_length

        # Вирізаємо поточне вікно з сигналу
        windowed_signal = signal[start:end]

        # Застосовуємо вікно Ханна (Hanning window)
        windowed_signal *= np.hanning(window_length)

        # Обчислюємо швидке перетворення Фур'є (FFT)
        stft_result[i] = fft(windowed_signal, n=window_length)

    return stft_result


def fftfreq(n, d=1.0):
    """Compute the sample frequencies for an FFT of length n.

    Parameters:
        n (int): The number of samples in the FFT.
        d (float, optional): The sample spacing (inverse of the sampling frequency). Default is 1.0.

    Returns:
        ndarray: Array of length `n` containing the sample frequencies.

    Example:
        >>> fftfreq(6)
        array([0.        , 0.16666667, 0.33333333, -0.5       , -0.33333333, -0.16666667])
    """
    if n % 2 == 0:
        val = np.arange(0, n // 2 + 1, dtype=int)
    else:
        val = np.arange(0, (n - 1) // 2 + 1, dtype=int)
    return np.hstack((val, -val[::-1])) / (n * d)


def find_peaks(x, prominence=None, distance=None):
    peaks = []
    peak_heights = []
    left_bases = []
    right_bases = []
    prominences = []

    # Find peaks
    for i in range(1, len(x) - 1):
        if x[i] > x[i - 1] and x[i] > x[i + 1]:
            peaks.append(i)
            peak_heights.append(x[i])

    # Calculate left and right bases, and prominences
    for peak in peaks:
        left_base = peak
        right_base = peak
        prominence_value = x[peak]

        # Find left base
        while left_base > 0 and x[left_base] <= x[left_base - 1]:
            left_base -= 1
        left_bases.append(left_base)

        # Find right base
        while right_base < len(x) - 1 and x[right_base] <= x[right_base + 1]:
            right_base += 1
        right_bases.append(right_base)

        # Calculate prominence
        prominence_value -= min(x[left_base], x[right_base])
        prominences.append(prominence_value)

    # Apply prominence filter
    if prominence is not None:
        filtered_peaks = []
        filtered_peak_heights = []
        filtered_left_bases = []
        filtered_right_bases = []
        filtered_prominences = []

        for i in range(len(peaks)):
            if prominences[i] >= prominence:
                filtered_peaks.append(peaks[i])
                filtered_peak_heights.append(peak_heights[i])
                filtered_left_bases.append(left_bases[i])
                filtered_right_bases.append(right_bases[i])
                filtered_prominences.append(prominences[i])

        peaks = filtered_peaks
        peak_heights = filtered_peak_heights
        left_bases = filtered_left_bases
        right_bases = filtered_right_bases
        prominences = filtered_prominences

    # Apply distance filter
    if distance is not None:
        filtered_peaks = []
        filtered_peak_heights = []
        filtered_left_bases = []
        filtered_right_bases = []
        filtered_prominences = []

        for i in range(1, len(peaks)):
            if peaks[i] - peaks[i - 1] >= distance:
                filtered_peaks.append(peaks[i])
                filtered_peak_heights.append(peak_heights[i])
                filtered_left_bases.append(left_bases[i])
                filtered_right_bases.append(right_bases[i])
                filtered_prominences.append(prominences[i])

        peaks = filtered_peaks
        peak_heights = filtered_peak_heights
        left_bases = filtered_left_bases
        right_bases = filtered_right_bases
        prominences = filtered_prominences

    return {'peaks': np.array(peaks),
            'peak_heights': np.array(peak_heights),
            'prominences': np.array(prominences),
            'left_bases': np.array(left_bases),
            'right_bases': np.array(right_bases)}
