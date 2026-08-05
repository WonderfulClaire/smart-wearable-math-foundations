
# 多通道复数向量与 Hermitian 结构

## 1. 工程问题

一副带有 $M$ 个麦克风的智能耳机，同时采集到 $M$ 路时域信号。经过短时傅里叶变换（STFT）后，在频点 $f$、时间帧 $t$ 上得到

$$
\mathbf{x}(f,t)=
\begin{bmatrix}
x_1(f,t) & x_2(f,t) & \cdots & x_M(f,t)
\end{bmatrix}^{T}
\in \mathbb{C}^{M}.
$$

为什么这里不是 $M$ 个互不相关的标量，而要写成一个复数向量？原因是算法需要同时利用：

- 每个通道在该频点的幅度；
- 通道之间由传播时延引起的相位差；
- 所有通道共同构成的空间方向；
- 滤波后信号的能量和目标方向增益。

如果把复数只保留幅度，通道间的相位关系就会丢失；如果分别处理每个通道，又无法表达空间滤波。

## 2. 数学对象

| 符号 | 维度 | 工程含义 |
|---|---:|---|
| $M$ | 标量 | 传感器或麦克风数量 |
| $\mathbf{x}(f,t)$ | $M\times 1$ | 一个时频点上的多通道观测 |
| $\mathbf{d}(f)$ | $M\times 1$ | 目标方向相对于各通道的复数响应 |
| $\mathbf{w}(f)$ | $M\times 1$ | 空间滤波器权重 |
| $\mathbf{w}^{H}\mathbf{x}$ | 标量 | 滤波器在该时频点的输出 |
| $\mathbf{a}^{H}\mathbf{b}$ | 标量 | 复数向量的内积 |
| $\lVert\mathbf{x}\rVert_2$ | 标量 | 多通道观测的欧氏范数 |

上标 $T$ 表示转置，$*$ 表示复共轭，$H$ 表示共轭转置：

$$
\mathbf{x}^{H}=(\mathbf{x}^{*})^{T}.
$$

## 3. 为什么复数内积需要共轭

实数向量的长度平方是 $\mathbf{x}^{T}\mathbf{x}$。对复数向量，如果仍使用普通转置，会得到

$$
\mathbf{x}^{T}\mathbf{x}=\sum_{m=1}^{M}x_m^2,
$$

它可能是复数，也可能因为相位抵消而等于零，不能稳定地表示能量。

复数空间使用 Hermitian 内积：

$$
\langle \mathbf{a},\mathbf{b}\rangle
=\mathbf{a}^{H}\mathbf{b}
=\sum_{m=1}^{M}a_m^{*}b_m.
$$

于是向量长度平方为

$$
\lVert\mathbf{x}\rVert_2^2
=\mathbf{x}^{H}\mathbf{x}
=\sum_{m=1}^{M}|x_m|^2
\ge 0.
$$

这与“各通道在该时频点的幅度平方之和”一致，结果必为非负实数。共轭不是记号习惯，而是保证长度和能量有合理含义所必需的结构。

Hermitian 内积还满足共轭对称性：

$$
\mathbf{a}^{H}\mathbf{b}
=\left(\mathbf{b}^{H}\mathbf{a}\right)^{*}.
$$

因此，交换两个向量时相似程度的幅度不变，而相位符号相反。

## 4. 相位差怎样编码方向

考虑远场窄带平面波。目标信号到达第 $m$ 个麦克风，相对于参考麦克风的时延为 $\tau_m$。在频率 $f$ 上，这个时延对应相位旋转

$$
d_m(f)=e^{-j2\pi f\tau_m}.
$$

把所有通道的响应放在一起：

$$
\mathbf{d}(f)=
\begin{bmatrix}
e^{-j2\pi f\tau_1} &
\cdots &
e^{-j2\pi f\tau_M}
\end{bmatrix}^{T}.
$$

$\mathbf{d}(f)$ 常称为导向向量。它不是声源位置本身，而是“该方向在当前阵列、频率和参考约定下应该呈现的跨通道复数模式”。

滤波器输出为

$$
y(f,t)=\mathbf{w}(f)^{H}\mathbf{x}(f,t).
$$

若希望目标方向不失真，需要

$$
\mathbf{w}(f)^{H}\mathbf{d}(f)=1.
$$

