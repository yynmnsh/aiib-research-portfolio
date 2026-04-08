"""
Country Net-Zero Infrastructure Analysis: Indonesia
AIIB ECON — Research & Analytics Intern Portfolio
Yayan Puji Riyanto
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(page_title="Net-Zero Analysis: Indonesia", page_icon="\U0001f30f", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,500;9..40,700&family=JetBrains+Mono:wght@400;600&display=swap');
html,body,[class*="stApp"] { font-family:'DM Sans',sans-serif; }
p,span,h1,h2,h3,h4,h5,h6,label,div,button,input,textarea,select { font-family:'DM Sans',sans-serif; }
.stIconMaterial,.material-icons,.material-symbols-rounded { font-family:'Material Symbols Rounded' !important; }
code,pre { font-family:'JetBrains Mono',monospace !important; }

:root { --accent:#059669; --border:#e2e8f0; --radius:14px; }
.block-container { padding-top:2rem; max-width:1250px; }
[data-testid="stSidebar"] { background:linear-gradient(170deg,#021a0e,#0a2e1a,#041f10); }
[data-testid="stSidebar"] * { color:#cbd5e1 !important; }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,[data-testid="stSidebar"] strong { color:#f1f5f9 !important; }

@keyframes fadeUp { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
.mc { background:white; border:1px solid var(--border); border-radius:var(--radius); padding:18px; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,.04); animation:fadeUp .5s ease-out both; transition:transform .2s; }
.mc:hover { transform:translateY(-2px); box-shadow:0 4px 12px rgba(0,0,0,.08); }
.mc h3 { font-size:10px; color:#94a3b8; margin:0 0 4px; text-transform:uppercase; letter-spacing:.8px; }
.mc .v { font-size:24px; font-weight:700; color:#0f172a; margin:0; }
.mc .s { font-size:11px; color:#94a3b8; margin-top:3px; }
.sh { background:linear-gradient(135deg,#052e16,#065f46,#059669); color:white; padding:13px 22px; border-radius:10px; font-size:17px; font-weight:600; margin:24px 0 14px; }
.ib { background:#f0fdf4; border-left:4px solid #059669; padding:14px 18px; border-radius:0 var(--radius) var(--radius) 0; margin:10px 0; font-size:14px; color:#334155; line-height:1.7; }
.aiib-card { background:linear-gradient(135deg,#ecfdf5,#d1fae5); border:1px solid #a7f3d0; border-radius:var(--radius); padding:20px; margin:8px 0; }
.warn-card { background:linear-gradient(135deg,#fffbeb,#fef3c7); border:1px solid #fde68a; border-radius:var(--radius); padding:16px; margin:8px 0; font-size:13px; color:#92400e; }
#MainMenu{visibility:hidden;} footer{visibility:hidden;} .stDeployButton{display:none;}
</style>
""", unsafe_allow_html=True)

def mc(l,v,s=""):
    st.markdown(f'<div class="mc"><h3>{l}</h3><p class="v">{v}</p><p class="s">{s}</p></div>',unsafe_allow_html=True)

