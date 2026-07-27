<div align="center">

# 智能穿戴设备的数学基础

**不把数学停留在定理和习题里 —— 每一个公式，都对应一个真实的工程问题。**

*From matrix analysis to statistical learning theory, connected to real-world audio algorithms, array signal processing, and wearable device engineering.*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)](https://numpy.org/)
[![License](https://img.shields.io/github/license/WonderfulClaire/smart-wearable-math-foundations?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)
[![GitHub Stars](https://img.shields.io/github/stars/WonderfulClaire/smart-wearable-math-foundations?style=social)](https://github.com/WonderfulClaire/smart-wearable-math-foundations/stargazers)

**简体中文** · [English](README_en.md)

[四门课与真实任务](#-四门课与真实任务) · [六部分框架](#-六部分笔记框架) · [快速开始](#-快速开始) · [学习路线](#-推荐学习路线) · [贡献指南](CONTRIBUTING.md)

</div>

---

## 💡 为什么做这个仓库？

你是不是也有这种感觉：

> 矩阵分析、随机过程、凸优化……课都学过，定理也背过，
> 但一看到音频算法、阵列信号处理的论文，还是一脸懵——
> **这些公式到底对应设备里的哪一块？理想假设在真实传感器上为什么会失效？**

市面上的数学教材讲定理，工程论文讲结论，中间缺了一座桥。

**这个仓库就是那座桥。**

面向希望进入**智能耳机、智能眼镜、手表、手环、助听设备、多传感器终端算法**领域的学习者，把四门核心数学课——**矩阵分析、随机过程、凸优化、统计学习理论**——重新讲一遍，但每一个知识点都从一个真实的工程问题出发。

---

## ✨ 核心特色

### 🎯 从工程问题出发，不是从定理出发
每一章开头先抛一个真实问题（"多麦克风信号怎样联合表示？噪声能量怎样度量？"），然后再引入数学工具。学完立刻知道"这个公式能解决什么问题"。

### 🧩 六部分标准化笔记框架
每篇笔记固定包含六个部分，形成完整闭环——见下方框架图。

### 🔬 可运行的数值实验
`examples/` 下四个最小实验，**仅依赖 NumPy**，直接 `python` 跑就能看到诊断数字（条件数、噪声功率、跨用户准确率落差等），改参数、看效果、建立直觉。

### 🌉 跨领域迁移
同一个数学概念，在阵列信号、音频算法、机器学习里怎么用——打通来看，理解更深刻。

---

## 📚 四门课与真实任务

| 数学主线 | 典型知识点 | 穿戴设备中的问题 | 对应算法 |
|:--------:|-----------|-----------------|----------|
| [**矩阵分析**](01-矩阵分析/README.md) | 复数向量、Hermitian 矩阵、二次型、特征分解、SVD | 多麦克风信号怎样联合表示？噪声能量怎样度量？ | SCM、MVDR、PCA、低秩压缩 |
| [**随机过程**](02-随机过程/README.md) | 平稳性、自相关、PSD、随机状态空间 | 运动伪影和环境噪声为什么随时间变化？ | 谱估计、Wiener 滤波、Kalman 滤波 |
| [**凸优化**](03-凸优化/README.md) | 凸集、拉格朗日乘子、KKT、正则化 | 怎样在保真、降噪、功耗之间求可解释的最优解？ | MVDR、最小二乘、稀疏恢复、传感器标定 |
| [**统计学习理论**](04-统计学习理论/README.md) | 泛化、偏差—方差、正则化、分布偏移 | 离线准确率很高，为什么换用户或换佩戴位置就失效？ | 活动识别、健康指标估计、跨设备评测 |

---

## 🔬 六部分笔记框架

以「协方差矩阵与 MVDR」为例：

<img src="assets/note-framework.svg" alt="六部分笔记框架：工程问题 → 数学对象 → 核心推导 → 数值实验 → 工程陷阱 → 迁移问题" width="100%">

---

## 🚀 快速开始

### 环境要求
- Python 3.10+
- NumPy（`examples/` 仅需 NumPy）

### 三步跑通第一个实验

```bash
# 1. 克隆仓库
git clone https://github.com/WonderfulClaire/smart-wearable-math-foundations.git
cd smart-wearable-math-foundations

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行第一个实验：协方差与 MVDR（对角加载稳定化）
python examples/01_covariance_and_mvdr.py
```

会打印协方差特征值、对角加载前后的条件数、目标方向增益与输出噪声功率对比。

### 运行全部四个实验
```bash
python examples/01_covariance_and_mvdr.py      # 矩阵分析：协方差与 MVDR
python examples/02_psd_estimation.py           # 随机过程：周期图 vs Welch 谱估计
python examples/03_regularized_sensor_fusion.py # 凸优化：L2 正则化传感器融合
python examples/04_domain_shift_evaluation.py  # 统计学习：随机切分 vs 按用户留出
```

---

## 📁 项目结构

```
smart-wearable-math-foundations/
├── 01-矩阵分析/              # 矩阵分析笔记
├── 02-随机过程/              # 随机过程笔记
├── 03-凸优化/                # 凸优化笔记
├── 04-统计学习理论/          # 统计学习理论笔记
├── examples/                # 四个最小可运行实验（仅需 NumPy）
│   ├── 01_covariance_and_mvdr.py
│   ├── 02_psd_estimation.py
│   ├── 03_regularized_sensor_fusion.py
│   └── 04_domain_shift_evaluation.py
├── docs/                    # 学习路线与笔记模板
│   ├── 学习路线.md
│   └── 笔记模板.md
├── requirements.txt         # 依赖清单
├── CONTRIBUTING.md          # 贡献指南
├── LICENSE                  # MIT 许可证
└── README.md                # 你正在看的文件
```

---

## 🛤️ 推荐学习路线

- **第 1–2 周：矩阵分析** —— 看懂协方差矩阵、二次型和 MVDR。
- **第 3–4 周：随机过程** —— 理解 PSD、局部平稳和传感器噪声建模。
- **第 5 周：凸优化** —— 能从工程约束写出目标函数，并推导一个闭式解。
- **第 6 周：统计学习理论** —— 能设计跨用户、跨设备、跨场景的可信评测。
- **第 7–8 周：项目复盘** —— 完成四个小实验，写一篇贯通四门课的复盘。

更细的顺序见 [docs/学习路线.md](docs/学习路线.md)。

---

## 🎯 适合谁？

- **想入行智能穿戴算法的学生**：系统建立数学 → 工程的连接
- **音频 / 阵列信号工程师**：补数学基础，理解算法底层原理
- **机器学习工程师转 wearable 方向**：快速建立信号处理直觉
- **对智能眼镜、耳机算法好奇的开发者**：从零开始的入门路径

---

## 🤝 贡献

欢迎补充知识点、推导、图解和实验——但不接受只有定义、没有工程问题的孤立笔记。请先读 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [docs/笔记模板.md](docs/笔记模板.md)。

<a href="https://github.com/WonderfulClaire/smart-wearable-math-foundations/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=WonderfulClaire/smart-wearable-math-foundations" />
</a>

---

## 📄 许可证

内容与代码采用 [MIT License](LICENSE)。引用本仓库时，建议同时保留原始论文、教材或官方文档的出处。

<div align="center">

**如果这个仓库对你有帮助，点个 ⭐ Star 支持一下吧！**

</div>
