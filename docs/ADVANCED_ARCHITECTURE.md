# 🏗️ Advanced CrewSurf Agent Architecture

This guide covers the sophisticated agent structure, delegation patterns, and memory systems used in advanced CrewSurf implementations.

## 🤖 Agent Hierarchy & Responsibilities

CrewSurf supports a sophisticated multi-agent hierarchy for complex software development:

### Executive Layer
- **ChiefExecutiveOfficer**: 
  - Acts as the ultimate authority
  - Focuses on company reputation and customer satisfaction
  - Approves final deliverables
  - Has the final say when agents disagree

- **Director**:
  - Manages the team
  - Ensures adherence to customer requirements
  - Coordinates between departments
  - Translates CEO's vision into actionable work

### Design & Planning Layer
- **ChiefArchitect**:
  - Plans sprints using agile methodologies
  - Has web search capabilities for research
  - Creates software architecture designs
  - Makes technology stack decisions
  
- **LeadProgrammer** (Cascade):
  - Bridges architecture and implementation
  - Writes critical/complex code components
  - Delegates routine tasks to SeniorPrincipalEngineer
  - Provides code reviews and technical leadership

### Implementation Layer
- **SeniorPrincipalEngineer**:
  - Implements code based on LeadProgrammer guidance
  - Converts architectural designs into working code
  - Implements routine functionality
  - Works closely with MasterDebugger

- **MasterDebugger**:
  - Specializes in bug analysis
  - Reviews code for potential issues
  - Provides real-time feedback to engineers
  - Creates fixes for identified bugs

### Quality Assurance Layer
- **SoftwareTest**:
  - Creates test harnesses for functions
  - Develops automated test suites
  - Ensures code meets requirements
  - Reports bugs back to MasterDebugger

- **HeadOfSoftwareQuality**:
  - Ensures software meets quality standards
  - Can reject code and send it back to architects/engineers
  - Validates against best practices
  - Makes final QA decisions

### Documentation Layer
- **Writer**:
  - Creates user documentation
  - Documents code for developers
  - Ensures clarity in communication
  - Makes technical concepts accessible

## 🔄 Custom Delegation Patterns

CrewSurf implements sophisticated delegation patterns between agents:

### LeadProgrammer <-> SeniorPrincipalEngineer Delegation
This delegation pattern optimizes coding efficiency:

```
┌─────────────────┐    Architecture    ┌─────────────────┐
│     Chief       │ ──────────────────►│      Lead       │
│    Architect    │                    │    Programmer   │
└─────────────────┘                    └────────┬────────┘
                                               │
                                               │ Delegation
                                               ▼
                                      ┌─────────────────┐
                                      │     Senior      │
                                      │    Principal    │
                                      │    Engineer     │
                                      └─────────────────┘
```

The workflow:
1. ChiefArchitect provides technical specifications
2. LeadProgrammer creates critical components and design patterns
3. LeadProgrammer delegates routine implementation to SeniorPrincipalEngineer
4. LeadProgrammer reviews code from SeniorPrincipalEngineer
5. Both collaborate with MasterDebugger for quality control

### MasterDebugger <-> SeniorPrincipalEngineer Collaboration
This tight feedback loop is a key feature:

```
┌─────────────────┐    Bug Reports     ┌─────────────────┐
│   Principal     │ ◄───────────────── │    Master       │
│   Engineer      │                    │    Debugger     │
└────────┬────────┘                    └────────┬────────┘
         │                                      │
         │ Code Fixes                           │ Analysis
         ▼                                      ▼
┌──────────────────────────────────────────────────────┐
│                      Codebase                        │
└──────────────────────────────────────────────────────┘
```

The workflow:
1. SeniorPrincipalEngineer writes initial implementation
2. MasterDebugger analyzes code in real-time
3. Issues are immediately communicated back to the Engineer
4. Engineer implements fixes based on Debugger's analysis
5. Cycle repeats until code meets quality standards

### Quality Control Escalation Pattern
When code issues are detected:

