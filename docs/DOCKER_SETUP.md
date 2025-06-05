# Docker Setup for CrewSurf

This guide explains how to set up Docker for enabling code execution capabilities in CrewSurf's specialized agents.

## Why Docker is Needed

CrewSurf's sophisticated agent team includes specialized roles that benefit from code execution:
- **SoftwareTest** - Executes test harnesses to validate functionality
- **MasterDebugger** - Runs code to diagnose and identify issues
- **HeadOfSoftwareQuality** - Validates code quality through execution
- **LeadProgrammer** - Tests implementation components

Docker provides a secure, isolated environment for these agents to execute code without risking your system.

## Installation Steps

### 1. Install Docker Desktop

Download and install Docker Desktop for your operating system:
- [Windows](https://www.docker.com/products/docker-desktop/)
- [macOS](https://www.docker.com/products/docker-desktop/)
- [Linux](https://www.docker.com/products/docker-desktop/)

#### Windows-Specific Instructions:
1. Download the installer from the Docker website
2. Run the installer with default options
3. When prompted, select "Use WSL 2" if available
4. After installation, Docker will start automatically

### 2. Verify Docker Installation

Open a terminal/command prompt and run:

```bash
docker --version
```

You should see output similar to:
```
Docker version 24.0.2, build cb74dfcd85
```

### 3. Start Docker Service

Ensure the Docker service is running:
- On Windows/Mac: Look for the Docker whale icon in the system tray/menu bar
- On Linux: Run `sudo systemctl start docker`

### 4. Test Docker Setup

Run a simple test container:

```bash
docker run hello-world
```

If successful, you'll see a message indicating Docker is working properly.

## Relationship with Conda Environment

Docker operates independently from your conda environment:
- Your conda environment contains the Python dependencies for CrewSurf
- Docker provides isolated containers for code execution
- CrewAI connects these systems automatically - no manual configuration needed

## Troubleshooting

### Docker Desktop not starting
- Check system requirements (Windows 10/11 Pro, Education, or Enterprise)
- WSL 2 may need to be enabled on Windows
- Virtualization must be enabled in BIOS/UEFI

### Permission errors on Linux
- Add your user to the docker group:
  ```bash
  sudo usermod -aG docker $USER
  ```
- Log out and log back in or restart

### Resource concerns
- Docker Desktop can be configured to use limited resources
- Open Docker Desktop > Settings > Resources to adjust memory/CPU limits

## Next Steps

Once Docker is installed and running, CrewSurf agents will automatically use it when `allow_code_execution=True` is set in their configuration.

No additional setup is required - CrewAI handles the Docker integration internally.
