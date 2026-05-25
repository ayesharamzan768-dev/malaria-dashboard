import pandas as pd
import numpy as np
from pathlib import Path
import requests, io

DATA_PATH = Path(__file__).parent / 'data' / 'MALARIA002.csv'
ATHENA_URL = 'https://apps.who.int/gho/athena/data/GHO/MALARIA002.csv'
ODATA_URL = 'https://ghoapi.azureedge.net/api/MALARIA002'

def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    mapping = {}
    for c in df.columns:
        lc = c.lower()
        if lc in ['spatialdim','countrycode','country_code','code']:
            mapping[c] = 'COUNTRY_CODE'
        elif lc in ['parentlocation','region','who_region']:
            mapping[c] = 'REGION'
        elif lc in ['location','country','countryname']:
            mapping[c] = 'COUNTRY'
        elif lc in ['period','year','time_dim']:
            mapping[c] = 'YEAR'
        elif lc in ['factvaluenumeric','numeric','value']:
            mapping[c] = 'Numeric'
        elif lc in ['factvaluenumericlow','low']:
            mapping[c] = 'Low'
        elif lc in ['factvaluenumerichigh','high']:
            mapping[c] = 'High'
        elif lc in ['factvalue','display value','displayvalue']:
            mapping[c] = 'Display Value'
        elif lc == 'dim1':
            mapping[c] = 'SEX'
    df = df.rename(columns=mapping)
    needed = ['COUNTRY','COUNTRY_CODE','REGION','YEAR','Numeric','Low','High','Display Value','SEX','AGEGROUP','GHO']
    for col in needed:
        if col not in df.columns:
            df[col] = 'Unknown' if col not in ['YEAR','Numeric','Low','High'] else np.nan
    df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce').astype('Int64')
    for col in ['Numeric','Low','High']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['COUNTRY'] = df['COUNTRY'].replace('', np.nan).fillna('Unknown')
    df['REGION'] = df['REGION'].replace('', np.nan).fillna('Unknown')
    df['CASES_MILLIONS'] = df['Numeric'] / 1_000_000
    df = df.dropna(subset=['YEAR','Numeric'])
    return df

def download_latest_data() -> pd.DataFrame | None:
    # The old Athena URL may redirect to WHO legacy page; OData is tried as fallback.
    try:
        r = requests.get(ATHENA_URL, timeout=20)
        if r.ok and 'COUNTRY' in r.text[:5000] and ',' in r.text[:5000]:
            return _standardize_columns(pd.read_csv(io.StringIO(r.text)))
    except Exception:
        pass
    try:
        r = requests.get(ODATA_URL, timeout=20)
        if r.ok:
            data = r.json().get('value', [])
            if data:
                return _standardize_columns(pd.DataFrame(data))
    except Exception:
        pass
    return None

def load_data(refresh: bool=False) -> pd.DataFrame:
    if refresh:
        latest = download_latest_data()
        if latest is not None and not latest.empty:
            latest.to_csv(DATA_PATH, index=False)
            return latest
    return _standardize_columns(pd.read_csv(DATA_PATH))

def apply_filters(df, years, regions, countries, min_cases, max_cases, search):
    out = df.copy()
    if years:
        out = out[(out['YEAR'] >= years[0]) & (out['YEAR'] <= years[1])]
    if regions:
        out = out[out['REGION'].isin(regions)]
    if countries:
        out = out[out['COUNTRY'].isin(countries)]
    out = out[(out['Numeric'] >= min_cases) & (out['Numeric'] <= max_cases)]
    if search:
        s = search.lower().strip()
        out = out[out['COUNTRY'].str.lower().str.contains(s, na=False) | out['REGION'].str.lower().str.contains(s, na=False)]
    return out

def kpis(df):
    latest_year = int(df['YEAR'].max()) if len(df) else 0
    latest = df[df['YEAR'] == latest_year]
    return {
        'records': len(df),
        'latest_year': latest_year,
        'total_cases': latest['Numeric'].sum(),
        'avg_cases': latest['Numeric'].mean() if len(latest) else 0,
        'highest_country': latest.sort_values('Numeric', ascending=False)['COUNTRY'].iloc[0] if len(latest) else 'N/A',
        'highest_value': latest['Numeric'].max() if len(latest) else 0,
    }
