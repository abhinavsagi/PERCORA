
import math
import requests
import streamlit as st

st.set_page_config(
    page_title="PECORA — Investor Decision Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# STYLE
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:Inter,sans-serif}
.stApp{background:#f7faf9}
.block-container{max-width:1450px;padding:1rem 2rem 3rem}
#MainMenu,footer,header{visibility:hidden}

.navbar{background:#fff;border:1px solid #e3ebe8;border-radius:20px;padding:11px 16px;margin-bottom:22px;box-shadow:0 5px 20px rgba(15,35,30,.04)}
.brand{font-size:24px;font-weight:800;color:#101b2b;letter-spacing:-1px}
.brand span{color:#0aa77d}
.nav-note{font-size:12px;color:#7b8795;font-weight:600}

.hero,.panel,.info-card,.metric-card,.decision-box,.learn-card,.journal-card{
 background:#fff;border:1px solid #e3ebe8;border-radius:22px;box-shadow:0 7px 25px rgba(15,35,30,.035)
}
.hero{padding:38px 42px}
.eyebrow{color:#0aa77d;font-size:11px;font-weight:800;letter-spacing:2.5px;text-transform:uppercase}
.logo{font-size:70px;line-height:.95;font-weight:800;letter-spacing:-5px;color:#101b2b}
.logo span{color:#0aa77d}
.tagline{font-size:28px;font-weight:800;color:#152235;margin-top:12px}
.copy{font-size:14px;line-height:1.65;color:#687486;max-width:700px}
.status{display:inline-flex;gap:7px;align-items:center;background:#e9f8f3;color:#087b5d;border-radius:999px;padding:7px 12px;font-size:11px;font-weight:700}
.dot{width:8px;height:8px;border-radius:50%;background:#0aa77d}

.illustration{height:270px;border-radius:22px;background:linear-gradient(145deg,#eefaf6,#fff);border:1px solid #dfece7;position:relative;overflow:hidden}
.illus-title{position:absolute;top:22px;left:24px;font-size:13px;font-weight:800;color:#263346}
.bar{position:absolute;bottom:40px;width:42px;background:#d7f2e8;border-radius:8px 8px 0 0}
.b1{left:35px;height:48px}.b2{left:88px;height:78px}.b3{left:141px;height:110px}.b4{left:194px;height:145px}.b5{left:247px;height:185px}
.chartline{position:absolute;left:30px;top:60px;width:280px;height:145px}
.chartline svg{width:100%;height:100%}
.illus-card{position:absolute;right:17px;bottom:17px;width:150px;background:white;border:1px solid #e0e9e5;border-radius:15px;padding:12px;box-shadow:0 8px 25px rgba(20,50,40,.08)}
.illus-card b{font-size:12px;color:#142135}.illus-card p{margin:5px 0 0;font-size:10px;color:#6c7786;line-height:1.45}

.info-card{padding:21px;min-height:145px}
.info-label{font-size:10px;font-weight:800;letter-spacing:1.5px;color:#0aa77d;text-transform:uppercase}
.info-title{font-size:19px;font-weight:800;color:#172337;margin:7px 0}
.info-text{font-size:13px;color:#697586;line-height:1.55}

.section-title{font-size:24px;font-weight:800;color:#152235;margin:8px 0 4px}
.section-sub{font-size:13px;color:#6d7888;margin-bottom:16px}
.panel{padding:25px}
.metric-card{padding:18px}
.metric-label{font-size:10px;color:#718092;font-weight:800;text-transform:uppercase;letter-spacing:.6px}
.metric-value{font-size:25px;font-weight:800;color:#172337;margin-top:5px}
.metric-good{color:#0a9a73}.metric-warn{color:#d9822b}
.small-note{font-size:11px;color:#84909e}

.decision-box{padding:25px}
.nav-active{background:#0aa77d;color:white!important;border-radius:12px}
.page-title{font-size:36px;font-weight:800;color:#152235;letter-spacing:-1px}
.page-sub{font-size:14px;color:#6c7786;max-width:780px;line-height:1.6}

div.stButton>button{width:100%;border-radius:14px;border:1px solid #dce6e2;background:#fff;color:#172337;font-weight:700;min-height:48px}
div.stButton>button:hover{border-color:#0aa77d;color:#087b5d}
button[kind="primary"]{background:#0aa77d!important;border-color:#0aa77d!important;color:white!important}
section[data-testid="stSidebar"]{background:#fff;border-right:1px solid #e5ece9}
section[data-testid="stSidebar"] .block-container{padding:1.2rem 1rem}
hr{border:none;border-top:1px solid #e8efed;margin:24px 0}

.sim-row{background:#fff;border:1px solid #e3ebe8;border-radius:16px;padding:18px}
.sim-head{font-weight:800;color:#172337;font-size:16px}
.sim-num{font-size:23px;font-weight:800;color:#0a9a73;margin-top:6px}

.learn-card{padding:22px;min-height:170px}
.learn-title{font-size:18px;font-weight:800;color:#172337;margin:7px 0}
.learn-text{font-size:13px;line-height:1.55;color:#687486}

.journal-card{padding:18px;margin-bottom:10px}
.badge{display:inline-block;padding:5px 9px;border-radius:999px;background:#edf8f4;color:#087b5d;font-size:10px;font-weight:800}
</style>
""", unsafe_allow_html=True)

# =========================================================
# STATE
# =========================================================
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "decision" not in st.session_state:
    st.session_state.decision = "Continue SIP"
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "journal" not in st.session_state:
    st.session_state.journal = []

API_URL = "http://127.0.0.1:8000"

# =========================================================
# SIDEBAR — common investor context
# =========================================================
with st.sidebar:
    st.markdown("### ◉ Investor context")
    name = st.text_input("Name", "Abhinav")
    age = st.number_input("Age", 18, 80, 20)
    goal = st.selectbox("Goal", ["Wealth creation","Home","Education","Retirement","Emergency corpus"])
    goal_amount = st.number_input("Goal amount (₹)", 10000, 100000000, 1500000, 50000)
    corpus = st.number_input("Current corpus (₹)", 0, 100000000, 300000, 10000)
    sip = st.number_input("Monthly SIP (₹)", 500, 1000000, 5000, 500)
    horizon = st.number_input("Investment horizon (years)", 1, 40, 6)
    risk = st.selectbox("Risk profile", ["Conservative","Moderate","Aggressive"])
    st.markdown("---")
    st.caption("PECORA explains the decision. It does not block or execute investments.")

# =========================================================
# NAV
# =========================================================
pages = ["Home","Market Analysis","Decision Simulator","Journal","Learn","About"]
nav_cols = st.columns([1.3,1,1.2,.85,.75,.75,1.25])
for i, p in enumerate(pages):
    with nav_cols[i]:
        if st.button(("⌂ " if p=="Home" else "") + p, key="nav_"+p, type="primary" if st.session_state.page==p else "secondary"):
            st.session_state.page = p
            st.rerun()
    if i == len(pages)-1:
        with nav_cols[i]:
            st.markdown('<div class="nav-note" style="text-align:right;padding-top:14px;">● Prototype Mode</div>', unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================
annual_return = 0.10
months = max(1, horizon*12)
r = annual_return/12

def fv(monthly, n):
    if r == 0:
        return corpus + monthly*n
    return corpus*(1+r)**n + monthly*(((1+r)**n-1)/r)

def scenario_values():
    cont = fv(sip, months)
    pause = corpus*(1+r)**months + (sip*(((1+r)**(months-min(6,months))-1)/r) if months>min(6,months) else 0)
    stop = corpus*(1+r)**months
    return cont, pause, stop

def backend_analyze(decision):
    payload = {
        "name":name,"age":age,"goal":goal,"goal_amount":goal_amount,
        "current_corpus":corpus,"monthly_sip":sip,"horizon_years":horizon,
        "risk_profile":risk,"decision":decision,
        "market_move_pct":-4.8,"portfolio_move_pct":-4.2
    }
    try:
        resp = requests.post(API_URL+"/analyze", json=payload, timeout=4)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None

# =========================================================
# HOME
# =========================================================
def render_home():
    c1,c2=st.columns([1.5,1],gap="large")
    with c1:
        st.markdown("""
        <div class="hero">
        <div class="eyebrow">Decision intelligence for investors</div>
        <div class="logo">PECO<span>RA</span></div>
        <div class="tagline">Think beyond the moment.</div>
        <div class="copy">An AI-powered decision-support layer that helps investors understand the personal consequences of a SIP decision before they act.</div>
        <div class="status" style="margin-top:18px"><span class="dot"></span> Investor context loaded</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="illustration">
        <div class="illus-title">Your decision → your future path</div>
        <div class="bar b1"></div><div class="bar b2"></div><div class="bar b3"></div><div class="bar b4"></div><div class="bar b5"></div>
        <div class="chartline"><svg viewBox="0 0 280 145" preserveAspectRatio="none"><path d="M5,112 C35,104 43,82 68,90 C94,99 103,65 128,72 C152,80 164,40 187,48 C211,56 216,23 239,31 C260,39 270,16 275,8" fill="none" stroke="#0aa77d" stroke-width="5" stroke-linecap="round"/><circle cx="275" cy="8" r="6" fill="#0aa77d"/></svg></div>
        <div class="illus-card"><b>Better decisions.</b><p>Understand the impact before you pause, reduce or stop.</p></div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    a,b,c=st.columns(3)
    cards=[
        ("Problem","Information ≠ context","Investors can see market data, but often lack personalized context at decision time."),
        ("Intervention","Pause → Understand","PECORA compares the potential long-term impact of different SIP actions."),
        ("Control","You decide","PECORA explains. It does not block, execute, or guarantee an investment outcome.")
    ]
    for col,(lab,title,txt) in zip([a,b,c],cards):
        with col:
            st.markdown(f'<div class="info-card"><div class="info-label">{lab}</div><div class="info-title">{title}</div><div class="info-text">{txt}</div></div>',unsafe_allow_html=True)
    st.markdown("<div style='height:18px'></div>",unsafe_allow_html=True)
    x,y=st.columns([1,1.15])
    progress=min(corpus/goal_amount,1) if goal_amount else 0
    with x:
        st.markdown(f'<div class="metric-card"><b style="font-size:18px">◎ Goal progress</b><div style="height:10px;background:#e8efed;border-radius:20px;margin:15px 0 9px"><div style="height:10px;width:{progress*100:.1f}%;background:#0aa77d;border-radius:20px"></div></div><span class="small-note">₹{corpus:,.0f} / ₹{goal_amount:,.0f} · {horizon} years remaining</span></div>',unsafe_allow_html=True)
    with y:
        st.markdown('<div class="metric-card"><b style="font-size:18px">⌁ Market snapshot</b><div style="display:flex;gap:10px;margin-top:13px"><div style="flex:1;background:#f7faf9;border-radius:12px;padding:11px"><span class="metric-label">NIFTY 50</span><div class="metric-value">24,872</div><span class="small-note" style="color:#0a9a73">▲ +0.68%</span></div><div style="flex:1;background:#f7faf9;border-radius:12px;padding:11px"><span class="metric-label">SENSEX</span><div class="metric-value">81,148</div><span class="small-note" style="color:#0a9a73">▲ +0.71%</span></div><div style="flex:1;background:#f7faf9;border-radius:12px;padding:11px"><span class="metric-label">USD/INR</span><div class="metric-value">83.24</div><span class="small-note">Latest available</span></div></div></div>',unsafe_allow_html=True)

    st.markdown("<hr>",unsafe_allow_html=True)
    st.markdown('<div class="section-title">What would you like to do?</div><div class="section-sub">Choose the SIP action you are considering. PECORA will compare its potential long-term impact.</div>',unsafe_allow_html=True)
    d1,d2,d3=st.columns(3)
    for col,label,desc,icon in [(d1,"Continue SIP","Keep current amount","▶"),(d2,"Pause SIP","Temporarily stop","Ⅱ"),(d3,"Stop SIP","Stop future contributions","■")]:
        with col:
            if st.button(f"{icon}  {label}\n{desc}",key="home_"+label):
                st.session_state.decision=label
                st.session_state.page="Decision Simulator"
                st.rerun()
    st.markdown("<div style='height:15px'></div>",unsafe_allow_html=True)
    if st.button("Open Decision Simulator →", type="primary", use_container_width=True):
        st.session_state.page="Decision Simulator"
        st.rerun()

# =========================================================
# MARKET
# =========================================================
def render_market():
    st.markdown('<div class="eyebrow">Market context</div><div class="page-title">Market Analysis</div><div class="page-sub">A clean market-context layer for PECORA. This first frontend version uses clearly labeled illustrative values; live feeds can be connected later through the backend.</div>',unsafe_allow_html=True)
    st.markdown("<div style='height:20px'></div>",unsafe_allow_html=True)
    cols=st.columns(4)
    data=[("NIFTY 50","24,872","+0.68%"),("SENSEX","81,148","+0.71%"),("USD/INR","83.24","-0.12%"),("Market volatility","Moderate","12.8%")]
    for col,(a,b,c) in zip(cols,data):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-label">{a}</div><div class="metric-value">{b}</div><div class="small-note" style="color:#0a9a73">{c}</div></div>',unsafe_allow_html=True)
    st.markdown("<div style='height:18px'></div>",unsafe_allow_html=True)
    left,right=st.columns([1.5,1])
    with left:
        st.markdown('<div class="panel"><b style="font-size:18px">NIFTY 50 — illustrative intraday path</b>',unsafe_allow_html=True)
        # Native Streamlit chart, no backend required
        import pandas as pd
        base=24800
        vals=[base+40,base+95,base+70,base+130,base+180,base+150,base+220,base+195,base+260,base+310]
        chart=pd.DataFrame({"NIFTY 50":vals})
        st.line_chart(chart, height=300)
        st.markdown('<span class="small-note">Demo visualization — not a live trading feed.</span></div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><b style="font-size:18px">What this means</b><p class="copy" style="margin-top:12px">A market move alone does not tell an investor what action to take. PECORA combines market movement with portfolio, goal, risk and time horizon before presenting a decision context.</p><hr><b>Investor context</b><p class="small-note">Goal: '+goal+'<br>Horizon: '+str(horizon)+' years<br>Risk: '+risk+'<br>Monthly SIP: ₹'+f'{sip:,.0f}'+'</p></div>',unsafe_allow_html=True)

# =========================================================
# SIMULATOR
# =========================================================
def render_simulator():
    st.markdown('<div class="eyebrow">Decision intervention</div><div class="page-title">Decision Simulator</div><div class="page-sub">This is the core PECORA experience: compare the choices before you finalize a SIP action.</div>',unsafe_allow_html=True)
    st.markdown("<div style='height:20px'></div>",unsafe_allow_html=True)
    d1,d2,d3=st.columns(3)
    for col,label,desc,icon in [(d1,"Continue SIP","Keep current SIP","▶"),(d2,"Pause SIP","Pause for 6 months","Ⅱ"),(d3,"Stop SIP","Stop future SIPs","■")]:
        with col:
            if st.button(f"{icon}  {label}\n{desc}",key="sim_"+label):
                st.session_state.decision=label
                st.session_state.analysis_result=None
                st.rerun()
    decision=st.session_state.decision
    cont,pause,stop=scenario_values()
    vals={"Continue SIP":cont,"Pause SIP":pause,"Stop SIP":stop}
    selected=vals[decision]
    gap=max(goal_amount-selected,0)
    st.markdown("<div style='height:20px'></div>",unsafe_allow_html=True)
    st.markdown(f'<div class="decision-box"><div class="eyebrow">Selected action</div><div style="font-size:27px;font-weight:800;color:#152235">{decision}</div><div class="copy">PECORA is showing the potential long-term consequence of this choice using the current investor profile.</div></div>',unsafe_allow_html=True)
    st.markdown("<div style='height:14px'></div>",unsafe_allow_html=True)
    a,b,c=st.columns(3)
    for col,label,value,note,cls in [
        (a,"Projected corpus",f"₹{selected:,.0f}","Illustrative 10% annual return", "metric-good"),
        (b,"Goal gap",f"₹{gap:,.0f}","Target − projected corpus","metric-warn"),
        (c,"Current SIP",f"₹{sip:,.0f}","Monthly contribution","")
    ]:
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value {cls}">{value}</div><div class="small-note">{note}</div></div>',unsafe_allow_html=True)
    st.markdown("<div style='height:18px'></div>",unsafe_allow_html=True)
    st.markdown('<div class="section-title">Side-by-side comparison</div><div class="section-sub">The point is not to tell you what to do. It is to make the trade-off visible.</div>',unsafe_allow_html=True)
    rows=[("Continue SIP",cont),("Pause SIP",pause),("Stop SIP",stop)]
    for label,val in rows:
        gap2=max(goal_amount-val,0)
        pct=min(val/goal_amount,1) if goal_amount else 0
        st.markdown(f'<div class="sim-row" style="margin-bottom:9px"><div style="display:flex;justify-content:space-between"><span class="sim-head">{label}</span><span class="badge">{pct*100:.0f}% of target</span></div><div class="sim-num">₹{val:,.0f}</div><div class="small-note">Illustrative goal gap: ₹{gap2:,.0f}</div></div>',unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>",unsafe_allow_html=True)
    if st.button("Analyze My Decision →",key="sim_analyze",type="primary",use_container_width=True):
        result=backend_analyze(decision)
        if result:
            st.session_state.analysis_result=result
            st.session_state.journal.insert(0,{"date":"05 Oct 2026","decision":decision,"market":"-4.8%","portfolio":"-4.2%","stress":result["decision_stress_score"],"goal_prob":result["goal_probability"]})
        else:
            st.session_state.analysis_result={"offline":True}
    result=st.session_state.analysis_result
    if result:
        st.markdown("<div style='height:16px'></div>",unsafe_allow_html=True)
        if result.get("offline"):
            st.warning("Backend is not connected. The comparison above still works locally. Start FastAPI to enable the AI intervention.")
        else:
            r1,r2,r3=st.columns(3)
            with r1: st.metric("Decision Stress",f"{result['decision_stress_score']:.0f}/100")
            with r2: st.metric("Goal Probability",f"{result['goal_probability']*100:.1f}%")
            with r3: st.metric("AI Confidence",f"{result['ai_confidence']*100:.0f}%")
            st.success(result["explanation"])

# =========================================================
# JOURNAL
# =========================================================
def render_journal():
    st.markdown('<div class="eyebrow">Decision history</div><div class="page-title">Journal</div><div class="page-sub">A simple record of the decisions you explored with PECORA. This becomes the behavioral-memory layer later.</div>',unsafe_allow_html=True)
    st.markdown("<div style='height:20px'></div>",unsafe_allow_html=True)
    if not st.session_state.journal:
        st.markdown('<div class="panel" style="text-align:center;padding:55px"><div style="font-size:40px">▤</div><h3>No decisions recorded yet</h3><p class="small-note">Go to Decision Simulator and analyze a SIP decision. PECORA will add it here.</p></div>',unsafe_allow_html=True)
    else:
        for item in st.session_state.journal:
            st.markdown(f'<div class="journal-card"><div style="display:flex;justify-content:space-between"><b>{item["decision"]}</b><span class="badge">{item["date"]}</span></div><div class="small-note" style="margin-top:9px">Market {item["market"]} · Portfolio {item["portfolio"]} · Stress {item["stress"]:.0f}/100 · Goal probability {item["goal_prob"]*100:.1f}%</div></div>',unsafe_allow_html=True)
    if st.session_state.journal and st.button("Clear Journal"):
        st.session_state.journal=[]
        st.rerun()

# =========================================================
# LEARN
# =========================================================
def render_learn():
    st.markdown('<div class="eyebrow">Financial intelligence</div><div class="page-title">Learn</div><div class="page-sub">Short explanations that help an investor understand the context behind a SIP decision.</div>',unsafe_allow_html=True)
    topics=[
        ("What is a SIP?","A Systematic Investment Plan invests a fixed amount at regular intervals. It creates a disciplined contribution path rather than relying on one large entry."),
        ("Why do markets fall?","Prices can move because of earnings, interest rates, macroeconomic conditions, news, liquidity and investor expectations. A short-term fall does not by itself define a long-term goal."),
        ("SIP during volatility","A falling market can change portfolio value in the short run while future SIP contributions continue. The relevant question is how the move interacts with your goal and horizon."),
        ("Compounding","Returns can themselves generate future returns when invested. Time and continued contributions can therefore materially affect a long-term corpus."),
        ("Risk vs return","Higher expected return generally comes with higher uncertainty. PECORA uses the investor's stated risk profile as context rather than treating one return assumption as universally suitable."),
        ("Goal-based investing","A portfolio should be evaluated against the purpose, amount and time horizon it is meant to support—not only today's market movement.")
    ]
    for i in range(0,len(topics),2):
        a,b=st.columns(2)
        for col,(title,txt) in zip([a,b],topics[i:i+2]):
            with col:
                st.markdown(f'<div class="learn-card" style="margin-bottom:14px"><div class="info-label">Learn</div><div class="learn-title">{title}</div><div class="learn-text">{txt}</div></div>',unsafe_allow_html=True)

# =========================================================
# ABOUT
# =========================================================
def render_about():
    st.markdown('<div class="eyebrow">Product</div><div class="page-title">About PECORA</div><div class="page-sub">Think beyond the moment.</div>',unsafe_allow_html=True)
    st.markdown("<div style='height:20px'></div>",unsafe_allow_html=True)
    a,b=st.columns([1.3,1])
    with a:
        st.markdown('<div class="panel"><div class="logo" style="font-size:58px">PECO<span>RA</span></div><h3>Decision intelligence for investors</h3><p class="copy">PECORA is designed around one intervention moment: when an investor is about to pause or stop a SIP. Instead of simply confirming the action, PECORA surfaces the potential consequences in the context of the investor’s goal, risk profile and time horizon.</p><hr><b>Core principle</b><p class="copy">Existing platforms provide information. PECORA adds personalized context at decision time.</p></div>',unsafe_allow_html=True)
    with b:
        st.markdown('<div class="panel"><b style="font-size:18px">How it works</b><ol class="copy"><li>Understand investor context</li><li>Detect a meaningful SIP decision</li><li>Calculate scenario impact</li><li>Explain the trade-off</li><li>Let the investor decide</li></ol><hr><b>User control</b><p class="copy">PECORA never blocks, executes or guarantees an investment outcome.</p></div>',unsafe_allow_html=True)
    st.markdown("<div style='height:14px'></div>",unsafe_allow_html=True)
    a,b,c=st.columns(3)
    for col,title,txt in [(a,"Quantitative engine","SIP projection, goal gap, scenario comparison and probabilistic extensions."),(b,"AI layer","Context-aware explanation that translates analytical outputs into understandable language."),(c,"Future scope","Live market data, portfolio integrations, stronger models, backtesting and suitability controls.")]:
        with col:
            st.markdown(f'<div class="info-card"><div class="info-label">PECORA</div><div class="info-title">{title}</div><div class="info-text">{txt}</div></div>',unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;margin-top:28px;color:#8a95a1;font-size:11px'>PECORA • STARKX • Abhinav Sagi</div>",unsafe_allow_html=True)

# =========================================================
# ROUTER
# =========================================================
if st.session_state.page=="Home":
    render_home()
elif st.session_state.page=="Market Analysis":
    render_market()
elif st.session_state.page=="Decision Simulator":
    render_simulator()
elif st.session_state.page=="Journal":
    render_journal()
elif st.session_state.page=="Learn":
    render_learn()
else:
    render_about()
