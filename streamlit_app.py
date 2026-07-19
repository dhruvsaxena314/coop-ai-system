import streamlit as st
import pandas as pd
import networkx as nx
from orchestrator import Orchestrator
from agents.ai_agent import FlexibleAIAgent
from agents.analysis_agent import AnalysisAgent
from agents.knowledge_graph_agent import KnowledgeGraphAgent
from config import AIConfig
from visualizer import Visualizer

st.set_page_config(
    page_title="Co-op AI Management System",
    page_icon="⚙️",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono&display=swap');
    * {
        font-family: 'DM Mono', monospace;
    }
    .stApp {
        background-color: #0e1117;
    }
    .main-header {
        color: #ffffff;
        font-size: 2rem;
        font-weight: bold;
        padding: 1rem 0;
        border-bottom: 2px solid #2d3138;
    }
    .status-ok {
        color: #4caf50;
    }
    .status-error {
        color: #f44336;
    }
    .sidebar-box {
        background-color: #1e2128;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .agent-box {
        background-color: #1e2128;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #4a9eff;
    }
    .finding {
        color: #e0e0e0;
        font-size: 0.9rem;
    }
    .recommendation-box {
        background-color: #1e2128;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 2px solid #4a9eff;
    }
    .recommendation-text {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: bold;
    }
    .risk-low {
        color: #4caf50;
    }
    .risk-medium {
        color: #ff9800;
    }
    .risk-high {
        color: #f44336;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #1e2128;
        border-radius: 8px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 8px 16px;
        color: #888888;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2d3138;
        color: #ffffff;
    }
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

    # Mode selector with fallback
    mode_options = ['local', 'web', 'hybrid']
    current_mode = ai_agent.mode.strip()
    if current_mode not in mode_options:
        current_mode = "web"

    selected_mode = st.selectbox("AI Mode", mode_options, index=mode_options.index(current_mode))
    if selected_mode != ai_agent.mode:
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

st.markdown("<div class='main-header'>⚙️ Co-operative AI Management System</div>", unsafe_allow_html=True)

# Tabs (All 4 features)
tab1, tab2, tab3, tab4 = st.tabs(["📊 Decision Analysis", "💬 AI Chat", "📈 Dashboard", "🔗 Knowledge Graph"])

# ==================== TAB 1: Decision Analysis ====================
with tab1:
    st.markdown("<p style='color: #888888;'>Ask a question about your co-operative operations</p>", unsafe_allow_html=True)

    query = st.text_input("Your Question", placeholder="Example: Can we accept the 500 unit bulk order?")

    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        analyze_btn = st.button("Analyze", type="primary", use_container_width=True)
    with col2:
        sample_btn = st.button("Load Sample", use_container_width=True)

    if sample_btn:
        st.session_state.query = "Can we accept the 500 unit bulk order from the city distributor?"
        st.rerun()

    if "query" not in st.session_state:
        st.session_state.query = ""

    if analyze_btn or st.session_state.query:
        if not query and not st.session_state.query:
            st.warning("Please enter a question.")
        else:
            with st.spinner("Analyzing with all agents..."):
                # Structured analysis
                analysis = analysis_agent.analyze(query)
                # AI response
                ai_response = ai_agent.chat(query)

                st.markdown("---")
                st.markdown("<h3 style='color:#ffffff;'>Decision Summary</h3>", unsafe_allow_html=True)

                # Recommendation box
                st.markdown(f"""
                <div class='recommendation-box'>
                    <p class='recommendation-text'>{ai_response}</p>
                    <p style='color: #888888; font-size: 0.8rem; margin-top: 0.5rem;'>
                    AI Recommendation
                    </p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<h4 style='color:#ffffff; margin-top: 1.5rem;'>Data Insights</h4>", unsafe_allow_html=True)

                if analysis['insights']:
                    for insight in analysis['insights']:
                        st.markdown(f"<div class='agent-box'><p class='finding'>{insight}</p></div>", unsafe_allow_html=True)
                else:
                    st.info("No specific data insights found for this query.")

# ==================== TAB 2: AI Chat ====================
with tab2:
    st.markdown("<h3 style='color:#ffffff;'>💬 AI Assistant</h3>", unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
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

# ==================== TAB 3: Dashboard ====================
with tab3:
    st.markdown("<h3 style='color:#ffffff;'>📈 Analytics Dashboard</h3>", unsafe_allow_html=True)

    try:
        finance_df = pd.read_csv("data/finances.csv")
        inventory_df = pd.read_csv("data/inventory.csv")
        orders_df = pd.read_csv("data/orders.csv")
        members_df = pd.read_csv("data/members.csv")

        # Metrics row
        col1, col2, col3, col4, col5 = st.columns(5)
        total_sales = finance_df[finance_df['type'] == 'income']['amount'].sum()
        total_expenses = finance_df[finance_df['type'] == 'expense']['amount'].sum()
        profit = total_sales - total_expenses

        col1.metric("Total Sales", f"Rs {total_sales:,.0f}")
        col2.metric("Total Expenses", f"Rs {total_expenses:,.0f}")
        col3.metric("Net Profit", f"Rs {profit:,.0f}")
        col4.metric("Inventory Items", len(inventory_df))
        col5.metric("Members", len(members_df))

        # Charts row 1
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(Visualizer.plot_sales_trend(finance_df), use_container_width=True)
        with col2:
            st.plotly_chart(Visualizer.plot_cash_flow(finance_df), use_container_width=True)

        # Charts row 2
        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(Visualizer.plot_inventory_status(inventory_df), use_container_width=True)
        with col4:
            st.plotly_chart(Visualizer.plot_portfolio_distribution(finance_df), use_container_width=True)

    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        st.info("Make sure all CSV files exist in the data/ folder.")

# ==================== TAB 4: Knowledge Graph ====================
with tab4:
    st.markdown("<h3 style='color:#ffffff;'>🔗 Knowledge Graph</h3>", unsafe_allow_html=True)

    # Graph stats
    col1, col2, col3 = st.columns(3)
    col1.metric("Nodes", len(kg.graph.nodes) if kg.graph else 0)
    col2.metric("Edges", len(kg.graph.edges) if kg.graph else 0)

    # Interactive graph
    try:
        if kg.graph and kg.graph.nodes:
            net = kg.visualize_graph()
            net.show("kg_visualization.html")
            with open("kg_visualization.html", "r", encoding="utf-8") as f:
                st.components.v1.html(f.read(), height=500)
        else:
            st.info("No data available for knowledge graph. Add data to see connections.")
    except Exception as e:
        st.error(f"Error displaying knowledge graph: {str(e)}")

    # Query interface
    st.markdown("<h4 style='color:#ffffff;'>Query Graph</h4>", unsafe_allow_html=True)
    node_name = st.text_input("Enter node name to find connections:", placeholder="Example: Rajesh Kumar")
    if node_name:
        connections = kg.get_connections(node_name) if kg.graph else []
        if connections:
            st.write(f"**Connections for '{node_name}':**")
            for conn in connections:
                st.write(f"- {conn}")
        else:
            st.write(f"Node '{node_name}' not found or has no connections")

    # Node type filter
    node_types = []
    if kg.graph and kg.graph.nodes:
        try:
            node_types = list(set(nx.get_node_attributes(kg.graph, 'type').values()))
        except:
            pass

    if node_types:
        selected_type = st.selectbox("Filter by type", ["All"] + node_types)
        if selected_type != "All":
            filtered_nodes = [n for n, d in kg.graph.nodes(data=True) if d.get('type') == selected_type]
            st.write(f"**Nodes of type '{selected_type}':** {len(filtered_nodes)}")
            if filtered_nodes:
                st.write(filtered_nodes[:10])

st.markdown("---")
st.markdown("<p style='color: #444444; font-size: 0.7rem; text-align: center;'>⚙️ AI Management System for Cooperatives and Cottage Industries</p>", unsafe_allow_html=True)
