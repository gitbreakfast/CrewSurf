"""
CrewSurf - First Time Setup Helper

This friendly script helps new users get started with CrewSurf.
Just run it and follow the simple steps!
"""
import os
import sys
import subprocess
import time

def print_big_welcome():
    """Print a fun welcome message"""
    welcome_text = """
    🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️
    
       WELCOME TO CREWSURF SETUP HELPER!
       
    🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️🏄‍♂️
    """
    print(welcome_text)
    print("\nLet's get your AI helper team ready!\n")

def check_python():
    """Check if Python is installed correctly"""
    print("Step 1: Checking your Python installation...")
    
    try:
        python_version = sys.version
        print(f"✅ Found Python {python_version}")
        return True
    except:
        print("❌ Couldn't find Python!")
        print("\nPlease install Python from https://www.python.org/downloads/")
        print("Make sure to check 'Add Python to PATH' during installation.")
        return False

def check_pip():
    """Check if pip is installed"""
    print("\nStep 2: Checking if pip is installed...")
    
    try:
        # Try running pip version command
        if os.name == 'nt':  # Windows
            result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                                  capture_output=True, text=True)
        else:
            result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                                  capture_output=True, text=True)
            
        if result.returncode == 0:
            print(f"✅ Found pip: {result.stdout.strip()}")
            return True
        else:
            print("❌ Pip seems to be having issues")
            print(result.stderr)
            return False
    except:
        print("❌ Couldn't find pip!")
        print("\nTry reinstalling Python and make sure pip is included.")
        return False

def check_ollama():
    """Check if Ollama is installed"""
    print("\nStep 3: Checking if Ollama is installed...")
    
    try:
        # Try running ollama version command
        if os.name == 'nt':  # Windows
            result = subprocess.run(["ollama", "version"], 
                                  capture_output=True, text=True)
        else:
            result = subprocess.run(["ollama", "version"], 
                                  capture_output=True, text=True)
            
        if result.returncode == 0:
            print(f"✅ Found Ollama: {result.stdout.strip()}")
            return True
        else:
            print("❌ Ollama seems to be having issues")
            print(result.stderr)
            return False
    except:
        print("❌ Couldn't find Ollama!")
        print("\nPlease install Ollama from https://ollama.ai/download")
        return False

def install_requirements():
    """Install required packages"""
    print("\nStep 4: Installing required packages...")
    
    try:
        # Install packages from requirements.txt
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Installed all required packages!")
        return True
    except Exception as e:
        print(f"❌ Error installing packages: {e}")
        print("\nTry running this command manually:")
        print(f"{sys.executable} -m pip install -r requirements.txt")
        return False

def download_ai_model():
    """Download the required AI model"""
    print("\nStep 5: Setting up the AI model...")
    
    try:
        print("Checking if the AI model is already downloaded...")
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        
        if "qwen:7b" in result.stdout:
            print("✅ AI model already downloaded!")
            return True
            
        print("\n📥 Downloading the AI model (this might take 5-10 minutes)...")
        print("☕ Feel free to grab a drink while you wait!")
        
        # Download the model
        if os.name == 'nt':  # Windows
            os.system("start cmd /c ollama pull qwen:7b")
            print("📱 The download is happening in a new window.")
            print("   Please wait until it shows 'Done' and then come back here.")
            
            input("\nPress Enter once the download is finished...")
            return True
        else:
            subprocess.run(["ollama", "pull", "qwen:7b"])
            print("✅ AI model downloaded!")
            return True
    except Exception as e:
        print(f"❌ Error downloading AI model: {e}")
        print("\nMake sure Ollama is running and try again.")
        print("If you're still having trouble, try downloading it manually by running:")
        print("ollama pull qwen:7b")
        return False

def setup_complete():
    """Show setup completion message"""
    success_text = """
    🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
    
      SETUP COMPLETE! WOHOO!
      
    🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
    
    You're all ready to use CrewSurf!
    
    To start your AI helper team, run:
    python -m crewsurf.start_team
    
    Have fun talking to your AI helpers!
    """
    print(success_text)

def main():
    """Run the setup steps"""
    print_big_welcome()
    
    # Check prerequisites
    python_ok = check_python()
    if not python_ok:
        input("\nPress Enter to exit...")
        return
        
    pip_ok = check_pip()
    if not pip_ok:
        input("\nPress Enter to exit...")
        return
        
    ollama_ok = check_ollama()
    if not ollama_ok:
        input("\nPress Enter to exit...")
        return
    
    # Install requirements
    reqs_ok = install_requirements()
    if not reqs_ok:
        input("\nPress Enter to exit...")
        return
        
    # Download AI model
    model_ok = download_ai_model()
    if not model_ok:
        input("\nPress Enter to exit...")
        return
    
    # Show completion message
    setup_complete()
    input("\nPress Enter to exit...")
    
if __name__ == "__main__":
    main()
