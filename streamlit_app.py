import streamlit as st
import pandas as pd
import networkx as nx
from orchestrator import Orchestrator
from agents.ai_agent import FlexibleAIAgent
from agents.analysis_agent import AnalysisAgent
from agents.knowledge_graph_agent import KnowledgeGraphAgent
from config import AIConfig
from visualizer import Visualizer

st.set_page_config(page_title="Co-op AI", page_icon="", layout="wide")

# Professional dark theme – no extra fluff
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono&display=swap');
    * { font-family: 'DM Mono', monospace; }
    .stApp { background-color: #0b0e14; }
    .main-header { color: #ffffff; font-size: 1.8rem; font-weight: 400; padding: 0.5rem 0; border-bottom: 1px solid #2a2f3a; }
    .sidebar-box { background-color: #131821; padding: 0.8rem; border-radius: 6px; margin: 0.5rem 0; }
    .status-text { color: #aaaaaa; font-size: 0.75rem; line-height: 1.6; }
    .insight-box { background-color: #131821; padding: 0.8rem 1.2rem; border-radius: 4px; margin: 0.3rem 0; border-left: 3px solid #4a9eff; }
    .cot-box { background-color: #1a1f2a; padding: 0.8rem 1.2rem; border-radius: 4px; margin: 0.5rem 0; font-size: 0.85rem; border: 1px solid #2a2f3a; }
    .reference { color: #7799cc; font-size: 0.7rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; background-color: #131821; border-radius: 6px; padding: 4px; }
    .stTabs [data-baseweb="tab"] { border-radius: 4px; padding: 6px 14px; color: #888; }
    .stTabs [aria-selected="true"] { background-color: #2a2f3a; color: #fff; }
    .stButton button { background-color: #2a2f3a; color: #fff; border: none; border-radius: 4px; }
    .stButton button:hover { background-color: #3a3f4a; }
</style>
""", unsafe_allow_html=True)

# Init
orchestrator = Orchestrator()
ai_agent = FlexibleAIAgent()
analysis_agent = AnalysisAgent()
kg = KnowledgeGraphAgent()

# Sidebar – minimal
with st.sidebar:
    st.markdown("<div style='font-size:1.2rem; color:#fff;'>⚙ Config</div>", unsafe_allow_html=True)
    mode_options = ['local', 'web', 'hybrid']
    cur = ai_agent.mode.strip()
    if cur not in mode_options: cur = 'web'
    sel = st.selectbox("Mode", mode_options, index=mode_options.index(cur))
    if sel != ai_agent.mode:
        ai_agent.set_mode(sel)
        st.rerun()
    
    if ai_agent.ollama_available:
        models = ai_agent.list_ollama_models()
        if models:
            m_cur = ai_agent.local_model
            m_sel = st.selectbox("Local model", models, index=models.index(m_cur) if m_cur in models else 0)
            if m_sel != m_cur:
                ai_agent.set_local_model(m_sel)
                st.rerun()
    
    st.markdown("---")
    status = ai_agent.get_status()
    st.markdown(f"""
    <div class='sidebar-box'>
        <div class='status-text'>
        Mode: <span style='color:#fff;'>{status['mode'].upper()}</span><br>
        Groq: {'✅' if status['groq'] else '❌'} {status['groq_model']}<br>
        Ollama: {'🟢' if status['ollama_available'] else '🔴'} {status['local_model']}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-header'>Co‑operative AI · Decision Intelligence</div>", unsafe_allow_html=True)

tabs = st.tabs(["📊 Decision", "💬 Chat", "📈 Dashboard", "🔗 Graph"])

# ========== TAB 1: Decision ==========
with tabs[0]:
    st.markdown("<p style='color:#888;'>Ask a business question – get data‑backed reasoning</p>", unsafe_allow_html=True)
    query = st.text_input("", placeholder="e.g. Can we accept the 500 unit bulk order?")
    col1, col2 = st.columns([1, 4])
    with col1:
        go = st.button("Analyze", type="primary", use_container_width=True)
    with col2:
        if st.button("Load example", use_container_width=True):
            query = "Can we accept the 500 unit bulk order from the city distributor?"
            st.rerun()
    
    if go and query:
        with st.spinner("Analyzing data..."):
            analysis = analysis_agent.analyze(query)
            ai_answer = ai_agent.chat(query, analysis['context'])
            
            st.markdown("---")
            # Final decision (brief)
            st.markdown(f"<div style='background:#1a1f2a; padding:1.2rem; border-radius:6px; border-left:4px solid #4a9eff;'>"
                        f"<span style='color:#fff; font-size:1.1rem;'>{ai_answer}</span></div>", unsafe_allow_html=True)
            
            # Chain of Thought
            if analysis.get('cot'):
                st.markdown("<div style='margin-top:1rem; font-size:0.9rem; color:#aaa;'>Reasoning</div>", unsafe_allow_html=True)
                for step in analysis['cot']:
                    st.markdown(f"<div class='cot-box'>→ {step}</div>", unsafe_allow_html=True)
            
            # Insights + references
            if analysis['insights']:
                st.markdown("<div style='margin-top:1rem; font-size:0.9rem; color:#aaa;'>Data insights</div>", unsafe_allow_html=True)
                for ins in analysis['insights']:
                    st.markdown(f"<div class='insight-box'>{ins}</div>", unsafe_allow_html=True)
            if analysis.get('references'):
                refs = " | ".join(analysis['references'])
                st.markdown(f"<div class='reference'>References: {refs}</div>", unsafe_allow_html=True)

# ========== TAB 2: Chat ==========
with tabs[1]:
    st.markdown("<p style='color:#888;'>Conversational AI with data awareness</p>", unsafe_allow_html=True)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    user_input = st.chat_input("Type your question...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        with st.spinner("Thinking..."):
            analysis = analysis_agent.analyze(user_input)
            response = ai_agent.chat(user_input, analysis['context'])
        with st.chat_message("assistant"):
            st.write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# ========== TAB 3: Dashboard ==========
with tabs[2]:
    st.markdown("<p style='color:#888;'>Key metrics & charts</p>", unsafe_allow_html=True)
    try:
        fin = pd.read_csv("data/finances.csv")
        inv = pd.read_csv("data/inventory.csv")
        orders = pd.read_csv("data/orders.csv")
        members = pd.read_csv("data/members.csv")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        total_sales = fin[fin['type']=='income']['amount'].sum()
        total_exp = fin[fin['type']=='expense']['amount'].sum()
        col1.metric("Revenue", f"Rs {total_sales:,.0f}")
        col2.metric("Expenses", f"Rs {total_exp:,.0f}")
        col3.metric("Profit", f"Rs {total_sales-total_exp:,.0f}")
        col4.metric("Inventory items", len(inv))
        col5.metric("Members", len(members))
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(Visualizer.plot_sales_trend(fin), use_container_width=True)
        with col2:
            st.plotly_chart(Visualizer.plot_cash_flow(fin), use_container_width=True)
        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(Visualizer.plot_inventory_status(inv), use_container_width=True)
        with col4:
            st.plotly_chart(Visualizer.plot_portfolio_distribution(fin), use_container_width=True)
        
        with st.expander("Raw data"):
            st.dataframe(fin)
    except Exception as e:
        st.error(f"Dashboard error: {e}")

# ========== TAB 4: Knowledge Graph ==========
with tabs[3]:
    st.markdown("<p style='color:#888;'>Entity relationships in your cooperative</p>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        if kg._built and len(kg.graph.nodes) > 0:
            net = kg.visualize()
            if net:
                net.show("kg.html")
                with open("kg.html", "r", encoding="utf-8") as f:
                    st.components.v1.html(f.read(), height=500)
            else:
                st.info("Graph is empty – add more data.")
        else:
            st.info("Build graph from CSV data (check data files).")
    with col2:
        st.markdown("### Query")
        node = st.text_input("Node name")
        if node:
            conn = kg.get_connections(node)
            if conn:
                st.write("**Connections:**")
                for c in conn:
                    st.write(f"- {c}")
            else:
                st.write("No connections or node not found.")
