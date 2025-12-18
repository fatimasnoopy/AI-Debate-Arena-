# AI Debate Arena - Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Key
Create a `.env` file:
```
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Run Application
```bash
streamlit run app.py
```

### 4. Use the App
1. Enter a debate topic
2. Define two opposing positions
3. Choose number of rounds (1-5)
4. Click "Start Debate"
5. Click "Next Round" to proceed through debate
6. Click "Generate Conclusion" for final synthesis
7. Export transcript as TXT or JSON

## Example: Quick Test

**Topic**: "Remote work is better than office work"

**Agent A Position**: Remote work improves productivity, reduces commute stress, and offers better work-life balance

**Agent B Position**: Office work promotes team collaboration, company culture, and prevents isolation

**Rounds**: 2

---

## Detailed Features

### 🎤 Debate Interface
- **Live View**: Watch AI agents argue in real-time
- **Color-Coded**: Blue for Agent A, Purple for Agent B, Green for Moderator
- **Interactive Controls**: Next Round, Generate Conclusion, Reset

### 🔍 Reasoning Display
- View token usage per response
- See model information
- Display API statistics
- Optional detailed reasoning steps

### 📊 Analysis Tab
- Moderator's balanced conclusion
- Agent position summary
- Debate progress metrics

### 📄 Transcript Tab
- Full formatted debate text
- Copy to clipboard functionality
- Download as TXT file
- Export as structured JSON
- Includes metadata and timestamps

## API Requirements

- **Service**: OpenAI API
- **Model**: GPT-4 (recommended) or GPT-3.5-turbo
- **Cost**: Approximately $0.01-0.10 per debate (depending on rounds)
- **Sign up**: https://platform.openai.com

## Configuration

Edit `config.py` or `.env` to customize:

```python
OPENAI_API_KEY      # Your API key
MODEL_NAME          # gpt-4-turbo-preview (recommended)
TEMPERATURE         # 0.7 (0.0-1.0 for creativity)
MAX_TOKENS         # 1500 (max response length)
DEBATE_ROUNDS      # 3 (number of debate rounds)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Invalid API Key" | Check `.env` file has correct key from OpenAI |
| "ModuleNotFoundError" | Run `pip install -r requirements.txt` |
| "Rate limit" | Wait 1 minute, check API plan limits |
| "Empty responses" | Verify API key is active, check quota |

## Architecture

```
User Input (Topic & Positions)
           ↓
    Debate Manager
           ↓
    ┌─────┴─────┐
    ↓           ↓
Agent A      Agent B
    ↓           ↓
    └─────┬─────┘
           ↓
      Moderator
           ↓
     Final Conclusion
           ↓
   Export (TXT/JSON)
```

## Advanced: Custom Prompts

To customize agent behavior, edit the prompts in `agents.py`:

```python
# In DebateAgent.opening_statement()
prompt = f"""Your custom prompt here..."""
```

Experiment with different prompt templates to achieve:
- More aggressive debate style
- More collaborative tone
- Focus on different argument types
- Varying response lengths

## Tips for Best Results

1. **Be Specific**: Detailed topic descriptions lead to better arguments
2. **Set Clear Positions**: Explicitly define what each agent should argue
3. **Choose 2-3 Rounds**: Usually sufficient for substantive debate
4. **Enable Reasoning**: Helpful for understanding AI's thinking
5. **Save Transcripts**: Download for reference and sharing

## Example Topics to Try

1. **Technology**: "Cryptocurrency should be a primary currency"
2. **Environment**: "We should prioritize climate action over economic growth"
3. **Society**: "Universal Basic Income should be implemented"
4. **Education**: "Online education is superior to traditional schooling"
5. **Health**: "Processed foods should be heavily taxed"

---

**Ready to start? Open the app with `streamlit run app.py` and choose your debate topic!** 🎤
