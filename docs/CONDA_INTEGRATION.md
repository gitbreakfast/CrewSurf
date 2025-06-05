# 🐍 Conda Integration Guide for CrewSurf

This guide helps you set up and run CrewSurf using conda environments within Windsurf/Cascade.

## 🔧 Setting Up Your Conda Environment

1. **Create a dedicated conda environment**:
   ```bash
   conda create -n crewai python=3.9
   conda activate crewai
   ```

2. **Install CrewSurf and dependencies**:
   ```bash
   pip install git+https://github.com/gitbreakfast/crewsurf.git
   pip install -U duckduckgo-search
   ```
   
   > **Note**: The `duckduckgo-search` package is required for the ChiefArchitect agent's web search capabilities. Without it, you'll encounter ImportError when running CrewSurf.

## 🚀 Running CrewSurf in Windsurf/Cascade

### Option 1: Initialize Conda in Windsurf Terminal

Create a file named `initialize_conda_terminal.ps1` in your project directory:

```powershell
# PowerShell script to initialize Anaconda in Windsurf terminal
Write-Output "Initializing Anaconda environment for CrewSurf..."

# Find Anaconda installation
$condaPaths = @(
    "$env:USERPROFILE\miniconda3",
    "$env:USERPROFILE\Anaconda3",
    "C:\ProgramData\miniconda3",
    "C:\ProgramData\Anaconda3"
)

$condaPath = $null
foreach ($path in $condaPaths) {
    if (Test-Path "$path\Scripts\activate.ps1") {
        $condaPath = $path
        break
    }
}

if ($condaPath -eq $null) {
    Write-Output "❌ Could not find Anaconda/Miniconda installation."
    return
}

Write-Output "✅ Found Conda at: $condaPath"

# Initialize conda for PowerShell
& "$condaPath\shell\condabin\conda-hook.ps1"
conda activate crewai

# Show conda info
Write-Output ""
Write-Output "====== CrewSurf Environment Info ======"
conda info
Write-Output ""
Write-Output "Python: $(python --version)"
Write-Output "======================================"
Write-Output ""
Write-Output "🏄‍♂️ CrewSurf conda environment is ready!"
```

Then run this command in your Windsurf terminal:
```
powershell -ExecutionPolicy Bypass -File "path\to\initialize_conda_terminal.ps1"
```

### Option 2: Using the Batch File Approach

Create a file named `run_crewsurf.bat` in your project:

```batch
@echo off
echo Opening Anaconda Prompt with crewai environment...

:: Find Conda
set CONDA_PATH=%USERPROFILE%\miniconda3
if exist "%CONDA_PATH%\Scripts\activate.bat" goto FOUND_CONDA
set CONDA_PATH=%USERPROFILE%\Anaconda3
if exist "%CONDA_PATH%\Scripts\activate.bat" goto FOUND_CONDA
set CONDA_PATH=C:\ProgramData\miniconda3
if exist "%CONDA_PATH%\Scripts\activate.bat" goto FOUND_CONDA
set CONDA_PATH=C:\ProgramData\Anaconda3
if exist "%CONDA_PATH%\Scripts\activate.bat" goto FOUND_CONDA

echo Could not find Anaconda/Miniconda installation.
goto END

:FOUND_CONDA
echo Found Conda at %CONDA_PATH%

:: Activate conda and the crewai environment
call "%CONDA_PATH%\Scripts\activate.bat"
call conda activate crewai

:: Run CrewSurf
python -m crewsurf.start_team
goto END

:END
pause
```

Double-click this batch file to run CrewSurf in the correct environment.

## ⚠️ Handling PowerShell Execution Policy

When running PowerShell scripts in Windsurf, you might see a security prompt:

```
File is published by [...] and is not trusted on your system. 
Only run scripts from trusted publishers.
[V] Never run  [D] Do not run  [R] Run once  [A] Always run  [?] Help
```

**Recommended options**:
- Choose `[R] Run once` for one-time testing
- Choose `[A] Always run` for Microsoft official extensions (generally safe)

## 🧩 Advanced Agent Configuration

For users building sophisticated agent teams:

1. **Using multiple specialized agents**:
   The default CrewSurf setup includes basic agents, but you can configure your own team with:
   - ChiefExecutiveOfficer
   - Director
   - ChiefArchitect
   - SeniorPrincipalEngineer
   - SoftwareTest
   - MasterDebugger
   - HeadOfSoftwareQuality
   - Writer

2. **Advanced memory system**:
   - Enable codebase scanning with vector memory
   - Import `scan_codebase` and `create_memory_store` from crewsurf.memory

3. **Custom delegation patterns**:
   - Create tight collaboration between agents
   - Enable specialized workflows (like MasterDebugger<->SeniorPrincipalEngineer)

## 🛠️ Troubleshooting

1. **"python not found" error**:
   - Make sure to run within an activated conda environment
   - Never run python directly from PowerShell without conda activation

2. **Import errors with crewai**:
   - Check that your crewai version is compatible (use `pip show crewai`)
   - Update imports for newer versions:
     - Use `from langchain.tools import Tool` (not `from crewai import Tool`)
     - Use `from langchain_community.vectorstores import Chroma`

3. **Ollama model issues**:
   - Verify Ollama is running with `ollama list`
   - Use `qwen:7b` or similar sized model for best performance
