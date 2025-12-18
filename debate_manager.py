from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from agents import DebateAgent, ModeratorAgent


@dataclass
class DebateMessage:
    """Represents a message in the debate"""
    agent_name: str
    content: str
    timestamp: str
    reasoning_visible: bool = False
    usage_stats: Dict[str, int] = None
    api_type: str = None
    
    def to_dict(self):
        return asdict(self)


class DebateManager:
    """Manages the complete debate flow"""
    
    def __init__(self, topic: str, agent_a_position: str, agent_b_position: str):
        self.topic = topic
        # Tous les agents utilisent Groq
        self.agent_a = DebateAgent("Agent A", agent_a_position, agent_a_position)
        self.agent_b = DebateAgent("Agent B", agent_b_position, agent_b_position)
        # Moderator aussi utilise Groq
        self.moderator = ModeratorAgent()
        
        self.debate_history = []
        self.round_analyses = []
        self.final_conclusion = None
    
    def start_debate(self) -> Dict[str, Any]:
        """Initialize debate with opening statements"""
        results = {
            "agent_a_opening": None,
            "agent_b_opening": None,
            "success": False
        }
        
        # Get opening statements
        agent_a_response = self.agent_a.opening_statement(self.topic)
        results["agent_a_opening"] = agent_a_response
        self.debate_history.append({
            "agent": "Agent A",
            "type": "opening",
            "content": agent_a_response.get("response", ""),
            "raw_response": agent_a_response,
            "api_type": agent_a_response.get("api_type", "gpt")
        })
        
        agent_b_response = self.agent_b.opening_statement(self.topic)
        results["agent_b_opening"] = agent_b_response
        self.debate_history.append({
            "agent": "Agent B",
            "type": "opening",
            "content": agent_b_response.get("response", ""),
            "raw_response": agent_b_response,
            "api_type": agent_b_response.get("api_type", "gemini")
        })
        
        results["success"] = True
        return results
    
    def execute_round(self, round_number: int) -> Dict[str, Any]:
        """Execute one round of rebuttals"""
        results = {
            "round": round_number,
            "agent_a_rebuttal": None,
            "agent_b_rebuttal": None,
            "moderator_analysis": None,
            "success": False
        }
        
        # Get last arguments from each agent
        agent_b_last_arg = self.debate_history[-1]["content"] if self.debate_history else ""
        agent_a_last_arg = self.debate_history[-2]["content"] if len(self.debate_history) > 1 else ""
        
        # Agent A rebuttal
        agent_a_rebuttal = self.agent_a.respond_to_opponent(agent_b_last_arg, self.topic)
        results["agent_a_rebuttal"] = agent_a_rebuttal
        self.debate_history.append({
            "agent": "Agent A",
            "type": f"rebuttal_round_{round_number}",
            "content": agent_a_rebuttal.get("response", ""),
            "raw_response": agent_a_rebuttal,
            "api_type": agent_a_rebuttal.get("api_type", "gpt")
        })
        
        # Agent B rebuttal
        agent_b_rebuttal = self.agent_b.respond_to_opponent(agent_a_rebuttal.get("response", ""), self.topic)
        results["agent_b_rebuttal"] = agent_b_rebuttal
        self.debate_history.append({
            "agent": "Agent B",
            "type": f"rebuttal_round_{round_number}",
            "content": agent_b_rebuttal.get("response", ""),
            "raw_response": agent_b_rebuttal,
            "api_type": agent_b_rebuttal.get("api_type", "gemini")
        })
        
        # Moderator analysis
        analysis = self.moderator.analyze_round(
            agent_a_rebuttal.get("response", ""),
            agent_b_rebuttal.get("response", ""),
            self.topic
        )
        results["moderator_analysis"] = analysis
        
        results["success"] = True
        return results
    
    def conclude_debate(self) -> Dict[str, Any]:
        """Generate final moderator conclusion with quality evaluation"""
        all_arguments = [msg["content"] for msg in self.debate_history]
        
        # Generate final conclusion
        conclusion = self.moderator.final_conclusion(all_arguments, self.topic)
        self.final_conclusion = conclusion
        
        # Evaluate debate quality
        transcript = self.get_debate_transcript()
        quality_eval = self.moderator.evaluate_debate_quality(transcript, self.topic)
        
        # Check for fairness
        agent_a_args = [msg["content"] for msg in self.debate_history if msg["agent"] == "Agent A"]
        agent_b_args = [msg["content"] for msg in self.debate_history if msg["agent"] == "Agent B"]
        fairness_check = self.moderator.critique_debate_fairness(agent_a_args, agent_b_args)
        
        return {
            "conclusion": conclusion,
            "quality_evaluation": quality_eval,
            "fairness_check": fairness_check,
            "success": True
        }
    
    def get_debate_transcript(self) -> str:
        """Generate a formatted debate transcript"""
        transcript = f"""
{'='*80}
DEBATE TRANSCRIPT
{'='*80}

TOPIC: {self.topic}

Agent A Position: {self.agent_a.position}
Agent B Position: {self.agent_b.position}

{'='*80}

"""
        
        for i, msg in enumerate(self.debate_history, 1):
            transcript += f"\n[{i}] {msg['agent']} - {msg['type'].upper()}\n"
            transcript += "-" * 40 + "\n"
            transcript += msg["content"] + "\n"
        
        if self.final_conclusion:
            transcript += f"\n{'='*80}\n"
            transcript += "MODERATOR FINAL CONCLUSION\n"
            transcript += "="*80 + "\n"
            transcript += self.final_conclusion.get("response", "") + "\n"
        
        transcript += f"\n{'='*80}\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        return transcript
    
    def get_debate_summary(self) -> Dict[str, Any]:
        """Get a summary of the debate"""
        return {
            "topic": self.topic,
            "agent_a_position": self.agent_a.position,
            "agent_b_position": self.agent_b.position,
            "num_rounds": len([m for m in self.debate_history if "rebuttal" in m["type"]]),
            "total_messages": len(self.debate_history),
            "conclusion_available": self.final_conclusion is not None
        }
