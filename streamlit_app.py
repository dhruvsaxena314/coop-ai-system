import streamlit as st
import pandas as pd
from orchestrator import Orchestrator
from agents.external_agent import ExternalAgent
from visualizer import Visualizer

st.set_page_config(
    page_title="Co-operative Decision Intelligence",
    page_icon="",
    layout="wide"
)

# Professional dark theme - no emojis
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    * {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background-color: #0a0e17;
    }
    .main-header {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 600;
        padding: 0.8rem 0;
        border-bottom: 1px solid #1e2a3a;
        letter-spacing: -0.02em;
    }
    .sub-header {
        color: #6b7a8f;
        font-size: 0.85rem;
        font-weight: 300;
        margin-top: 0.2rem;
    }
    .sidebar-box {
        background-color: #111927;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #1e2a3a;
    }
    .metric-value {
        color: #ffffff;
        font-size: 1.4rem;
        font-weight: 600;
    }
    .metric-label {
        color: #6b7a8f;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .insight-box {
        background-color: #111927;
        padding: 0.8rem 1.2rem;
        border-radius: 6px;
        margin: 0.3rem 0;
        border-left: 3px solid #3b82f6;
    }
    .cot-box {
        background-color: #111927;
        padding: 0.8rem 1.2rem;
        border-radius: 6px;
        margin: 0.4rem 0;
        font-size: 0.85rem;
        border: 1px solid #1e2a3a;
        color: #c8d0dc;
    }
    .recommendation-box {
        background-color: #111927;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #3b82f6;
    }
    .recommendation-text {
        color: #ffffff;
        font-size: 1.05rem;
        font-weight: 400;
        line-height: 1.6;
    }
    .stButton button {
        background-color: #1e2a3a;
        color: #ffffff;
        border: 1px solid #2a3a4a;
        border-radius: 6px;
        font-weight: 400;
        transition: all 0.2s;
    }
    .stButton button:hover {
        background-color: #2a3a4a;
        border-color: #3b82f6;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #111927;
        border-radius: 8px;
        padding: 4px;
        border: 1px solid #1e2a3a;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 8px 18px;
        color: #6b7a8f;
        font-weight: 400;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e2a3a;
        color: #ffffff;
    }
    .risk-low { color: #22c55e; }
    .risk-medium { color: #eab308; }
    .risk-high { color: #ef4444; }
    .dataframe {
        background-color: #111927 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize
orchestrator = Orchestrator()
ext = ExternalAgent()
analysis = orchestrator.analysis

st.markdown("<div class='main-header'>Co-operative Decision Intelligence</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Real-time decision support for cooperatives and cottage industries</div>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<div style='color:#ffffff; font-weight:600; font-size:1.1rem;'>System Status</div>", unsafe_allow_html=True)
    
    # External data
    with st.expander("External Intelligence", expanded=True):
        cotton = ext.get_cotton_price()
        weather = ext.get_weather()
        exchange = ext.get_exchange_rate()
        
        if cotton:
            st.markdown(f"<div><span class='metric-label'>Cotton Price</span><br><span class='metric-value'>${cotton}</span></div>", unsafe_allow_html=True)
        if weather:
            w = weather[0]
            st.markdown(f"<div><span class='metric-label'>Weather</span><br><span class='metric-value'>{w['main']['temp']}°C</span><span style='color:#6b7a8f; font-size:0.8rem;'> {w['weather'][0]['description']}</span></div>", unsafe_allow_html=True)
        if exchange:
            st.markdown(f"<div><span class='metric-label'>USD/INR</span><br><span class='metric-value'>{exchange}</span></div>", unsafe_allow_html=True)
    
    with st.expander("Decision Intelligence", expanded=True):
        st.markdown("""
        <div style='font-size:0.8rem; color:#6b7a8f; line-height:1.6;'>
        <b style='color:#c8d0dc;'>Risk Assessment</b><br>
        Multi-factor risk scoring combining financial, operational, and external risks.
        <br><br>
        <b style='color:#c8d0dc;'>TOPSIS Engine</b><br>
        Multi-criteria decision analysis for order acceptance and strategic choices.
        </div>
        """, unsafe_allow_html=True)

# Tabs
tabs = st.tabs(["Decision Engine", "Analytics", "Intelligence", "Knowledge"])

# TAB 1: Decision Engine
with tabs[0]:
    st.markdown("<p style='color:#6b7a8f;'>Query the decision intelligence system</p>", unsafe_allow_html=True)
    
    query = st.text_input("", placeholder="e.g., Should we accept the 500 unit bulk order?")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_btn = st.button("Analyze", type="primary", use_container_width=True)
    
    if analyze_btn and query:
        with st.spinner("Processing..."):
            result = orchestrator.analyze_query(query)
            
            # Recommendation
            st.markdown("<div class='recommendation-box'>", unsafe_allow_html=True)
            st.markdown(f"<div class='recommendation-text'>{result['synthesis']['response']}</div>", unsafe_allow_html=True)
            risk = result['decision']['risk_level']
            risk_class = "risk-low" if risk == "Low" else "risk-medium" if risk == "Medium" else "risk-high"
            st.markdown(f"<div style='margin-top:0.5rem;'><span class='metric-label'>Risk Assessment</span><br><span class='{risk_class}' style='font-size:1.1rem;font-weight:600;'>{risk}</span> | <span style='color:#6b7a8f;'>Recommendation: {result['decision']['recommendation']}</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Chain of Thought
            st.markdown("<div style='margin-top:1rem;'><span style='color:#c8d0dc; font-weight:500;'>Reasoning Chain</span></div>", unsafe_allow_html=True)
            for step in result['agents']:
                st.markdown(f"<div class='cot-box'><span style='color:#3b82f6;'>→</span> {step['finding']}</div>", unsafe_allow_html=True)
            
            # Data Insights
            st.markdown("<div style='margin-top:1rem;'><span style='color:#c8d0dc; font-weight:500;'>Data Insights</span></div>", unsafe_allow_html=True)
            for agent in result['agents']:
                st.markdown(f"<div class='insight-box'>{agent['finding']}</div>", unsafe_allow_html=True)

# TAB 2: Analytics
with tabs[1]:
    st.markdown("<p style='color:#6b7a8f;'>Key performance indicators and forecasts</p>", unsafe_allow_html=True)
    
    try:
        fin = pd.read_csv("data/finances.csv")
        inv = pd.read_csv("data/inventory.csv")
        members = pd.read_csv("data/members.csv")
        orders = pd.read_csv("data/orders.csv")
        
        # Metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        income = fin[fin['type']=='income']['amount'].sum()
        expenses = fin[fin['type']=='expense']['amount'].sum()
        profit = income - expenses
        
        col1.metric("Revenue", f"Rs {income:,.0f}")
        col2.metric("Expenses", f"Rs {expenses:,.0f}")
        col3.metric("Profit", f"Rs {profit:,.0f}")
        col4.metric("Inventory", len(inv))
        col5.metric("Members", len(members))
        
        # Charts
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
        
        # News
        news = ext.get_news()
        if news:
            st.markdown("<div style='margin-top:1rem;'><span style='color:#c8d0dc; font-weight:500;'>Industry Intelligence</span></div>", unsafe_allow_html=True)
            for item in news[:3]:
                st.markdown(f"<div class='insight-box'>📰 {item['title']} <span style='color:#6b7a8f;font-size:0.75rem;'>— {item['source']}</span></div>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Analytics error: {e}")

# TAB 3: Intelligence
with tabs[2]:
    st.markdown("<p style='color:#6b7a8f;'>Government policies and external intelligence</p>", unsafe_allow_html=True)
    
    # Government policies
    policies = ext.policy.get_active_policies()
    if policies:
        st.markdown("<div style='color:#c8d0dc; font-weight:500; margin-bottom:0.5rem;'>Active Government Policies</div>", unsafe_allow_html=True)
        for p in policies:
            st.markdown(f"""
            <div class='insight-box'>
                <b>{p.get('name', '')}</b><br>
                <span style='color:#6b7a8f;font-size:0.85rem;'>{p.get('description', '')}</span><br>
                <span style='color:#6b7a8f;font-size:0.75rem;'>Effective: {p.get('effective', 'Unknown')} | Impact Score: {p.get('impact_score', 0)}/5</span>
            </div>
            """, unsafe_allow_html=True)
    
    # External data
    st.markdown("<div style='margin-top:1rem;color:#c8d0dc;font-weight:500;'>Live External Data</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        cotton = ext.get_cotton_price()
        if cotton:
            st.metric("Cotton Price", f"${cotton}")
        weather = ext.get_weather()
        if weather:
            w = weather[0]
            st.metric("Weather", f"{w['main']['temp']}°C", w['weather'][0]['description'])
    with col2:
        exchange = ext.get_exchange_rate()
        if exchange:
            st.metric("USD/INR", exchange)
        news = ext.get_news()
        if news:
            st.metric("News Articles", len(news))

# TAB 4: Knowledge
with tabs[3]:
    st.markdown("<p style='color:#6b7a8f;'>Entity relationships and knowledge graph</p>", unsafe_allow_html=True)
    
    kg = orchestrator.analysis.data
    if kg:
        st.write("Knowledge Graph loaded with internal data and external policies.")
        st.write(f"Entities: {sum(len(v) for v in kg.values() if isinstance(v, pd.DataFrame))}")
    
    # Graph visualization placeholder
    st.info("Interactive knowledge graph available on local deployment")

st.markdown("<div style='margin-top:2rem;padding-top:1rem;border-top:1px solid #1e2a3a;'><span style='color:#3b4a5a;font-size:0.7rem;'>Decision Intelligence System v2.0</span></div>", unsafe_allow_html=True)
