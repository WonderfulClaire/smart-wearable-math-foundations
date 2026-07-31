
"""矩阵分析示例：SVD 奇异值谱、秩选择与低秩去噪。"""

import numpy as np


def truncated_svd(matrix: np.ndarray, rank: int) -> np.ndarray:
    """返回 Frobenius 范数下的秩 rank 截断 SVD 重建。"""
    left, singular_values, right_h = np.linalg.svd(matrix, full_matrices=False)
    return (left[:, :rank] * singular_values[:rank]) @ right_h[:rank]


rng = np.random.default_rng(23)
channels = 6
samples = 600
true_rank = 2

spatial_modes, _ = np.linalg.qr(rng.normal(size=(channels, true_rank)))
time = np.linspace(0, 6 * np.pi, samples)
temporal_modes = np.vstack((np.sin(time), 0.65 * np.cos(0.37 * time + 0.4)))
clean = spatial_modes @ temporal_modes
noisy = clean + 0.28 * rng.normal(size=clean.shape)

singular_values = np.linalg.svd(noisy, compute_uv=False)
relative_values = singular_values / singular_values[0]

print("相对奇异值:", np.round(relative_values, 3))
print("含噪观测相对误差:", f"{np.linalg.norm(noisy - clean) / np.linalg.norm(clean):.3f}")

for rank in (1, 2, 4):
    reconstructed = truncated_svd(noisy, rank)
    error = np.linalg.norm(reconstructed - clean) / np.linalg.norm(clean)
    print(f"秩 {rank} 重建相对误差:", f"{error:.3f}")
