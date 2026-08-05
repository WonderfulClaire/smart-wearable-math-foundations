
# 协方差矩阵、二次型与 MVDR

## 1. 工程问题

智能耳机在地铁里同时接收到目标语音、列车噪声、广播和混响。多个麦克风上的噪声不是相互独立的：同一噪声源会以不同幅度和相位到达各通道。

我们需要回答三个问题：

1. 怎样用一个矩阵描述多通道噪声的能量与相关性？
2. 给定滤波权重后，怎样计算输出噪声功率？
3. 怎样在保持目标方向不失真的同时，让输出噪声功率最小？

这三个问题分别对应协方差矩阵、二次型和 MVDR 波束形成。

## 2. 数学对象与信号模型

在一个固定频点上省略 $f$，将观测写成

$$
\mathbf{x}(t)=\mathbf{d}s(t)+\mathbf{n}(t),
$$

其中 $\mathbf{d}\in\mathbb{C}^{M}$ 是目标导向向量，$s(t)$ 是目标信号，$\mathbf{n}(t)$ 是多通道噪声。

| 符号 | 维度 | 工程含义 |
|---|---:|---|
| $\mathbf{x}(t)$ | $M\times 1$ | 多通道观测 |
| $\mathbf{n}(t)$ | $M\times 1$ | 多通道噪声 |
| $\mathbf{d}$ | $M\times 1$ | 目标方向响应 |
| $\mathbf{R}_n$ | $M\times M$ | 噪声空间协方差矩阵 |
| $\mathbf{w}$ | $M\times 1$ | 波束形成权重 |
| $y(t)$ | 标量 | 波束形成输出 |

假设噪声均值为零，则噪声空间协方差矩阵为

$$
\mathbf{R}_n
=\mathbb{E}\left[\mathbf{n}(t)\mathbf{n}(t)^{H}\right].
$$

矩阵第 $(i,j)$ 个元素为

$$
[\mathbf{R}_n]_{ij}
=\mathbb{E}\left[n_i(t)n_j(t)^{*}\right],
$$

对角元素描述各通道噪声功率，非对角元素描述通道间相关性。

实际只有 $T$ 帧数据，因此常用样本协方差

$$
\widehat{\mathbf{R}}_n
=\frac{1}{T}\sum_{t=1}^{T}\mathbf{n}(t)\mathbf{n}(t)^{H}.
$$

“真实协方差”是统计模型中的期望；代码得到的通常只是有限数据上的估计量。

## 3. 为什么协方差矩阵是 Hermitian 半正定矩阵

先看共轭转置：

$$
\mathbf{R}_n^{H}
=\mathbb{E}\left[
\left(\mathbf{n}\mathbf{n}^{H}\right)^{H}
\right]
=\mathbb{E}\left[\mathbf{n}\mathbf{n}^{H}\right]
=\mathbf{R}_n.
$$

因此 $\mathbf{R}_n$ 是 Hermitian 矩阵。

再取任意 $\mathbf{z}\in\mathbb{C}^{M}$：

$$
\begin{aligned}
\mathbf{z}^{H}\mathbf{R}_n\mathbf{z}
&=\mathbb{E}\left[
\mathbf{z}^{H}\mathbf{n}\mathbf{n}^{H}\mathbf{z}
\right] \\
&=\mathbb{E}\left[
\left|\mathbf{n}^{H}\mathbf{z}\right|^2
\right] \\
&\ge 0.
\end{aligned}
$$

所以 $\mathbf{R}_n$ 至少是半正定的。半正定不等于可逆：如果通道完全重复、样本数不足或噪声只占据低维子空间，矩阵会有零特征值。

## 4. 输出功率为什么是二次型

波束形成输出为

$$
y(t)=\mathbf{w}^{H}\mathbf{x}(t).
$$

只考虑噪声分量：

$$
y_n(t)=\mathbf{w}^{H}\mathbf{n}(t).
$$

输出噪声功率为

$$
\begin{aligned}
P_{\text{out}}
&=\mathbb{E}\left[|y_n(t)|^2\right] \\
&=\mathbb{E}\left[
\mathbf{w}^{H}\mathbf{n}(t)\mathbf{n}(t)^{H}\mathbf{w}
\right] \\
&=\mathbf{w}^{H}\mathbf{R}_n\mathbf{w}.
\end{aligned}
$$

这个二次型把“权重选择”和“噪声空间结构”连接起来。若某个方向对应较大的噪声特征值，权重在该方向上的分量会产生更大的输出功率。

## 5. 从约束问题推导 MVDR

我们希望最小化输出噪声功率，同时保持目标方向增益为 1：

$$
\min_{\mathbf{w}}
\quad \mathbf{w}^{H}\mathbf{R}_n\mathbf{w}
\qquad
\text{s.t.}
\quad \mathbf{w}^{H}\mathbf{d}=1.
$$

当 $\mathbf{R}_n$ 正定时，目标函数严格凸，解唯一。使用复数 Lagrangian 可得到一阶条件

$$
\mathbf{R}_n\mathbf{w}=\lambda\mathbf{d}.
$$

于是

$$
\mathbf{w}=\lambda\mathbf{R}_n^{-1}\mathbf{d}.
$$

代入约束：

$$
\lambda^{*}
\mathbf{d}^{H}\mathbf{R}_n^{-1}\mathbf{d}
=1.
$$

因为 Hermitian 正定矩阵对应的二次型为正实数，最终得到

$$
\boxed{
\mathbf{w}_{\text{MVDR}}
=
\frac{
\mathbf{R}_n^{-1}\mathbf{d}
}{
\mathbf{d}^{H}\mathbf{R}_n^{-1}\mathbf{d}
}
}.
$$

