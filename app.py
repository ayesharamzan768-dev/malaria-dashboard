import streamlit as st
import pandas as pd
from filters import load_data, apply_filters, kpis, DATA_PATH, ATHENA_URL
from charts import *

st.set_page_config(page_title='WHO Malaria Analytics Dashboard', page_icon='🦟', layout='wide')

st.markdown('''
<style>
[data-testid="stAppViewContainer"]{background: radial-gradient(circle at top left,#123456 0,#07111f 34%,#030712 100%);} 
.block-container{padding-top:1.4rem;}
.hero{border:1px solid rgba(56,189,248,.25);border-radius:28px;padding:32px;background:linear-gradient(135deg,rgba(14,165,233,.22),rgba(15,23,42,.88));box-shadow:0 24px 80px rgba(0,0,0,.35);}
.hero h1{font-size:48px;line-height:1.05;margin:0;font-weight:900;background:linear-gradient(90deg,#fff,#7dd3fc,#34d399);-webkit-background-clip:text;color:transparent;}
.hero p{font-size:17px;color:#cbd5e1;margin-top:14px;max-width:980px;}
.kpi{border:1px solid rgba(148,163,184,.22);border-radius:22px;padding:20px;background:rgba(15,23,42,.72);box-shadow:0 12px 36px rgba(2,6,23,.35);}
.kpi small{color:#94a3b8;font-size:13px}.kpi h2{font-size:28px;margin:4px 0;color:#f8fafc}.kpi span{color:#38bdf8;font-size:13px}
.section-title{font-size:24px;font-weight:800;margin:18px 0 6px;color:#f8fafc}.subtle{color:#94a3b8;font-size:14px}
.stPlotlyChart{border:1px solid rgba(148,163,184,.16);border-radius:22px;background:rgba(15,23,42,.45);padding:8px;}
</style>
''', unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def get_data(refresh=False):
    return load_data(refresh=refresh)

with st.sidebar:
    st.title('🦟 Filters')
    st.caption('All filters update every chart at the same time.')
    refresh = st.button('🔄 Try refresh from WHO source')
    df = get_data(refresh)
    min_year, max_year = int(df.YEAR.min()), int(df.YEAR.max())
    years = st.slider('Year range', min_year, max_year, (min_year, max_year))
    regions = st.multiselect('WHO Region', sorted(df.REGION.dropna().unique()), default=sorted(df.REGION.dropna().unique()))
    available_countries = sorted(df[df.REGION.isin(regions)].COUNTRY.dropna().unique()) if regions else sorted(df.COUNTRY.dropna().unique())
    countries = st.multiselect('Countries', available_countries, default=available_countries[:min(12,len(available_countries))])
    min_cases, max_cases = int(df.Numeric.min()), int(df.Numeric.max())
    case_range = st.slider('Case value range', min_cases, max_cases, (min_cases, max_cases))
    search = st.text_input('Search country / region')
    st.divider()
    st.caption(f'Dataset file: `{DATA_PATH.name}`')
    st.caption('WHO source attempted first; local CSV keeps the dashboard running offline.')

filtered = apply_filters(df, years, regions, countries, case_range[0], case_range[1], search)
metrics = kpis(filtered)

st.markdown(f'''
<div class="hero">
<h1>WHO Malaria Intelligence Dashboard</h1>
<p>Country-level malaria cases from 2000 onward using the WHO Global Health Observatory indicator <b>MALARIA002</b>. This dashboard is built in a modern executive style with linked filters, KPI cards, professional charts, and deployment-ready Streamlit structure.</p>
</div>
''', unsafe_allow_html=True)

st.write('')
c1,c2,c3,c4,c5 = st.columns(5)
vals = [
    ('Total Records', f"{metrics['records']:,}", 'filtered rows'),
    ('Latest Year', f"{metrics['latest_year']}", 'after filters'),
    ('Latest Total Cases', f"{metrics['total_cases']/1_000_000:,.2f}M", 'sum of latest year'),
    ('Average Cases', f"{metrics['avg_cases']/1_000_000:,.2f}M", 'latest year mean'),
    ('Highest Country', metrics['highest_country'], f"{metrics['highest_value']/1_000_000:,.2f}M cases"),
]
for col, (label, value, note) in zip([c1,c2,c3,c4,c5], vals):
    col.markdown(f'<div class="kpi"><small>{label}</small><h2>{value}</h2><span>{note}</span></div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Core Trends</div><div class="subtle">Line and area charts show movement across time and regions.</div>', unsafe_allow_html=True)
a,b = st.columns([1.2,1])
a.plotly_chart(line_trend(filtered), use_container_width=True)
b.plotly_chart(area_trend(filtered), use_container_width=True)

st.markdown('<div class="section-title">Country and Regional Burden</div>', unsafe_allow_html=True)
a,b = st.columns([1.15,.85])
a.plotly_chart(bar_top_countries(filtered), use_container_width=True)
b.plotly_chart(pie_region(filtered), use_container_width=True)

st.markdown('<div class="section-title">Distribution and Relationships</div>', unsafe_allow_html=True)
a,b = st.columns(2)
a.plotly_chart(histogram_cases(filtered), use_container_width=True)
b.plotly_chart(scatter_uncertainty(filtered), use_container_width=True)
a,b = st.columns(2)
a.plotly_chart(box_region(filtered), use_container_width=True)
b.plotly_chart(violin_region(filtered), use_container_width=True)

st.markdown('<div class="section-title">Feature Summary</div>', unsafe_allow_html=True)
a,b = st.columns(2)
a.plotly_chart(count_region(filtered), use_container_width=True)
b.plotly_chart(heatmap_corr(filtered), use_container_width=True)
st.plotly_chart(bubble_chart(filtered), use_container_width=True)

with st.expander('View filtered data table'):
    st.dataframe(filtered, use_container_width=True, hide_index=True)

st.info('Data note: The original WHO Athena link now redirects to the WHO legacy page. This app still keeps that URL in the source logic and also tries the current GHO OData endpoint before using the included MALARIA002.csv file.')
