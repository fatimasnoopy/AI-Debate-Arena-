# AI Debate Arena 🎤

A sophisticated Streamlit application where three LLM-based agents engage in structured debate with transparent reasoning and balanced moderation.

## Features

### 🎯 Core Functionality

- **User-Defined Topics**: Debate any topic of your choice
- **Three Specialized Agents**:
  - **Agent A**: Defends viewpoint 1 with logical arguments
  - **Agent B**: Defends opposing viewpoint 2
  - **Moderator**: Observes debate, analyzes arguments, provides balanced conclusion

- **Transparent Reasoning**: 
  - View internal thinking processes of each agent
  - See token usage and model statistics
  - Follow chain-of-thought reasoning
  - Track argument refinement

- **Structured Debate Flow**:
  - Opening statements from both agents
  - Multi-round rebuttals with opponent engagement
  - Round-by-round moderator analysis
  - Final balanced synthesis

- **Rich UI & Export Options**:
  - Live debate view with color-coded agents
  - Analysis tab with moderator insights
  - Full transcript display
  - Download as TXT or JSON formats

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key (for GPT models)
- Google Gemini API key (for Gemini models)

### Setup

1. Clone or download the project:
```bash
cd "projet gen ia"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```env
# OpenAI (GPT)
OPENAI_API_KEY=your_openai_api_key_here
GPT_MODEL_NAME=gpt-4-turbo-preview

# Google (Gemini)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL_NAME=gemini-pro

# Settings
TEMPERATURE=0.7
MAX_TOKENS=1500
DEBATE_ROUNDS=3
```

### Running the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
projet gen ia/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration and environment variables
├── agents.py              # LLM agent implementations
├── debate_manager.py      # Debate orchestration and management
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
└── README.md              # This file
```

## How to Use

### 1. **Setup Phase**
   - Enter a debate topic in the sidebar
   - Define Agent A's position (Pro)
   - Define Agent B's position (Con)
   - **Select API for each agent** (GPT or Gemini)
   - Configure number of debate rounds (1-5)
   - Optionally enable "Show detailed reasoning steps"
   - Click "Start Debate"

### 2. **Debate Execution**
   - View opening statements from both agents
   - Click "Next Round" to proceed through rebuttals
   - Each round includes:
     - Agent A's rebuttal to Agent B
     - Agent B's rebuttal to Agent A
     - Moderator's round analysis
   - Repeat until all rounds are complete

### 3. **Conclusion**
   - After all rounds, click "Generate Conclusion"
   - View moderator's balanced final synthesis
   - Access analysis tab for detailed insights

### 4. **Export**
   - **Analysis Tab**: View full moderator conclusion
   - **Transcript Tab**: 
     - Copy full debate text
     - Download as TXT file
     - Export as JSON with metadata

## Configuration

Edit `.env` file to customize:

- `OPENAI_API_KEY`: Your OpenAI API key (for GPT)
- `GPT_MODEL_NAME`: GPT model (default: gpt-4-turbo-preview)
- `GEMINI_API_KEY`: Your Google Gemini API key
- `GEMINI_MODEL_NAME`: Gemini model (default: gemini-pro)
- `TEMPERATURE`: Response creativity (0.0-1.0, default: 0.7)
- `MAX_TOKENS`: Maximum response length (default: 1500)
- `DEBATE_ROUNDS`: Number of debate rounds (default: 3)

## Agent Classes

### LLMAgent
Base class for all agents with thinking and critique capabilities.

**Methods:**
- `think()`: Generate response with OpenAI API
- `critique_and_refine()`: Self-critique based on counter-arguments

### DebateAgent
Specialized debate agent with specific viewpoint.

**Methods:**
- `opening_statement()`: Generate opening argument
- `respond_to_opponent()`: Create rebuttal to opponent's argument

### ModeratorAgent
Neutral moderator analyzing debate quality.

**Methods:**
- `analyze_round()`: Evaluate both agents' arguments
- `final_conclusion()`: Generate balanced final synthesis

## DebateManager
Orchestrates entire debate flow.

**Key Methods:**
- `start_debate()`: Initialize with opening statements
- `execute_round()`: Run rebuttal and analysis for one round
- `conclude_debate()`: Generate final moderator conclusion
- `get_debate_transcript()`: Export formatted text transcript
- `get_debate_summary()`: Get debate statistics

## Example Debate Topics

- "AI will have more positive than negative impact on society"
- "Remote work is more beneficial than office work"
- "Social media does more harm than good"
- "Climate change is the most pressing global issue"
- "Universal Basic Income should be implemented"

## Features Demonstration

### Transparent Reasoning
- Token usage statistics for each response
- API type display (GPT or Gemini)
- Internal model information
- Detailed reasoning steps (when enabled)

### Balanced Moderation
- Round-by-round argument analysis
- Identification of logical fallacies
- Recognition of valid counter-points
- Nuanced final conclusion

### Professional Transcripts
- Timestamped debate progression
- Formatted text export
- Structured JSON export with metadata
- Ready for sharing and review

## Limitations & Notes

- Requires valid OpenAI API key (for GPT) and/or Google Gemini API key (for Gemini)
- API costs depend on token usage
- Quality depends on model selection
- Long debates may require more tokens
- Rate limiting applies based on API plan
- Gemini API may have different response formatting than GPT

## Future Enhancements

- [ ] Support for more LLM providers (Claude, Llama, etc.)
- [ ] Custom API selection per agent
- [ ] Debate history and comparison features
- [ ] User voting on argument strength
- [ ] Integration with knowledge bases
- [ ] Multi-language support
- [ ] Real-time streaming responses
- [ ] Custom agent personalities

## Troubleshooting

### "API Key not found"
- Ensure `.env` file is created with valid API keys
- For GPT: add `OPENAI_API_KEY`
- For Gemini: add `GEMINI_API_KEY`
- File should be in the same directory as `app.py`

### "Rate limit exceeded"
- Wait before starting new debates
- Check your OpenAI API usage and plan limits

### "Empty responses"
- Verify API key is valid
- Check model name is correct
- Ensure sufficient tokens in MAX_TOKENS setting

### "Debate not progressing"
- Click "Next Round" to proceed through rounds
- All rounds must complete before conclusion
- View Live Debate tab for progress

## Author Notes

This application demonstrates:
- **Chain-of-Thought Reasoning**: Agents think through arguments step-by-step
- **ReAct Pattern**: Agents react to opponent arguments
- **Self-Critique**: Agents refine positions based on counter-arguments
- **Transparent AI**: All reasoning visible in UI

The glass-box approach ensures users understand how AI reaches its conclusions.

## License

This project is provided as-is for educational and research purposes.

---

**Happy Debating! 🎤**
