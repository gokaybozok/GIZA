import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="GIZA Token Dashboard",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .highlight-card {
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    .blue-card { background-color: #eff6ff; color: #1d4ed8; }
    .green-card { background-color: #f0fdf4; color: #15803d; }
    .purple-card { background-color: #faf5ff; color: #7c3aed; }
    .orange-card { background-color: #fff7ed; color: #ea580c; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_giza_data():
    """Fetch GIZA token data from CoinGecko API"""
    try:
        url = "https://api.coingecko.com/api/v3/coins/giza"
        params = {
            'localization': 'false',
            'tickers': 'false', 
            'market_data': 'true',
            'community_data': 'false',
            'developer_data': 'false'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        market_data = data['market_data']
        
        return {
            'price': market_data['current_price']['usd'],
            'change_24h': market_data['price_change_percentage_24h'],
            'change_7d': market_data.get('price_change_percentage_7d', 0),
            'market_cap': market_data['market_cap']['usd'],
            'volume_24h': market_data['total_volume']['usd'],
            'circulating_supply': market_data['circulating_supply'],
            'total_supply': market_data.get('total_supply', 1000000000),
            'ath': market_data['ath']['usd'],
            'atl': market_data['atl']['usd'],
            'ath_date': market_data['ath_date']['usd'],
            'atl_date': market_data['atl_date']['usd']
        }
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

@st.cache_data(ttl=300)
def fetch_price_history():
    """Fetch historical price data"""
    try:
        url = "https://api.coingecko.com/api/v3/coins/giza/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': '30',
            'interval': 'daily'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        prices = data['prices']
        
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['date_str'] = df['date'].dt.strftime('%m/%d')
        
        return df
    except Exception as e:
        st.error(f"Error fetching price history: {str(e)}")
        return pd.DataFrame()

def format_number(num):
    """Format large numbers with K, M, B suffixes"""
    if num >= 1e9:
        return f"${num/1e9:.2f}B"
    elif num >= 1e6:
        return f"${num/1e6:.1f}M"
    elif num >= 1e3:
        return f"${num/1e3:.0f}K"
    else:
        return f"${num:.2f}"

def format_price(price):
    """Format price with appropriate decimal places"""
    if price >= 1:
        return f"${price:.4f}"
    else:
        return f"${price:.6f}"

def format_percent(percent):
    """Format percentage with color"""
    color = "green" if percent >= 0 else "red"
    sign = "+" if percent >= 0 else ""
    return f":{color}[{sign}{percent:.2f}%]"

# Main app
def main():
    # Header
    st.title("🏛️ GIZA Token Dashboard")
    st.markdown("**Real-time analytics for Giza Protocol's autonomous finance ecosystem**")
    
    # Refresh button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🔄 Refresh Data", type="primary"):
            st.cache_data.clear()
            st.rerun()
    
    with col3:
        st.markdown(f"*Last updated: {datetime.now().strftime('%H:%M:%S')}*")
    
    # Fetch data
    with st.spinner("Loading GIZA token data..."):
        token_data = fetch_giza_data()
        price_history = fetch_price_history()
    
    if token_data is None:
        st.error("Failed to load token data. Please try again later.")
        return
    
    # Key Metrics Row
    st.markdown("### 📊 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Current Price",
            value=format_price(token_data['price']),
            delta=f"{token_data['change_24h']:.2f}%" if token_data['change_24h'] else None
        )
    
    with col2:
        st.metric(
            label="📈 Market Cap",
            value=format_number(token_data['market_cap']),
        )
    
    with col3:
        st.metric(
            label="📊 24h Volume", 
            value=format_number(token_data['volume_24h']),
        )
    
    with col4:
        circulation_pct = (token_data['circulating_supply'] / token_data['total_supply']) * 100
        st.metric(
            label="👥 Circulating Supply",
            value=f"{token_data['circulating_supply']/1e6:.1f}M",
            delta=f"{circulation_pct:.1f}% of total"
        )
    
    # Charts Section
    st.markdown("### 📈 Charts & Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Price Trend (30 Days)")
        if not price_history.empty:
            fig = px.line(
                price_history, 
                x='date_str', 
                y='price',
                title="",
                labels={'price': 'Price (USD)', 'date_str': 'Date'}
            )
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis_title="Date",
                yaxis_title="Price (USD)"
            )
            fig.update_traces(line_color='#3B82F6', line_width=2)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Price history data not available")
    
    with col2:
        st.markdown("#### Token Distribution")
        
        # Token distribution data
        distribution_data = {
            'Category': ['Investors', 'Community', 'Treasury', 'Team', 'Partners'],
            'Percentage': [31.44, 22.21, 22.10, 18.25, 6.00],
            'Tokens': [314.4, 222.1, 221.0, 182.5, 60.0]
        }
        
        df_dist = pd.DataFrame(distribution_data)
        
        fig = px.pie(
            df_dist,
            values='Percentage',
            names='Category',
            title="",
            color_discrete_sequence=['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']
        )
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=True,
            legend=dict(orientation="v", x=1.05, y=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Protocol Highlights
    st.markdown("### 🚀 Protocol Highlights")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="highlight-card blue-card">
            <h3>$474M</h3>
            <p>ARMA Agent Volume</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="highlight-card green-card">
            <h3>+83%</h3>
            <p>Yield Improvement</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="highlight-card purple-card">
            <h3>150+</h3>
            <p>Active Agents</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="highlight-card orange-card">
            <h3>$5.7M</h3>
            <p>Total Funding</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance Analysis
    st.markdown("### 🎯 Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Price Performance")
        
        # Calculate performance metrics
        ath_performance = ((token_data['price'] - token_data['atl']) / token_data['atl']) * 100
        ath_drawdown = ((token_data['ath'] - token_data['price']) / token_data['ath']) * 100
        
        performance_data = {
            'Metric': ['From ATL', 'From ATH', '24h Change', '7d Change'],
            'Performance': [
                ath_performance,
                -ath_drawdown,
                token_data['change_24h'],
                token_data['change_7d']
            ]
        }
        
        df_perf = pd.DataFrame(performance_data)
        
        # Create color list based on positive/negative values
        colors = ['green' if x >= 0 else 'red' for x in df_perf['Performance']]
        
        fig = go.Figure(data=[
            go.Bar(
                x=df_perf['Metric'],
                y=df_perf['Performance'],
                marker_color=colors,
                text=[f"{x:+.1f}%" for x in df_perf['Performance']],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            yaxis_title="Performance (%)",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Supply Metrics")
        
        # Supply analysis
        total_supply = token_data['total_supply']
        circ_supply = token_data['circulating_supply']
        locked_supply = total_supply - circ_supply
        
        st.write(f"**Total Supply:** {total_supply:,.0f} GIZA")
        st.write(f"**Circulating Supply:** {circ_supply:,.0f} GIZA")
        st.write(f"**Locked Supply:** {locked_supply:,.0f} GIZA")
        
        # Progress bar for circulation
        circulation_ratio = circ_supply / total_supply
        st.progress(circulation_ratio, text=f"Circulation: {circulation_ratio:.1%}")
        
        # All-time high/low
        st.markdown("---")
        st.write(f"**All-Time High:** {format_price(token_data['ath'])}")
        st.write(f"**All-Time Low:** {format_price(token_data['atl'])}")
        
        # ATH/ATL dates
        ath_date = datetime.fromisoformat(token_data['ath_date'].replace('Z', '+00:00'))
        atl_date = datetime.fromisoformat(token_data['atl_date'].replace('Z', '+00:00'))
        
        st.write(f"*ATH Date: {ath_date.strftime('%b %d, %Y')}*")
        st.write(f"*ATL Date: {atl_date.strftime('%b %d, %Y')}*")
    
    # Key Insights
    st.markdown("### 💡 Key Insights")
    
    insights = [
        {
            "title": "🤖 Autonomous Finance Pioneer",
            "description": "GIZA enables AI agents to execute DeFi strategies 24/7, achieving 83% higher yields than static positions."
        },
        {
            "title": "🔒 Strong Token Utility", 
            "description": "GIZA tokens are required for agent deployment, network security staking, and governance participation."
        },
        {
            "title": "🏢 Institutional Adoption",
            "description": "Re7 Capital deployed $500K through ARMA agent, demonstrating institutional trust in the technology."
        },
        {
            "title": "🛡️ Security Track Record",
            "description": "Zero security incidents since launch, with rigorous testing and gradual rollout approach."
        }
    ]
    
    for insight in insights:
        with st.expander(insight["title"]):
            st.write(insight["description"])
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6B7280; font-size: 0.9rem;'>
        <p>📊 Data source: CoinGecko API • Built for GIZA Protocol Internship Challenge</p>
        <p>🐍 Built with Python & Streamlit • Updates in real-time</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