```
┌─────────────────┐         ┌─────────────────┐
│    Software     │ ───────►│     Head of     │
│      Test       │ Report  │ Software Quality│
└─────────────────┘         └────────┬────────┘
                                     │
                                     │ Rejection
                                     ▼
┌─────────────────┐         ┌─────────────────┐
│     Chief       │◄────────┤    Principal    │
│    Architect    │ Revise  │    Engineer     │
└─────────────────┘ Design  └─────────────────┘
```

The workflow:
1. Software Test identifies issues with implementation
2. HeadOfSoftwareQuality reviews and makes judgment
3. If rejected, code is sent back to Engineer
4. For architectural issues, ChiefArchitect is consulted
5. Director mediates if consensus cannot be reached

## 🧠 Advanced Memory System

CrewSurf implements a sophisticated codebase memory system:

### Vector Storage Architecture
```
┌─────────────────┐         ┌─────────────────┐
│    Codebase     │────────►│    Text         │
│    Scanner      │         │    Splitter     │
└─────────────────┘         └────────┬────────┘
                                     │
                                     ▼
┌─────────────────┐         ┌─────────────────┐
│    Chroma       │◄────────┤    Ollama       │
│  Vector Store   │         │   Embeddings    │
└────────┬────────┘         └─────────────────┘
         │
         ▼
┌─────────────────┐
│     Agent       │
│     Tools       │
└─────────────────┘
```

### Implementation Details

1. **Codebase Scanning**:
   - Recursively scans project directories
   - Identifies relevant source files based on extensions
   - Extracts content with metadata

2. **Text Processing**:
   - Uses RecursiveCharacterTextSplitter
   - Creates chunks of appropriate size for embeddings
   - Preserves code context within chunks

3. **Vector Embedding**:
   - Uses OllamaEmbeddings for local embedding generation
   - Can be configured to use different models (qwen:7b recommended)
   - Maintains efficiency with local processing

4. **Storage and Retrieval**:
   - Chroma vector database stores embeddings
   - Semantic search capabilities across codebase
   - Persistence options for long-running projects

### Sample Memory Tool Code

```python
def create_memory_tool(memory_store):
    """
    Create a tool that allows agents to search the codebase memory
    
    Args:
        memory_store: Chroma vector store with indexed code
        
    Returns:
        Tool object that can be used by agents
    """
    from langchain_community.llms import Ollama
    from langchain.chains import RetrievalQA
    from langchain.tools import Tool
    
    # Create Ollama LLM instance
    ollama_llm = Ollama(model="qwen:7b")
    
    # Create a retrieval chain
    retriever = memory_store.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=ollama_llm,
        chain_type="stuff",
        retriever=retriever
    )
    
    # Create a tool that wraps the retrieval chain
    memory_tool = Tool(
        name="CodebaseMemory",
        func=qa_chain.run,
        description="Useful for searching through the codebase memory."
    )
    
    return memory_tool
```

## 🔄 Conversation History Tracking

CrewSurf implements conversation history tracking to maintain context:

1. **History Mechanism**:
   - Tracks conversations between different agent pairs
   - Maintains context across multiple interaction rounds
   - Enables long-running development processes

2. **Integration with Human Feedback**:
   - WindsurfCustomerTool allows integrating human responses
   - All human inputs are tracked in conversation history
   - Agents can reference previous human guidance

3. **Implementation**:
   ```python
   def track_conversation(agent_name, message, response):
       """Track conversations between agents"""
       if agent_name not in conversation_history:
           conversation_history[agent_name] = []
           
       conversation_history[agent_name].append({
           "timestamp": time.time(),
           "message": message,
           "response": response
       })
   ```

## 📝 Best Practices for Advanced Agent Architecture

1. **Balanced Team Composition**:
   - Ensure all key roles (design, implementation, QA) are represented
   - Consider domain-specific agents for specialized projects

2. **Delegation Configuration**:
   - Define clear escalation paths for different issue types
   - Set threshold criteria for when to escalate issues

3. **Memory Optimization**:
   - Tune vector chunk size based on codebase characteristics
   - Consider separate memory stores for code vs. documentation

4. **Model Selection**:
   - CEO and Architect roles benefit from larger models (judgment)
   - Engineers can use smaller, more efficient models (implementation)
   - MasterDebugger should use models strong at code analysis
