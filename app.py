import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pickle
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# ══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Shopper Spectrum",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════
#  CUSTOM CSS — Dark premium theme
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0f1629 50%, #0a0e1a 100%);
    color: #e8eaf0;
}

/* ── Hide default streamlit elements ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem; max-width: 1400px; }

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #1a1f35 0%, #16213e 40%, #1a1035 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #6366f1, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.5rem 0;
    line-height: 1.1;
}
.hero-sub {
    color: #94a3b8;
    font-size: 1.05rem;
    font-weight: 400;
    margin: 0;
}
.hero-badges {
    display: flex;
    gap: 0.6rem;
    margin-top: 1.2rem;
    flex-wrap: wrap;
}
.badge {
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.35);
    color: #a78bfa;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.02em;
}

/* ── Metric Cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.metric-card {
    background: linear-gradient(135deg, #1e2438 0%, #1a1f35 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
}
.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(99,102,241,0.4);
}
.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    border-radius: 14px 0 0 14px;
}
.metric-card.purple::after { background: #6366f1; }
.metric-card.blue::after   { background: #38bdf8; }
.metric-card.green::after  { background: #34d399; }
.metric-card.orange::after { background: #fb923c; }

.metric-icon { font-size: 1.8rem; margin-bottom: 0.5rem; display: block; }
.metric-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: #f1f5f9;
    line-height: 1;
}
.metric-label {
    color: #64748b;
    font-size: 0.8rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.3rem;
}

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin: 2rem 0 1.2rem 0;
}
.section-icon {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
}
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    font-weight: 600;
    color: #f1f5f9;
    margin: 0;
}
.section-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(99,102,241,0.4), transparent);
}

/* ── Input Card ── */
.input-card {
    background: linear-gradient(135deg, #1e2438 0%, #1a1f35 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
}

/* ── Recommendation Cards ── */
.rec-card {
    background: linear-gradient(135deg, #1e2438 0%, #1a1f35 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1rem 1.3rem;
    margin: 0.5rem 0;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: border-color 0.2s, transform 0.15s;
}
.rec-card:hover {
    border-color: rgba(99,102,241,0.5);
    transform: translateX(4px);
}
.rec-rank {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #4f46e5;
    min-width: 32px;
}
.rec-name {
    font-weight: 500;
    color: #e2e8f0;
    font-size: 0.95rem;
    flex: 1;
}
.rec-score-bar {
    width: 100px;
    height: 6px;
    background: rgba(255,255,255,0.1);
    border-radius: 3px;
    overflow: hidden;
}
.rec-score-fill {
    height: 100%;
    background: linear-gradient(90deg, #6366f1, #a78bfa);
    border-radius: 3px;
}
.rec-pct {
    font-size: 0.82rem;
    color: #a78bfa;
    font-weight: 600;
    min-width: 45px;
    text-align: right;
}

/* ── Segment Result Card ── */
.seg-result {
    border-radius: 16px;
    padding: 2rem 2.4rem;
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
}
.seg-result-icon {
    font-size: 3.5rem;
    display: block;
    margin-bottom: 0.5rem;
}
.seg-result-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
}
.seg-result-desc {
    font-size: 1rem;
    opacity: 0.85;
    margin: 0 0 1rem 0;
    line-height: 1.6;
}

/* ── RFM Input Boxes ── */
.stNumberInput > label {
    color: #94a3b8 !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}
input[type="number"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
}
input[type="number"]:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.2) !important;
}
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    font-size: 1rem !important;
    padding: 0.7rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.2) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(99,102,241,0.4) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    border-radius: 9px !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1.4rem !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1629 0%, #0a0e1a 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
section[data-testid="stSidebar"] .stMarkdown p {
    color: #94a3b8;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.06) !important; }

/* ── Tooltip info boxes ── */
.info-box {
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 10px;
    padding: 0.8rem 1.1rem;
    margin: 0.8rem 0;
    font-size: 0.88rem;
    color: #a5b4fc;
    line-height: 1.5;
}

/* ── Strategy Tags ── */
.strategy-tag {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.3);
    color: #a78bfa;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
    margin: 0.2rem 0.2rem 0.2rem 0;
}

