"""
app.py — Global Job Market Analysis System
Enterprise Edition: Streamlit + SQLite + Python Analytics ML
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import init_db, get_connection, DB_PATH
from ml.analytics import (predict_salary, forecast_demand, cost_adjusted_salary,
                           skill_gap_score, salary_benchmark, top_paying_roles,
                           company_insights, summary_stats)

# ── INIT ───────────────────────────────────────────────────────────────────────
init_db()

st.set_page_config(
    page_title="Global Job Market Analytics",
    page_icon="🌍", layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
html,body,[class*="css"]{font-family:'Space Grotesk',sans-serif}
[data-testid="stAppViewContainer"]{background:#060a14}
[data-testid="stSidebar"]{background:#0d1526!important;border-right:1px solid #1e3058}
[data-testid="stSidebar"] *{color:#e2eaf8!important}
.stTabs [data-baseweb="tab-list"]{background:#0d1526;border-radius:10px;padding:4px;gap:4px}
.stTabs [data-baseweb="tab"]{background:transparent;color:#6b84a8!important;border-radius:8px;padding:8px 20px;font-weight:600}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#00d4ff22,#7b5ea722)!important;color:#00d4ff!important;border-bottom:2px solid #00d4ff}
.hero{font-family:'Syne',sans-serif;font-size:2.6rem;font-weight:800;
  background:linear-gradient(135deg,#00d4ff,#7b5ea7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;
  text-align:center;line-height:1.1;margin-bottom:.3rem}
.hero-sub{text-align:center;color:#6b84a8;font-size:.95rem;margin-bottom:1.5rem}
.kc{background:#0d1526;border:1px solid #1e3058;border-radius:12px;padding:1.1rem 1.3rem;border-top:3px solid}
.kl{font-size:.7rem;color:#6b84a8;text-transform:uppercase;letter-spacing:.07em;margin-bottom:.3rem}
.kv{font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:#e2eaf8}
.ks{font-size:.74rem;color:#6b84a8;margin-top:.15rem}
.stag{display:inline-block;background:rgba(0,212,255,.1);border:1px solid rgba(0,212,255,.3);
  color:#00d4ff;font-size:.68rem;padding:.15rem .5rem;border-radius:4px;font-family:monospace;margin-right:.5rem}
.stitle{font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;color:#e2eaf8;display:inline}
.ic{background:#111d35;border:1px solid #1e3058;border-radius:12px;padding:1rem;border-left:3px solid #00d4ff;margin-bottom:.75rem}
.ic.p{border-left-color:#7b5ea7}.ic.o{border-left-color:#ff6b35}.ic.g{border-left-color:#2dd4a0}
.it{font-family:'Syne',sans-serif;font-size:.8rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:#e2eaf8;margin-bottom:.3rem}
.ip{font-size:.8rem;color:#6b84a8;line-height:1.6}.ip strong{color:#e2eaf8}
.pill-row{display:flex;flex-wrap:wrap;gap:.6rem;justify-content:center;margin-bottom:1.5rem}
.pill{background:#0d1526;border:1px solid #1e3058;border-radius:40px;padding:.35rem .9rem;font-size:.8rem;color:#6b84a8;display:inline-block}
.pill b{color:#00d4ff}
.pred-box{background:#0d1526;border:1px solid #1e3058;border-radius:12px;padding:1.2rem;margin-top:.5rem}
.pred-val{font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:#00d4ff}
div[data-testid="stMetric"]{background:#0d1526;border-radius:10px;padding:.8rem;border:1px solid #1e3058}
div[data-testid="stMetric"] label{color:#6b84a8!important;font-size:.72rem!important}
div[data-testid="stMetric"] div{color:#e2eaf8!important}
.stButton>button{background:linear-gradient(135deg,#00d4ff,#0099cc)!important;color:#000!important;
  font-family:'Syne',sans-serif!important;font-weight:700!important;border:none!important;
  border-radius:8px!important;width:100%!important}
.stDataFrame{background:#0d1526!important}
/* 🔥 Fix white dropdown boxes ONLY */
div[data-baseweb="select"] > div {
    background-color: #0d1526 !important;
    color: #e2eaf8 !important;
    border: 1px solid #1e3058 !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] span {
    color: #e2eaf8 !important;
}

div[data-baseweb="select"] svg {
    fill: #6b84a8 !important;
}
</style>
""", unsafe_allow_html=True)

# ── HELPERS ────────────────────────────────────────────────────────────────────
LAYOUT = dict(paper_bgcolor='#0d1526', plot_bgcolor='#0d1526',
    font_color='#6b84a8', font_family='Space Grotesk',
    margin=dict(l=20,r=20,t=40,b=20),
    legend=dict(bgcolor='rgba(0,0,0,0)', font_color='#e2eaf8'))
AX = dict(gridcolor='#1e3058', zerolinecolor='#1e3058', color='#6b84a8')
COLORS = ['#00d4ff','#7b5ea7','#ff6b35','#2dd4a0','#fbbf24','#f472b6','#818cf8','#34d399','#fb923c','#60a5fa','#a78bfa','#6ee7b7','#fcd34d','#f9a8d4','#93c5fd']

def sf(fig):
    fig.update_layout(**LAYOUT)
    fig.update_xaxes(**AX)
    fig.update_yaxes(**AX)
    return fig

