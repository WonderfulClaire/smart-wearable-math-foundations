<div align="center">

# Mathematical Foundations for Smart Wearables

**Don't leave math stranded in theorems and homework — every formula maps to a real engineering problem.**

*From matrix analysis to statistical learning theory, connected to real-world audio algorithms, array signal processing, and wearable device engineering.*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)](https://numpy.org/)
[![License](https://img.shields.io/github/license/WonderfulClaire/smart-wearable-math-foundations?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)
[![GitHub Stars](https://img.shields.io/github/stars/WonderfulClaire/smart-wearable-math-foundations?style=social)](https://github.com/WonderfulClaire/smart-wearable-math-foundations/stargazers)

[简体中文](README.md) · **English**

[Courses & Real Tasks](#-four-courses-real-tasks) · [Six-Part Framework](#-the-six-part-note-framework) · [Quick Start](#-quick-start) · [Learning Path](#-recommended-learning-path) · [Contributing](CONTRIBUTING.md)

</div>

---

## 💡 Why this repo?

Sound familiar?

> You took matrix analysis, stochastic processes, convex optimization…
> you memorized the theorems — but the moment you open a paper on audio
> algorithms or array signal processing, you're lost again:
> **which part of the device does this formula actually correspond to?
> Why do the ideal assumptions break down on real sensors?**

Math textbooks teach theorems. Engineering papers report conclusions. The bridge between them is missing.

**This repo is that bridge.**

For anyone aiming to work on algorithms for **smart earbuds, smart glasses, watches, bands, hearing aids, and multi-sensor terminals**, it re-teaches four core math courses — **matrix analysis, stochastic processes, convex optimization, and statistical learning theory** — but every concept starts from a real engineering problem.

---

## ✨ Highlights

### 🎯 Start from the engineering problem, not the theorem
Each chapter opens with a real question ("How do we jointly represent multi-microphone signals? How do we measure noise energy?") before introducing the math. You immediately know *what problem the formula solves*.

### 🧩 A standardized six-part note framework
Every note follows the same six sections, forming a complete loop — see the framework diagram below.

### 🔬 Runnable numerical experiments
The four minimal experiments under `examples/` depend on **NumPy only**. Run them with plain `python` and watch the diagnostic numbers appear (condition numbers, noise power, cross-user accuracy gaps). Tweak the parameters, see the effect, build intuition.

### 🌉 Cross-domain transfer
The same math concept, used in array signal processing, audio algorithms, and machine learning — connected so you understand it more deeply.

---

## 📚 Four Courses, Real Tasks

| Math Track | Key Concepts | Problem in Wearables | Related Algorithms |
|:----------:|-------------|----------------------|--------------------|
| [**Matrix Analysis**](01-矩阵分析/README.md) | complex vectors, Hermitian matrices, quadratic forms, eigendecomposition, SVD | How to jointly represent multi-mic signals? How to measure noise energy? | SCM, MVDR, PCA, low-rank compression |
| [**Stochastic Processes**](02-随机过程/README.md) | stationarity, autocorrelation, PSD, stochastic state-space | Why do motion artifacts and ambient noise vary over time? | spectral estimation, Wiener filtering, Kalman filtering |
| [**Convex Optimization**](03-凸优化/README.md) | convex sets, Lagrange multipliers, KKT, regularization | How to trade off fidelity, denoising, and power into an interpretable optimum? | MVDR, least squares, sparse recovery, sensor calibration |
| [**Statistical Learning Theory**](04-统计学习理论/README.md) | generalization, bias–variance, regularization, distribution shift | Offline accuracy is high — why does it collapse for a new user or wearing position? | activity recognition, health-metric estimation, cross-device evaluation |

> The note directories use their original Chinese names (`01-矩阵分析/`, `02-随机过程/`, `03-凸优化/`, `04-统计学习理论/`); the links above point to them directly.

---

## 🔬 The Six-Part Note Framework

Using "Covariance Matrix & MVDR" as an example:

```
┌─────────────────────────────────────────────────────────────┐
│  1. Engineering problem: how does multi-mic denoising         │
│     optimally suppress interference directions?               │
├─────────────────────────────────────────────────────────────┤
│  2. Math object: what does R = E[xxᴴ] physically mean?        │
│     x  —— microphone array receive vector                     │
│     R  —— spatial covariance matrix, energy distribution      │
├─────────────────────────────────────────────────────────────┤
│  3. Core derivation: MVDR optimal weight w = R⁻¹a / aᴴR⁻¹a    │
│     constrained optimization → Lagrangian → KKT, step by step │
├─────────────────────────────────────────────────────────────┤
│  4. Numerical experiment: run examples/01, watch how          │
│     diagonal loading changes condition number, target gain,   │
│     and output noise power                                     │
├─────────────────────────────────────────────────────────────┤
│  5. Engineering pitfalls:                                     │
│     • finite snapshots make R estimation noisy               │
│     • mic mismatch shifts the null                           │
│     • at low SNR, R is ill-conditioned; inversion unstable   │
├─────────────────────────────────────────────────────────────┤
│  6. Transfer: where else does this show up?                  │
│     • audio: weight solving for multi-channel denoising      │
│     • ML: Mahalanobis distance & whitening                   │
│     • comms: beamforming for antenna arrays                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Requirements
- Python 3.10+
- NumPy (`examples/` needs NumPy only)

### Run your first experiment in three steps

```bash
# 1. Clone
git clone https://github.com/WonderfulClaire/smart-wearable-math-foundations.git
cd smart-wearable-math-foundations

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the first experiment: covariance & MVDR (diagonal-loading stabilization)
python examples/01_covariance_and_mvdr.py
```

It prints the covariance eigenvalues, the condition number before/after diagonal loading, and the target-direction gain vs. output noise power.

### Run all four experiments
```bash
python examples/01_covariance_and_mvdr.py       # Matrix analysis: covariance & MVDR
python examples/02_psd_estimation.py            # Stochastic processes: periodogram vs Welch PSD
python examples/03_regularized_sensor_fusion.py # Convex optimization: L2-regularized sensor fusion
python examples/04_domain_shift_evaluation.py   # Statistical learning: random split vs leave-one-user-out
```

---

## 📁 Project Structure

```
smart-wearable-math-foundations/
├── 01-矩阵分析/              # Matrix analysis notes
├── 02-随机过程/              # Stochastic processes notes
├── 03-凸优化/                # Convex optimization notes
├── 04-统计学习理论/          # Statistical learning theory notes
├── examples/                # Four minimal runnable experiments (NumPy only)
│   ├── 01_covariance_and_mvdr.py
│   ├── 02_psd_estimation.py
│   ├── 03_regularized_sensor_fusion.py
│   └── 04_domain_shift_evaluation.py
├── docs/                    # Learning path & note template
│   ├── 学习路线.md
│   └── 笔记模板.md
├── requirements.txt         # Dependencies
├── CONTRIBUTING.md          # Contribution guide
├── LICENSE                  # MIT License
└── README.md                # The file you're reading (Chinese)
```

---

## 🛤️ Recommended Learning Path

- **Weeks 1–2: Matrix Analysis** — understand the covariance matrix, quadratic forms, and MVDR.
- **Weeks 3–4: Stochastic Processes** — grasp PSD, local stationarity, and sensor-noise modeling.
- **Week 5: Convex Optimization** — turn engineering constraints into an objective and derive a closed-form solution.
- **Week 6: Statistical Learning Theory** — design trustworthy cross-user / cross-device / cross-scenario evaluation.
- **Weeks 7–8: Capstone review** — finish the four experiments and write a retrospective that ties all four courses together.

See [docs/学习路线.md](docs/学习路线.md) for the detailed order.

---

## 🎯 Who is it for?

- **Students entering wearable-algorithm roles**: build the math → engineering connection systematically
- **Audio / array-signal engineers**: fill in the math foundations, understand the theory behind the algorithms
- **ML engineers moving into wearables**: quickly build signal-processing intuition
- **Developers curious about smart-glasses / earbud algorithms**: a from-scratch entry path

---

## 🤝 Contributing

Contributions of concepts, derivations, diagrams, and experiments are welcome — but isolated notes with only definitions and no engineering problem won't be accepted. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/笔记模板.md](docs/笔记模板.md) first.

<a href="https://github.com/WonderfulClaire/smart-wearable-math-foundations/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=WonderfulClaire/smart-wearable-math-foundations" />
</a>

---

## 📄 License

Content and code are under the [MIT License](LICENSE). When citing this repo, please also keep the original papers, textbooks, or official docs attribution.

<div align="center">

**If this repo helps you, drop a ⭐ Star to support it!**

</div>
