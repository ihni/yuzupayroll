<div align="center">
	<img src=".github/fruit.png" height="80px" width="80px" alt="Yuzu Payroll">
	<h2>Yuzu Payroll</h2>
	<p align="center">
		<p>An open source payroll management system</p>
	</p>
</div>

## Purpose
A project made with a small team of 4 to create a simple and featureful application. Built using python as the backend and MySQL as the database dialect, it is a current work-in-progress web based application so we can test our programming capabilites.

---

## Getting setup

### Requirements
Feel free to use your respective package managers, e.g, `brew`, to install these:
- [Podman](https://podman.io/)
- [Podman Compose](https://github.com/containers/podman-compose) (alternative to Docker Compose)
- Python (version 3.9 or higher)

### Setup
#### 1. Initialize the VM
```bash
podman machine init
```
#### 2. Start the VM (Optional if not on Linux or WSL)
```bash
podman machine start
```

#### 3. Build the container
```bash
podman-compose up --build
```

### Using Make
You can also use `make` for convenience:
```bash
make help
```
This will list available targets like up, down, etc.

### Environment Compatibility

> This project has been confirmed to run successfully in the following environments:
> - Fedora 42 on WSL (Windows Subsystem for Linux)
> - macOS (ARM)
>
> ❗ Other environments (e.g., native Linux distros, Windows without WSL) are untested and may require additional configuration.
> [view it here](docs/debugging_wsl_podman.md)