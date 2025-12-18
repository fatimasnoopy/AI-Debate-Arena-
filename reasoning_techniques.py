"""
Advanced reasoning techniques for LLM agents:
- Chain of Thought (CoT)
- Tree of Thoughts (ToT)
- ReAct (Reason + Act)
- Self-Correction
"""

from typing import Dict, List, Any, Optional
from enum import Enum


class ReasoningTechnique(Enum):
    """Enumeration of reasoning techniques"""
    CHAIN_OF_THOUGHT = "cot"
    TREE_OF_THOUGHTS = "tot"
    REACT = "react"
    SELF_CORRECTION = "self_correction"


class ChainOfThoughtPrompter:
    """Chain of Thought: Force step-by-step decomposition"""
    
    @staticmethod
    def create_cot_prompt(task: str, context: str = "") -> str:
        """Create a prompt that forces CoT reasoning"""
        return f"""You are a critical thinker engaged in structured reasoning.

{context}

TASK: {task}

INSTRUCTIONS - Think step by step:
1. **UNDERSTAND**: Analyze what is being asked
2. **DECOMPOSE**: Break down the problem into smaller components
3. **ANALYZE**: Examine each component carefully
4. **SYNTHESIZE**: Connect the parts to form a coherent argument
5. **CONCLUDE**: State your final position clearly

Show your thinking process explicitly. Use phrases like:
- "First, I notice that..."
- "This suggests that..."
- "Therefore, I conclude that..."

Provide your structured response below:"""

    @staticmethod
    def extract_reasoning_steps(response: str) -> List[str]:
        """Extract individual reasoning steps from CoT response"""
        steps = []
        lines = response.split('\n')
        current_step = []
        
        for line in lines:
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', 'First', 'Second', 'Third', 'Finally')):
                if current_step:
                    steps.append('\n'.join(current_step).strip())
                current_step = [line]
            else:
                current_step.append(line)
        
        if current_step:
            steps.append('\n'.join(current_step).strip())
        
        return [step for step in steps if step.strip()]