# ═══ INDONESIA NET-ZERO DATA ═══
@st.cache_data
def build_data():
    np.random.seed(2024)
    YEARS = list(range(2010, 2051))

    # Historical emissions by sector (MtCO2e) — calibrated to Indonesia NDC data
    SECTORS = {
        'Energy':        {'base':615,'growth':.032,'peak_yr':2030,'decay':-.035,'color':'#f59e0b','share':.38},
        'LULUCF':        {'base':460,'growth':-.01,'peak_yr':2025,'decay':-.045,'color':'#22c55e','share':.28},
        'Agriculture':   {'base':195,'growth':.015,'peak_yr':2035,'decay':-.015,'color':'#06b6d4','share':.12},
        'Industry':      {'base':180,'growth':.04,'peak_yr':2032,'decay':-.030,'color':'#8b5cf6','share':.11},
        'Waste':         {'base':105,'growth':.025,'peak_yr':2028,'decay':-.025,'color':'#ec4899','share':.06},
        'Transport':     {'base':85, 'growth':.05,'peak_yr':2033,'decay':-.028,'color':'#3b82f6','share':.05},
    }

    rows = []
    for sector, m in SECTORS.items():
        for yr in YEARS:
            t = yr - 2010
            if yr <= m['peak_yr']:
                val = m['base'] * (1 + m['growth'])**t + np.random.normal(0, m['base']*.015)
            else:
                t_post = yr - m['peak_yr']
                peak_val = m['base'] * (1 + m['growth'])**(m['peak_yr']-2010)
                val = peak_val * (1 + m['decay'])**t_post + np.random.normal(0, m['base']*.01)
            rows.append({'year':yr,'sector':sector,'emissions':max(val,0),'color':m['color']})

    em_df = pd.DataFrame(rows)

    # NDC scenarios
    scenarios = {}
    total_by_yr = em_df.groupby('year').emissions.sum()
    for scen, reduction in [('BAU',0),('NDC Unconditional',-.32),('NDC Enhanced',-.43),('Net-Zero 2060',-.85)]:
        sc = []
        for yr in YEARS:
            base = total_by_yr.get(yr, 1640)
            if yr <= 2024:
                sc.append({'year':yr,'scenario':scen,'emissions':base})
            else:
                t = yr - 2024
                if scen == 'BAU':
                    sc.append({'year':yr,'scenario':scen,'emissions':base*(1+.025)**t})
                elif scen == 'Net-Zero 2060':
                    target = base * max(0.05, 1 - (t/(2060-2024))**1.3)
                    sc.append({'year':yr,'scenario':scen,'emissions':target})
                else:
                    factor = 1 + reduction * min(1, t/6)
                    sc.append({'year':yr,'scenario':scen,'emissions':base*max(0.3, factor)})
        scenarios[scen] = pd.DataFrame(sc)
    scen_df = pd.concat(scenarios.values())

    # Infrastructure carbon intensity by province
    PROVINCES = ['DKI Jakarta','West Java','East Java','Central Java','Banten',
                 'North Sumatra','South Sulawesi','East Kalimantan','Bali',
                 'West Kalimantan','Riau','South Sumatra','Lampung','Papua',
                 'NTB','NTT','Aceh','DIY Yogyakarta','Maluku','West Papua']
    prov_data = []
    for prov in PROVINCES:
        is_java = 'Java' in prov or prov in ['DKI Jakarta','Banten','DIY Yogyakarta']
        gdp_pc = np.random.uniform(40000, 250000) if is_java else np.random.uniform(15000, 80000)
        pop = np.random.uniform(5, 50) if is_java else np.random.uniform(1, 15)
        carbon_int = np.random.uniform(0.3, 0.6) if is_java else np.random.uniform(0.5, 1.8)
        re_share = np.random.uniform(0.05, 0.25)
        infra_gap = np.random.uniform(0.3, 0.8) if not is_java else np.random.uniform(0.1, 0.4)

        lat = np.random.uniform(-8, 5) if 'Kalimantan' in prov or 'Sumatra' in prov or 'Sulawesi' in prov else (
              np.random.uniform(-9, -6) if is_java else np.random.uniform(-10, 2))
        lon = np.random.uniform(95, 141)

        prov_data.append({
            'province':prov,'is_java':is_java,'lat':lat,'lon':lon,
            'gdp_pc_idr':round(gdp_pc),'population_m':round(pop,1),
            'carbon_intensity':round(carbon_int,3), 're_share':round(re_share,3),
            'infra_gap_index':round(infra_gap,3),
            'priority_score':round(carbon_int*.30 + infra_gap*.30 + (1-re_share)*.20 + (1-gdp_pc/250000)*.20, 3),
        })
    prov_df = pd.DataFrame(prov_data).sort_values('priority_score', ascending=False)

    # Renewable energy trajectory
    re_data = []
    for yr in YEARS:
        if yr <= 2024:
            solar = 0.05 * max(0, yr-2015)**1.8
            wind = 0.02 * max(0, yr-2018)**1.5
            geo = 2.1 + 0.05*(yr-2010)
            hydro = 6.0 + 0.15*(yr-2010)
            bio = 1.8 + 0.1*(yr-2010)
        else:
            t = yr - 2024
            solar = 2.5 * (1 + .25)**t
            wind = 0.8 * (1 + .20)**t
            geo = 2.8 + 0.15*t
            hydro = 8.5 + 0.3*t
            bio = 3.2 + 0.2*t
        total_re = solar+wind+geo+hydro+bio
        total_fossil = max(40, 55 - 0.3*(yr-2024)) if yr>2024 else 55 + 0.5*(yr-2010)
        re_data.append({'year':yr,'Solar':round(solar,2),'Wind':round(wind,2),'Geothermal':round(geo,2),
                        'Hydro':round(hydro,2),'Biomass':round(bio,2),'total_re':round(total_re,2),
                        're_pct':round(total_re/(total_re+total_fossil)*100, 1)})
    re_df = pd.DataFrame(re_data)

    return em_df, scen_df, prov_df, re_df, SECTORS

