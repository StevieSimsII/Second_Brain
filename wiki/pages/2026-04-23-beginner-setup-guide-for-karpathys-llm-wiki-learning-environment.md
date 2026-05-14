---
title: "Beginner Setup Guide for Karpathy's LLM Wiki Learning Environment"
source: "personal notes"
date: "2026-04-23"
tags: [llm, python, pytorch, setup, environment]
---

## Overview

These notes outline a practical beginner setup for studying large language models through Karpathy-style educational material. The focus is not just on installing tools, but on creating a clean, repeatable environment for running notebooks, experimenting with PyTorch code, organizing datasets, and verifying that CPU or GPU execution works correctly from the start.

This matters because many beginners get stuck on environment issues before they ever reach core LLM concepts like tokenization, next-token prediction, or transformer blocks. A simple but well-structured local setup makes it easier to follow tutorials, reproduce examples, debug problems, and gradually move from toy neural networks to small language models.

## Key Concepts

- **Isolated Python environments**: Use `venv` or conda to avoid package conflicts and keep experiments reproducible. This makes it safe to install and upgrade LLM-related packages without affecting other projects.
- **PyTorch as the core framework**: Most Karpathy-style LLM tutorials use PyTorch for tensors, autograd, and neural network layers. A working install is the main prerequisite for running examples.
- **CPU vs GPU execution**: Small experiments can run on CPU, but GPU support dramatically improves training speed. Early device checks help confirm whether CUDA or MPS acceleration is available.
- **Tokenizer and dataset plumbing**: Language models train on token IDs, not raw text. Even simple projects need a pipeline for reading text, building vocabularies or tokenizers, and converting data into tensors.
- **Notebook-first, script-backed workflow**: Notebooks are useful for exploration and debugging, while scripts are better for repeatable training runs. A good learning setup supports both.
- **Verification and reproducibility**: Installation is only the first step. You should verify imports, package versions, hardware access, and a minimal forward/backward pass to ensure the environment actually works.

## How It Works

A practical LLM study environment is usually built in layers.

First, prepare the base system with a recent Python version, `git`, and a package manager such as `pip`. If using an NVIDIA GPU, confirm drivers are installed before dealing with Python dependencies. Then create an isolated environment so the setup is disposable and project-specific:

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows PowerShell
python -m pip install --upgrade pip
```

Next, install the core packages. For a beginner workflow, this usually means PyTorch plus notebook and utility packages:

```bash
pip install torch torchvision torchaudio
pip install jupyter matplotlib tqdm numpy
```

After installation, verify the runtime before doing anything more complicated. This confirms imports work and that hardware is visible:

```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

On Apple Silicon, check MPS support instead:

```bash
python -c "import torch; print(torch.backends.mps.is_available())"
```

Once the runtime is healthy, organize the project directory so learning materials stay manageable. A simple structure such as the following supports both experiments and reusable code:

```text
llm-wiki-lab/
├── .venv/
├── data/
├── notebooks/
├── outputs/
├── src/
└── requirements.txt
```

The most important validation step is a minimal end-to-end training loop. A tiny neural network trained on random data proves that tensors, autograd, optimizers, and device placement all work together:

```python
import torch
import torch.nn as nn

device = "cuda" if torch.cuda.is_available() else "cpu"
x = torch.randn(64, 32).to(device)
y = torch.randint(0, 10, (64,)).to(device)

model = nn.Sequential(
    nn.Linear(32, 64),
    nn.ReLU(),
    nn.Linear(64, 10)
).to(device)

opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
loss_fn = nn.CrossEntropyLoss()

for step in range(10):
    logits = model(x)
    loss = loss_fn(logits, y)
    opt.zero_grad()
    loss.backward()
    opt.step()
    print(step, float(loss))
```

From there, the workflow shifts toward language-model-specific tasks: loading text files, tokenizing them into integer IDs, building fixed-length context windows, training a small next-token model, and sampling outputs. This progression is useful because it keeps the setup grounded in fundamentals rather than hiding everything behind large pretrained-model APIs.

Good reproducibility habits should be part of the environment from the beginning. Freeze dependencies with `pip freeze > requirements.txt`, keep data paths relative to the project root, separate exploratory notebooks by topic, and save checkpoints or generated text to `outputs/`. It is also helpful to record whether an experiment ran on CPU, CUDA, or MPS so performance expectations stay realistic.

