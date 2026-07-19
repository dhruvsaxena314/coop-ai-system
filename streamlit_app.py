import streamlit as st
import pandas as pd
from orchestrator import Orchestrator
from agents.ai_agent import FlexibleAIAgent
from agents.analysis_agent import AnalysisAgent
from config import AIConfig
from visualizer import Visualizer
from agents.knowledge_graph_agent import KnowledgeGraphAgent
import os
import networkx as nx  

st.set_page_config(
    page_title="Co-op AI Management System",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono&display=swap');
    * { font-family: 'DM Mono', monospace; }
    .stApp { background-color: #0e1117; }
    .main-header { color: #ffffff; font-size: 2rem; font-weight: bold; padding: 1rem 0; border-bottom: 2px solid #2d3138; }
    .status-ok { color: #4caf50; }
    .status-error { color: #f44336; }
    .sidebar-box { background-color: #1e2128; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

# Initialize components
orchestrator = Orchestrator()
ai_agent = FlexibleAIAgent()
analysis_agent = AnalysisAgent()
kg = KnowledgeGraphAgent()

# Sidebar - AI Configuration
with st.sidebar:
    st.markdown("<h3 style='color:#ffffff;'>AI Configuration</h3>", unsafe_allow_html=True)
    
    # Mode selector
    current_mode = ai_agent.mode
    mode_options = ['local', 'web', 'hybrid']
   current_mode = ai_agent.mode.strip()
   selected_mode = st.selectbox("AI Mode", mode_options, index=mode_options.index(current_mode) if current_mode in mode_options else 0)
    if selected_mode != current_mode:
        ai_agent.set_mode(selected_mode)
        st.rerun()
    
    st.markdown("---")
    
    # Ollama model selector
    if ai_agent.ollama_available:
        models = ai_agent.list_ollama_models()
        if models:
            current_model = ai_agent.local_model
            selected_model = st.selectbox("Local Model", models, index=models.index(current_model) if current_model in models else 0)
            if selected_model != current_model:
                ai_agent.set_local_model(selected_model)
                st.success(f"Switched to {selected_model}")
        else:
            st.warning("No Ollama models found. Run 'ollama pull mistral'")
    else:
        st.error("Ollama not running. Start with 'ollama serve'")
    
    st.markdown("---")
    
    # Status display
    st.markdown("<h4 style='color:#ffffff;'>Status</h4>", unsafe_allow_html=True)
    status = ai_agent.get_status()
    
    st.markdown(f"""
    <div class='sidebar-box'>
        <p style='color:#888888; font-size:0.8rem;'>
        Mode: <span style='color:#ffffff;'>{status['mode'].upper()}</span><br>
        Ollama: {'🟢 Running' if status['ollama_available'] else '🔴 Not running'}<br>
        Local Model: <span style='color:#ffffff;'>{status['local_model']}</span><br>
        OpenRouter: {'✅ Configured' if status['openrouter'] else '❌ Not configured'}<br>
        Web Model: <span style='color:#ffffff;'>{status['openrouter_model']}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-header'>Co-operative AI Management System</div>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Decision Analysis", "Intelligence System ", "Dashboard", "Knowledge Graph"])

# Tab 1: Decision Analysis
with tab1:
    st.markdown("<p style='color: #888888;'>Ask a question/p>", unsafe_allow_html=True)
    
    query = st.text_input("Your Question", placeholder="ask here")
    if st.button("Analyze", type="primary"):
        if query:
            with st.spinner("Analyzing..."):
                # Structured analysis
                analysis = analysis_agent.analyze(query)
                # AI response
                ai_response = ai_agent.chat(query)
                
                st.markdown("### Analysis Results")
                if analysis['insights']:
                    st.write("**Data Insights:**")
                    for insight in analysis['insights']:
                        st.write(f"- {insight}")
                
                st.write("**AI Recommendation:**")
                st.write(ai_response)

# Tab 2: AI Chat
with tab2:
    st.markdown("<h3 style='color:#ffffff;'>AI Assistant</h3>", unsafe_allow_html=True)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    user_input = st.chat_input("Ask anything about your cooperative...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.spinner("Thinking..."):
            response = ai_agent.chat(user_input)
        with st.chat_message("assistant"):
            st.write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# Tab 3: Dashboard
with tab3:
    st.markdown("<h3 style='color:#ffffff;'>Analytics Dashboard</h3>", unsafe_allow_html=True)
    
    try:
        finance_df = pd.read_csv("data/finances.csv")
        inventory_df = pd.read_csv("data/inventory.csv")
        
        col1, col2, col3, col4 = st.columns(4)
        total_sales = finance_df[finance_df['type'] == 'income']['amount'].sum()
        total_expenses = finance_df[finance_df['type'] == 'expense']['amount'].sum()
        profit = total_sales - total_expenses
        
        col1.metric("Total Sales", f"Rs {total_sales:,.0f}")
        col2.metric("Total Expenses", f"Rs {total_expenses:,.0f}")
        col3.metric("Net Profit", f"Rs {profit:,.0f}")
        col4.metric("Inventory Items", len(inventory_df))
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(Visualizer.plot_sales_trend(finance_df), use_container_width=True)
        with col2:
            st.plotly_chart(Visualizer.plot_cash_flow(finance_df), use_container_width=True)
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")

# Tab 4: Knowledge Graph
with tab4:
    st.markdown("<h3 style='color:#ffffff;'>Knowledge Graph</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Nodes", len(kg.graph.nodes))
    col2.metric("Edges", len(kg.graph.edges))
    
    net = kg.visualize_graph()
    net.show("kg_visualization.html")
    with open("kg_visualization.html", "r", encoding="utf-8") as f:
        st.components.v1.html(f.read(), height=500)