def qdf(sql, p=()):
    conn = get_connection()
    df = pd.read_sql_query(sql, conn, params=list(p))
    conn.close()
    return df

# ── LOAD SELECTORS ─────────────────────────────────────────────────────────────
@st.cache_data
def load_selectors():
    countries = qdf("SELECT code, name FROM countries ORDER BY name")
    roles     = qdf("SELECT id, title, category FROM job_roles ORDER BY title")
    return countries, roles

countries_df, roles_df = load_selectors()
cmap = {"All Countries": ""} | dict(zip(countries_df['name'], countries_df['code']))
rmap = {"All Roles": ""}     | dict(zip(roles_df['title'], roles_df['id'].astype(str)))

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌍 Filters")
    st.markdown("---")
    sel_country = st.selectbox("🏳️ Country",  list(cmap.keys()))
    sel_role    = st.selectbox("💼 Job Role",  list(rmap.keys()))
    sel_mode    = st.selectbox("🏢 Work Mode", ["Hybrid","Onsite","Remote"])
    st.markdown("---")
    
    st.markdown("---")
    st.markdown("**🗄️ Database Stats**")
    stats = summary_stats()
    st.markdown(f"""
    <div style='font-size:.78rem;color:#6b84a8;line-height:2'>
    📋 Job Postings: <b style='color:#00d4ff'>{stats['total_postings']:,}</b><br>
    🌐 Countries: <b style='color:#00d4ff'>{stats['total_countries']}</b><br>
    💼 Roles: <b style='color:#00d4ff'>{stats['total_roles']}</b><br>
    💰 Global Avg: <b style='color:#00d4ff'>${stats['global_avg_salary']:,}</b><br>
    🏆 Top Role: <b style='color:#2dd4a0'>{stats['highest_paying_role'].get('title','—')}</b>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""**📊 Data Sources**
<div style='font-size:.73rem;color:#6b84a8;line-height:1.9'>
• World Bank Labor Statistics<br>
• OECD Employment Outlook<br>
• LinkedIn Economic Graph<br>
• Glassdoor Salary Reports<br>
• National Labor Statistics<br>
• 8 CSV Datasets · SQLite DB
</div>""", unsafe_allow_html=True)

cid  = cmap[sel_country]
rid  = rmap[sel_role]
mode = sel_mode

# ── HERO ───────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero">🌍 Global Job Market Analysis System</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Enterprise Edition · Python Analytics · SQLite · 8 Datasets · 2015–2025</div>', unsafe_allow_html=True)
st.markdown("""<div class="pill-row">
<span class="pill"><b>10</b> Countries</span>
<span class="pill"><b>15</b> Job Roles</span>
<span class="pill"><b>3</b> Work Modes</span>
<span class="pill"><b>11yr</b> Trends</span>
<span class="pill"><b>500+</b> Job Postings</span>
<span class="pill"><b>8</b> CSV Datasets</span>
<span class="pill"><b>ML</b> Predictions</span>
<span class="pill"><b>SQLite</b> DB</span>
</div>""", unsafe_allow_html=True)

# ── KPI ROW ────────────────────────────────────────────────────────────────────
sal_sql = "SELECT AVG(avg_salary_usd) as v FROM salary_data WHERE work_mode=?"
sal_p   = [mode]
if cid: sal_sql += " AND country_code=?"; sal_p.append(cid)
if rid: sal_sql += " AND role_id=?";      sal_p.append(rid)
cur_sal = qdf(sal_sql, sal_p)['v'].iloc[0] or 0

trend_sql = "SELECT year, AVG(avg_salary_usd) as avg FROM salary_trends WHERE 1=1"
trend_p = []
if cid: trend_sql += " AND country_code=?"; trend_p.append(cid)
if rid: trend_sql += " AND role_id=?";      trend_p.append(rid)
trend_sql += " GROUP BY year ORDER BY year"
trend_df = qdf(trend_sql, trend_p)
sal_growth = 0
if len(trend_df) >= 2:
    sal_growth = round((trend_df['avg'].iloc[-1]-trend_df['avg'].iloc[0])/trend_df['avg'].iloc[0]*100,1)

wm_sql = "SELECT work_mode, AVG(avg_salary_usd) as avg FROM salary_data WHERE 1=1"
wm_p   = []
if cid: wm_sql += " AND country_code=?"; wm_p.append(cid)
if rid: wm_sql += " AND role_id=?";      wm_p.append(rid)
wm_sql += " GROUP BY work_mode"
wm_df  = qdf(wm_sql, wm_p)
wm_map = dict(zip(wm_df['work_mode'], wm_df['avg']))
rem_premium = round((wm_map.get('Remote',0)-wm_map.get('Onsite',1))/max(wm_map.get('Onsite',1),1)*100,1)

dem_sql = "SELECT year, AVG(demand_index) as idx FROM demand_trends WHERE 1=1"
dem_p   = []
if cid: dem_sql += " AND country_code=?"; dem_p.append(cid)
if rid: dem_sql += " AND role_id=?";      dem_p.append(rid)
dem_sql += " GROUP BY year ORDER BY year"
dem_df  = qdf(dem_sql, dem_p)
demand_status = "Stable"
if len(dem_df) >= 2:
    yg = (dem_df['idx'].iloc[-1]-dem_df['idx'].iloc[-2])/dem_df['idx'].iloc[-2]*100
    demand_status = "Growing" if yg>5 else "Declining" if yg<-3 else "Stable"

