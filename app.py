"""
SaaS AI Replacement Calculator.

Interactive tool that compares the cost of SaaS AI subscriptions
vs deploying equivalent capabilities on local infrastructure.

Shows: monthly/annual costs, break-even point, 3-year TCO,
and architecture comparison.
"""
import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="SaaS AI Replacement Calculator",
    page_icon="💰",
    layout="wide",
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .subtitle {
        font-size: 1rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #6c757d;
        margin-top: 0.3rem;
    }
    .savings-positive {
        color: #0f9b0f;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .savings-negative {
        color: #dc3545;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .comparison-header {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e0e0e0;
    }
    .architecture-box {
        background: #f0f4f8;
        border-radius: 10px;
        padding: 1.5rem;
        font-family: monospace;
        font-size: 0.85rem;
        line-height: 1.6;
    }
    .saas-box {
        border-left: 4px solid #dc3545;
    }
    .local-box {
        border-left: 4px solid #0f9b0f;
    }
    .privacy-warning {
        background: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .privacy-safe {
        background: #d4edda;
        border: 1px solid #28a745;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SAAS PRICING DATABASE
# ============================================================
SAAS_TOOLS = {
    "ChatGPT Team": {
        "monthly_per_user": 25,
        "description": "OpenAI's business tier",
        "category": "General AI Assistant",
        "data_risk": "Prompts processed on OpenAI servers",
    },
    "ChatGPT Enterprise": {
        "monthly_per_user": 60,
        "description": "OpenAI enterprise with SOC2",
        "category": "General AI Assistant",
        "data_risk": "Prompts processed on OpenAI servers (SOC2 compliant)",
    },
    "GitHub Copilot Business": {
        "monthly_per_user": 19,
        "description": "AI code completion",
        "category": "Code Assistant",
        "data_risk": "Code sent to GitHub/Microsoft servers",
    },
    "Jasper Business": {
        "monthly_per_user": 49,
        "description": "AI content generation",
        "category": "Content Generation",
        "data_risk": "Content data processed externally",
    },
    "Intercom Fin AI": {
        "monthly_per_user": 99,
        "description": "AI customer support agent",
        "category": "Customer Support",
        "data_risk": "Customer conversations on Intercom servers",
    },
    "Copy.ai": {
        "monthly_per_user": 36,
        "description": "AI marketing copy",
        "category": "Content Generation",
        "data_risk": "Marketing data processed externally",
    },
    "Custom OpenAI API": {
        "monthly_per_user": 80,
        "description": "Direct API usage (estimated per user)",
        "category": "API Integration",
        "data_risk": "All prompts and data sent to OpenAI",
    },
}

VPS_OPTIONS = {
    "Hetzner CX41 (8 vCPU, 16GB)": {"monthly": 15, "gpu": False},
    "Hetzner CCX33 (8 vCPU, 32GB)": {"monthly": 35, "gpu": False},
    "Hetzner CCX53 (16 vCPU, 64GB)": {"monthly": 70, "gpu": False},
    "Hetzner GPU (RTX 3090)": {"monthly": 180, "gpu": True},
    "OVH GPU (A100 40GB)": {"monthly": 350, "gpu": True},
    "On-premise (existing hardware)": {"monthly": 0, "gpu": False},
    "AWS g5.xlarge (A10G)": {"monthly": 550, "gpu": True},
}

# ============================================================
# HEADER
# ============================================================
st.markdown('<p class="main-title">💰 SaaS AI → Local Infrastructure</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">'
    'Calculate how much you save by replacing SaaS AI tools with private, self-hosted alternatives'
    '</p>',
    unsafe_allow_html=True,
)

# ============================================================
# INPUT SECTION
# ============================================================
st.markdown("---")
col_saas, col_local = st.columns(2)

with col_saas:
    st.markdown('<p class="comparison-header">☁️ Current SaaS Setup</p>', unsafe_allow_html=True)

    selected_tools = st.multiselect(
        "Which AI tools are you currently using?",
        options=list(SAAS_TOOLS.keys()),
        default=["ChatGPT Team", "Jasper Business"],
    )

    num_users = st.slider("Number of users", min_value=1, max_value=200, value=15)

    custom_monthly = st.number_input(
        "Additional monthly AI costs ($)",
        min_value=0,
        value=0,
        step=50,
        help="Include any other AI subscriptions not listed above",
    )

with col_local:
    st.markdown('<p class="comparison-header">🔒 Local Alternative</p>', unsafe_allow_html=True)

    selected_vps = st.selectbox(
        "Infrastructure option",
        options=list(VPS_OPTIONS.keys()),
        index=2,
    )

    setup_cost = st.number_input(
        "One-time setup cost ($)",
        min_value=0,
        value=5000,
        step=500,
        help="Professional setup: LLM deployment, RAG pipeline, UI, documentation",
    )

    maintenance_monthly = st.number_input(
        "Monthly maintenance ($)",
        min_value=0,
        value=500,
        step=100,
        help="Ongoing support, model updates, monitoring",
    )

# ============================================================
# CALCULATIONS
# ============================================================
# SaaS costs
saas_monthly = sum(
    SAAS_TOOLS[tool]["monthly_per_user"] * num_users
    for tool in selected_tools
) + custom_monthly
saas_annual = saas_monthly * 12
saas_3year = saas_annual * 3

# Local costs
vps_monthly = VPS_OPTIONS[selected_vps]["monthly"]
local_monthly = vps_monthly + maintenance_monthly
local_annual = local_monthly * 12 + setup_cost  # Setup cost in year 1
local_3year = local_monthly * 36 + setup_cost

# Savings
monthly_savings = saas_monthly - local_monthly
annual_savings = saas_annual - local_annual
savings_3year = saas_3year - local_3year

# Break-even
if monthly_savings > 0:
    breakeven_months = setup_cost / monthly_savings if monthly_savings > 0 else float('inf')
else:
    breakeven_months = float('inf')

# ============================================================
# RESULTS
# ============================================================
st.markdown("---")
st.markdown("## 📊 Cost Comparison")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">${saas_monthly:,.0f}</div>
        <div class="metric-label">SaaS Monthly Cost</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">${local_monthly:,.0f}</div>
        <div class="metric-label">Local Monthly Cost</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    savings_class = "savings-positive" if savings_3year > 0 else "savings-negative"
    st.markdown(f"""
    <div class="metric-card">
        <div class="{savings_class}">${savings_3year:,.0f}</div>
        <div class="metric-label">3-Year Savings</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    if breakeven_months < float('inf') and breakeven_months > 0:
        breakeven_display = f"{breakeven_months:.1f} mo"
    else:
        breakeven_display = "N/A"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{breakeven_display}</div>
        <div class="metric-label">Break-Even Point</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# COST TIMELINE CHART
# ============================================================
st.markdown("### 📈 Cumulative Cost Over 36 Months")

import pandas as pd

months = list(range(0, 37))
saas_cumulative = [saas_monthly * m for m in months]
local_cumulative = [setup_cost + local_monthly * m for m in months]

chart_data = pd.DataFrame({
    "Month": months,
    "SaaS AI (recurring)": saas_cumulative,
    "Local Infrastructure": local_cumulative,
})
chart_data = chart_data.set_index("Month")
st.line_chart(chart_data, use_container_width=True)

# ============================================================
# DETAILED BREAKDOWN
# ============================================================
st.markdown("---")
col_detail_saas, col_detail_local = st.columns(2)

with col_detail_saas:
    st.markdown("### ☁️ SaaS Cost Breakdown")
    if selected_tools:
        breakdown_data = []
        for tool in selected_tools:
            tool_data = SAAS_TOOLS[tool]
            monthly = tool_data["monthly_per_user"] * num_users
            breakdown_data.append({
                "Tool": tool,
                "Per User": f"${tool_data['monthly_per_user']}",
                "Users": num_users,
                "Monthly": f"${monthly:,}",
                "Annual": f"${monthly * 12:,}",
            })
        st.table(pd.DataFrame(breakdown_data))

    if custom_monthly > 0:
        st.info(f"Additional costs: ${custom_monthly:,}/month")

    st.markdown(f"**Total annual SaaS cost: ${saas_annual:,.0f}**")

with col_detail_local:
    st.markdown("### 🔒 Local Infrastructure Breakdown")
    local_breakdown = [
        {"Item": "One-time setup", "Cost": f"${setup_cost:,}", "Frequency": "Once"},
        {"Item": f"VPS ({selected_vps.split('(')[0].strip()})", "Cost": f"${vps_monthly:,}", "Frequency": "Monthly"},
        {"Item": "Maintenance & support", "Cost": f"${maintenance_monthly:,}", "Frequency": "Monthly"},
    ]
    st.table(pd.DataFrame(local_breakdown))
    st.markdown(f"**Year 1 total: ${local_annual:,.0f}**")
    st.markdown(f"**Year 2+ annual: ${local_monthly * 12:,.0f}**")

# ============================================================
# ARCHITECTURE COMPARISON
# ============================================================
st.markdown("---")
st.markdown("## 🏗️ Architecture Comparison")

col_arch_saas, col_arch_local = st.columns(2)

with col_arch_saas:
    st.markdown("""
    <div class="architecture-box saas-box">
    <strong>☁️ SaaS Architecture</strong><br><br>
    Your App → Internet → OpenAI/SaaS API<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    &nbsp;&nbsp;&nbsp;&nbsp;Third-party servers<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Response back<br><br>
    ⚠️ Data processed externally<br>
    ⚠️ Vendor controls pricing<br>
    ⚠️ Rate limits apply<br>
    ⚠️ API changes break your app
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="privacy-warning">
        <strong>⚠️ Data Privacy Risk</strong><br>
        Every query sends your data to external servers.
        Compliance with GDPR, HIPAA, or internal policies
        may be compromised.
    </div>
    """, unsafe_allow_html=True)

with col_arch_local:
    st.markdown("""
    <div class="architecture-box local-box">
    <strong>🔒 Local Architecture</strong><br><br>
    Your App → Your Server → Ollama/LLM<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    &nbsp;&nbsp;&nbsp;&nbsp;ChromaDB (your disk)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Response (local)<br><br>
    ✅ All data stays on your server<br>
    ✅ Fixed cost, unlimited queries<br>
    ✅ No rate limits<br>
    ✅ Full control over updates
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="privacy-safe">
        <strong>✅ Data Privacy Guaranteed</strong><br>
        Zero data leaves your infrastructure.
        GDPR, HIPAA, and internal compliance
        satisfied by architecture.
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# WHAT YOU GET
# ============================================================
st.markdown("---")
st.markdown("## 📦 What Local Deployment Includes")

col_inc1, col_inc2, col_inc3 = st.columns(3)

with col_inc1:
    st.markdown("""
    **Infrastructure**
    - Ollama + Llama 3 / Mistral
    - ChromaDB vector store
    - Docker containerization
    - VPS or on-premise setup
    """)

with col_inc2:
    st.markdown("""
    **Application**
    - RAG pipeline over your docs
    - Web-based chat interface
    - API endpoints for integration
    - Custom system prompts
    """)

with col_inc3:
    st.markdown("""
    **Operations**
    - Deployment documentation
    - Monitoring setup
    - Model update procedures
    - Optional maintenance retainer
    """)

# ============================================================