分子寻找“在噪声度量下有利于目标方向”的权重，分母负责归一化，使 $\mathbf{w}^{H}\mathbf{d}=1$。

## 6. 不要在代码里直接求逆

公式写成 $\mathbf{R}_n^{-1}\mathbf{d}$，代码不必显式构造逆矩阵。应求解线性方程

$$
\mathbf{R}_n\mathbf{u}=\mathbf{d},
$$

再归一化：

$$
\mathbf{w}=\frac{\mathbf{u}}{\mathbf{d}^{H}\mathbf{u}}.
$$

NumPy 写法：

```python
u = np.linalg.solve(Rn, d)
w = u / np.vdot(d, u)
```

`solve` 通常比 `inv(Rn) @ d` 更稳定，也避免计算并不需要的完整逆矩阵。

### 对角加载

当样本协方差病态或导向向量存在误差时，可使用

$$
\widetilde{\mathbf{R}}_n
=\widehat{\mathbf{R}}_n+\delta\mathbf{I},
\qquad \delta>0.
$$

若 $\lambda_i$ 是原矩阵特征值，加载后的特征值为 $\lambda_i+\delta$。最小特征值被抬高，条件数通常下降：

$$
\kappa(\widetilde{\mathbf{R}}_n)
=\frac{\lambda_{\max}+\delta}{\lambda_{\min}+\delta}.
$$

代价是引入偏差：过大的 $\delta$ 会让算法逐渐忽略真实空间相关性，趋向更保守的权重。

一个与尺度相关的简单选择是

$$
\delta=\alpha\frac{\operatorname{tr}(\widehat{\mathbf{R}}_n)}{M},
$$

其中 $\alpha$ 是无量纲超参数。这样整体信号增益改变时，加载量也会相应缩放。

## 7. 最小实验

运行：

```bash
python examples/01_covariance_and_mvdr.py
```

重点观察：

1. 协方差矩阵的特征值是否全部非负；
2. 病态矩阵在加载前后的条件数；
3. $\left|\mathbf{w}^{H}\mathbf{d}\right|$ 是否接近 1；
4. MVDR 输出噪声功率是否低于简单平均；
5. 加载量过小时是否仍不稳定，过大时是否损失空间选择性。

建议修改实验中的快拍数、最小特征值和对角加载系数，记录结果，而不是只运行默认参数。

## 8. 工程陷阱

### 噪声协方差被目标语音污染

若估计区间含有目标语音，算法可能把目标的一部分结构当成需要压制的噪声。VAD 错误会进一步放大这一问题。

### 快拍数太少

当 $T<M$ 时，样本协方差的秩最多为 $T$，必然不可逆。即使 $T$ 略大于 $M$，估计方差也可能很大。

### 导向向量失配

头部运动、近场效应、佩戴松动、麦克风遮挡和阵列几何误差都会使真实目标响应偏离 $\mathbf{d}$。MVDR 可能在错误方向保持不失真，甚至压制真实目标。

### 跨频点独立处理造成不一致

每个频点独立估计权重可能带来频率间跳变。真实系统常需要时间平滑、频率平滑或结构化估计。

### 忽略数值尺度

固定写死的 $\delta$ 在不同增益、位深和归一化方式下含义不同。加载量应与协方差尺度一起报告。

### 把低输出功率等同于高语音质量

输出功率降低可能来自噪声抑制，也可能来自目标失真。必须同时检查目标方向增益、语音质量和任务指标。

## 9. 迁移问题

1. 对多轴 IMU 做线性融合时，$\mathbf{R}$ 可以表示什么误差结构？
2. PPG 多波长通道的运动伪影高度相关时，协方差的主特征向量可能表示什么？
3. Ridge 回归中的 $\lambda\mathbf{I}$ 与协方差对角加载有什么共同的稳定化作用？
4. 如果两个麦克风完全相同，协方差矩阵的秩和可逆性会怎样变化？
5. 将 $\mathbf{R}_n$ 乘以任意正常数，MVDR 权重是否变化？请用公式验证。

## 10. 过关标准

学完本单元，你应该能够：

- 解释协方差矩阵对角元素和非对角元素的工程含义；
- 证明协方差矩阵是 Hermitian 半正定矩阵；
- 从滤波输出推导二次型功率；
- 从约束问题得到 MVDR 闭式解；
- 说明为什么实际代码优先使用线性方程求解；
- 诊断样本不足、目标污染、导向失配和条件数过大。

## 11. 参考资料

1. J. Capon, “High-resolution frequency-wavenumber spectrum analysis,” *Proceedings of the IEEE*, 57(8), 1969.
2. H. L. Van Trees, *Optimum Array Processing*, Wiley, 2002, Chapters 2 and 6.
3. J. Benesty, J. Chen, and Y. Huang, *Microphone Array Signal Processing*, Springer, 2008, Chapters 2–3.
4. G. H. Golub and C. F. Van Loan, *Matrix Computations*, 4th ed., Johns Hopkins University Press, 2013, Chapters 2 and 4.

## 推荐视频

- **3Blue1Brown《线性代数的本质》** 『三维线性变换』『行列式』『基变换』『逆矩阵·列空间·零空间（不可逆 = 压扁）』几集——合集 [BV1ys411472E](https://www.bilibili.com/video/BV1ys411472E/)。
- **漫士沉思录《无痛线代》** 二次型 / 协方差矩阵 / 行列式 相关单集（B站搜“漫士沉思录 无痛线代 二次型 协方差”，[主页](https://space.bilibili.com/266765166)）。
- **StatQuest** *Covariance and Correlation*（[视频索引](https://statquest.org/video-index/)）：协方差、方差、相关性的图解，和本讲“协方差矩阵描述空间相关性”直接对应。
