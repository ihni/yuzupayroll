<div align="center">
	<img src=".github/fruit.png" height="80px" width="80px" alt="Yuzu Payroll">
	<h2>Yuzu Payroll</h2>
	<p align="center">
		<p>A free and open source payroll management system</p>
	</p>
</div>

## Overview
Built using Python and MySQL, Yuzu Payroll is designed to help small teams or organizations manage employees, work logs, and payroll operations

> This project is actively developed by a team of 4 students as a learning experience in backend, frontend, and database-heavy application designs


### Documentation
Documentation over the project structure can be read here:
[documentation](docs/overview.md)

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

> [!IMPORTANT]
> Always read through the source code before running any scripts from the internet

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