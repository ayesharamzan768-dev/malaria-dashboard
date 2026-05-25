import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

TEMPLATE = 'plotly_dark'
COLORS = px.colors.sequential.Tealgrn

def empty_fig(title='No data available'):
    fig = go.Figure()
    fig.update_layout(template=TEMPLATE, title=title, height=420)
    return fig

def line_trend(df):
    if df.empty: return empty_fig()
    d = df.groupby('YEAR', as_index=False)['Numeric'].sum()
    return px.line(d, x='YEAR', y='Numeric', markers=True, template=TEMPLATE, title='Malaria Cases Trend Over Time')

def area_trend(df):
    if df.empty: return empty_fig()
    d = df.groupby(['YEAR','REGION'], as_index=False)['Numeric'].sum()
    return px.area(d, x='YEAR', y='Numeric', color='REGION', template=TEMPLATE, title='Regional Cumulative Area Trend')

def bar_top_countries(df, n=10):
    if df.empty: return empty_fig()
    latest = df[df['YEAR'] == df['YEAR'].max()].groupby('COUNTRY', as_index=False)['Numeric'].sum().nlargest(n,'Numeric')
    return px.bar(latest, x='Numeric', y='COUNTRY', orientation='h', template=TEMPLATE, color='Numeric', color_continuous_scale='Tealgrn', title='Top Countries by Latest Malaria Cases')

def pie_region(df):
    if df.empty: return empty_fig()
    d = df[df['YEAR'] == df['YEAR'].max()].groupby('REGION', as_index=False)['Numeric'].sum()
    return px.pie(d, names='REGION', values='Numeric', hole=.45, template=TEMPLATE, title='Latest Cases Share by Region')

def histogram_cases(df):
    if df.empty: return empty_fig()
    return px.histogram(df, x='Numeric', nbins=25, template=TEMPLATE, title='Histogram of Malaria Case Values')

def scatter_uncertainty(df):
    if df.empty: return empty_fig()
    return px.scatter(df, x='Low', y='High', size='Numeric', color='REGION', hover_name='COUNTRY', template=TEMPLATE, title='Scatter Plot: Low vs High Estimates')

def box_region(df):
    if df.empty: return empty_fig()
    return px.box(df, x='REGION', y='Numeric', color='REGION', template=TEMPLATE, title='Box Plot: Distribution by Region')

def violin_region(df):
    if df.empty: return empty_fig()
    return px.violin(df, x='REGION', y='Numeric', color='REGION', box=True, points='all', template=TEMPLATE, title='Violin Plot: Density by Region')

def count_region(df):
    if df.empty: return empty_fig()
    d = df.groupby('REGION', as_index=False).size().rename(columns={'size':'Records'})
    return px.bar(d, x='REGION', y='Records', color='REGION', template=TEMPLATE, title='Count Plot: Records by Region')

def heatmap_corr(df):
    nums = df[['YEAR','Numeric','Low','High','CASES_MILLIONS']].dropna()
    if nums.empty: return empty_fig()
    corr = nums.corr()
    return px.imshow(corr, text_auto=True, color_continuous_scale='Tealgrn', template=TEMPLATE, title='Correlation Heatmap')

def bubble_chart(df):
    if df.empty: return empty_fig()
    latest = df[df['YEAR'] == df['YEAR'].max()].copy()
    return px.scatter(latest, x='COUNTRY', y='Numeric', size='Numeric', color='REGION', template=TEMPLATE, title='Bonus Bubble Chart: Latest Cases by Country')
