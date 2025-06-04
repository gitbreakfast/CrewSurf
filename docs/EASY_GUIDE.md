# 🏄‍♂️ CrewSurf Super Easy Guide

This guide will help you set up CrewSurf step by step with pictures! No computer expert skills needed!

## 📋 What You'll Need

- A computer (Windows, Mac, or Linux)
- Internet connection (just for setup)
- About 15 minutes

## 🚀 Part 1: Install Python

Python is the program that makes everything work.

### Windows:
1. Go to [Python.org](https://www.python.org/downloads/)
2. Click the big yellow "Download Python" button
3. Open the downloaded file
4. **IMPORTANT**: Check "Add Python to PATH"
5. Click "Install Now"

![Install Python](images/python_install.png)

### Mac:
1. Go to [Python.org](https://www.python.org/downloads/)
2. Click the big yellow "Download Python" button
3. Open the downloaded file
4. Follow the simple steps in the installer

## 🤖 Part 2: Install Ollama (Your AI Brain)

Ollama lets AI models run on your computer.

### Windows:
1. Go to [Ollama.ai/download](https://ollama.ai/download)
2. Click "Download for Windows"
3. Open the downloaded file and follow the simple steps

### Mac:
1. Go to [Ollama.ai/download](https://ollama.ai/download)
2. Click "Download for macOS"
3. Open the downloaded file
4. Drag Ollama to your Applications folder

![Install Ollama](images/ollama_install.png)

## 🔍 Part 3: Install a Simple AI Model

1. Open your computer's Command Prompt (Windows) or Terminal (Mac)
2. Type this and press Enter:
   ```
   ollama run qwen:7b
   ```
3. Wait for it to download (this might take a few minutes)
4. When it's ready, type "hello" and press Enter
5. The AI should say hello back!
6. Type "exit" and press Enter to close it

![Run Ollama](images/ollama_run.png)

## 🧩 Part 4: Install CrewSurf

1. Open your computer's Command Prompt (Windows) or Terminal (Mac) 
2. Type this command and press Enter:
   ```
   pip install crewsurf
   ```
3. Wait until it says "Successfully installed crewsurf"

![Install CrewSurf](images/pip_install.png)

## 🎮 Part 5: Run Your AI Team!

1. In the same Command Prompt or Terminal, type:
   ```
   python -m crewsurf.start_team
   ```
2. Wait a moment for the AI team to start up
3. You'll see a welcome message when it's ready

## 💬 Part 6: Start Talking to Your AI Team

1. When the program asks for your input, just type what you want and press Enter
2. The AI team will work together to help you
3. You can ask questions about coding or ask them to build something for you!

![Talking to AI](images/talking.png)

## ❓ Common Problems & Fixes

### "Python not found" error:
- Try installing Python again and make sure to check "Add Python to PATH"

### "Ollama not running" error:
- Make sure you started Ollama by clicking its icon

### Computer seems slow:
- Try using a smaller AI model by typing: `ollama run phi3:mini`

## 🎉 You Did It!

You now have a team of AI helpers ready to work with you. Have fun coding!

---

## 📱 Want More Help?

Visit our [GitHub page](https://github.com/yourusername/crewsurf) or email us at help@example.com
