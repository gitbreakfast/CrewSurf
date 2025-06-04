from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crewsurf",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Seamless integration between CrewAI agents, local LLMs, and interactive development environments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/crewsurf",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/crewsurf/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "crewai>=0.19.0",
        "langchain>=0.0.267",
        "langchain_community>=0.0.5",
        "chromadb>=0.4.13",
        "flask>=2.0.0",
        "requests>=2.28.0",
    ],
)
