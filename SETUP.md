# 📦 Project Setup & Run Guide

This guide explains how to set up the project, install dependencies, and run/debug the application using a Python virtual environment.

---

## 🚀 Prerequisites

- Python 3 installed (`python3 --version`)
- pip available
- Terminal (zsh/bash)

---

## 📁 Project Setup

### 1. Navigate to Project

```bash
cd /path/to/your/project
```

---

### 2. Create Virtual Environment (if not present)

```bash
python3 -m venv venv
```

---

### 3. Activate Virtual Environment

```bash
source venv/bin/activate
```

---

### 4. Verify Python

```bash
python --version
which python
```

---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 💾 Save Dependencies

```bash
pip freeze > requirements.txt
```

---

## ▶️ Run the Project

```bash
python your_script.py
```

---

## 🐞 Debugging

### Quick Debug
```python
print("value:", variable)
```

### Using pdb
```python
import pdb; pdb.set_trace()
```

Commands:
- n → next
- s → step
- c → continue
- p var → print
- q → quit

---

## ⚠️ Notes

- Always activate venv
- Do not install globally
- Recreate venv if path changes

---

## 🔄 Recreate Environment

```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ❌ Deactivate

```bash
deactivate
```

---

## 🎯 Summary

- Activate venv
- Install dependencies
- Run project
- Debug when needed