这个等式同时约束目标方向的幅度和相位。若误写成 $\mathbf{w}^{T}\mathbf{d}=1$，优化问题对应的复数几何结构就被改变了。

## 5. 最小数值检查

下面的代码构造两个只差全局相位的复数向量。普通转置不能给出可靠能量，Hermitian 内积则始终给出非负实数。

```python
import numpy as np

x = np.array([1 + 1j, 2 - 1j, -0.5 + 0.2j])
phase = np.exp(1j * 0.7)
x_rotated = phase * x

print("x.T @ x =", x.T @ x)
print("x.H @ x =", np.vdot(x, x))
print("rotated energy =", np.vdot(x_rotated, x_rotated))
print("same energy =", np.allclose(np.vdot(x, x), np.vdot(x_rotated, x_rotated)))
```

预期观察：

1. `x.T @ x` 一般是复数；
2. `np.vdot(x, x)` 是非负实数；
3. 所有通道同时旋转相同相位后，能量不变。

在 NumPy 中，`np.vdot(a, b)` 会对第一个输入取共轭；矩阵写法则使用 `a.conj().T @ b`。

## 6. 工程陷阱

### 通道没有同步

采样时钟偏差或丢帧会使通道间相位随时间漂移。此时即使几何位置准确，固定导向向量也会逐渐失配。

### 参考通道约定不一致

导向向量可以相对于任意参考通道定义，但训练数据、仿真器和在线算法必须使用同一约定。参考变化通常只引入全局相位，却可能让直接比较复数权重的测试失败。

### 远场与窄带假设失效

近场声源不仅产生时延差，也会产生明显的幅度差；低频和高频的阵列可分辨性也不同。智能眼镜和耳机离嘴很近，不能无条件照搬远场模型。

### 麦克风增益和相位未校准

真实传感器响应不是理想的 $e^{-j2\pi f\tau_m}$。制造误差、壳体遮挡和佩戴方式都会改变跨通道响应。

### 把复数拆成实部和虚部后忘记结构

复数向量可以等价地写成更高维实数向量，但内积、约束和协方差也必须相应变换。只拼接实部和虚部、却继续使用原来的公式，会造成维度或能量定义不一致。

## 7. 迁移问题

1. 三轴 IMU 是实数向量。坐标系从设备坐标转到世界坐标时，哪些量保持不变？
2. 多波长 PPG 的各通道没有复相位，为什么仍适合用向量和内积表示？
3. 神经网络中的复数频谱特征若拆成实部和虚部，怎样验证网络输入仍保留相位信息？
4. 若所有麦克风通道同时乘以相同的复数相位，输出功率和目标方向约束分别怎样变化？

## 8. 过关标准

学完本单元，你应该能够：

- 写出多通道 STFT 观测、导向向量和滤波权重的维度；
- 解释普通转置、复共轭和共轭转置的区别；
- 从能量非负性说明为什么复数内积必须取共轭；
- 解释传播时延怎样变成频域相位；
- 列出至少三个会破坏理想导向向量的设备因素。

## 9. 参考资料

1. G. Strang, *Linear Algebra and Learning from Data*, Wellesley-Cambridge Press, 2019.
2. H. L. Van Trees, *Optimum Array Processing*, Wiley, 2002, Chapters 1–2.
3. J. Benesty, J. Chen, and Y. Huang, *Microphone Array Signal Processing*, Springer, 2008, Chapters 1–2.

## 推荐视频

- **3Blue1Brown《线性代数的本质》** 『向量究竟是什么』『线性组合·张成的空间与基』『点积与对偶性（内积）』几集——合集 [BV1ys411472E](https://www.bilibili.com/video/BV1ys411472E/)，B站搜“线性代数的本质 点积 对偶”直达。
- **漫士沉思录《无痛线代》** 复数向量与内积相关单集（B站搜“漫士沉思录 无痛线代 内积 复向量”，[主页](https://space.bilibili.com/266765166)）。
- **飞天闪客** *从函数到神经网络* 系列里“向量 / 高维空间”相关片段（[BV1NCgVzoEG9](https://www.bilibili.com/video/BV1NCgVzoEG9)），帮助把“向量 = 高维空间中的点”建立几何直觉。
