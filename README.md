# 🏄‍♂️ CrewSurf

> Seamlessly merge CrewAI's multi-agent teams with Windsurf/Cascade for powerful human-in-the-loop development. Enable AI agent collaboration without leaving your IDE.

![CrewSurf Banner](docs/images/banner.png)

## 🤔 What is CrewSurf?

CrewSurf lets you talk to AI helpers without leaving your coding tool. It's like having a team of smart assistants that you can chat with while you code!

## ✨ Cool Things It Can Do

- 💬 **Chat With AI Helpers**: Ask questions and get help without switching windows
- 🧠 **AI Remembers Your Code**: The AI can look at your code and understand it
- 🌎 **Reduced API Dependency**: Uses local AI models through Ollama - no expensive API credits needed!
- 🤝 **Team of Experts**: Different AI helpers with different skills work together
- 🔧 **Easy Setup**: Simple steps to get everything running
- 💻 **Advanced Architecture**: Support for [sophisticated agent teams](docs/ADVANCED_ARCHITECTURE.md) with specialized roles

## 🚀 Getting Started (Super Easy!)

### Step 1: Install Stuff You Need

1. Download and install [Python](https://www.python.org/downloads/) (the program that runs everything)
2. Download and install [Ollama](https://ollama.ai/download) (runs AI on your computer)
3. Install CrewSurf:
   ```
   pip install crewsurf
   ```

> **Using Conda?** If you prefer conda environments, check out our [Conda Integration Guide](docs/CONDA_INTEGRATION.md) for running CrewSurf with conda!

### Step 2: Start Your AI Team

Just run this command:
```
python -m crewsurf.start_team
```

### Step 3: Start Talking!

When the program is running, just type your questions or ideas when asked!

## 👀 See It In Action

![CrewSurf Demo](docs/images/demo.gif)

## 🙋‍♀️ Questions? Problems?

Check out our [Super Simple Guide](docs/EASY_GUIDE.md) for step-by-step help with pictures!

Or [create an issue](https://github.com/yourusername/crewsurf/issues) if you're stuck.

## 🙏 Acknowledgments & Attributions

CrewSurf builds upon the work of several incredible open-source projects:

### Core Dependencies

- [CrewAI](https://github.com/joaomdmoura/crewai) (MIT License) - The foundational multi-agent framework that powers our agent interactions and task delegation system
- [LiteLLM](https://github.com/BerriAI/litellm) (MIT License) - Unified interface for LLM providers with our custom patches for local Ollama integration
- [Ollama](https://github.com/ollama/ollama) (MIT License) - Local model inference engine that enables API-free operation
- [LangChain](https://github.com/langchain-ai/langchain) (MIT License) - Building blocks for language model applications used for memory and embeddings
- [FAISS](https://github.com/facebookresearch/faiss) (MIT License) - Vector similarity search library for efficient code memory storage
- [Docker](https://github.com/docker/docker-ce) (Apache License 2.0) - Containerization platform used for secure code execution in isolated environments

### Development & Integration

- [Windsurf/Cascade](https://www.anthropic.com) - The coding tool integration that enables seamless human-in-the-loop collaboration

### Special Thanks

Special thanks to João Moura, creator of CrewAI, and the entire open source community that makes projects like this possible.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Made with ❤️ to make AI collaboration simple for everyone!
