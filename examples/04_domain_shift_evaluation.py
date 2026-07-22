"""统计学习示例：随机切分为何会泄漏用户指纹。"""

import numpy as np


def predict_1nn(
    train_x: np.ndarray, train_y: np.ndarray, test_x: np.ndarray
) -> np.ndarray:
    """最小化示例用的 1-NN；分块计算以保持内存占用稳定。"""
    predictions = []
    for batch_start in range(0, len(test_x), 128):
        batch = test_x[batch_start : batch_start + 128]
        distances = ((batch[:, None, :] - train_x[None, :, :]) ** 2).sum(axis=2)
        predictions.append(train_y[np.argmin(distances, axis=1)])
    return np.concatenate(predictions)


def accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.mean(y_true == y_pred))


rng = np.random.default_rng(31)
users = 12
samples_per_user = 80
features, labels, groups = [], [], []

for user in range(users):
    user_fingerprint = rng.normal(scale=4.0, size=2)
    # 模拟不同佩戴方向：同一活动在不同用户上可能发生符号翻转。
    orientation = 1.0 if user % 2 == 0 else -1.0
    activity = rng.integers(0, 2, size=samples_per_user)
    activity_signal = orientation * (2.0 * activity - 1.0)
    x_user = np.column_stack(
        [
            np.repeat(user_fingerprint[None, :], samples_per_user, axis=0),
            activity_signal,
        ]
    ) + rng.normal(
        scale=0.22, size=(samples_per_user, 3)
    )
    features.append(x_user)
    labels.append(activity)
    groups.append(np.full(samples_per_user, user))

x = np.vstack(features)
y = np.concatenate(labels)
group = np.concatenate(groups)

# 随机切分：同一用户会同时出现在训练和测试中。
order = rng.permutation(len(x))
cut = int(0.8 * len(x))
train_idx, test_idx = order[:cut], order[cut:]
random_score = accuracy(
    y[test_idx], predict_1nn(x[train_idx], y[train_idx], x[test_idx])
)

# 按用户切分：最后 3 个用户完全不出现在训练集。
train_group = group < users - 3
test_group = ~train_group
group_score = accuracy(
    y[test_group], predict_1nn(x[train_group], y[train_group], x[test_group])
)

print("随机窗口切分准确率:", f"{random_score:.3f}")
print("按用户留出准确率:", f"{group_score:.3f}")
print("两者差距体现了用户指纹泄漏与真实跨用户泛化的区别。")
