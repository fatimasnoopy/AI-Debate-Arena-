import streamlit as st
import json
from datetime import datetime
from debate_manager import DebateManager
from agents import DebateAgent, ModeratorAgent
import io

# Page configuration
st.set_page_config(
    page_title="AI Debate Arena",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .debate-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .agent-a {
        background-color: #e3f2fd;
        border-left: 5px solid #1976d2;
    }
    .agent-b {
        background-color: #f3e5f5;
        border-left: 5px solid #7b1fa2;
    }
    .moderator {
        background-color: #e8f5e9;
        border-left: 5px solid #388e3c;
    }
    .reasoning-box {
        background-color: #fff9e6;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        border: 1px solid #fbc02d;
    }
    .loading-spinner {
        text-align: center;
        font-size: 24px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "debate_manager" not in st.session_state:
    st.session_state.debate_manager = None
if "debate_started" not in st.session_state:
    st.session_state.debate_started = False
if "current_round" not in st.session_state:
    st.session_state.current_round = 0
if "show_reasoning" not in st.session_state:
    st.session_state.show_reasoning = False

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Debate Configuration")
    st.divider()
    
    if not st.session_state.debate_started:
        st.subheader("Setup")
        
        # Topic input
        debate_topic = st.text_area(
            "💬 What's the debate topic?",
            placeholder="e.g., Artificial Intelligence will have more positive than negative impact on society",
            height=100
        )
        
        st.divider()
        st.subheader("Agent Positions")
        
        # Agent A position
        agent_a_position = st.text_area(
            "Agent A's Position (Pro)",
            placeholder="State the position Agent A will defend...",
            height=80,
            key="agent_a_pos"
        )
        
        # Agent B position
        agent_b_position = st.text_area(
            "Agent B's Position (Con)",
            placeholder="State the position Agent B will defend...",
            height=80,
            key="agent_b_pos"
        )
        
        st.divider()
        st.subheader("Debate Settings")
        
        # Number of rounds
        num_rounds = st.slider(
            "Number of debate rounds",
            min_value=1,
            max_value=5,
            value=2,
            help="Each round includes a rebuttal from each agent"
        )
        
        # Show reasoning toggle
        show_reasoning = st.checkbox(
            "Show detailed reasoning steps",
            value=False,
            help="Display the AI's internal reasoning process"
        )
        
        st.session_state.show_reasoning = show_reasoning
        
        st.divider()
        
        # Start debate button
        if st.button("🚀 Start Debate", use_container_width=True, type="primary"):
            if debate_topic and agent_a_position and agent_b_position:
                try:
                    with st.spinner("Initializing debate..."):
                        st.session_state.debate_manager = DebateManager(
                            topic=debate_topic,
                            agent_a_position=agent_a_position,
                            agent_b_position=agent_b_position
                        )
                        st.session_state.num_rounds = num_rounds
                        st.session_state.debate_started = True
                        st.session_state.current_round = 0
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("Please fill in all fields to start the debate")
    
    else:
        # Debate in progress
        st.subheader("📊 Debate Progress")
        
        manager = st.session_state.debate_manager
        summary = manager.get_debate_summary()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Current Round", st.session_state.current_round, f"/ {st.session_state.num_rounds}")
        with col2:
            st.metric("Total Messages", summary["total_messages"])
        
        st.divider()
        
        if st.button("🔄 Reset Debate", use_container_width=True):
            st.session_state.debate_manager = None
            st.session_state.debate_started = False
            st.session_state.current_round = 0
            st.rerun()

# Main content
if not st.session_state.debate_started:
    # Welcome screen
    st.title("🎤 AI Debate Arena")
    st.subheader("Watch AI agents engage in structured debate with transparent reasoning")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("💡 **Any Topic**\nChoose any debate topic you want to explore")
    
    with col2:
        st.info("🤖 **AI Agents**\nThree LLM agents engage in logical debate")
    
    with col3:
        st.info("🔍 **Transparent Reasoning**\nSee how AI thinks through arguments")
    
    st.divider()
    st.markdown("""
    ### How it works:
    1. **Setup** - Define your debate topic and agent positions
    2. **Opening** - Each agent presents their initial argument
    3. **Rounds** - Agents rebut each other while moderator analyzes
    4. **Conclusion** - Moderator provides balanced final synthesis
    
    Configure the debate in the left sidebar to get started! ➡️
    """)

else:
    manager = st.session_state.debate_manager
    
    st.title("🎤 AI Debate Arena")
    st.markdown(f"### Topic: {manager.topic}")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Live Debate", "Analysis", "Transcript"])
    
    with tab1:
        # Display opening statements if debate hasn't started
        if st.session_state.current_round == 0 and len(manager.debate_history) == 0:
            st.subheader("⏳ Generating Opening Statements...")
            
            with st.spinner("Agent A is preparing their opening statement..."):
                opening_result = manager.start_debate()
            
            st.success("✅ Opening statements generated!")
            st.session_state.current_round = 1
        
        # Display debate history
        for msg_idx, msg in enumerate(manager.debate_history):
            agent_name = msg["agent"]
            content = msg["content"]
            msg_type = msg["type"]
            
            if agent_name == "Agent A":
                col_class = "agent-a"
            elif agent_name == "Agent B":
                col_class = "agent-b"
            else:
                col_class = "moderator"
            
            st.markdown(f"""
            <div class="debate-container {col_class}">
                <b>{agent_name}</b> - {msg_type.replace('_', ' ').title()}
            </div>
            """, unsafe_allow_html=True)
            
            st.write(content)
            
            # Show reasoning technique if available
            if msg.get("raw_response"):
                raw = msg["raw_response"]
                
                # Display reasoning technique
                if raw.get('reasoning_technique'):
                    st.info(f"**🧠 Technique de raisonnement:** {raw['reasoning_technique']}")
                
                # Display reasoning steps for CoT
                if raw.get('reasoning_steps'):
                    with st.expander("📊 Étapes de raisonnement (Chain of Thought)"):
                        for i, step in enumerate(raw['reasoning_steps'], 1):
                            st.write(f"**Étape {i}:**\n{step}")
                
                # Display ReAct cycles
                if raw.get('react_cycles'):
                    with st.expander("🔄 Cycles ReAct"):
                        for i, cycle in enumerate(raw['react_cycles'], 1):
                            st.write(f"**Cycle {i}:**")
                            if cycle.get('thought'):
                                st.write(f"💭 Pensée: {cycle['thought']}")
                            if cycle.get('action'):
                                st.write(f"⚡ Action: {cycle['action']}")
                            if cycle.get('observation'):
                                st.write(f"👁️ Observation: {cycle['observation']}")
                            if cycle.get('reasoning'):
                                st.write(f"🧠 Raisonnement: {cycle['reasoning']}")
                
                # Display improvements from Self-Correction
                if raw.get('improvements'):
                    improvements = raw['improvements']
                    with st.expander("✨ Améliorations (Self-Correction)"):
                        if improvements.get('weaknesses'):
                            st.write("**Faiblesses identifiées:**")
                            for weakness in improvements['weaknesses']:
                                st.write(f"- {weakness}")
                        if improvements.get('valid_points'):
                            st.write("**Points valides du contradicteur:**")
                            for point in improvements['valid_points']:
                                st.write(f"- {point}")
                        st.write(f"**Niveau de confiance:** {improvements.get('confidence', 5)}/10")
            
            # Show reasoning if enabled and available
            if st.session_state.show_reasoning and msg.get("raw_response"):
                raw = msg["raw_response"]
                api_type = msg.get("api_type", "unknown")
                
                if "usage" in raw:
                    usage = raw["usage"]
                    with st.expander(f"📊 {api_type.upper()} - Token usage"):
                        st.write(usage)
        
        # Debate controls
        st.divider()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("▶️ Next Round", use_container_width=True, type="secondary"):
                if st.session_state.current_round < st.session_state.num_rounds:
                    with st.spinner(f"Executing round {st.session_state.current_round + 1}..."):
                        manager.execute_round(st.session_state.current_round)
                    st.session_state.current_round += 1
                    st.rerun()
                else:
                    st.warning("All rounds completed! Go to the 'Analysis' tab for conclusion.")
        
        with col2:
            if st.session_state.current_round >= st.session_state.num_rounds:
                if st.button("📋 Generate Conclusion", use_container_width=True, type="primary"):
                    with st.spinner("Moderator is drafting the conclusion..."):
                        manager.conclude_debate()
                    st.rerun()
        
        with col3:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.debate_started = False
                st.session_state.debate_manager = None
                st.rerun()
    
    with tab2:
        st.subheader("🔍 Analysis & Conclusions")
        
        if manager.final_conclusion:
            st.success("✅ Debate Concluded")
            st.markdown("### 📝 Moderator's Final Conclusion")
            st.write(manager.final_conclusion.get("response", ""))
            
            if st.session_state.show_reasoning:
                with st.expander("📊 Generation Statistics"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Model", manager.final_conclusion.get("model", "Unknown"))
                    with col2:
                        usage = manager.final_conclusion.get("usage", {})
                        st.metric("Prompt Tokens", usage.get("prompt_tokens", "N/A"))
                    with col3:
                        st.metric("Completion Tokens", usage.get("completion_tokens", "N/A"))
        else:
            if st.session_state.current_round < st.session_state.num_rounds:
                st.info(f"Complete all {st.session_state.num_rounds} rounds to see the moderator's conclusion.")
            else:
                st.info("Click 'Generate Conclusion' in the Live Debate tab to get the final analysis.")
        
        # Agent positions summary
        st.divider()
        st.subheader("📌 Debate Positions")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Agent A (Pro)**")
            st.write(manager.agent_a.position)
        with col2:
            st.markdown("**Agent B (Con)**")
            st.write(manager.agent_b.position)
    
    with tab3:
        st.subheader("📄 Full Transcript")
        
        transcript = manager.get_debate_transcript()
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📋 Copy to Clipboard"):
                st.success("Transcript copied! (Use Ctrl+V or Cmd+V to paste)")
        
        with col2:
            # Download transcript
            transcript_bytes = transcript.encode('utf-8')
            st.download_button(
                label="⬇️ Download Transcript (.txt)",
                data=transcript_bytes,
                file_name=f"debate_transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        st.divider()
        
        # Display transcript in a text area
        st.text_area(
            "Debate Transcript",
            value=transcript,
            height=500,
            disabled=True
        )
        
        # JSON export option
        st.divider()
        st.subheader("📊 Export as JSON")
        
        if st.button("⬇️ Download as JSON"):
            debate_data = {
                "metadata": {
                    "topic": manager.topic,
                    "agent_a_position": manager.agent_a.position,
                    "agent_b_position": manager.agent_b.position,
                    "date": datetime.now().isoformat(),
                    "total_rounds": st.session_state.current_round
                },
                "messages": manager.debate_history,
                "conclusion": manager.final_conclusion.get("response", "") if manager.final_conclusion else None
            }
            
            json_str = json.dumps(debate_data, indent=2, ensure_ascii=False)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"debate_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        # Display JSON preview
        if manager.final_conclusion:
            with st.expander("📄 JSON Preview"):
                st.json({
                    "metadata": {
                        "topic": manager.topic,
                        "date": datetime.now().isoformat()
                    },
                    "messages_count": len(manager.debate_history),
                    "has_conclusion": manager.final_conclusion is not None
                })

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🤖 AI Debate Arena | Powered by LLMs | Transparent AI Reasoning</p>
</div>
""", unsafe_allow_html=True)
