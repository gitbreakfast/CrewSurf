@echo off
REM Batch file to activate conda and run CrewAI with local LLM setup

REM Activate conda environment
call conda activate crewai

REM Set important environment variables for ChromaDB and CrewAI
set CHROMA_OPENAI_API_KEY=not-needed-using-local-embeddings
set CREWAI_FORCE_LOCAL_EMBEDDINGS=true
set CREWAI_LLM_PROVIDER=ollama
set CHROMA_API_IMPL=local
set OPENAI_API_KEY=
set LANGCHAIN_OPENAI_API_KEY=

REM Run the script
python -m core.run_with_cascade

REM Keep window open if there are errors
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo An error occurred. Press any key to close...
    pause > nul
)
