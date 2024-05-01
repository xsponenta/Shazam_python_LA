import numpy as np

def fft(signal, n=None):
    if n is None:
        n = len(signal)

    return np.sum(signal * np.exp(-2j * np.pi * np.arange(n) / n)[:, None], axis=0)


def stft(signal, window_length, hop_length):
    signal_length = len(signal)

    num_windows = 1 + (signal_length - window_length) // hop_length

    stft_result = np.zeros((num_windows, window_length), dtype=np.complex128)

    for i in range(num_windows):
        start = i * hop_length
        end = start + window_length

        windowed_signal = signal[start:end].astype(np.float64)

        windowed_signal *= np.hanning(window_length)

        fft_result = np.fft.fft(windowed_signal)

        stft_result[i, :] = fft_result

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

    for i in range(1, len(x) - 1):
        if x[i] > x[i - 1] and x[i] > x[i + 1]:
            peaks.append(i)
            peak_heights.append(x[i])

    for peak in peaks:
        left_base = peak
        right_base = peak
        prominence_value = x[peak]

        while left_base > 0 and x[left_base] <= x[left_base - 1]:
            left_base -= 1
        left_bases.append(left_base)

        while right_base < len(x) - 1 and x[right_base] <= x[right_base + 1]:
            right_base += 1
        right_bases.append(right_base)

        prominence_value -= min(x[left_base], x[right_base])
        prominences.append(prominence_value)

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

    if distance is not None:
        filtered_peaks = [peaks[0]]
        filtered_peak_heights = [peak_heights[0]]
        filtered_left_bases = [left_bases[0]]
        filtered_right_bases = [right_bases[0]]
        filtered_prominences = [prominences[0]]

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

