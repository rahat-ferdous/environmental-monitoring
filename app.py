import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Economic Zone Environmental Monitoring",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(45deg, #00b894, #00cec9, #0984e3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 800;
    }
    .section-header {
        font-size: 2.2rem;
        color: #2d3436;
        border-left: 5px solid #00b894;
        padding-left: 1rem;
        margin: 2rem 0 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem;
        text-align: center;
    }
    .warning-card {
        background: linear-gradient(135deg, #ff7675, #d63031);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .safe-card {
        background: linear-gradient(135deg, #55efc4, #00b894);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Generate synthetic environmental data
@st.cache_data
def generate_environmental_data():
    np.random.seed(42)
    
    # Generate dates for the past year
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    
    # Air Quality Data
    air_data = []
    monitoring_stations = ['North Zone', 'South Zone', 'Industrial Area', 'Residential Area', 'Commercial District']
    
    for date in dates:
        for station in monitoring_stations:
            # Base levels with seasonal variation
            seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * date.dayofyear / 365)
            
            if station == 'Industrial Area':
                base_pm25 = 45
                base_so2 = 25
                base_no2 = 40
            elif station == 'Residential Area':
                base_pm25 = 25
                base_so2 = 12
                base_no2 = 18
            else:
                base_pm25 = 35
                base_so2 = 18
                base_no2 = 25
            
            air_data.append({
                'Date': date,
                'Station': station,
                'PM2.5': max(10, np.random.normal(base_pm25 * seasonal_factor, 8)),
                'PM10': max(20, np.random.normal(base_pm25 * 2 * seasonal_factor, 15)),
                'SO2': max(5, np.random.normal(base_so2 * seasonal_factor, 4)),
                'NO2': max(8, np.random.normal(base_no2 * seasonal_factor, 6)),
                'O3': max(20, np.random.normal(35 * seasonal_factor, 10)),
                'CO': max(0.5, np.random.normal(1.2 * seasonal_factor, 0.3))
            })
    
    air_df = pd.DataFrame(air_data)
    
    # Water Quality Data
    water_bodies = ['River North', 'Lake Central', 'Canal Industrial', 'Reservoir South']
    water_data = []
    
    for date in dates[::7]:  Weekly data
        for water_body in water_bodies:
            if 'Industrial' in water_body:
                base_ph = 6.2
                base_bod = 8
                base_cod = 15
            else:
                base_ph = 7.1
                base_bod = 3
                base_cod = 6
            
            water_data.append({
                'Date': date,
                'Water_Body': water_body,
                'pH': np.random.normal(base_ph, 0.3),
                'Dissolved_Oxygen': max(2, np.random.normal(6, 1.5)),
                'BOD': max(1, np.random.normal(base_bod, 2)),
                'COD': max(3, np.random.normal(base_cod, 3)),
                'Turbidity': np.random.normal(15, 8),
                'Heavy_Metals': np.random.normal(0.05, 0.02)
            })
    
    water_df = pd.DataFrame(water_data)
    
    # Biodiversity Data
    species_data = []
    species_list = ['Mangrove Trees', 'Fish Species', 'Bird Species', 'Mammal Species', 'Insect Species']
    
    for date in dates[::30]:  Monthly data
        for species in species_list:
            trend = 1 + 0.1 * (date.month - 6) / 6  # Seasonal trend
            if 'Industrial' in station:
                base_count = 50
            else:
                base_count = 120
            
            species_data.append({
                'Date': date,
                'Species': species,
                'Count': max(10, int(np.random.normal(base_count * trend, 20))),
                'Health_Index': np.random.normal(75, 15)
            })
    
    biodiversity_df = pd.DataFrame(species_data)
    
    return air_df, water_df, biodiversity_df

# Load data
air_df, water_df, biodiversity_df = generate_environmental_data()

# ===== DASHBOARD HEADER =====
st.markdown('<h1 class="main-header">🌍 Economic Zone Environmental Monitoring System</h1>', unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; font-size: 1.3rem; color: #555; margin-bottom: 2rem;'>
    Comprehensive EIA Compliance Monitoring • Real-time Environmental Analytics • Regulatory Reporting
</div>
""", unsafe_allow_html=True)

# ===== EXECUTIVE SUMMARY =====
st.markdown('<h2 class="section-header">📊 Executive Summary</h2>', unsafe_allow_html=True)

# Key Metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    latest_air = air_df[air_df['Date'] == air_df['Date'].max()]
    avg_pm25 = latest_air['PM2.5'].mean()
    status = "⚠️ Alert" if avg_pm25 > 35 else "✅ Normal"
    st.metric("Air Quality (PM2.5)", f"{avg_pm25:.1f} µg/m³", status)

with col2:
    latest_water = water_df[water_df['Date'] == water_df['Date'].max()]
    avg_ph = latest_water['pH'].mean()
    ph_status = "⚠️ Alert" if avg_ph < 6.5 or avg_ph > 8.5 else "✅ Normal"
    st.metric("Water pH", f"{avg_ph:.1f}", ph_status)

with col3:
    total_species = biodiversity_df[biodiversity_df['Date'] == biodiversity_df['Date'].max()]['Count'].sum()
    st.metric("Biodiversity Index", f"{total_species:,}")

with col4:
    compliance_rate = 87.5  # Simulated compliance rate
    st.metric("EIA Compliance", f"{compliance_rate}%")

with col5:
    alerts_count = len(air_df[air_df['PM2.5'] > 35]) + len(water_df[water_df['pH'] < 6.5])
    st.metric("Active Alerts", f"{alerts_count}")

# ===== AIR QUALITY MONITORING =====
st.markdown('<h2 class="section-header">🌬️ Air Quality Monitoring</h2>', unsafe_allow_html=True)

# Air Quality Trends
st.subheader("Pollutant Trends Over Time")

pollutant = st.selectbox("Select Pollutant", ['PM2.5', 'PM10', 'SO2', 'NO2', 'O3', 'CO'])

fig_air = px.line(air_df, x='Date', y=pollutant, color='Station',
                  title=f'{pollutant} Levels Across Monitoring Stations',
                  labels={pollutant: f'{pollutant} Concentration'})
st.plotly_chart(fig_air, use_container_width=True)

# Current Air Quality Status
st.subheader("Current Air Quality Status by Station")
latest_air_data = air_df[air_df['Date'] == air_df['Date'].max()]

cols = st.columns(len(latest_air_data['Station'].unique()))
for idx, (station, data) in enumerate(latest_air_data.groupby('Station')):
    with cols[idx]:
        pm25 = data['PM2.5'].iloc[0]
        if pm25 > 35:
            st.markdown(f'<div class="warning-card"><h4>{station}</h4>PM2.5: {pm25:.1f} µg/m³<br>⚠️ POOR</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="safe-card"><h4>{station}</h4>PM2.5: {pm25:.1f} µg/m³<br>✅ GOOD</div>', unsafe_allow_html=True)

# ===== WATER QUALITY MONITORING =====
st.markdown('<h2 class="section-header">💧 Water Quality Monitoring</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("pH Levels Across Water Bodies")
    fig_water_ph = px.box(water_df, x='Water_Body', y='pH', 
                         title='pH Distribution by Water Body')
    fig_water_ph.add_hline(y=6.5, line_dash="dash", line_color="red", annotation_text="Min Safe pH")
    fig_water_ph.add_hline(y=8.5, line_dash="dash", line_color="red", annotation_text="Max Safe pH")
    st.plotly_chart(fig_water_ph, use_container_width=True)

with col2:
    st.subheader("Pollution Indicators")
    fig_water_poll = px.scatter(water_df, x='BOD', y='COD', color='Water_Body',
                               title='BOD vs COD Correlation',
                               labels={'BOD': 'Biological Oxygen Demand', 'COD': 'Chemical Oxygen Demand'})
    st.plotly_chart(fig_water_poll, use_container_width=True)

# ===== BIODIVERSITY MONITORING =====
st.markdown('<h2 class="section-header">🦜 Biodiversity & Ecosystem Health</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Species Population Trends")
    fig_bio = px.line(biodiversity_df, x='Date', y='Count', color='Species',
                     title='Species Population Trends Over Time')
    st.plotly_chart(fig_bio, use_container_width=True)

with col2:
    st.subheader("Ecosystem Health Index")
    latest_bio = biodiversity_df[biodiversity_df['Date'] == biodiversity_df['Date'].max()]
    fig_health = px.bar(latest_bio, x='Species', y='Health_Index',
                       title='Current Ecosystem Health by Species',
                       color='Health_Index',
                       color_continuous_scale='RdYlGn')
    st.plotly_chart(fig_health, use_container_width=True)

# ===== EIA COMPLIANCE DASHBOARD =====
st.markdown('<h2 class="section-header">📋 EIA Compliance Monitoring</h2>', unsafe_allow_html=True)

# Compliance Metrics
compliance_data = {
    'Parameter': ['Air Quality Standards', 'Water Discharge Limits', 'Noise Pollution', 
                  'Waste Management', 'Biodiversity Protection', 'Community Health'],
    'Compliance Rate': [85, 90, 95, 80, 75, 88],
    'Status': ['Partially Compliant', 'Compliant', 'Compliant', 'Needs Improvement', 
               'Needs Improvement', 'Compliant']
}

compliance_df = pd.DataFrame(compliance_data)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Compliance Rates by Parameter")
    fig_compliance = px.bar(compliance_df, x='Compliance Rate', y='Parameter', 
                           orientation='h', color='Compliance Rate',
                           color_continuous_scale='RdYlGn',
                           title='EIA Parameter Compliance Rates')
    st.plotly_chart(fig_compliance, use_container_width=True)

with col2:
    st.subheader("Compliance Status")
    for _, row in compliance_df.iterrows():
        if row['Compliance Rate'] >= 90:
            st.markdown(f'<div class="safe-card">✅ {row["Parameter"]}: {row["Compliance Rate"]}%</div>', unsafe_allow_html=True)
        elif row['Compliance Rate'] >= 75:
            st.markdown(f'<div style="background: linear-gradient(135deg, #fdcb6e, #e17055); color: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">⚠️ {row["Parameter"]}: {row["Compliance Rate"]}%</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="warning-card">❌ {row["Parameter"]}: {row["Compliance Rate"]}%</div>', unsafe_allow_html=True)

# ===== ENVIRONMENTAL ALERTS =====
st.markdown('<h2 class="section-header">🚨 Environmental Alerts</h2>', unsafe_allow_html=True)

# Generate alerts
alerts = []
if len(air_df[air_df['PM2.5'] > 35]) > 0:
    alerts.append("🚨 HIGH PM2.5 levels detected in Industrial Area")
if len(water_df[water_df['pH'] < 6.5]) > 0:
    alerts.append("🚨 LOW pH levels detected in Canal Industrial")
if len(air_df[air_df['SO2'] > 20]) > 0:
    alerts.append("⚠️ Elevated SO2 levels in multiple stations")

if alerts:
    for alert in alerts:
        st.error(alert)
else:
    st.success("✅ No critical environmental alerts at this time")

# ===== REGULATORY REPORTING =====
st.markdown('<h2 class="section-header">📄 Regulatory Reporting</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Generate Monthly EIA Report"):
        st.success("Monthly EIA compliance report generated successfully!")
        st.download_button("📥 Download PDF Report", data="Simulated PDF content", 
                          file_name="eia_monthly_report.pdf")

with col2:
    if st.button("🌡️ Export Environmental Data"):
        st.success("Environmental data exported to CSV!")
        csv = air_df.to_csv().encode('utf-8')
        st.download_button("📥 Download Air Quality Data", data=csv, 
                          file_name="air_quality_data.csv")

with col3:
    if st.button("🔔 Generate Compliance Certificate"):
        st.success("Compliance certificate generated!")
        st.download_button("📥 Download Certificate", data="Simulated certificate", 
                          file_name="eia_compliance_certificate.pdf")

# ===== PREDICTIVE ANALYTICS =====
st.markdown('<h2 class="section-header">🔮 Predictive Analytics</h2>', unsafe_allow_html=True)

st.write("""
**Environmental Trend Forecast:**
- Air quality expected to improve by 15% in next quarter with current mitigation measures
- Water quality stability maintained in 80% of monitoring points
- Biodiversity index projected to increase by 8% with habitat restoration
""")

# ===== FOOTER =====
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <div style="font-size: 1.1rem; margin-bottom: 1rem;">
        <strong>Economic Zone Environmental Monitoring System • EIA Compliant</strong>
    </div>
    <div style="font-size: 0.9rem;">
        Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M")} • 
        Monitoring {len(air_df['Station'].unique())} stations • 
        <a href="#" style="color: #666;">Download Full Report</a>
    </div>
</div>
""", unsafe_allow_html=True)