The notes also include a concrete exercise: create a workspace, install tools, add an environment check script, run a tiny training script, then extend the lab into a text-based mini language model project. That sequence is a strong beginner path because it proves the environment works before introducing tokenization and model-building complexity.

## Personal Notes

Beginner Setup Guide for Karpathy's LLM Wiki and a Practical LLM Learning Environment

Source: https://youtu.be/iXd0t60YmMw?si=MLJtmH9k5GAFAiE5
Notion page: https://www.notion.so/Beginner-Setup-Guide-for-Karpathy-s-LLM-Wiki-and-a-Practical-LLM-Learning-Environment-34b01bb0839a81a1819afe0721a8003e

Tags: llm, setup, python, pytorch, environment, machine-learning

Overview

This lesson reconstructs the likely technical substance of a beginner-oriented setup guide for working through Karpathy-style large language model material: getting a machine ready, installing the core tooling, verifying that the stack works, and organizing a learning workflow around notebooks, scripts, datasets, and model experimentation. Even when the source is a video with little extractable text, the practical value is in understanding the standard local environment engineers use to study and run modern LLM examples.

If you are an engineer who wants to move from watching LLM tutorials to actually running code, this setup knowledge matters. A clean Python environment, the right deep learning libraries, optional GPU acceleration, and a repeatable project structure will save hours of debugging and make it much easier to follow educational resources, reproduce examples, and begin modifying toy language models yourself.

Key Concepts

  *   Isolated Python environments: LLM tutorials often depend on specific versions of Python packages such as PyTorch, tokenization libraries, and notebook tooling. Using a virtual environment or conda environment prevents conflicts with system Python and makes experiments reproducible. It also gives you a clean place to install and upgrade packages without breaking unrelated projects.
  *   PyTorch as the execution backbone: Most educational LLM material in the Karpathy ecosystem uses PyTorch for tensor operations, automatic differentiation, and neural network modules. Understanding that the framework handles the forward pass, gradient computation, and optimizer updates helps you connect the code to the math. A working PyTorch install is usually the first hard requirement for reproducing examples.
  *   CPU vs GPU execution: Small examples can run on CPU, but training even toy transformers becomes much faster on GPU. Setup guides usually distinguish between a minimal CPU-only path and an accelerated CUDA or Metal path depending on hardware. Verifying device detection early avoids confusion later when training appears unexpectedly slow.
  *   Tokenizer and dataset plumbing: Language models do not consume raw text directly; they consume token IDs generated by a tokenizer. Even simple beginner projects need a pipeline that loads text, splits or chunks it, and converts it into tensors for training and evaluation. This data preparation step is often where file layout and dependency setup begin to matter.
  *   Notebook-first exploration vs script-based training: A common learning pattern is to inspect ideas in Jupyter notebooks, then move stable training logic into Python scripts. Notebooks are excellent for debugging tensors, sampling outputs, and visualizing loss curves, while scripts are better for repeatable runs and parameterized experiments. A solid setup supports both modes.
  *   Reproducibility and verification: A setup is not complete just because installation commands succeeded. Engineers should verify Python version, package versions, hardware visibility, and a minimal forward/backward training step. This reduces the chance of subtle issues such as mismatched CUDA builds, broken kernels, or environment drift.

How It Works

A practical beginner setup for studying LLMs usually follows a layered approach:

1. **Prepare the base system** - Install a recent Python version supported by the target libraries. - Ensure you have `git` for cloning code and `pip` or `conda` for dependency management. - If you have an NVIDIA GPU, confirm that drivers are installed before worrying about Python packages.

2. **Create an isolated environment** A dedicated environment prevents package conflicts and makes your learning setup disposable and repeatable.

Example with `venv`: ```bash python3 -m venv .venv source .venv/bin/activate # macOS/Linux # .venv\Scripts\activate # Windows PowerShell python -m pip install --upgrade pip ```

3. **Install core packages** For a beginner LLM workflow, the baseline package set usually includes: - `torch` for model code - `jupyter` or `ipykernel` for notebooks - `numpy` for array manipulation - optional: `matplotlib`, `t