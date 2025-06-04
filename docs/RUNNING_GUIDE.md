# 🚀 Running Your CrewAI Agent Team

This guide explains how to run your sophisticated CrewAI agent team with Windsurf/Cascade integration.

## Prerequisites

- Anaconda or Miniconda installed
- Conda environment named `crewai` with all dependencies
- Ollama running with the appropriate model (qwen:7b recommended)

## 🌟 Option 1: Direct Windsurf Integration (Recommended)

This is the modern approach using WindsurfCustomerTool for direct human-in-the-loop interaction.

### Step 1: Open Anaconda Prompt

Search for "Anaconda Prompt" in your Windows Start menu and open it.

### Step 2: Navigate to Project Directory

```bash
cd F:\mycrewai
```

### Step 3: Activate Conda Environment

```bash
conda activate crewai
```

### Step 4: Run the Integration

```bash
python run_with_conda.py
```

This will:
- Start your full agent team (CEO, Director, ChiefArchitect, etc.)
- Enable the WindsurfCustomerTool for direct human-in-the-loop interaction
- Set up your advanced memory system for codebase scanning
- Configure agent delegation patterns

## 🔄 Option 2: Bridge Server Approach (Legacy)

This is the original approach using a separate bridge server.

### Step 1: Start Bridge Server

Open an Anaconda Prompt:

```bash
cd F:\mycrewai\cascade_bridge
conda activate crewai
python run_bridge.py
```

Keep this terminal open and running.

### Step 2: In a New Anaconda Prompt

Open a second Anaconda Prompt:

```bash
cd F:\mycrewai
conda activate crewai
python run_with_cascade.py
```

This will connect to the bridge server and run your agent team.

## 🛠️ Troubleshooting

### "Python not found" Error

If you see this error, it means you're not using an Anaconda Prompt. Make sure to:
1. Open Anaconda Prompt from Start menu
2. Not use regular Command Prompt or PowerShell

### "No connection could be made" Error

This error appears when using Option 2 and the bridge server isn't running. Make sure:
1. Bridge server is running in a separate terminal
2. It's using the same conda environment

### CrewAI API Errors

If you see import errors related to CrewAI:
1. Check your crewai version: `pip show crewai`
2. You may need to update import statements for newer versions

### Ollama Model Issues

If Ollama fails to generate embeddings or responses:
1. Verify Ollama is running: Check the Ollama icon in system tray
2. Confirm model is downloaded: `ollama list`
3. Pull the recommended model: `ollama pull qwen:7b`