class TreeOfThoughtsEvaluator:
    """Tree of Thoughts: Generate and evaluate multiple solution paths"""
    
    @staticmethod
    def create_tot_prompt(task: str, num_paths: int = 3) -> str:
        """Create prompt for generating multiple thought paths"""
        return f"""You are generating multiple approaches to a complex problem.

TASK: {task}

Generate {num_paths} DIFFERENT APPROACHES to this task:

For each approach:
1. State the approach clearly
2. Outline key steps
3. Evaluate strength (1-10)
4. Identify potential weaknesses

Format:
=== APPROACH 1 ===
Concept: [brief description]
Steps: [step by step]
Strength: [score 1-10]
Weaknesses: [list weaknesses]

=== APPROACH 2 ===
[repeat structure]

=== APPROACH 3 ===
[repeat structure]

Then:
=== EVALUATION ===
Best approach: [which is strongest]
Reasoning: [why it's superior]
Final position: [synthesized argument]"""

    @staticmethod
    def evaluate_paths(paths: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate multiple reasoning paths and select the best"""
        if not paths:
            return {}
        
        # Score paths by strength metric
        scored_paths = []
        for path in paths:
            strength = path.get('strength', 0)
            weaknesses = len(path.get('weaknesses', []))
            score = strength - (weaknesses * 0.5)
            scored_paths.append((path, score))
        
        # Sort by score
        scored_paths.sort(key=lambda x: x[1], reverse=True)
        
        return {
            'best_path': scored_paths[0][0],
            'all_paths': scored_paths,
            'reasoning': 'Selected strongest reasoning path based on logical coherence and evidence'
        }


class ReActAgent:
    """ReAct: Reason + Act loop - Agent takes actions based on reasoning"""
    
    @staticmethod
    def create_react_prompt(task: str, available_actions: List[str]) -> str:
        """Create prompt for ReAct reasoning loop"""
        actions_str = '\n'.join([f"- {action}" for action in available_actions])
        
        return f"""You are an agent engaged in Reason-Act-Observe cycles.

TASK: {task}

AVAILABLE ACTIONS:
{actions_str}

CYCLE STRUCTURE (repeat as needed):
1. THOUGHT: What do I need to understand next?
2. ACTION: Which action should I take? (format: ACTION: [action name])
3. OBSERVATION: What did I learn from this action?
4. REASONING: How does this inform my argument?

Continue cycling until you have sufficient evidence for a strong conclusion.

Format your response with clear THOUGHT, ACTION, OBSERVATION, REASONING blocks."""

    @staticmethod
    def parse_react_cycle(response: str) -> List[Dict[str, str]]:
        """Parse ReAct cycles from agent response"""
        cycles = []
        current_cycle = {}
        
        lines = response.split('\n')
        for line in lines:
            if 'THOUGHT:' in line:
                if current_cycle:
                    cycles.append(current_cycle)
                current_cycle = {'thought': line.split('THOUGHT:')[1].strip()}
            elif 'ACTION:' in line:
                current_cycle['action'] = line.split('ACTION:')[1].strip()
            elif 'OBSERVATION:' in line:
                current_cycle['observation'] = line.split('OBSERVATION:')[1].strip()
            elif 'REASONING:' in line:
                current_cycle['reasoning'] = line.split('REASONING:')[1].strip()
        
        if current_cycle:
            cycles.append(current_cycle)
        
        return cycles


class SelfCorrectionEngine:
    """Self-Correction: Agent critiques and refines its own response"""
    
    @staticmethod
    def create_critique_prompt(initial_response: str, counter_argument: Optional[str] = None) -> str:
        """Create prompt for self-critique"""
        counter_section = ""
        if counter_argument:
            counter_section = f"""
OPPONENT'S ARGUMENT:
"{counter_argument}"

How strong are these counter-points? Where are the weaknesses?
"""
        
        return f"""SELF-CRITIQUE: Review and improve your argument

YOUR INITIAL RESPONSE:
"{initial_response}"

{counter_section}

CRITICAL ANALYSIS:
1. What are the LOGICAL WEAKNESSES in my response?
2. What ASSUMPTIONS am I making?
3. What EVIDENCE am I missing?
4. What FALLACIES might I be committing?
5. How could an INTELLIGENT CRITIC attack this argument?

REFINEMENT:
Based on this critique, provide an IMPROVED version that:
- Addresses identified weaknesses
- Provides stronger evidence
- Acknowledges valid counter-points
- Uses more rigorous logic

FORMAT:
=== IDENTIFIED WEAKNESSES ===
[list weaknesses]

=== VALID COUNTER-POINTS ===
[acknowledge what's valid]

=== IMPROVED ARGUMENT ===
[refined response]

=== CONFIDENCE LEVEL ===
[1-10 score for improved argument]"""

    @staticmethod
    def extract_improvements(critique_response: str) -> Dict[str, Any]:
        """Extract improvement data from critique response"""
        sections = {
            'weaknesses': [],
            'valid_points': [],
            'improved_argument': '',
            'confidence': 5
        }
        
        lines = critique_response.split('\n')
        current_section = None
        
        for i, line in enumerate(lines):
            if 'IDENTIFIED WEAKNESSES' in line:
                current_section = 'weaknesses'
            elif 'VALID COUNTER-POINTS' in line:
                current_section = 'valid_points'
            elif 'IMPROVED ARGUMENT' in line:
                current_section = 'improved_argument'
            elif 'CONFIDENCE LEVEL' in line:
                current_section = 'confidence'
            elif current_section and line.strip():
                if current_section in ['weaknesses', 'valid_points']:
                    if line.strip().startswith('-'):
                        sections[current_section].append(line.strip()[2:])
                elif current_section == 'improved_argument':
                    sections[current_section] += line + '\n'
                elif current_section == 'confidence':
                    try:
                        score = int(line.strip()[0])
                        sections['confidence'] = score
                    except:
                        pass
        
        return sections


class ReflectiveThinking:
    """Meta-reflection: Agent reflects on its own reasoning process"""
    
    @staticmethod
    def create_reflection_prompt(debate_context: str, agent_position: str) -> str:
        """Create prompt for reflective thinking about reasoning quality"""
        return f"""REFLECTIVE ANALYSIS: Evaluate the quality of your reasoning

DEBATE CONTEXT: {debate_context}

YOUR POSITION: {agent_position}

REFLECTION QUESTIONS:
1. How CERTAIN am I in this position? (1-10)
2. What would CHANGE my mind?
3. What ASSUMPTIONS am I relying on?
4. How EMOTIONALLY INVESTED am I in this position?
5. What ALTERNATIVE viewpoints have merit?
6. Am I OVERCONFIDENT?
7. What EVIDENCE would I need to see to reconsider?

HONEST SELF-ASSESSMENT:
[Provide genuine reflection, not just defense of position]

AREAS FOR IMPROVEMENT:
[Identify where reasoning could be stronger]

CONCESSIONS:
[What valid points does the opponent have?]

META-ANALYSIS:
[How good is my overall reasoning?]"""


class DebateReasoningFramework:
    """Integrated framework combining all reasoning techniques"""
    
    def __init__(self):
        self.techniques = {
            ReasoningTechnique.CHAIN_OF_THOUGHT: ChainOfThoughtPrompter(),
            ReasoningTechnique.TREE_OF_THOUGHTS: TreeOfThoughtsEvaluator(),
            ReasoningTechnique.REACT: ReActAgent(),
            ReasoningTechnique.SELF_CORRECTION: SelfCorrectionEngine(),
        }
    
    def apply_technique(self, technique: ReasoningTechnique, task: str, **kwargs) -> str:
        """Apply a specific reasoning technique"""
        if technique == ReasoningTechnique.CHAIN_OF_THOUGHT:
            return ChainOfThoughtPrompter.create_cot_prompt(task, kwargs.get('context', ''))
        elif technique == ReasoningTechnique.TREE_OF_THOUGHTS:
            return TreeOfThoughtsEvaluator.create_tot_prompt(task, kwargs.get('num_paths', 3))
        elif technique == ReasoningTechnique.REACT:
            return ReActAgent.create_react_prompt(task, kwargs.get('actions', []))
        elif technique == ReasoningTechnique.SELF_CORRECTION:
            return SelfCorrectionEngine.create_critique_prompt(
                kwargs.get('initial_response', ''),
                kwargs.get('counter_argument')
            )
        return task
    
    def combine_techniques(self, task: str, techniques: List[ReasoningTechnique]) -> str:
        """Combine multiple techniques in sequence"""
        combined_prompt = f"Use multiple reasoning techniques to address this task:\n\n{task}\n\n"
        
        for technique in techniques:
            combined_prompt += f"\n--- {technique.value.upper()} ---\n"
            combined_prompt += self.apply_technique(technique, task) + "\n"
        
        return combined_prompt
