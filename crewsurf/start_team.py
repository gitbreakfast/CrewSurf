"""
CrewSurf Team Starter

This is the main script that starts your AI team. It's designed to be
super easy to use - just run it and start talking to your AI helpers!
"""
import os
import time
import sys

def show_welcome():
    """Show a fun welcome message"""
    print("\n" + "="*60)
    print("🏄‍♂️  WELCOME TO CREWSURF - YOUR AI HELPER TEAM!  🏄‍♂️")
    print("="*60)
    print("\nGetting everything ready for you...\n")

def check_ollama():
    """Check if Ollama is installed and running"""
    try:
        import requests
        print("🔍 Checking if Ollama is running...")
        
        try:
            # Try to connect to Ollama's API
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                print("✅ Ollama is running!")
                return True
        except:
            print("❌ Ollama is installed but not running.")
            print("   Please start Ollama first, then try again.")
            if os.name == 'nt':  # Windows
                print("\n💡 TIP: Find Ollama in your Start Menu and click on it.")
            else:  # macOS/Linux
                print("\n💡 TIP: Open a new terminal and type 'ollama serve'")
            return False
            
    except ImportError:
        print("📦 Installing required packages...")
        os.system(f"{sys.executable} -m pip install requests")
        return check_ollama()
    except Exception as e:
        print(f"❌ Problem checking Ollama: {e}")
        print("\n💡 TIP: Make sure you installed Ollama from https://ollama.ai/download")
        return False

def check_requirements():
    """Check and install required packages"""
    required = ["crewai", "langchain", "langchain_community", "chromadb"]
    
    print("📋 Checking for required packages...")
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"📦 Installing missing packages: {', '.join(missing)}")
        os.system(f"{sys.executable} -m pip install {' '.join(missing)}")
        print("✅ All packages installed!")
    else:
        print("✅ All required packages are installed!")

def start_ai_team():
    """Start the CrewAI team with Windsurf integration"""
    from crewsurf.windsurf_integration import WindsurfCustomerTool, CondaEnvironmentHandler
    
    print("\n🚀 Starting your AI helper team...\n")
    time.sleep(1)
    
    # Try to import the main modules needed
    try:
        from crewai import Crew, Agent, Task, Process
        from langchain_community.llms import Ollama
        
        # Check for model availability
        print("🤖 Checking available AI models...")
        model_name = "qwen:7b"
        
        try:
            # Create test Ollama instance
            test_ollama = Ollama(model=model_name)
            print(f"✅ Found AI model: {model_name}")
        except Exception:
            print(f"⚠️ Could not find model {model_name}. Let's download it...")
            if os.name == 'nt':  # Windows
                os.system(f"start cmd /k ollama pull {model_name}")
                print("📥 Downloading model in a new window. Please wait until it finishes.")
                print("   When it's done, close that window and run this program again.")
                return False
            else:
                os.system(f"ollama pull {model_name}")
        
        # Define basic agents with simple descriptions for the demo
        print("\n👥 Creating your AI helper team...")
        
        team_leader = Agent(
            role="Team Leader",
            goal="Help the user accomplish their goals",
            backstory="I coordinate the team and make sure we understand what you need",
            verbose=True,
            allow_delegation=True,
            llm=Ollama(model=model_name)
        )
        
        coder = Agent(
            role="Coding Expert",
            goal="Write great code to solve problems",
            backstory="I'm really good at programming and can write code to solve problems",
            verbose=True,
            allow_delegation=True,
            llm=Ollama(model=model_name)
        )
        
        researcher = Agent(
            role="Research Expert",
            goal="Find information and explain complicated things",
            backstory="I'm great at researching and explaining complicated topics",
            verbose=True,
            allow_delegation=True,
            llm=Ollama(model=model_name)
        )
        
        # Create customer input tool
        print("🔧 Setting up the way you'll talk to the AI team...")
        customer_tool = WindsurfCustomerTool.create_customer_input_tool()
        
        # Add the tool to all agents
        team_leader.tools.append(customer_tool)
        coder.tools.append(customer_tool)
        researcher.tools.append(customer_tool)
        
        # Define tasks
        task_understand = Task(
            description="Understand what the user wants and make a plan to help them",
            expected_output="A clear understanding of the user's needs and a plan to address them",
            agent=team_leader
        )
        
        task_solve = Task(
            description="Solve the user's problem with code, explanations, or other help",
            expected_output="Solution to the user's problem",
            agent=coder
        )
        
        task_explain = Task(
            description="Research any needed information and explain the solution clearly",
            expected_output="Clear explanation of the information and solution",
            agent=researcher
        )
        
        # Create the crew
        crew = Crew(
            agents=[team_leader, coder, researcher],
            tasks=[task_understand, task_solve, task_explain],
            verbose=True,
            process=Process.sequential
        )
        
        # Start the interaction
        print("\n" + "="*60)
        print("🎉 YOUR AI TEAM IS READY! Let's get started! 🎉")
        print("="*60 + "\n")
        time.sleep(1)
        
        print("💬 The AI team will ask you what you need help with.")
        print("   Just type your answers when you see the prompt!\n")
        time.sleep(2)
        
        # Start the crew
        result = crew.kickoff()
        
        print("\n" + "="*60)
        print("🏁 YOUR AI TEAM HAS FINISHED!")
        print("="*60 + "\n")
        print(result)
        print("\n👋 Thanks for using CrewSurf! Come back soon!\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Something went wrong: {e}")
        print("\nPlease try running the program again.")
        return False

def main():
    """Main function to run CrewSurf"""
    show_welcome()
    
    # Check prerequisites
    if not check_ollama():
        return
    
    check_requirements()
    
    # Start the AI team
    start_ai_team()

if __name__ == "__main__":
    main()