em_df, scen_df, prov_df, re_df, SECTORS = build_data()

# ═══ SIDEBAR ═══
with st.sidebar:
    st.markdown("""<div style="text-align:center;padding:10px 0 16px;">
        <div style="font-size:36px;">\U0001f1ee\U0001f1e9</div>
        <div style="font-size:16px;font-weight:700;color:#f1f5f9!important;">Indonesia</div>
        <div style="font-size:12px;color:#94a3b8!important;">Net-Zero Infrastructure</div>
    </div>""",unsafe_allow_html=True)
    st.divider()
    yr_view = st.slider("Projection Horizon", 2025, 2050, 2050)
    scenario = st.selectbox("NDC Scenario", ['NDC Enhanced','NDC Unconditional','BAU','Net-Zero 2060'])
    st.divider()

    em_2024 = em_df[em_df.year==2024].emissions.sum()
    em_latest = scen_df[(scen_df.scenario==scenario)&(scen_df.year==yr_view)].emissions.values
    em_target = em_latest[0] if len(em_latest) else em_2024
    reduction = (em_2024 - em_target)/em_2024 * 100

    st.markdown(f"""<div style="font-size:12px;">
        <div style="color:#64748b;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Scenario: {scenario}</div>
        <div style="display:flex;justify-content:space-between;margin:4px 0;"><span>2024 Emissions</span><span style="font-weight:600;color:#f1f5f9!important;">{em_2024:,.0f} Mt</span></div>
        <div style="display:flex;justify-content:space-between;margin:4px 0;"><span>{yr_view} Target</span><span style="font-weight:600;color:#86efac!important;">{em_target:,.0f} Mt</span></div>
        <div style="display:flex;justify-content:space-between;margin:4px 0;"><span>Reduction</span><span style="font-weight:600;color:#22c55e!important;">{reduction:+.0f}%</span></div>
    </div>""",unsafe_allow_html=True)
    st.divider()
    st.markdown("""<div style="font-size:11px;color:#64748b;line-height:1.6;">
        <strong style="color:#94a3b8!important;">Data Sources</strong><br>
        Calibrated to Indonesia NDC (2022 Enhanced), ESDM statistics, BPS. Synthetic for research demonstration.<br><br>
        <strong style="color:#94a3b8!important;">By</strong> Yayan Puji Riyanto
    </div>""",unsafe_allow_html=True)

# ═══ TABS ═══
tab1,tab2,tab3,tab4,tab5 = st.tabs(["\U0001f4ca Emissions Profile","\U0001f3d7\ufe0f Infrastructure Gap","\u26a1 Energy Transition","\U0001f3af Investment Priority","\U0001f4d6 About"])