/* ── Plotly charts transparent bg ── */
.js-plotly-plot .plotly { background: transparent !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb { background: #2d3556; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #6366f1; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  LOAD MODELS
# ══════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner=False)
def load_models():
    kmeans    = joblib.load("models/kmeans_model.pkl")
    scaler    = joblib.load("models/scaler.pkl")
    with open("models/label_map.pkl", "rb") as f:
        label_map = pickle.load(f)
    item_sim  = pd.read_pickle("models/item_similarity.pkl")
    with open("models/product_list.pkl", "rb") as f:
        product_list = pickle.load(f)
    rfm_df    = pd.read_csv("models/rfm_segments.csv")
    return kmeans, scaler, label_map, item_sim, product_list, rfm_df

@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_csv("data/online_retail.csv", encoding="latin1")
    df = df.dropna(subset=["CustomerID"])
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
    df = df[df["Quantity"] > 0]
    df = df[df["UnitPrice"] > 0]
    df = df.drop_duplicates()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["CustomerID"]  = df["CustomerID"].astype(int)
    df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]
    df["YearMonth"]   = df["InvoiceDate"].dt.to_period("M").astype(str)
    df["DayOfWeek"]   = df["InvoiceDate"].dt.day_name()
    return df

# Segment config
SEG_CONFIG = {
    "High-Value": {
        "icon": "💎", "color": "#10b981", "bg": "rgba(16,185,129,0.12)",
        "border": "rgba(16,185,129,0.4)",
        "desc": "Recent, frequent buyers with the highest spend. Your most loyal and profitable customers.",
        "strategies": ["VIP Loyalty Program", "Early Access Offers", "Premium Support", "Referral Rewards"]
    },
    "Regular": {
        "icon": "⭐", "color": "#6366f1", "bg": "rgba(99,102,241,0.12)",
        "border": "rgba(99,102,241,0.4)",
        "desc": "Consistent purchasers with moderate spend. Strong candidates for upselling and cross-selling.",
        "strategies": ["Bundle Offers", "Loyalty Points", "Cross-Sell Campaigns", "Monthly Newsletter"]
    },
    "Occasional": {
        "icon": "🌱", "color": "#f59e0b", "bg": "rgba(245,158,11,0.12)",
        "border": "rgba(245,158,11,0.4)",
        "desc": "Infrequent buyers who purchase occasionally. Can be grown with the right incentives.",
        "strategies": ["Seasonal Promotions", "First-Repeat Discounts", "Product Discovery Emails", "Flash Sales"]
    },
    "At-Risk": {
        "icon": "⚠️", "color": "#ef4444", "bg": "rgba(239,68,68,0.12)",
        "border": "rgba(239,68,68,0.4)",
        "desc": "Previously active customers who haven't purchased recently. Urgent win-back needed.",
        "strategies": ["Win-Back Campaign", "\"We Miss You\" Email", "Exclusive Discount", "Feedback Survey"]
    }
}

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#94a3b8"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", showline=False),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", showline=False),
    margin=dict(l=10, r=10, t=40, b=10)
)

# ══════════════════════════════════════════════════════════════
#  LOADING SCREEN
# ══════════════════════════════════════════════════════════════
with st.spinner(""):
    kmeans, scaler, label_map, item_sim, product_list, rfm_df = load_models()
    df = load_data()

# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 1.5rem 0;">
        <div style="font-size:2.5rem; margin-bottom:0.3rem;">🛒</div>
        <div style="font-family:'Space Grotesk',sans-serif; font-size:1.2rem; font-weight:700;
                    background:linear-gradient(135deg,#a78bfa,#38bdf8);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
            Shopper Spectrum
        </div>
        <div style="color:#475569; font-size:0.78rem; margin-top:0.2rem;">E-Commerce Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("#### 📌 Navigation")
    page = st.radio("", ["🏠 Dashboard", "🎯 Product Recommendations", "👤 Customer Segmentation", "📊 Analytics"],
                    label_visibility="collapsed")

    st.markdown("---")
    st.markdown("#### 📈 Quick Stats")

    total_customers = df["CustomerID"].nunique()
    total_revenue   = df["TotalAmount"].sum()
    total_products  = df["Description"].nunique()
    total_orders    = df["InvoiceNo"].nunique()

    st.markdown(f"""
    <div style="display:grid; gap:0.6rem;">
        <div style="background:rgba(99,102,241,0.1); border-radius:8px; padding:0.7rem 1rem;
                    border:1px solid rgba(99,102,241,0.2);">
            <div style="color:#a78bfa; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.05em;">Customers</div>
            <div style="color:#f1f5f9; font-weight:700; font-size:1.1rem;">{total_customers:,}</div>
        </div>
        <div style="background:rgba(56,189,248,0.1); border-radius:8px; padding:0.7rem 1rem;
                    border:1px solid rgba(56,189,248,0.2);">
            <div style="color:#38bdf8; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.05em;">Revenue</div>
            <div style="color:#f1f5f9; font-weight:700; font-size:1.1rem;">£{total_revenue/1e6:.2f}M</div>
        </div>
        <div style="background:rgba(52,211,153,0.1); border-radius:8px; padding:0.7rem 1rem;
                    border:1px solid rgba(52,211,153,0.2);">
            <div style="color:#34d399; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.05em;">Products</div>
            <div style="color:#f1f5f9; font-weight:700; font-size:1.1rem;">{total_products:,}</div>
        </div>
        <div style="background:rgba(251,146,60,0.1); border-radius:8px; padding:0.7rem 1rem;
                    border:1px solid rgba(251,146,60,0.2);">
            <div style="color:#fb923c; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.05em;">Orders</div>
            <div style="color:#f1f5f9; font-weight:700; font-size:1.1rem;">{total_orders:,}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="color:#334155; font-size:0.75rem; text-align:center; line-height:1.6;">
        Built with Streamlit · Scikit-Learn<br>
        KMeans · Cosine Similarity
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  HERO BANNER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-banner">
    <h1 class="hero-title">🛒 Shopper Spectrum</h1>
    <p class="hero-sub">Customer Segmentation & Product Intelligence Platform for E-Commerce</p>
    <div class="hero-badges">
        <span class="badge">RFM Analysis</span>
        <span class="badge">KMeans Clustering</span>
        <span class="badge">Collaborative Filtering</span>
        <span class="badge">Cosine Similarity</span>
        <span class="badge">2,941 Products</span>
        <span class="badge">4,338 Customers</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════
if "Dashboard" in page:

    # Metric cards
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card purple">
            <span class="metric-icon">👥</span>
            <div class="metric-value">{total_customers:,}</div>
            <div class="metric-label">Unique Customers</div>
        </div>
        <div class="metric-card blue">
            <span class="metric-icon">💷</span>
            <div class="metric-value">£{total_revenue/1e6:.2f}M</div>
            <div class="metric-label">Total Revenue</div>
        </div>
        <div class="metric-card green">
            <span class="metric-icon">📦</span>
            <div class="metric-value">{total_products:,}</div>
            <div class="metric-label">Unique Products</div>
        </div>
        <div class="metric-card orange">
            <span class="metric-icon">🧾</span>
            <div class="metric-value">{total_orders:,}</div>
            <div class="metric-label">Total Orders</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Row 1: Monthly Revenue + Segment Donut
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">📈</div>
            <h3 class="section-title">Monthly Revenue Trend</h3>
            <div class="section-line"></div>
        </div>
        """, unsafe_allow_html=True)

        monthly = df.groupby("YearMonth").agg(Revenue=("TotalAmount","sum")).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly["YearMonth"], y=monthly["Revenue"],
            mode="lines+markers",
            fill="tozeroy",
            fillcolor="rgba(99,102,241,0.12)",
            line=dict(color="#6366f1", width=2.5),
            marker=dict(color="#a78bfa", size=6),
            hovertemplate="<b>%{x}</b><br>Revenue: £%{y:,.0f}<extra></extra>"
        ))
        fig.update_layout(**PLOTLY_THEME, height=260,
                          title=dict(text="", x=0.5))
        fig.update_xaxes(tickangle=-30, tickfont=dict(size=10))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">🎯</div>
            <h3 class="section-title">Customer Segments</h3>
            <div class="section-line"></div>
        </div>
        """, unsafe_allow_html=True)

        seg_counts = rfm_df["Segment"].value_counts().reset_index()
        seg_counts.columns = ["Segment", "Count"]
        colors = [SEG_CONFIG[s]["color"] for s in seg_counts["Segment"]]

        fig2 = go.Figure(go.Pie(
            labels=seg_counts["Segment"],
            values=seg_counts["Count"],
            hole=0.55,
            marker=dict(colors=colors, line=dict(color="#0a0e1a", width=2)),
            textinfo="percent+label",
            textfont=dict(size=11, color="white"),
            hovertemplate="<b>%{label}</b><br>%{value:,} customers<br>%{percent}<extra></extra>"
        ))
        fig2.add_annotation(text=f"<b>{len(rfm_df):,}</b><br>customers",
                            x=0.5, y=0.5, showarrow=False,
                            font=dict(size=14, color="#f1f5f9", family="Space Grotesk"))
        fig2.update_layout(**PLOTLY_THEME, height=260, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Row 2: Top Products + Country
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">🏆</div>
            <h3 class="section-title">Top 10 Products</h3>
            <div class="section-line"></div>
        </div>
        """, unsafe_allow_html=True)

        top_prod = (df.groupby("Description")["TotalAmount"].sum()
                    .sort_values(ascending=False).head(10).reset_index())
        top_prod.columns = ["Product", "Revenue"]
        top_prod["Short"] = top_prod["Product"].str[:28] + "..."

        fig3 = go.Figure(go.Bar(
            x=top_prod["Revenue"], y=top_prod["Short"],
            orientation="h",
            marker=dict(
                color=top_prod["Revenue"],
                colorscale=[[0,"#3730a3"],[0.5,"#6366f1"],[1,"#a78bfa"]],
                showscale=False
            ),
            hovertemplate="<b>%{y}</b><br>Revenue: £%{x:,.0f}<extra></extra>"
        ))
        fig3.update_layout(**PLOTLY_THEME, height=300)
        fig3.update_yaxes(categoryorder="total ascending", tickfont=dict(size=9))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">🌍</div>
            <h3 class="section-title">Revenue by Country</h3>
            <div class="section-line"></div>
        </div>
        """, unsafe_allow_html=True)

        country = (df.groupby("Country")["TotalAmount"].sum()
                   .sort_values(ascending=False).head(10).reset_index())
        country.columns = ["Country","Revenue"]

        fig4 = go.Figure(go.Bar(
            x=country["Country"], y=country["Revenue"],
            marker=dict(
                color=country["Revenue"],
                colorscale=[[0,"#0c4a6e"],[0.5,"#0ea5e9"],[1,"#38bdf8"]],
                showscale=False
            ),
            hovertemplate="<b>%{x}</b><br>Revenue: £%{y:,.0f}<extra></extra>"
        ))
        fig4.update_layout(**PLOTLY_THEME, height=300)
        fig4.update_xaxes(tickangle=-30, tickfont=dict(size=10))
        st.plotly_chart(fig4, use_container_width=True)

    # Segment Summary Table
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📋</div>
        <h3 class="section-title">Segment Performance Overview</h3>
        <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    seg_table = rfm_df.groupby("Segment").agg(
        Customers=("CustomerID","count"),
        Avg_Recency=("Recency","mean"),
        Avg_Frequency=("Frequency","mean"),
        Avg_Monetary=("Monetary","mean"),
        Total_Revenue=("Monetary","sum")
    ).round(1).reset_index()

    for _, row in seg_table.iterrows():
        cfg = SEG_CONFIG.get(row["Segment"], {})
        color  = cfg.get("color","#6366f1")
        icon   = cfg.get("icon","•")
        pct    = row["Customers"] / len(rfm_df) * 100
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1e2438,#1a1f35);
                    border:1px solid rgba(255,255,255,0.07); border-left:4px solid {color};
                    border-radius:12px; padding:1rem 1.5rem; margin:0.4rem 0;
                    display:grid; grid-template-columns:2fr 1fr 1fr 1fr 1fr 1fr; gap:1rem; align-items:center;">
            <div>
                <span style="font-size:1.3rem;">{icon}</span>
                <span style="font-weight:600; color:#f1f5f9; margin-left:0.5rem;">{row["Segment"]}</span>
                <div style="color:#475569; font-size:0.78rem; margin-top:0.1rem;">{pct:.1f}% of customers</div>
            </div>
            <div><div style="color:#64748b;font-size:0.72rem;text-transform:uppercase;">Customers</div>
                 <div style="color:#f1f5f9;font-weight:600;">{int(row["Customers"]):,}</div></div>
            <div><div style="color:#64748b;font-size:0.72rem;text-transform:uppercase;">Avg Recency</div>
                 <div style="color:#f1f5f9;font-weight:600;">{row["Avg_Recency"]:.0f} days</div></div>
            <div><div style="color:#64748b;font-size:0.72rem;text-transform:uppercase;">Avg Frequency</div>
                 <div style="color:#f1f5f9;font-weight:600;">{row["Avg_Frequency"]:.1f} orders</div></div>
            <div><div style="color:#64748b;font-size:0.72rem;text-transform:uppercase;">Avg Spend</div>
                 <div style="color:#f1f5f9;font-weight:600;">£{row["Avg_Monetary"]:,.0f}</div></div>
            <div><div style="color:#64748b;font-size:0.72rem;text-transform:uppercase;">Total Revenue</div>
                 <div style="color:{color};font-weight:700;">£{row["Total_Revenue"]/1e3:,.1f}K</div></div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  PAGE: PRODUCT RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════
elif "Recommendations" in page:

    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🎯</div>
        <h3 class="section-title">Product Recommendation Engine</h3>
        <div class="section-line"></div>
    </div>
    <div class="info-box">
        💡 <b>How it works:</b> Enter any product name and our Item-Based Collaborative Filtering engine
        computes cosine similarity across all 2,941 products to find what customers most often buy together.
    </div>
    """, unsafe_allow_html=True)

    col_inp, col_cfg = st.columns([3, 1])
    with col_inp:
        product_input = st.text_input(
            "🔍 Search Product",
            placeholder="e.g.  WHITE HANGING HEART T-LIGHT HOLDER",
            help="Type a product name or keyword. Partial match supported."
        )
    with col_cfg:
        top_n = st.selectbox("Results", [3, 5, 10], index=1)

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        go_btn = st.button("🚀 Get Recommendations")

    if go_btn:
        if not product_input.strip():
            st.warning("⚠️ Please enter a product name.")
        else:
            query = product_input.strip().upper()
            matches = [p for p in item_sim.index if query == p.upper()]
            if not matches:
                matches = [p for p in item_sim.index if query in p.upper()]

            if not matches:
                st.error(f"❌ **'{product_input}'** not found. Try a different keyword.")
            else:
                product = matches[0]
                similar = (item_sim[product].drop(labels=[product])
                           .sort_values(ascending=False)
                           .head(top_n).reset_index())
                similar.columns = ["Product", "Score"]

                st.markdown(f"""
                <div style="margin:1.2rem 0 0.8rem 0;">
                    <div style="color:#64748b; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.05em;">Showing results for</div>
                    <div style="font-family:'Space Grotesk',sans-serif; font-size:1.3rem; font-weight:600; color:#a78bfa;">
                        📌 {product}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                rank_colors = ["#ffd700","#c0c0c0","#cd7f32","#6366f1","#6366f1",
                               "#6366f1","#6366f1","#6366f1","#6366f1","#6366f1"]

                for i, row in similar.iterrows():
                    score = row["Score"]
                    fill_w = int(score * 100)
                    rank_c = rank_colors[i] if i < len(rank_colors) else "#6366f1"
                    st.markdown(f"""
                    <div class="rec-card">
                        <div class="rec-rank" style="color:{rank_c};">#{i+1}</div>
                        <div class="rec-name">{row["Product"]}</div>
                        <div class="rec-score-bar">
                            <div class="rec-score-fill" style="width:{fill_w}%;"></div>
                        </div>
                        <div class="rec-pct">{score*100:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Similarity bar chart
                st.markdown("<br>", unsafe_allow_html=True)
                fig = go.Figure(go.Bar(
                    y=[p[:35]+"..." if len(p)>35 else p for p in similar["Product"]],
                    x=similar["Score"],
                    orientation="h",
                    marker=dict(
                        color=similar["Score"],
                        colorscale=[[0,"#3730a3"],[1,"#a78bfa"]],
                        showscale=False
                    ),
                    hovertemplate="<b>%{y}</b><br>Similarity: %{x:.4f}<extra></extra>"
                ))
                fig.update_layout(**PLOTLY_THEME, height=50+top_n*40,
                                  title=dict(text="Similarity Scores", font=dict(color="#94a3b8", size=13)))
                fig.update_yaxes(categoryorder="total ascending", tickfont=dict(size=9))
                st.plotly_chart(fig, use_container_width=True)

    # Product Catalog
    st.markdown("---")
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📋</div>
        <h3 class="section-title">Product Catalog</h3>
        <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    search = st.text_input("Filter catalog", placeholder="Type to search...", label_visibility="collapsed")
    filtered = [p for p in product_list if search.upper() in p.upper()] if search else product_list

    col_a, col_b, col_c = st.columns(3)
    third = len(filtered[:300]) // 3
    for col, chunk in zip([col_a, col_b, col_c],
                          [filtered[:third], filtered[third:2*third], filtered[2*third:300]]):
        with col:
            for p in chunk:
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06);
                            border-radius:6px; padding:0.4rem 0.8rem; margin:0.2rem 0;
                            font-size:0.8rem; color:#94a3b8; cursor:pointer;">
                    {p[:45]}{'...' if len(p)>45 else ''}
                </div>
                """, unsafe_allow_html=True)

    st.markdown(f"<div style='color:#475569;font-size:0.78rem;margin-top:0.5rem;'>Showing {min(300,len(filtered))} of {len(filtered)} products</div>",
                unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  PAGE: CUSTOMER SEGMENTATION
# ══════════════════════════════════════════════════════════════
elif "Segmentation" in page:

    st.markdown("""
    <div class="section-header">
        <div class="section-icon">👤</div>
        <h3 class="section-title">Customer Segment Predictor</h3>
        <div class="section-line"></div>
    </div>
    <div class="info-box">
        💡 <b>How it works:</b> Enter a customer's RFM values. The KMeans model (trained on 4,338 customers)
        assigns them to one of 4 business segments with personalised marketing strategies.
    </div>
    """, unsafe_allow_html=True)

    col_form, col_guide = st.columns([3, 2])

    with col_form:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        st.markdown("#### 📥 Enter Customer RFM Values")

        c1, c2, c3 = st.columns(3)
        with c1:
            recency = st.number_input("📅 Recency (days)", min_value=0, max_value=1000, value=30,
                                       help="Days since the customer's last purchase")
        with c2:
            frequency = st.number_input("🔁 Frequency (orders)", min_value=1, max_value=500, value=5,
                                         help="Total number of unique orders")
        with c3:
            monetary = st.number_input("💰 Monetary (£ total)", min_value=0.0, max_value=500000.0,
                                        value=250.0, step=10.0,
                                        help="Total amount spent by the customer")

        predict_btn = st.button("🔮 Predict Segment", type="primary")
        st.markdown("</div>", unsafe_allow_html=True)

        if predict_btn:
            with st.spinner("Analysing customer profile..."):
                time.sleep(0.4)
                X = np.array([[np.log1p(recency), np.log1p(frequency), np.log1p(monetary)]])
                X_scaled = scaler.transform(X)
                cluster_id = kmeans.predict(X_scaled)[0]
                segment    = label_map[cluster_id]
                cfg        = SEG_CONFIG[segment]

            st.markdown(f"""
            <div class="seg-result" style="background:{cfg['bg']}; border:2px solid {cfg['border']};">
                <span class="seg-result-icon">{cfg['icon']}</span>
                <div class="seg-result-title" style="color:{cfg['color']};">{segment} Customer</div>
                <p class="seg-result-desc">{cfg['desc']}</p>
                <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin-top:1rem;">
                    <div style="background:rgba(0,0,0,0.2); border-radius:10px; padding:0.8rem; text-align:center;">
                        <div style="color:#64748b;font-size:0.72rem;text-transform:uppercase;">Recency</div>
                        <div style="color:#f1f5f9;font-weight:700;font-size:1.2rem;">{recency}d</div>
                    </div>
                    <div style="background:rgba(0,0,0,0.2); border-radius:10px; padding:0.8rem; text-align:center;">
                        <div style="color:#64748b;font-size:0.72rem;text-transform:uppercase;">Frequency</div>
                        <div style="color:#f1f5f9;font-weight:700;font-size:1.2rem;">{frequency}</div>
                    </div>
                    <div style="background:rgba(0,0,0,0.2); border-radius:10px; padding:0.8rem; text-align:center;">
                        <div style="color:#64748b;font-size:0.72rem;text-transform:uppercase;">Monetary</div>
                        <div style="color:#f1f5f9;font-weight:700;font-size:1.2rem;">£{monetary:,.0f}</div>
                    </div>
                </div>
                <div style="margin-top:1.2rem;">
                    <div style="color:#64748b;font-size:0.8rem;margin-bottom:0.5rem;">RECOMMENDED STRATEGIES</div>
                    {''.join([f"<span class='strategy-tag'>{s}</span>" for s in cfg['strategies']])}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_guide:
        st.markdown("#### 🗺️ Segment Guide")
        for seg, cfg in SEG_CONFIG.items():
            rfm_seg = rfm_df[rfm_df["Segment"] == seg]
            count = len(rfm_seg)
            pct   = count / len(rfm_df) * 100
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1e2438,#1a1f35);
                        border:1px solid rgba(255,255,255,0.07); border-left:3px solid {cfg['color']};
                        border-radius:10px; padding:1rem 1.2rem; margin:0.5rem 0;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:600; color:#f1f5f9;">{cfg['icon']} {seg}</span>
                    <span style="color:{cfg['color']}; font-size:0.85rem; font-weight:600;">{pct:.1f}%</span>
                </div>
                <div style="color:#475569; font-size:0.78rem; margin-top:0.3rem;">{cfg['desc'][:80]}...</div>
                <div style="margin-top:0.5rem;">
                    <div style="height:4px; background:rgba(255,255,255,0.05); border-radius:2px; overflow:hidden;">
                        <div style="height:100%; width:{pct}%; background:{cfg['color']}; border-radius:2px;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Batch mode
    st.markdown("---")
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📊</div>
        <h3 class="section-title">RFM Segment Explorer</h3>
        <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    sample = rfm_df.sample(min(200, len(rfm_df)), random_state=42)
    fig = px.scatter(sample, x="Frequency", y="Monetary", color="Segment",
                     size="Monetary", hover_data=["CustomerID","Recency"],
                     color_discrete_map={s: SEG_CONFIG[s]["color"] for s in SEG_CONFIG},
                     title="Customer Segments: Frequency vs Monetary",
                     height=450,
                     labels={"Frequency":"Frequency (# Orders)","Monetary":"Monetary (£ Total Spend)"})
    fig.update_layout(**PLOTLY_THEME)
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════
#  PAGE: ANALYTICS
# ══════════════════════════════════════════════════════════════
elif "Analytics" in page:

    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📊</div>
        <h3 class="section-title">Deep Analytics</h3>
        <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🕐 Time Analysis", "🌍 Geo Analysis", "🧮 RFM Deep Dive"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
            dow = df.groupby("DayOfWeek")["TotalAmount"].sum().reindex(dow_order).reset_index()
            fig = go.Figure(go.Bar(
                x=dow["DayOfWeek"], y=dow["TotalAmount"],
                marker=dict(color=dow["TotalAmount"],
                            colorscale=[[0,"#1e3a5f"],[1,"#38bdf8"]], showscale=False),
                hovertemplate="<b>%{x}</b><br>Revenue: £%{y:,.0f}<extra></extra>"
            ))
            fig.update_layout(**PLOTLY_THEME, title="Revenue by Day of Week", height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            hour_df = df.groupby(df["InvoiceDate"].dt.hour)["TotalAmount"].sum().reset_index()
            hour_df.columns = ["Hour","Revenue"]
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=hour_df["Hour"], y=hour_df["Revenue"],
                mode="lines+markers", fill="tozeroy",
                fillcolor="rgba(52,211,153,0.1)",
                line=dict(color="#34d399", width=2),
                marker=dict(color="#34d399", size=7),
                hovertemplate="<b>%{x}:00</b><br>Revenue: £%{y:,.0f}<extra></extra>"
            ))
            fig.update_layout(**PLOTLY_THEME, title="Revenue by Hour of Day", height=300)
            st.plotly_chart(fig, use_container_width=True)

        monthly2 = df.groupby("YearMonth").agg(
            Revenue=("TotalAmount","sum"),
            Orders=("InvoiceNo","nunique"),
            Customers=("CustomerID","nunique")
        ).reset_index()
        fig = make_subplots(rows=1, cols=3,
                            subplot_titles=["Monthly Revenue","Monthly Orders","Monthly Customers"])
        for i, (col, color) in enumerate(zip(["Revenue","Orders","Customers"],
                                              ["#6366f1","#38bdf8","#34d399"])):
            fig.add_trace(go.Scatter(x=monthly2["YearMonth"], y=monthly2[col],
                                     mode="lines+markers", fill="tozeroy",
                                     fillcolor=f"rgba({','.join(str(int(c,16)) for c in [color[1:3],color[3:5],color[5:]])},0.1)",
                                     line=dict(color=color, width=2),
                                     marker=dict(color=color, size=5),
                                     showlegend=False), row=1, col=i+1)
        fig.update_layout(**PLOTLY_THEME, height=280, title="Monthly Trends Overview")
        fig.update_xaxes(tickangle=-40, tickfont=dict(size=8))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        country_agg = (df.groupby("Country")
                       .agg(Revenue=("TotalAmount","sum"),
                            Customers=("CustomerID","nunique"),
                            Orders=("InvoiceNo","nunique"))
                       .sort_values("Revenue", ascending=False)
                       .reset_index())

        fig = px.bar(country_agg.head(15), x="Country", y="Revenue",
                     color="Customers",
                     color_continuous_scale=["#1e3a5f","#6366f1","#a78bfa"],
                     title="Top 15 Countries by Revenue (colored by Unique Customers)",
                     height=380,
                     hover_data=["Orders","Customers"])
        fig.update_layout(**PLOTLY_THEME)
        fig.update_xaxes(tickangle=-30)
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(country_agg.head(8), values="Revenue", names="Country",
                         title="Revenue Share (Top 8)", hole=0.4, height=320)
            fig.update_layout(**PLOTLY_THEME, showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(country_agg.head(10), x="Customers", y="Country",
                         orientation="h", title="Customers by Country (Top 10)",
                         height=320,
                         color="Revenue",
                         color_continuous_scale=["#0c4a6e","#38bdf8"])
            fig.update_layout(**PLOTLY_THEME)
            fig.update_yaxes(categoryorder="total ascending")
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            fig = px.histogram(rfm_df, x="Recency", nbins=50, title="Recency Distribution",
                               color_discrete_sequence=["#6366f1"], height=280)
            fig.update_layout(**PLOTLY_THEME)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.histogram(rfm_df[rfm_df["Frequency"] <= rfm_df["Frequency"].quantile(0.99)],
                               x="Frequency", nbins=50, title="Frequency Distribution",
                               color_discrete_sequence=["#38bdf8"], height=280)
            fig.update_layout(**PLOTLY_THEME)
            st.plotly_chart(fig, use_container_width=True)

        # 3D RFM scatter
        sample3d = rfm_df.sample(min(500, len(rfm_df)), random_state=42)
        fig = px.scatter_3d(sample3d, x="Recency", y="Frequency", z="Monetary",
                            color="Segment",
                            color_discrete_map={s: SEG_CONFIG[s]["color"] for s in SEG_CONFIG},
                            opacity=0.75, height=520,
                            title="3D RFM Customer Clusters",
                            labels={"Recency":"Recency (days)","Frequency":"Frequency","Monetary":"Monetary (£)"})
        fig.update_layout(**PLOTLY_THEME)
        st.plotly_chart(fig, use_container_width=True)

        # Box plots per segment
        fig = make_subplots(rows=1, cols=3, subplot_titles=["Recency","Frequency","Monetary"])
        seg_order = ["High-Value","Regular","Occasional","At-Risk"]
        for i, feat in enumerate(["Recency","Frequency","Monetary"]):
            for seg in seg_order:
                data = rfm_df[rfm_df["Segment"] == seg][feat]
                fig.add_trace(go.Box(y=data, name=seg,
                                     marker_color=SEG_CONFIG[seg]["color"],
                                     showlegend=(i == 0),
                                     boxmean=True), row=1, col=i+1)
        fig.update_layout(**PLOTLY_THEME, height=380, title="RFM Distribution per Segment")
        st.plotly_chart(fig, use_container_width=True)