k1,k2,k3,k4 = st.columns(4)
dc = {'Growing':'#2dd4a0','Stable':'#fbbf24','Declining':'#f87171'}[demand_status]
for col, label, val, sub, color in [
    (k1,'Avg Annual Salary',f"${round(cur_sal):,}",f"{mode} · {sel_role[:16]}…" if len(sel_role)>16 else f"{mode} · {sel_role}",'#00d4ff'),
    (k2,'11-Year Growth',f"+{sal_growth}%","2015 → 2025",'#7b5ea7'),
    (k3,'Remote Premium',f"{'+' if rem_premium>=0 else ''}{rem_premium}%","vs Onsite",'#ff6b35'),
    (k4,'Market Demand',demand_status,"Current status",dc),
]:
    col.markdown(f'<div class="kc" style="border-top-color:{color}"><div class="kl">{label}</div><div class="kv" style="color:{color}">{val}</div><div class="ks">{sub}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tabs = st.tabs(["📊 Salary","📈 Trends","📉 Demand","🏢 Work Mode","🧠 Skills","🔮 ML Predictions","💼 Job Market","🌐 Global Overview"])

# ── TAB 1: SALARY ──────────────────────────────────────────────────────────────
with tabs[0]:
    st.markdown('<span class="stag">01</span><span class="stitle">Average Annual Salary Analysis</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    c_sql = f"SELECT cn.name as Country, AVG(s.avg_salary_usd) as Avg, AVG(s.min_salary_usd) as Min, AVG(s.max_salary_usd) as Max FROM salary_data s JOIN countries cn ON s.country_code=cn.code WHERE s.work_mode=?{' AND s.role_id=?' if rid else ''} GROUP BY cn.code ORDER BY Avg DESC"
    c_df = qdf(c_sql, [mode]+([rid] if rid else []))

    r_sql = f"SELECT r.title as Role, r.category, AVG(s.avg_salary_usd) as Avg FROM salary_data s JOIN job_roles r ON s.role_id=r.id WHERE s.work_mode=?{' AND s.country_code=?' if cid else ''} GROUP BY r.id ORDER BY Avg DESC"
    r_df = qdf(r_sql, [mode]+([cid] if cid else []))

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(c_df, x='Country', y='Avg', title=f'Country-wise Salary ({mode})',
                     color='Country', color_discrete_sequence=COLORS,
                     labels={'Avg':'Avg Salary (USD)'})
        fig.update_traces(texttemplate='$%{y:,.0f}', textposition='outside')
        sf(fig); fig.update_yaxes(tickprefix='$',tickformat=',.0f',**AX); fig.update_xaxes(tickangle=-35,**AX)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(r_df, x='Avg', y='Role', title='Role-wise Salary Distribution',
                      orientation='h', color='category', color_discrete_sequence=COLORS,
                      labels={'Avg':'Avg Salary (USD)','Role':'Job Role'})
        fig2.update_traces(texttemplate='$%{x:,.0f}', textposition='outside')
        sf(fig2); fig2.update_xaxes(tickprefix='$',tickformat=',.0f',**AX)
        fig2.update_yaxes(autorange='reversed',**AX)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Min / Avg / Max Range Chart**")
    fig3 = go.Figure()
    for i, row in c_df.iterrows():
        fig3.add_trace(go.Bar(name=row['Country'], x=[row['Country']],
            y=[row['Max']-row['Min']], base=[row['Min']],
            marker_color=COLORS[i % len(COLORS)],
            hovertemplate=f"<b>{row['Country']}</b><br>Min: $"+"%{base:,.0f}<br>Max: $%{y:,.0f}<extra></extra>"))
    sf(fig3); fig3.update_layout(showlegend=True, barmode='group', title='Salary Range by Country (Min–Max Band)')
    fig3.update_yaxes(tickprefix='$',tickformat=',.0f',**AX); fig3.update_xaxes(**AX)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("**📋 Summary Table**")
    disp = c_df.copy()
    disp['Avg'] = disp['Avg'].apply(lambda x: f"${round(x):,}")
    disp['Min'] = disp['Min'].apply(lambda x: f"${round(x):,}")
    disp['Max'] = disp['Max'].apply(lambda x: f"${round(x):,}")
    disp.index = range(1, len(disp)+1)
    disp.columns = ['Country','Avg Salary','Min Salary','Max Salary']
    st.dataframe(disp, use_container_width=True)

# ── TAB 2: SALARY TRENDS ───────────────────────────────────────────────────────
with tabs[1]:
    st.markdown('<span class="stag">02</span><span class="stitle">Salary Trend Analysis (2015–2025)</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=trend_df['year'], y=trend_df['avg'].round(0),
        mode='lines+markers', name='Avg Salary',
        line=dict(color='#00d4ff',width=2.5), fill='tozeroy', fillcolor='rgba(0,212,255,.07)',
        marker=dict(size=7,color='#00d4ff'),
        hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>'))
    for yr,lbl,clr in [(2020,'📉 COVID Dip','#f87171'),(2023,'🤖 AI Surge','#2dd4a0'),(2025,'📈 2025','#fbbf24')]:
        row = trend_df[trend_df['year']==yr]
        if not row.empty:
            fig.add_annotation(x=yr,y=row['avg'].iloc[0],text=lbl,showarrow=True,
                arrowhead=2,arrowcolor=clr,font=dict(color=clr,size=11),
                bgcolor='#0d1526',bordercolor=clr,borderwidth=1,ay=-45)
    sf(fig); fig.update_layout(title='11-Year Salary Growth (2015–2025)',xaxis_title='Year',yaxis_title='Avg Salary (USD)')
    fig.update_yaxes(tickprefix='$',tickformat=',.0f',**AX); fig.update_xaxes(**AX)
    st.plotly_chart(fig, use_container_width=True)

    # Multi-country trend comparison
    st.markdown("**Multi-Country Salary Trend Comparison**")
    mc_df = qdf("""SELECT t.year, AVG(t.avg_salary_usd) as avg, c.name as country
        FROM salary_trends t JOIN countries c ON t.country_code=c.code
        WHERE t.work_mode IS NULL GROUP BY t.year, t.country_code ORDER BY t.year""") if False else \
        qdf("""SELECT t.year, AVG(t.avg_salary_usd) as avg, c.name as country
        FROM salary_trends t JOIN countries c ON t.country_code=c.code
        """ + (f" WHERE t.role_id={rid}" if rid else "") + " GROUP BY t.year, t.country_code ORDER BY t.year")
    fig2 = px.line(mc_df, x='year', y='avg', color='country',
                   title='Salary Trend by Country (All Roles Average)',
                   color_discrete_sequence=COLORS,
                   labels={'avg':'Avg Salary (USD)','year':'Year','country':'Country'})
    sf(fig2); fig2.update_yaxes(tickprefix='$',tickformat=',.0f',**AX); fig2.update_xaxes(**AX)
    st.plotly_chart(fig2, use_container_width=True)

# ── TAB 3: DEMAND ──────────────────────────────────────────────────────────────
with tabs[2]:
    st.markdown('<span class="stag">03</span><span class="stitle">Job Demand Trend Analysis</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    post_df = qdf("""SELECT year, AVG(job_postings_thousands) as posts, AVG(remote_postings_thousands) as remote_posts
        FROM demand_trends WHERE 1=1""" +
        (f" AND country_code='{cid}'" if cid else "") +
        (f" AND role_id={rid}" if rid else "") +
        " GROUP BY year ORDER BY year")

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dem_df['year'], y=dem_df['idx'],
            mode='lines+markers', name='Demand Index',
            line=dict(color='#7b5ea7',width=2.5), fill='tozeroy', fillcolor='rgba(123,94,167,.09)',
            marker=dict(size=6,color='#7b5ea7')))
        sf(fig); fig.update_layout(title='Demand Index (Base 2015=100)',xaxis_title='Year',yaxis_title='Demand Index')
        fig.update_xaxes(**AX); fig.update_yaxes(**AX)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=post_df['year'], y=post_df['posts'],
            mode='lines+markers', name='Total Postings',
            line=dict(color='#2dd4a0',width=2.5), fill='tozeroy', fillcolor='rgba(45,212,160,.1)',
            marker=dict(size=6,color='#2dd4a0')))
        fig2.add_trace(go.Scatter(x=post_df['year'], y=post_df['remote_posts'],
            mode='lines+markers', name='Remote Postings',
            line=dict(color='#fbbf24',width=2,dash='dash'), marker=dict(size=5,color='#fbbf24')))
        sf(fig2); fig2.update_layout(title='Job Postings Volume (Thousands)',xaxis_title='Year',yaxis_title='Postings (K)')
        fig2.update_xaxes(**AX); fig2.update_yaxes(**AX)
        st.plotly_chart(fig2, use_container_width=True)

    # Role-wise demand heatmap
    st.markdown("**Role-wise Demand Index (Latest Year)**")
    heat_df = qdf("""SELECT r.title as role, AVG(d.demand_index) as idx
        FROM demand_trends d JOIN job_roles r ON d.role_id=r.id
        WHERE d.year=2025 GROUP BY d.role_id ORDER BY idx DESC""")
    fig3 = px.bar(heat_df, x='idx', y='role', orientation='h',
                  color='idx', color_continuous_scale=['#1e3058','#00d4ff'],
                  title='Demand Index by Role (2025)',
                  labels={'idx':'Demand Index','role':'Job Role'})
    sf(fig3); fig3.update_yaxes(autorange='reversed',**AX); fig3.update_xaxes(**AX)
    fig3.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)

# ── TAB 4: WORK MODE ───────────────────────────────────────────────────────────
with tabs[3]:
    st.markdown('<span class="stag">04</span><span class="stitle">Salary Comparison Across Work Modes</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    wm_full = qdf("""SELECT work_mode, AVG(avg_salary_usd) as Avg, AVG(min_salary_usd) as Min, AVG(max_salary_usd) as Max
        FROM salary_data WHERE 1=1""" +
        (f" AND country_code='{cid}'" if cid else "") +
        (f" AND role_id={rid}" if rid else "") +
        " GROUP BY work_mode ORDER BY Avg DESC")

    mc = {'Onsite':'#ff6b35','Hybrid':'#00d4ff','Remote':'#2dd4a0'}

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        for col_name, opacity in [('Min',0.35),('Avg',0.72),('Max',1.0)]:
            fig.add_trace(go.Bar(name=col_name,x=wm_full['work_mode'],y=wm_full[col_name].round(0),
                marker_color=[f"rgba({','.join(str(int(c.lstrip('#')[i:i+2],16)) for i in (0,2,4))},{opacity})"
                    for c in [mc.get(m,'#888') for m in wm_full['work_mode']]],
                hovertemplate='<b>%{x}</b><br>'+col_name+': $%{y:,.0f}<extra></extra>'))
        sf(fig); fig.update_layout(barmode='group',title='Grouped Compensation by Work Mode')
        fig.update_yaxes(tickprefix='$',tickformat=',.0f',**AX); fig.update_xaxes(**AX)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.pie(wm_full, values='Avg', names='work_mode',
                      title='Work Mode Share of Avg Compensation',
                      color='work_mode', color_discrete_map=mc, hole=0.55)
        sf(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Work Mode Breakdown**")
    for _, row in wm_full.iterrows():
        m   = row['work_mode']
        clr = mc.get(m,'#888')
        st.markdown(f"""<div style='background:#111d35;border-left:3px solid {clr};border-radius:8px;
            padding:1rem;margin-bottom:.7rem;display:flex;justify-content:space-between;align-items:center'>
            <div><span style='font-weight:700;color:#e2eaf8;font-size:1rem'>{m}</span>
            <div style='font-size:.76rem;color:#6b84a8;margin-top:.2rem'>Range: ${round(row["Min"]):,} – ${round(row["Max"]):,}</div></div>
            <span style='font-family:monospace;color:{clr};font-size:1.4rem;font-weight:700'>${round(row["Avg"]):,}</span>
            </div>""", unsafe_allow_html=True)

# ── TAB 5: SKILLS ──────────────────────────────────────────────────────────────
with tabs[4]:
    st.markdown('<span class="stag">05</span><span class="stitle">Skill Requirement Analysis</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not rid:
        st.info("💡 Select a specific Job Role from the sidebar to view skill requirements.")
    else:
        sk_df = qdf("SELECT skill_name, skill_type, percentage FROM skills WHERE role_id=? ORDER BY percentage DESC", [rid])
        col1, col2 = st.columns(2)
        with col1:
            tech = sk_df[sk_df['skill_type']=='Technical']['percentage'].sum()
            soft = sk_df[sk_df['skill_type']=='Soft']['percentage'].sum()
            st.markdown(f"<span style='color:#00d4ff;font-size:.82rem'>● Technical ({tech:.0f}%)</span>&nbsp;&nbsp;<span style='color:#7b5ea7;font-size:.82rem'>● Soft ({soft:.0f}%)</span>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            for _, row in sk_df.iterrows():
                clr = 'linear-gradient(90deg,#00d4ff,#0099cc)' if row['skill_type']=='Technical' else 'linear-gradient(90deg,#7b5ea7,#9b6dd4)'
                w = min(row['percentage']*3, 100)
                st.markdown(f"""<div style='margin-bottom:.7rem'>
                    <div style='display:flex;justify-content:space-between;font-size:.83rem;color:#e2eaf8;margin-bottom:.25rem'>
                        <span>{row['skill_name']}</span><span style='color:#6b84a8;font-family:monospace'>{row['percentage']}%</span>
                    </div>
                    <div style='background:#0d1526;border-radius:4px;height:8px;overflow:hidden'>
                        <div style='width:{w}%;background:{clr};height:8px;border-radius:4px'></div>
                    </div></div>""", unsafe_allow_html=True)

        with col2:
            fig = px.pie(sk_df, values='percentage', names='skill_name',
                         title='Skill Distribution', hole=0.6, color_discrete_sequence=COLORS)
            sf(fig)
            st.plotly_chart(fig, use_container_width=True)

        # Skill Gap Checker
        st.markdown("---")
        st.markdown("**🔍 Skill Gap Analyser — Check Your Readiness**")
        user_input = st.text_input("Enter your skills (comma separated):", placeholder="e.g. Python, SQL, Communication, Cloud")
        if user_input:
            user_skills = [s.strip() for s in user_input.split(',') if s.strip()]
            result = skill_gap_score(int(rid), user_skills)
            if result:
                score = result['match_score']
                color = '#2dd4a0' if score>=70 else '#fbbf24' if score>=40 else '#f87171'
                s1,s2,s3 = st.columns(3)
                s1.metric("Match Score", f"{score}%")
                s2.metric("Readiness", result['readiness'])
                s3.metric("Skills Matched", f"{len(result['matched_skills'])}/{len(result['matched_skills'])+len(result['missing_skills'])}")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**✅ You Have:**")
                    for sk in result['matched_skills']:
                        st.markdown(f"<span style='color:#2dd4a0'>✓</span> {sk['skill']} ({sk['weight']}%)", unsafe_allow_html=True)
                with col2:
                    st.markdown("**❌ You Need:**")
                    for sk in result['missing_skills']:
                        st.markdown(f"<span style='color:#f87171'>✗</span> {sk['skill']} ({sk['weight']}%)", unsafe_allow_html=True)

# ── TAB 6: ML PREDICTIONS ──────────────────────────────────────────────────────
with tabs[5]:
    st.markdown('<span class="stag">06</span><span class="stitle">ML Predictions & Analytics</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🔮 Salary Predictor (Linear Regression)**")
        p_country = st.selectbox("Country", list(cmap.keys())[1:], key='p_c')
        p_role    = st.selectbox("Role",    list(rmap.keys())[1:],  key='p_r')
        p_mode    = st.selectbox("Mode",    ["Hybrid","Onsite","Remote"], key='p_m')
        p_year    = st.slider("Predict for Year", 2026, 2030, 2026)
        if st.button("Predict Salary", key='pred_btn'):
            pcid = cmap[p_country]; prid = rmap[p_role]
            result = predict_salary(pcid, int(prid), p_mode, p_year)
            if result:
                st.markdown(f"""<div class='pred-box'>
                    <div style='color:#6b84a8;font-size:.75rem;text-transform:uppercase;margin-bottom:.3rem'>Predicted Salary {p_year}</div>
                    <div class='pred-val'>${result['predicted_salary']:,}</div>
                    <div style='font-size:.78rem;color:#6b84a8;margin-top:.5rem'>
                    Growth/yr: <b style='color:#2dd4a0'>+${result['slope_per_year']:,.0f}</b>&nbsp;·&nbsp;
                    R²: <b style='color:#00d4ff'>{result['r_squared']}</b>&nbsp;·&nbsp;
                    Rate: <b style='color:#fbbf24'>{result['growth_rate_pct']}%/yr</b>
                    </div></div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("**📈 Demand Forecasting (Moving Average)**")
        f_country = st.selectbox("Country", list(cmap.keys())[1:], key='f_c')
        f_role    = st.selectbox("Role",    list(rmap.keys())[1:],  key='f_r')
        f_years   = st.slider("Forecast Horizon (years)", 1, 5, 3)
        if st.button("Forecast Demand", key='fore_btn'):
            fcid = cmap[f_country]; frid = rmap[f_role]
            result = forecast_demand(fcid, int(frid), f_years)
            if result:
                fc = result['forecasts']
                st.markdown(f"""<div class='pred-box'>
                    <div style='display:flex;gap:1rem;margin-bottom:.7rem'>
                        <div><div style='color:#6b84a8;font-size:.72rem'>Status</div><div style='color:{"#2dd4a0" if result["status"]=="Growing" else "#f87171" if result["status"]=="Declining" else "#fbbf24"};font-weight:700'>{result['status']}</div></div>
                        <div><div style='color:#6b84a8;font-size:.72rem'>Growth Rate</div><div style='color:#00d4ff;font-weight:700'>{result["growth_rate_pct"]}%/yr</div></div>
                        <div><div style='color:#6b84a8;font-size:.72rem'>Confidence</div><div style='color:#7b5ea7;font-weight:700'>{result["confidence"]}</div></div>
                    </div>""", unsafe_allow_html=True)
                for f in fc:
                    st.markdown(f"<div style='padding:.5rem;background:#0d1526;border-radius:6px;margin-bottom:.4rem;font-size:.83rem'>"
                                f"<b style='color:#e2eaf8'>{f['year']}</b> — Index: <b style='color:#7b5ea7'>{f['demand_index']}</b> · Postings: <b style='color:#2dd4a0'>{f['postings_k']}K</b></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # PPP / Cost-adjusted salary
    st.markdown("**💰 Cost-of-Living Adjusted Salary (PPP)**")
    col3, col4 = st.columns(2)
    with col3:
        ppp_country = st.selectbox("Country", list(cmap.keys())[1:], key='ppp_c')
        ppp_role    = st.selectbox("Role",    list(rmap.keys())[1:],  key='ppp_r')
        ppp_mode    = st.selectbox("Mode", ["Hybrid","Onsite","Remote"], key='ppp_m')
        if st.button("Calculate Adjusted Salary", key='ppp_btn'):
            result = cost_adjusted_salary(cmap[ppp_country], int(rmap[ppp_role]), ppp_mode)
            if result:
                with col4:
                    m1,m2 = st.columns(2)
                    m1.metric("Raw Salary",        f"${result['raw_salary']:,}")
                    m2.metric("After Tax",          f"${result['after_tax']:,}")
                    m1.metric("PPP Adjusted",       f"${result['ppp_adjusted_salary']:,}")
                    m2.metric("Disposable Income",  f"${result['disposable_income']:,}")
                    st.metric("Annual Housing Cost",f"${result['annual_housing_cost']:,}")
                    st.markdown(f"<div style='font-size:.78rem;color:#6b84a8;margin-top:.5rem'>CoL Index: <b>{result['col_index']}</b> · Tax Rate: <b>{result['income_tax_rate']*100:.0f}%</b></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**🏆 Global Salary Benchmark**")
    if rid:
        bench = salary_benchmark(int(rid), mode)
        if bench:
            b1,b2,b3,b4 = st.columns(4)
            b1.metric("Global Average",  f"${bench['global_avg']:,}")
            b2.metric("Global Median",   f"${bench['global_median']:,}")
            b3.metric("Highest",         f"${bench['global_max']:,}")
            b4.metric("Lowest",          f"${bench['global_min']:,}")
            rank_df = pd.DataFrame(bench['rankings'])
            rank_df.index = range(1,len(rank_df)+1)
            rank_df['salary'] = rank_df['salary'].apply(lambda x: f"${x:,}")
            rank_df.columns = ['Country','Region','Salary (USD)']
            st.dataframe(rank_df, use_container_width=True)
    else:
        st.info("Select a Job Role to see global salary benchmark.")

# ── TAB 7: JOB MARKET ─────────────────────────────────────────────────────────
with tabs[6]:
    st.markdown('<span class="stag">07</span><span class="stitle">Live Job Market Insights</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🏢 Top Companies by Avg Salary**")
        comp_df = pd.DataFrame(company_insights(15))
        fig = px.bar(comp_df, x='avg_salary', y='company', orientation='h',
                     color='avg_salary', color_continuous_scale=['#1e3058','#00d4ff'],
                     title='Top Paying Companies',
                     labels={'avg_salary':'Avg Salary (USD)','company':'Company'})
        sf(fig); fig.update_yaxes(autorange='reversed',**AX)
        fig.update_xaxes(tickprefix='$',tickformat=',.0f',**AX)
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**📊 Postings by Experience Level**")
        exp_df = qdf("SELECT experience_level, COUNT(*) as cnt, AVG(salary_usd) as avg_sal FROM job_postings GROUP BY experience_level ORDER BY avg_sal DESC")
        fig2 = px.bar(exp_df, x='experience_level', y='avg_sal',
                      color='experience_level', color_discrete_sequence=COLORS,
                      title='Avg Salary by Experience Level',
                      labels={'experience_level':'Level','avg_sal':'Avg Salary (USD)'})
        sf(fig2); fig2.update_yaxes(tickprefix='$',tickformat=',.0f',**AX); fig2.update_xaxes(**AX)
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Postings over time
    st.markdown("**📅 Job Postings Over Time**")
    time_df = qdf("""SELECT substr(posted_date,1,7) as month, COUNT(*) as cnt, AVG(salary_usd) as avg_sal
        FROM job_postings GROUP BY month ORDER BY month""")
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=time_df['month'], y=time_df['cnt'], name='Postings',
        marker_color='#00d4ff', hovertemplate='<b>%{x}</b><br>Postings: %{y}<extra></extra>'))
    fig3.add_trace(go.Scatter(x=time_df['month'], y=time_df['avg_sal'], name='Avg Salary',
        yaxis='y2', line=dict(color='#fbbf24',width=2), mode='lines+markers', marker=dict(size=5)))
    sf(fig3); fig3.update_layout(
        title='Monthly Job Postings + Avg Salary',
        yaxis=dict(title='# Postings', **AX),
        yaxis2=dict(title='Avg Salary (USD)', overlaying='y', side='right', tickprefix='$', tickformat=',.0f', **AX),
        xaxis=dict(title='Month', **AX))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("**📋 Recent Job Postings**")
    postings_raw = qdf("""SELECT jp.company, cn.name as country, r.title as role, jp.work_mode,
        jp.salary_usd, jp.experience_level, jp.posted_date, jp.applicants
        FROM job_postings jp JOIN countries cn ON jp.country_code=cn.code
        JOIN job_roles r ON jp.role_id=r.id ORDER BY jp.posted_date DESC LIMIT 50""")
    postings_raw['salary_usd'] = postings_raw['salary_usd'].apply(lambda x: f"${round(x):,}")
    st.dataframe(postings_raw, use_container_width=True)

# ── TAB 8: GLOBAL OVERVIEW ─────────────────────────────────────────────────────
with tabs[7]:
    st.markdown('<span class="stag">08</span><span class="stitle">Global Overview & Academic Insights</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Scatter: GDP vs Salary
    gdp_sal = qdf("""SELECT c.name as country, c.gdp_per_capita, c.region,
        AVG(s.avg_salary_usd) as avg_sal
        FROM salary_data s JOIN countries c ON s.country_code=c.code
        WHERE s.work_mode='Hybrid' GROUP BY s.country_code""")
    fig = px.scatter(gdp_sal, x='gdp_per_capita', y='avg_sal', color='region',
                     size='avg_sal', hover_name='country', text='country',
                     title='GDP per Capita vs Avg Tech Salary (Hybrid)',
                     color_discrete_sequence=COLORS,
                     labels={'gdp_per_capita':'GDP per Capita (USD)','avg_sal':'Avg Salary (USD)'})
    sf(fig); fig.update_xaxes(tickprefix='$',tickformat=',.0f',**AX)
    fig.update_yaxes(tickprefix='$',tickformat=',.0f',**AX)
    fig.update_traces(textposition='top center')
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        top_roles = pd.DataFrame(top_paying_roles(cid if cid else None, mode))
        fig2 = px.funnel(top_roles, x='avg_salary', y='role',
                         title=f'Top Paying Roles ({mode})',
                         color_discrete_sequence=['#00d4ff'],
                         labels={'avg_salary':'Avg Salary (USD)','role':'Role'})
        sf(fig2); fig2.update_xaxes(tickprefix='$',**AX); fig2.update_yaxes(**AX)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        region_df = qdf("""SELECT c.region, AVG(s.avg_salary_usd) as avg_sal
            FROM salary_data s JOIN countries c ON s.country_code=c.code
            WHERE s.work_mode='Hybrid' GROUP BY c.region ORDER BY avg_sal DESC""")
        fig3 = px.pie(region_df, values='avg_sal', names='region',
                      title='Avg Salary Share by Region',
                      color_discrete_sequence=COLORS, hole=0.5)
        sf(fig3)
        st.plotly_chart(fig3, use_container_width=True)

    # Academic Insights
    st.markdown("---")
    st.markdown("**📚 Academic Insight Summary**")
    is_ai = sel_role in ['AI Engineer','Machine Learning Engineer','Data Scientist']
    rem_txt = f"Remote roles command a premium of <strong>+{rem_premium}%</strong> over onsite positions." if rem_premium >= 0 else f"Onsite positions offer <strong>{abs(rem_premium)}%</strong> premium in this market."
    ai_txt  = "This role is experiencing <strong>accelerated growth post-2022</strong> due to generative AI adoption. Organisations are competing aggressively for AI talent." if is_ai else "Adjacent AI tools are increasing productivity expectations and gradually lifting compensation benchmarks."

    col1, col2 = st.columns(2)
    with col1:
        for cls,icon,title,text in [
            ('','📊','Demand Status', f"The job market for <strong>{sel_role}</strong> in <strong>{sel_country}</strong> is currently <strong>{demand_status}</strong>. 11-year demand growth stands at significant levels, driven by continued digital transformation investment globally."),
            ('p','💰','Salary Growth', f"Over 2015–2025, compensation has grown by <strong>{sal_growth}%</strong>. A COVID dip occurred in 2020, followed by sharp recovery. 2023 onward shows AI-driven acceleration with <strong>2025 recording the highest salaries</strong> in the dataset."),
            ('o','🌍','Country Advantage', "The <strong>United States</strong> leads in absolute compensation, followed by <strong>Canada</strong>, <strong>Australia</strong>, and <strong>Singapore</strong>. <strong>India</strong> offers competitive cost-adjusted salaries especially for remote roles targeting global clients."),
        ]:
            st.markdown(f'<div class="ic {cls}"><div class="it">{icon} {title}</div><div class="ip">{text}</div></div>', unsafe_allow_html=True)

    with col2:
        for cls,icon,title,text in [
            ('g','🏠','Remote Work Impact', rem_txt + " Hybrid arrangements are 2–5% above onsite, representing the compensation equilibrium in 2025."),
            ('p','🤖','AI Acceleration', ai_txt),
            ('o','🧠','Skill Shift', "Critical skill shifts 2022–2025: <strong>Python (ML/LLMs)</strong>, <strong>Cloud Platforms</strong>, and <strong>MLOps</strong> dominate. Soft skills — <strong>Communication</strong>, <strong>Critical Thinking</strong>, <strong>Adaptability</strong> — now carry 20–35% weight in hiring decisions."),
        ]:
            st.markdown(f'<div class="ic {cls}"><div class="it">{icon} {title}</div><div class="ip">{text}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**📋 Final Summary Metrics**")
    m1,m2,m3,m4,m5,m6 = st.columns(6)
    m1.metric("Current Avg",   f"${round(cur_sal):,}")
    m2.metric("Onsite",        f"${round(wm_map.get('Onsite',0)):,}")
    m3.metric("Hybrid",        f"${round(wm_map.get('Hybrid',0)):,}")
    m4.metric("Remote",        f"${round(wm_map.get('Remote',0)):,}")
    m5.metric("Growth 10yr",   f"+{sal_growth}%")
    m6.metric("Demand",        demand_status)

st.markdown("---")
st.markdown("""
<h2 style='color:#e2eaf8; font-family:Syne; font-weight:700'>
📊 High-Level Academic Insight Summary
</h2>
""", unsafe_allow_html=True)

role_txt = sel_role
country_txt = sel_country
mode_txt = mode

# Demand %
demand_growth = 0
if len(dem_df) >= 2:
    demand_growth = round((dem_df['idx'].iloc[-1] - dem_df['idx'].iloc[0]) / dem_df['idx'].iloc[0] * 100, 1)

# AI role check
is_ai = role_txt in ['AI Engineer','Machine Learning Engineer','Data Scientist']

summary = f"""
📊 **Demand Status**  
The current job market for **{role_txt}** in **{country_txt}** is classified as **{demand_status}**. 
Since 2015, demand has changed by **{demand_growth}%**, indicating market momentum.

💰 **Salary Growth**  
Between 2015–2025, average compensation has grown by **{sal_growth}%**. 
A dip occurred in 2020 followed by strong recovery and acceleration post-2022.

🌍 **Country Salary Advantage**  
The **United States** leads in absolute compensation globally, followed by **Canada**, **Australia**, and **Singapore**.  
**India** remains strong in cost-adjusted salary value for global roles.

🏠 **Remote Work Impact**  
Remote roles show a **{('+' if rem_premium>=0 else '')}{rem_premium}%** difference vs onsite.  
Hybrid roles typically balance flexibility and compensation.

🤖 **AI Role Acceleration**  
{"This role is experiencing strong AI-driven demand growth." if is_ai else "AI tools are indirectly increasing productivity expectations and salary benchmarks."}

🧠 **Skill Demand Shift**  
Top demand skills include **Python, Cloud, and Data tools**, while soft skills like **Communication and Adaptability** contribute 20–35%.

---

"""

st.markdown(f"""
<div style='background:#0d1526;
            padding:1.2rem;
            border-radius:12px;
            border:1px solid #1e3058;
            color:#e2eaf8;
            line-height:1.7;
            font-size:0.9rem'>

{summary}

</div>
""", unsafe_allow_html=True)

st.markdown("""<br><div style='text-align:center;color:#6b84a8;font-size:.73rem;border-top:1px solid #1e3058;padding-top:1rem'>
Global Job Market Analysis System · Enterprise Edition ·
Data: World Bank, OECD, LinkedIn Economic Graph, Glassdoor ·
Built with Python · SQLite · Streamlit · Plotly · ML Analytics
</div>""", unsafe_allow_html=True)