# ═══ TAB 1: EMISSIONS ═══
with tab1:
    st.markdown("""<h1 style="font-size:26px;font-weight:700;color:#0f172a;margin-bottom:4px;">Indonesia Emissions Profile & NDC Pathways</h1>
        <p style="font-size:14px;color:#64748b;">Sectoral decomposition and scenario analysis toward Net-Zero 2060</p>""",unsafe_allow_html=True)

    em_2024_total = em_df[em_df.year==2024].emissions.sum()
    em_2010_total = em_df[em_df.year==2010].emissions.sum()
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: mc("2024 Emissions",f"{em_2024_total:,.0f}","MtCO2e")
    with c2: mc("Growth (2010-24)",f"{(em_2024_total/em_2010_total-1)*100:+.0f}%","Total change")
    with c3: mc("Largest Sector","Energy",f"{em_df[(em_df.year==2024)&(em_df.sector=='Energy')].emissions.values[0]:,.0f} Mt")
    with c4: mc("NDC Target (2030)","-31.9%","vs BAU (unconditional)")
    with c5: mc("Net-Zero Target","2060","Long-term strategy")

    # Sectoral stacked area
    st.markdown('<div class="sh">\U0001f4c8 Historical & Projected Emissions by Sector</div>',unsafe_allow_html=True)
    em_pivot = em_df[em_df.year<=yr_view].pivot_table(values='emissions',index='year',columns='sector',aggfunc='sum')
    fig_area = go.Figure()
    for sec in ['LULUCF','Agriculture','Waste','Transport','Industry','Energy']:
        if sec in em_pivot.columns:
            fig_area.add_trace(go.Scatter(
                x=em_pivot.index, y=em_pivot[sec], name=sec, fill='tonexty',
                line=dict(width=0.5, color=SECTORS[sec]['color']),
                fillcolor=SECTORS[sec]['color'].replace(')', ',0.6)').replace('rgb','rgba') if 'rgb' in SECTORS[sec]['color'] else SECTORS[sec]['color'],
            ))
    fig_area.add_vline(x=2024, line_dash='dash', line_color='white', opacity=.4,
        annotation_text='Historical | Projected', annotation_position='top right') # Geser anotasi ke kanan
    fig_area.update_layout(height=400, plot_bgcolor='white', margin=dict(t=40,b=20), # Tambah margin atas (t=40)
        yaxis=dict(title='Emissions (MtCO2e)',gridcolor='#f1f5f9'),
        legend=dict(orientation='h',y=-0.15,x=.5,xanchor='center',font=dict(size=10))) # Pindah legenda ke bawah
    st.plotly_chart(fig_area, use_container_width=True)

    # NDC scenario pathways
    st.markdown('<div class="sh">\U0001f30d NDC Scenario Pathways</div>',unsafe_allow_html=True)
    scen_colors = {'BAU':'#ef4444','NDC Unconditional':'#f59e0b','NDC Enhanced':'#3b82f6','Net-Zero 2060':'#22c55e'}
    fig_scen = go.Figure()
    for scen_name, color in scen_colors.items():
        sc = scen_df[(scen_df.scenario==scen_name)&(scen_df.year<=yr_view)]
        lw = 3 if scen_name == scenario else 1.5
        dash = 'solid' if scen_name == scenario else 'dot'
        fig_scen.add_trace(go.Scatter(x=sc.year, y=sc.emissions, name=scen_name,
            line=dict(color=color,width=lw,dash=dash), mode='lines'))
    fig_scen.add_vline(x=2024, line_dash='dash', line_color='white', opacity=.3)
    fig_scen.update_layout(height=380, plot_bgcolor='white', margin=dict(t=20,b=20),
        yaxis=dict(title='Total Emissions (MtCO2e)',gridcolor='#f1f5f9'),
        legend=dict(orientation='h',y=1.08,x=.5,xanchor='center'))
    st.plotly_chart(fig_scen, use_container_width=True)

    # Sector breakdown 2024
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sh">\U0001f3af 2024 Sector Breakdown</div>',unsafe_allow_html=True)
        sec_24 = em_df[em_df.year==2024].sort_values('emissions',ascending=False)
        fig_pie = go.Figure(go.Pie(labels=sec_24.sector, values=sec_24.emissions, hole=.45,
            marker=dict(colors=[SECTORS[s]['color'] for s in sec_24.sector]),
            textinfo='label+percent', textposition='outside'))
        fig_pie.update_layout(height=350, margin=dict(t=10,b=10,l=10,r=10), showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown('<div class="sh">\U0001f4c9 Sector Trajectories (Indexed: 2010=100)</div>',unsafe_allow_html=True)
        fig_idx = go.Figure()
        for sec in SECTORS:
            s_data = em_df[em_df.sector==sec].sort_values('year')
            base = s_data.emissions.iloc[0]
            fig_idx.add_trace(go.Scatter(x=s_data.year, y=s_data.emissions/base*100,
                name=sec, line=dict(color=SECTORS[sec]['color'],width=2)))
        fig_idx.add_hline(y=100, line_dash='dot', line_color='white', opacity=.3)
        fig_idx.update_layout(height=350, plot_bgcolor='white', margin=dict(t=10,b=20),
            yaxis=dict(title='Index (2010=100)',gridcolor='#f1f5f9'),
            legend=dict(orientation='h',y=1.06,x=.5,xanchor='center',font=dict(size=9)))
        st.plotly_chart(fig_idx, use_container_width=True)

# ═══ TAB 2: INFRASTRUCTURE ═══
with tab2:
    st.markdown("""<h1 style="font-size:26px;font-weight:700;color:#0f172a;margin-bottom:4px;">Subnational Infrastructure Carbon Intensity</h1>
        <p style="font-size:14px;color:#64748b;">Provincial-level analysis of infrastructure gaps and decarbonisation needs</p>""",unsafe_allow_html=True)

    st.markdown("""<div class="ib">
        Indonesia's infrastructure carbon intensity varies significantly across provinces. Java's dense urban centres have
        lower per-unit carbon intensity but high absolute emissions, while outer islands have higher intensity due to
        reliance on diesel generators and limited grid connectivity.
    </div>""",unsafe_allow_html=True)

    # Province map
    st.markdown('<div class="sh">\U0001f5fa\ufe0f Provincial Carbon Intensity Map</div>',unsafe_allow_html=True)
    fig_prov = px.scatter_geo(
        prov_df, lat='lat', lon='lon', size='population_m',
        color='carbon_intensity', size_max=30,
        color_continuous_scale=[[0,'#22c55e'],[.4,'#fde68a'],[.7,'#f59e0b'],[1,'#ef4444']],
        hover_name='province',
        hover_data={'carbon_intensity':':.3f','gdp_pc_idr':':,.0f','population_m':':.1f',
                    'infra_gap_index':':.2f','re_share':':.1%','lat':False,'lon':False},
        projection='natural earth',
    )
    fig_prov.update_geos(bgcolor='#06080f',landcolor='#111827',oceancolor='#060a14',
        coastlinecolor='#1e293b',countrycolor='#1e293b',showframe=False,
        lataxis_range=[-12,8],lonaxis_range=[92,145],fitbounds='locations')
    fig_prov.update_layout(paper_bgcolor='#06080f',height=450,margin=dict(t=10,b=10,l=10,r=10),
        coloraxis_colorbar=dict(
            title=dict(text='Carbon Int.', font=dict(color='#e2e8f0')), 
            tickfont=dict(color='#94a3b8')
        ),
        font=dict(color='#e2e8f0'))
    st.plotly_chart(fig_prov, use_container_width=True)

    # Scatter: carbon intensity vs GDP
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sh">\U0001f4ca Carbon Intensity vs Development</div>',unsafe_allow_html=True)
        fig_ci = go.Figure()
        java = prov_df[prov_df.is_java]
        outer = prov_df[~prov_df.is_java]
        fig_ci.add_trace(go.Scatter(x=java.gdp_pc_idr/1000, y=java.carbon_intensity, mode='markers+text',
            marker=dict(size=java.population_m, color='#3b82f6', sizemode='area', sizeref=0.5),
            text=java.province, textposition='top center', textfont=dict(size=8), name='Java'))
        fig_ci.add_trace(go.Scatter(x=outer.gdp_pc_idr/1000, y=outer.carbon_intensity, mode='markers+text',
            marker=dict(size=outer.population_m, color='#f59e0b', sizemode='area', sizeref=0.5),
            text=outer.province, textposition='top center', textfont=dict(size=8), name='Outer Islands'))
        fig_ci.update_layout(height=380, plot_bgcolor='white', margin=dict(t=10,b=10),
            xaxis=dict(title='GDP per Capita (IDR 000)',gridcolor='#f1f5f9'),
            yaxis=dict(title='Carbon Intensity (tCO2e/unit)',gridcolor='#f1f5f9'),
            legend=dict(orientation='h',y=1.06))
        st.plotly_chart(fig_ci, use_container_width=True)

    with col2:
        st.markdown('<div class="sh">\u26a1 Renewable Energy Penetration</div>',unsafe_allow_html=True)
        prov_sorted = prov_df.sort_values('re_share')
        fig_re_prov = go.Figure(go.Bar(
            y=prov_sorted.province, x=prov_sorted.re_share*100, orientation='h',
            marker_color=['#22c55e' if r>.15 else '#f59e0b' if r>.08 else '#ef4444' for r in prov_sorted.re_share],
            text=[f'{r:.0%}' for r in prov_sorted.re_share], textposition='auto'))
        fig_re_prov.add_vline(x=23, line_dash='dash', line_color='#22c55e', opacity=.5,
            annotation_text='2025 Target: 23%', annotation_position='top')
        fig_re_prov.update_layout(height=500, plot_bgcolor='white', margin=dict(t=10,b=10),
            xaxis=dict(title='Renewable Energy Share (%)',gridcolor='#f1f5f9'))
        st.plotly_chart(fig_re_prov, use_container_width=True)

# ═══ TAB 3: ENERGY ═══
with tab3:
    st.markdown("""<h1 style="font-size:26px;font-weight:700;color:#0f172a;margin-bottom:4px;">Energy Transition Pathways</h1>
        <p style="font-size:14px;color:#64748b;">Renewable energy trajectory and power sector decarbonisation</p>""",unsafe_allow_html=True)

    re_latest = re_df[re_df.year==2024].iloc[0]
    re_target = re_df[re_df.year==yr_view].iloc[0]
    c1,c2,c3,c4 = st.columns(4)
    with c1: mc("RE Share (2024)",f"{re_latest.re_pct:.0f}%","Of total generation")
    with c2: mc(f"RE Share ({yr_view})",f"{re_target.re_pct:.0f}%","Projected")
    with c3: mc("Solar (2024)",f"{re_latest.Solar:.1f} GW","Installed capacity")
    with c4: mc("Geothermal",f"{re_latest.Geothermal:.1f} GW","World 2nd largest")

    # RE capacity stacked area
    st.markdown('<div class="sh">\u26a1 Renewable Energy Capacity Trajectory</div>',unsafe_allow_html=True)
    re_view = re_df[re_df.year<=yr_view]
    re_colors = {'Hydro':'#3b82f6','Geothermal':'#8b5cf6','Solar':'#f59e0b','Wind':'#06b6d4','Biomass':'#22c55e'}
    fig_re = go.Figure()
    for source in ['Biomass','Wind','Solar','Geothermal','Hydro']:
        fig_re.add_trace(go.Scatter(x=re_view.year, y=re_view[source], name=source, fill='tonexty',
            line=dict(width=0.5,color=re_colors[source])))
    fig_re.add_vline(x=2024, line_dash='dash', line_color='white', opacity=.3)
    fig_re.update_layout(height=380, plot_bgcolor='white', margin=dict(t=20,b=20),
        yaxis=dict(title='Installed Capacity (GW)',gridcolor='#f1f5f9'),
        legend=dict(orientation='h',y=1.08,x=.5,xanchor='center'))
    st.plotly_chart(fig_re, use_container_width=True)

    # RE share trajectory
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sh">\U0001f4c8 RE Share of Generation (%)</div>',unsafe_allow_html=True)
        fig_re_pct = go.Figure()
        fig_re_pct.add_trace(go.Scatter(x=re_view.year, y=re_view.re_pct, fill='tozeroy',
            line=dict(color='#22c55e',width=3), fillcolor='rgba(34,197,94,.1)'))
        fig_re_pct.add_hline(y=23, line_dash='dash', line_color='#f59e0b', opacity=.6,
            annotation_text='RUEN Target: 23%')
        fig_re_pct.add_hline(y=50, line_dash='dot', line_color='#22c55e', opacity=.4,
            annotation_text='Net-Zero pathway: 50%')
        fig_re_pct.update_layout(height=350, plot_bgcolor='white', margin=dict(t=10,b=20),
            yaxis=dict(title='RE Share (%)',gridcolor='#f1f5f9'))
        st.plotly_chart(fig_re_pct, use_container_width=True)

    with col2:
        st.markdown('<div class="sh">\U0001f3af 2024 RE Mix</div>',unsafe_allow_html=True)
        re_24 = re_df[re_df.year==2024][['Solar','Wind','Geothermal','Hydro','Biomass']].iloc[0]
        fig_re_mix = go.Figure(go.Pie(labels=re_24.index, values=re_24.values, hole=.45,
            marker=dict(colors=[re_colors[s] for s in re_24.index])))
        fig_re_mix.update_layout(height=350, margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig_re_mix, use_container_width=True)

# ═══ TAB 4: PRIORITY ═══
with tab4:
    st.markdown("""<h1 style="font-size:26px;font-weight:700;color:#0f172a;margin-bottom:4px;">Investment Priority Scoring</h1>
        <p style="font-size:14px;color:#64748b;">Identifying provinces where AIIB green infrastructure investment has highest impact</p>""",unsafe_allow_html=True)

    st.markdown("""<div class="ib">
        <strong>Composite Priority Score</strong> = Carbon Intensity (30%) + Infrastructure Gap (30%) +
        Renewable Deficit (20%) + Development Need (20%). Higher score = greater need for green infrastructure investment.
    </div>""",unsafe_allow_html=True)

    # Priority ranking
    st.markdown('<div class="sh">\U0001f3c6 Provincial Investment Priority Ranking</div>',unsafe_allow_html=True)
    prov_ranked = prov_df.copy()
    prov_ranked['rank'] = range(1, len(prov_ranked)+1)
    prov_ranked['tier'] = prov_ranked.priority_score.apply(
        lambda x: 'Tier 1 (Critical)' if x > prov_ranked.priority_score.quantile(.75) else
                  'Tier 2 (High)' if x > prov_ranked.priority_score.quantile(.50) else
                  'Tier 3 (Medium)' if x > prov_ranked.priority_score.quantile(.25) else 'Tier 4 (Lower)')
    tier_colors = {'Tier 1 (Critical)':'#ef4444','Tier 2 (High)':'#f59e0b','Tier 3 (Medium)':'#3b82f6','Tier 4 (Lower)':'#22c55e'}

    fig_pri = go.Figure(go.Bar(
        y=prov_ranked.province, x=prov_ranked.priority_score, orientation='h',
        marker_color=[tier_colors[t] for t in prov_ranked.tier],
        text=[f'{s:.3f} ({t.split("(")[1]}' for s,t in zip(prov_ranked.priority_score, prov_ranked.tier)],
        textposition='auto'))
    fig_pri.update_layout(height=550, plot_bgcolor='white', margin=dict(t=10,b=10,l=10,r=10),
        xaxis=dict(title='Composite Priority Score',gridcolor='#f1f5f9'))
    fig_pri.update_yaxes(autorange='reversed')
    st.plotly_chart(fig_pri, use_container_width=True)

    # Radar: top 5 provinces
    st.markdown('<div class="sh">\U0001f4ca Top 5 Priority Province Profiles</div>',unsafe_allow_html=True)
    top5 = prov_ranked.head(5)
    dims = ['carbon_intensity','infra_gap_index','re_share','priority_score']
    dim_labels = ['Carbon Intensity','Infra Gap','RE Deficit','Priority Score']

    fig_radar = go.Figure()
    for _, r in top5.iterrows():
        vals = [r.carbon_intensity/2, r.infra_gap_index, 1-r.re_share, r.priority_score]
        fig_radar.add_trace(go.Scatterpolar(r=vals+[vals[0]], theta=dim_labels+[dim_labels[0]],
            name=r.province, fill='toself', opacity=.3))
    fig_radar.update_layout(height=400, polar=dict(radialaxis=dict(visible=True,range=[0,1],gridcolor='#e2e8f0')),
        legend=dict(orientation='h',y=-0.08,x=.5,xanchor='center',font=dict(size=10)))
    st.plotly_chart(fig_radar, use_container_width=True)

    # Recommendations
    st.markdown('<div class="sh">\U0001f4dd Investment Recommendations for AIIB</div>',unsafe_allow_html=True)
    recommendations = [
        ("Grid Connectivity for Outer Islands","High carbon intensity in Eastern Indonesia driven by diesel dependency. AIIB can finance submarine cable connections and mini-grid solar+storage systems."),
        ("Geothermal Expansion (Sumatra, Sulawesi)","Indonesia has world-2nd largest geothermal potential (29 GW) but only ~2.4 GW installed. AIIB green loans can de-risk exploration and development."),
        ("Urban Transit (Java)","Java concentrates 56% of population. BRT, LRT, and electrification of commuter rail can reduce transport emissions in Greater Jakarta, Surabaya, and Bandung."),
        ("LULUCF: Peatland Restoration (Kalimantan, Sumatra)","Peatland fires contribute ~30% of Indonesia emissions. AIIB can co-finance rewetting and restoration through green bonds."),
        ("Industrial Efficiency (West Java, Banten)","Manufacturing clusters in West Java industrial corridor. AIIB can finance energy efficiency retrofits and fuel switching in cement, steel, and textiles."),
    ]
    for title, desc in recommendations:
        st.markdown(f"""<div style="background:white;border:1px solid #e2e8f0;border-radius:12px;padding:16px 20px;margin:8px 0;border-left:4px solid #059669;">
            <div style="font-size:15px;font-weight:600;color:#0f172a;">{title}</div>
            <div style="font-size:13px;color:#475569;margin-top:4px;line-height:1.6;">{desc}</div>
        </div>""",unsafe_allow_html=True)

# ═══ TAB 5: ABOUT ═══
with tab5:
    st.markdown("""<h1 style="font-size:26px;font-weight:700;color:#0f172a;margin-bottom:4px;">About This Analysis</h1>
        <p style="font-size:14px;color:#64748b;">Context, methodology, and AIIB ECON relevance</p>""",unsafe_allow_html=True)

    st.markdown("""<div class="ib">
        This analysis directly supports AIIB ECON's <strong>Country Net-Zero Reports</strong> workstream.
        The dashboard demonstrates the analytical framework for assessing a member country's climate transition
        pathway and identifying infrastructure investment opportunities aligned with Paris Agreement goals.
    </div>""",unsafe_allow_html=True)

    r1,r2,r3 = st.columns(3)
    with r1:
        st.markdown("""<div class="aiib-card"><div style="font-size:24px;margin-bottom:6px;">\U0001f4ca</div>
            <h4 style="color:#065f46;margin-top:0;">Emissions Analytics</h4>
            <p style="font-size:13px;color:#334155;">6-sector emissions decomposition, 4 NDC scenario pathways,
            indexed sector trajectories, and stacked area projections to 2050.</p></div>""",unsafe_allow_html=True)
    with r2:
        st.markdown("""<div class="aiib-card"><div style="font-size:24px;margin-bottom:6px;">\U0001f5fa\ufe0f</div>
            <h4 style="color:#065f46;margin-top:0;">Subnational Mapping</h4>
            <p style="font-size:13px;color:#334155;">20-province carbon intensity map, Java vs outer islands analysis,
            infrastructure gap assessment, and renewable energy penetration by province.</p></div>""",unsafe_allow_html=True)
    with r3:
        st.markdown("""<div class="aiib-card"><div style="font-size:24px;margin-bottom:6px;">\U0001f3af</div>
            <h4 style="color:#065f46;margin-top:0;">Investment Prioritisation</h4>
            <p style="font-size:13px;color:#334155;">Composite priority scoring, radar profiles for top provinces,
            and 5 specific infrastructure investment recommendations for AIIB.</p></div>""",unsafe_allow_html=True)

st.divider()
st.markdown("""<div style="text-align:center;color:#94a3b8;font-size:12px;padding:8px 0 16px;line-height:1.8;">
    Country Net-Zero Infrastructure Analysis: Indonesia<br>
    <strong>Yayan Puji Riyanto</strong> \u00b7 PhD Candidate, Monash University \u00b7 MS Business Analytics, CU Boulder<br>
    <em>Prepared for AIIB Research and Analytics (Corporate) Intern</em>
</div>""",unsafe_allow_html=True)
