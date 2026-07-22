"""凸优化示例：L2 正则化稳定高度相关的多传感器融合。"""

import numpy as np


def fit_ridge(x: np.ndarray, y: np.ndarray, strength: float) -> np.ndarray:
    identity = np.eye(x.shape[1])
    return np.linalg.solve(x.T @ x + strength * identity, x.T @ y)


rng = np.random.default_rng(23)
samples = 45
latent = rng.normal(size=samples)

# 三个传感器都测量同一状态，前两个几乎重复，导致设计矩阵病态。
x = np.column_stack(
    [
        latent + 0.05 * rng.normal(size=samples),
        latent + 0.051 * rng.normal(size=samples),
        0.7 * latent + 0.20 * rng.normal(size=samples),
    ]
)
y = latent + 0.08 * rng.normal(size=samples)

unregularized = fit_ridge(x, y, strength=0.0)
regularized = fit_ridge(x, y, strength=0.5)

print("设计矩阵条件数:", f"{np.linalg.cond(x):.2e}")
print("无正则权重:", np.round(unregularized, 4))
print("L2 正则权重:", np.round(regularized, 4))
print("无正则权重范数:", f"{np.linalg.norm(unregularized):.4f}")
print("正则化权重范数:", f"{np.linalg.norm(regularized):.4f}")

