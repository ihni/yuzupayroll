# Payroll Management System

## Purpose
To learn containerization and compile a program for a final project for Information Management

## Overview
A containerized payroll management system built in Python and MySQL

---

## Getting Started

### ✅ Requirements
- [Podman](https://podman.io/)
- Podman Compose (alternative to Docker Compose)
- Python 3.9+

### Setup
```bash
podman machine init
podman machine start
podman-compose up --build
```

### 🛠️ Using Make
You can also use `make` for convenience:
```bash
make help
```
This will list available targets like up, down, etc.

### ✅ Environment Compatibility

> This project has been confirmed to run successfully in the following environments:
> - Fedora 42 on WSL (Windows Subsystem for Linux)
> - macOS (ARM)
>
> ❗ Other environments (e.g., native Linux distros, Windows without WSL) are untested and may require additional configuration.
> [view it here](docs/debugging_wsl_podman.md)