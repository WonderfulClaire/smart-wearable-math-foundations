"""随机过程示例：周期图与 Welch PSD 估计的方差。"""

import numpy as np


def periodogram(x: np.ndarray, sample_rate: int) -> tuple[np.ndarray, np.ndarray]:
    window = np.hanning(len(x))
    spectrum = np.fft.rfft(x * window)
    scale = sample_rate * np.sum(window**2)
    return np.fft.rfftfreq(len(x), 1 / sample_rate), np.abs(spectrum) ** 2 / scale


def welch(x: np.ndarray, sample_rate: int, segment: int) -> tuple[np.ndarray, np.ndarray]:
    hop = segment // 2
    estimates = []
    for start in range(0, len(x) - segment + 1, hop):
        frequencies, estimate = periodogram(x[start : start + segment], sample_rate)
        estimates.append(estimate)
    return frequencies, np.mean(estimates, axis=0)


rng = np.random.default_rng(11)
sample_rate = 200
seconds = 20
time = np.arange(sample_rate * seconds) / sample_rate

# 1.2 Hz 模拟步频；后半段加入更强的宽带运动扰动，形成非平稳过程。
signal = np.sin(2 * np.pi * 1.2 * time)
noise = 0.35 * rng.normal(size=len(time))
noise[len(time) // 2 :] *= 2.5
observation = signal + noise

freq_full, psd_full = periodogram(observation, sample_rate)
freq_welch, psd_welch = welch(observation, sample_rate, segment=512)

peak_full = freq_full[np.argmax(psd_full)]
peak_welch = freq_welch[np.argmax(psd_welch)]
low_band = (freq_welch >= 0.5) & (freq_welch <= 3.0)

print("单段周期图峰值频率:", f"{peak_full:.3f} Hz")
print("Welch 峰值频率:", f"{peak_welch:.3f} Hz")
print("Welch 低频带平均功率:", f"{psd_welch[low_band].mean():.6f}")
print("提示：分别估计前后半段，可观察非平稳噪声被全局平均掩盖。")

