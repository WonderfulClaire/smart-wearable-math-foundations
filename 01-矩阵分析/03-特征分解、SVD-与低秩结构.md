
# 特征分解、SVD 与低秩结构

## 1. 工程问题

智能眼镜的多个麦克风、三轴 IMU 和多波长 PPG 会持续产生高维数据，但真正决定任务的自由度通常远少于观测维度：

- 一个远场声源在阵列上形成近似一维空间模式；
- 重复步态在多个 IMU 轴上呈现少数共同变化模式；
- PPG 各波长通道共享心搏成分，同时混入通道独有噪声。

怎样找出主要模式？怎样区分信号子空间与噪声子空间？怎样在保留主要结构的同时压缩或去噪？这些问题对应特征分解、奇异值分解（SVD）和低秩近似。

## 2. 数学对象

把 $M$ 个传感器在 $T$ 个时刻的观测排成矩阵

$$
\mathbf{X}=
\begin{bmatrix}
| & | & & |\\
\mathbf{x}(1) & \mathbf{x}(2) & \cdots & \mathbf{x}(T)\\
| & | & & |
\end{bmatrix}
\in\mathbb{C}^{M\times T}.
$$

| 符号 | 维度 | 工程含义 |
|---|---:|---|
| $\mathbf{X}$ | $M\times T$ | 多通道、多个时刻的观测矩阵 |
| $\mathbf{R}=\mathbf{X}\mathbf{X}^{H}/T$ | $M\times M$ | 空间协方差估计 |
| $\mathbf{U}$ | $M\times M$ | 通道空间中的正交模式 |
| $\mathbf{\Sigma}$ | $M\times T$ | 按强弱排列的奇异值 |
| $\mathbf{V}$ | $T\times T$ | 时间或样本空间中的正交模式 |
| $r$ | 标量 | 保留的有效秩 |

## 3. Hermitian 矩阵的特征分解

协方差矩阵是 Hermitian 半正定矩阵，因此存在酉矩阵 $\mathbf{U}$ 和非负实特征值，使

$$
\mathbf{R}
=\mathbf{U}\mathbf{\Lambda}\mathbf{U}^{H},
\qquad
\mathbf{\Lambda}
=\operatorname{diag}(\lambda_1,\ldots,\lambda_M),
$$

并可约定

$$
\lambda_1\ge\lambda_2\ge\cdots\ge\lambda_M\ge0.
$$

每个特征向量 $\mathbf{u}_i$ 是通道空间中的一个正交方向，对应特征值表示数据沿该方向的平均能量：

$$
\mathbf{u}_i^{H}\mathbf{R}\mathbf{u}_i=\lambda_i.
$$

如果前两个特征值远大于其余特征值，说明大部分能量集中在一个二维子空间中。但“能量大”不自动等于“任务有用”：强运动伪影可能比心率信号拥有更大的特征值。

## 4. SVD 怎样连接数据矩阵与协方差

任意矩阵都可以做奇异值分解：

$$
\mathbf{X}
=\mathbf{U}\mathbf{\Sigma}\mathbf{V}^{H}.
$$

其中奇异值

$$
\sigma_1\ge\sigma_2\ge\cdots\ge0
$$

描述各正交模式的强度。将 SVD 代入样本协方差：

$$
\begin{aligned}
\mathbf{R}
&=\frac{1}{T}\mathbf{X}\mathbf{X}^{H}\\
&=\frac{1}{T}
\mathbf{U}\mathbf{\Sigma}\mathbf{V}^{H}
\mathbf{V}\mathbf{\Sigma}^{H}\mathbf{U}^{H}\\
&=\mathbf{U}
\frac{\mathbf{\Sigma}\mathbf{\Sigma}^{H}}{T}
\mathbf{U}^{H}.
\end{aligned}
$$

因此：

$$
\lambda_i=\frac{\sigma_i^2}{T}.
$$

协方差的特征向量就是数据矩阵的左奇异向量；协方差特征值是对应奇异值平方除以样本数。

在 $T\gg M$ 时，直接分解 $M\times M$ 协方差通常更省计算；但形成协方差会平方条件数，数值算法中直接对 $\mathbf{X}$ 做 SVD 往往更稳健。

## 5. 最优低秩近似

保留前 $r$ 个奇异值：

$$
\mathbf{X}_r
=\sum_{i=1}^{r}
\sigma_i\mathbf{u}_i\mathbf{v}_i^{H}.
$$

Eckart–Young–Mirsky 定理说明，在 Frobenius 范数下，$\mathbf{X}_r$ 是所有秩不超过 $r$ 的矩阵中最接近 $\mathbf{X}$ 的：

$$
\mathbf{X}_r
=\arg\min_{\operatorname{rank}(\mathbf{Z})\le r}
\lVert\mathbf{X}-\mathbf{Z}\rVert_F.
$$

最小误差满足

$$
\lVert\mathbf{X}-\mathbf{X}_r\rVert_F^2
=\sum_{i=r+1}^{\min(M,T)}\sigma_i^2.
$$

