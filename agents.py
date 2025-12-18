import os
from typing import Optional
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL_NAME, TEMPERATURE, MAX_TOKENS
from reasoning_techniques import (
    ChainOfThoughtPrompter, TreeOfThoughtsEvaluator, ReActAgent,
    SelfCorrectionEngine, ReflectiveThinking, DebateReasoningFramework,
    ReasoningTechnique
)

# Initialize Groq
groq_client = Groq(api_key=GROQ_API_KEY)


class LLMAgent:
    """Base class for LLM-based agents using Groq API"""
    
    def __init__(self, name: str, role: str, temperature: float = TEMPERATURE):
        self.name = name
        self.role = role
        self.temperature = temperature
        self.reasoning_steps = []
        self.model_name = GROQ_MODEL_NAME
    
    def think(self, prompt: str, max_tokens: int = MAX_TOKENS) -> dict:
        """Generate response with visible reasoning steps"""
        self.reasoning_steps = []
        
        # System prompt for structured thinking
        system_prompt = f"""You are {self.name}, {self.role}.
Your task is to think through your response step by step:
1. Analyze the question/statement
2. Identify key points to address
3. Generate your argument with logical flow
4. Review and refine your position

Be clear about your reasoning process."""
        
        try:
            return self._groq_think(system_prompt, prompt, max_tokens)
        except Exception as e:
            return {
                "response": f"Error: {str(e)}",
                "error": True
            }
    
    def _groq_think(self, system_prompt: str, prompt: str, max_tokens: int) -> dict:
        """Use Groq API"""
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=max_tokens,
        )
        
        content = response.choices[0].message.content
        
        return {
            "response": content,
            "model": GROQ_MODEL_NAME,
            "api_type": "groq",
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
            }
        }
    
    def critique_and_refine(self, initial_response: str, counter_argument: Optional[str] = None) -> dict:
        """Self-critique and refine response based on counter-argument"""
        
        critique_prompt = f"""Review your previous argument:
"{initial_response}"

"""
        if counter_argument:
            critique_prompt += f"""The opponent argued:
"{counter_argument}"

"""
        
        critique_prompt += """Now:
1. Identify weak points in your argument
2. Acknowledge valid counter-points
3. Strengthen your position with new evidence
4. Provide a refined version that is more robust

Format your response as:
WEAKNESSES: [list weak points]
VALID_COUNTER_POINTS: [acknowledge what's valid]
REFINEMENT: [improved argument]"""
        
        return self.think(critique_prompt, max_tokens=1200)


class DebateAgent(LLMAgent):
    """Agent specialized in debate with a specific viewpoint"""
    
    def __init__(self, name: str, viewpoint: str, position: str):
        super().__init__(name, f"a debate agent defending the position: {position}")
        self.viewpoint = viewpoint
        self.position = position
        self.reasoning_framework = DebateReasoningFramework()
        self.reasoning_steps = []
    
    def opening_statement(self, topic: str) -> dict:
        """Generate opening statement using Chain of Thought"""
        # Use Chain of Thought for structured reasoning
        cot_prompt = ChainOfThoughtPrompter.create_cot_prompt(
            f"""Debate Topic: {topic}
Your Position: {self.position}

Provide a compelling opening statement that:
1. Clearly states your viewpoint
2. Provides 2-3 key arguments
3. Uses evidence or logical reasoning
4. Sets a strong foundation for debate""",
            context="You are participating in a structured debate."
        )
        
        response = self.think(cot_prompt, max_tokens=1000)
        response['reasoning_technique'] = 'Chain of Thought'
        self.reasoning_steps = ChainOfThoughtPrompter.extract_reasoning_steps(response.get('response', ''))
        response['reasoning_steps'] = self.reasoning_steps
        return response
    
    def respond_to_opponent(self, opponent_argument: str, topic: str) -> dict:
        """Generate rebuttal using ReAct pattern"""
        react_prompt = ReActAgent.create_react_prompt(
            f"""Your opponent just argued:
"{opponent_argument}"

Debate Topic: {topic}
Your Position: {self.position}

Generate a strong rebuttal that addresses their points and strengthens your position.
Use the Reason-Act-Observe cycle to structure your thinking.""",
            available_actions=[
                "Analyze opponent's logical structure",
                "Identify fallacies or weak points",
                "Provide counter-evidence",
                "State your refined position"
            ]
        )
        
        response = self.think(react_prompt, max_tokens=800)
        response['reasoning_technique'] = 'ReAct'
        response['react_cycles'] = ReActAgent.parse_react_cycle(response.get('response', ''))
        return response
    
    def self_critique_and_improve(self, initial_response: str, counter_argument: Optional[str] = None) -> dict:
        """Critique own argument and generate improved version"""
        critique_prompt = SelfCorrectionEngine.create_critique_prompt(
            initial_response, counter_argument
        )
        
        response = self.think(critique_prompt, max_tokens=1200)
        response['reasoning_technique'] = 'Self-Correction'
        
        improvements = SelfCorrectionEngine.extract_improvements(response.get('response', ''))
        response['improvements'] = improvements
        response['improved_argument'] = improvements.get('improved_argument', '')
        response['confidence'] = improvements.get('confidence', 5)
        
        return response
    
    def reflect_on_position(self, debate_context: str) -> dict:
        """Reflective thinking about position quality"""
        reflection_prompt = ReflectiveThinking.create_reflection_prompt(
            debate_context, self.position
        )
        
        response = self.think(reflection_prompt, max_tokens=1000)
        response['reasoning_technique'] = 'Reflective Thinking'
        return response


