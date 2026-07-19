import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class Visualizer:
    @staticmethod
    def plot_sales_trend(df):
        if df.empty:
            return go.Figure()
        
        fig = px.line(df, x='date', y='amount', color='category', 
                      title='Sales Trend Over Time')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e0e0e0'
        )
        return fig
    
    @staticmethod
    def plot_inventory_status(df):
        if df.empty:
            return go.Figure()
        
        fig = px.bar(df, x='item_name', y='quantity', color='category',
                     title='Current Inventory Status')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e0e0e0'
        )
        return fig
    
    @staticmethod
    def plot_cash_flow(df):
        if df.empty:
            return go.Figure()
        
        df['date'] = pd.to_datetime(df['date'])
        monthly = df.groupby(df['date'].dt.month)['amount'].sum().reset_index()
        fig = px.bar(monthly, x='date', y='amount', title='Monthly Cash Flow')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e0e0e0'
        )
        return fig
    
    @staticmethod
    def plot_portfolio_distribution(df):
        if df.empty:
            return go.Figure()
        
        fig = px.pie(df, values='amount', names='category', title='Expense Distribution')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e0e0e0'
        )
        return fig