这给出一种简单去噪思路：若目标结构集中在前 $r$ 个模式，而噪声分散在其余模式，则截断 SVD 可以降低噪声。

常见能量保留率为

$$
\eta(r)
=\frac{\sum_{i=1}^{r}\sigma_i^2}
{\sum_i\sigma_i^2}.
$$

但不能只凭 $\eta(r)$ 选秩。若强干扰占据第一主成分，保留 95% 能量可能主要保留了干扰。

## 6. PCA、信号子空间与投影

前 $r$ 个左奇异向量构成

$$
\mathbf{U}_r=
\begin{bmatrix}
\mathbf{u}_1 & \cdots & \mathbf{u}_r
\end{bmatrix}.
$$

信号子空间投影矩阵为

$$
\mathbf{P}_s=\mathbf{U}_r\mathbf{U}_r^{H}.
$$

它满足

$$
\mathbf{P}_s^H=\mathbf{P}_s,
\qquad
\mathbf{P}_s^2=\mathbf{P}_s.
$$

投影后的观测

$$
\widehat{\mathbf{x}}
=\mathbf{P}_s\mathbf{x}
$$

只保留信号子空间中的分量。互补投影

$$
\mathbf{P}_n=\mathbf{I}-\mathbf{P}_s
$$

对应噪声子空间。这一结构连接了 PCA、低秩去噪和 MUSIC 等子空间方法。

## 7. 最小实验

运行：

```bash
python examples/05_low_rank_denoising.py
```

实验生成一个秩为 2 的多通道信号，再加入满秩噪声。重点观察：

1. 奇异值谱在第 2 个模式之后是否明显下降；
2. 秩 2 重建是否比原始含噪观测更接近干净信号；
3. 秩选得太小是否损失信号；
4. 秩选得太大是否重新引入噪声。

## 8. 工程陷阱

### 最大主成分可能是伪影

PCA 按方差排序，不知道任务标签。PPG 中的运动伪影、麦克风中的强风噪可能占据第一主成分。

### 样本太少导致子空间漂移

短窗口适合跟踪变化，却会增加协方差和奇异向量的估计方差。相邻窗口的主成分还可能出现符号或相位翻转。

### 奇异值没有天然阈值

“保留 95% 能量”只是启发式规则。有效秩应结合噪声水平、下游任务和跨用户验证确定。

### 非平稳过程不共享一个固定子空间

用户从静止变为跑步时，主要模式会变化。对整段数据做一次 SVD 可能把不同状态混在一起。

### 不同单位支配分解

把加速度、角速度和音频特征直接拼接时，数值尺度最大的模态会主导奇异值。需要先明确单位、归一化和加权方式。

### 近似误差小不等于任务误差小

Frobenius 重建误差关注整体能量；低能量但具有判别力的特征可能被截断。最终仍需用下游指标验证。

## 9. 迁移问题

1. 若四麦克风阵列只有一个无混响声源，理想空间协方差的秩是多少？
2. LoRA 用低秩矩阵表示参数更新，与截断 SVD 的共同结构和目标差异是什么？
3. 三轴 IMU 的重力分量在短时静止窗口中形成怎样的主方向？
4. 若两个奇异值非常接近，对应单个奇异向量是否稳定？对应子空间是否可能更稳定？
5. 为什么在量纲不同的多模态数据上直接做 PCA 可能产生误导？

## 10. 过关标准

学完本单元，你应该能够：

- 解释协方差特征值和数据奇异值之间的关系；
- 从 SVD 写出最佳秩 $r$ 近似和重建误差；
- 写出信号子空间投影矩阵并验证其幂等性；
- 区分“能量最大”“重建最好”和“任务最有用”；
- 诊断样本不足、尺度不一致和非平稳性导致的低秩失效。

## 11. 参考资料

1. G. H. Golub and C. F. Van Loan, *Matrix Computations*, 4th ed., Johns Hopkins University Press, 2013, Chapters 2 and 8.
2. G. Strang, *Linear Algebra and Learning from Data*, Wellesley-Cambridge Press, 2019, Chapters 1–4.
3. I. T. Jolliffe and J. Cadima, “Principal component analysis: a review and recent developments,” *Philosophical Transactions of the Royal Society A*, 374, 2016.


## 推荐视频

- **3Blue1Brown《线性代数的本质》** 『特征向量与特征值』『抽象向量空间』几集——合集 [BV1ys411472E](https://www.bilibili.com/video/BV1ys411472E/)。
- **漫士沉思录《无痛线代》** *彻底搞懂 SVD!矩阵究竟怎么就奇异了?* 等 SVD / 特征值单集（B站搜“漫士沉思录 无痛线代 SVD”，[主页](https://space.bilibili.com/266765166)）。
- **StatQuest** *Principal Component Analysis (PCA)*（[视频索引](https://statquest.org/video-index/)）：用 SVD / 协方差做降维，和本讲“低秩去噪、信号子空间”对应。