class ModeratorAgent(LLMAgent):
    """Agent specialized in moderating debates and providing balanced analysis"""
    
    def __init__(self):
        super().__init__("Moderator", "a neutral debate moderator and analyst")
        self.reasoning_framework = DebateReasoningFramework()
    
    def analyze_round(self, agent_a_argument: str, agent_b_argument: str, topic: str) -> dict:
        """Analyze a round of debate using Chain of Thought"""
        cot_prompt = ChainOfThoughtPrompter.create_cot_prompt(
            f"""Analyze this debate round objectively:

DEBATE TOPIC: {topic}

AGENT A'S ARGUMENT:
"{agent_a_argument}"

AGENT B'S ARGUMENT:
"{agent_b_argument}"

ANALYSIS STEPS:
1. Identify the core claim of each agent
2. Evaluate the strength of evidence presented
3. Spot logical fallacies or weak reasoning
4. Score each argument (Clarity: 0-10, Logic: 0-10, Evidence: 0-10)
5. Provide a balanced assessment

Be impartial and fair to both sides.""",
            context="You are a neutral moderator analyzing debate quality."
        )
        
        response = self.think(cot_prompt, max_tokens=800)
        response['reasoning_technique'] = 'Chain of Thought'
        response['reasoning_steps'] = ChainOfThoughtPrompter.extract_reasoning_steps(response.get('response', ''))
        return response
    
    def final_conclusion(self, all_arguments: list, topic: str) -> dict:
        """Generate final balanced conclusion using ReAct"""
        arguments_text = "\n\n".join(
            [f"Round {i+1}: {arg}" for i, arg in enumerate(all_arguments)]
        )
        
        react_prompt = ReActAgent.create_react_prompt(
            f"""Debate Topic: {topic}

All arguments presented throughout the debate:
{arguments_text}

Your task: Provide a comprehensive, balanced final conclusion that:
1. Summarizes strongest arguments from both sides
2. Identifies areas of agreement
3. Acknowledges validity of different perspectives
4. Provides nuanced synthesis
5. Suggests areas for further exploration

Use the Reason-Act-Observe cycle for rigorous analysis.""",
            available_actions=[
                "Identify common ground",
                "Evaluate argument quality",
                "Recognize valid perspectives",
                "Synthesize evidence",
                "Form balanced conclusion"
            ]
        )
        
        response = self.think(react_prompt, max_tokens=1200)
        response['reasoning_technique'] = 'ReAct'
        response['react_cycles'] = ReActAgent.parse_react_cycle(response.get('response', ''))
        return response
    
    def evaluate_debate_quality(self, debate_transcript: str, topic: str) -> dict:
        """Evaluate overall debate quality and reasoning"""
        reflection_prompt = f"""DEBATE QUALITY EVALUATION

TOPIC: {topic}

DEBATE TRANSCRIPT:
{debate_transcript}

EVALUATION CRITERIA:
1. Argument Quality: How well-structured and logical?
2. Evidence Use: How effectively is evidence used?
3. Logical Fallacies: How many fallacies were present?
4. Engagement: Did agents address opponent's points?
5. Neutrality: Was the moderator fair?
6. Overall Value: Did the debate illuminate the topic?

Provide scores (1-10) and constructive feedback for improvement."""
        
        response = self.think(reflection_prompt, max_tokens=1000)
        response['reasoning_technique'] = 'Reflective Thinking'
        return response
    
    def critique_debate_fairness(self, agent_a_args: list, agent_b_args: list) -> dict:
        """Self-critique: Ensure balanced analysis of both sides"""
        agent_a_text = "\n".join(agent_a_args)
        agent_b_text = "\n".join(agent_b_args)
        
        critique_prompt = SelfCorrectionEngine.create_critique_prompt(
            f"""MODERATOR FAIRNESS CHECK

AGENT A'S ARGUMENTS:
{agent_a_text}

AGENT B'S ARGUMENTS:
{agent_b_text}

SELF-CRITIQUE:
1. Have I been fair to both sides?
2. Which side did I favor (if any)?
3. What strengths did I miss in each argument?
4. Am I being biased toward any position?
5. How can I provide more balanced analysis?""",
            counter_argument=None
        )
        
        response = self.think(critique_prompt, max_tokens=1000)
        response['reasoning_technique'] = 'Self-Correction'
        improvements = SelfCorrectionEngine.extract_improvements(response.get('response', ''))
        response['fairness_assessment'] = improvements
        return response
