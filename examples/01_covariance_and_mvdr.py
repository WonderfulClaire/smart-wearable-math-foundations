"""矩阵分析示例：协方差矩阵、病态性、diagonal loading 与 MVDR。"""

import numpy as np


def mvdr_weights(noise_cov: np.ndarray, steering: np.ndarray) -> np.ndarray:
    """使用线性方程求解，避免显式计算矩阵逆。"""
    solved = np.linalg.solve(noise_cov, steering)
    return solved / (steering.conj().T @ solved)


rng = np.random.default_rng(7)
channels = 4
snapshots = 2_000

# 目标方向：不同麦克风之间存在相位差。
steering = np.exp(1j * np.linspace(0.0, 0.9, channels))

# 构造一个强方向性干扰和少量各向同性底噪。
interference_direction = np.exp(1j * np.linspace(0.0, 2.2, channels))
source = (rng.normal(size=snapshots) + 1j * rng.normal(size=snapshots)) / np.sqrt(2)
noise = interference_direction[:, None] * source[None, :]
noise += 0.02 * (
    rng.normal(size=(channels, snapshots))
    + 1j * rng.normal(size=(channels, snapshots))
) / np.sqrt(2)

noise_cov = noise @ noise.conj().T / snapshots
loading = 1e-2 * np.trace(noise_cov).real / channels
loaded_cov = noise_cov + loading * np.eye(channels)

plain = mvdr_weights(noise_cov, steering)
stable = mvdr_weights(loaded_cov, steering)

print("协方差特征值:", np.round(np.linalg.eigvalsh(noise_cov), 6))
print("原矩阵条件数:", f"{np.linalg.cond(noise_cov):.2e}")
print("加载后条件数:", f"{np.linalg.cond(loaded_cov):.2e}")
print("目标方向增益:", np.round(stable.conj().T @ steering, 6))
print("未加载输出噪声功率:", float(np.real(plain.conj().T @ noise_cov @ plain)))
print("稳定解输出噪声功率:", float(np.real(stable.conj().T @ noise_cov @ stable)))

