import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render_roi_calculator(df_roi):
    st.header("💰 ROI Calculator - Diversity Programs")
    
    # Paramètres interactifs
    st.subheader("🎛️ Program Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        company_size = st.number_input("Company Size (employees)", 500, 5000, 1200)
        avg_salary = st.number_input("Average Salary (€)", 40000, 120000, 75000)
        current_turnover = st.slider("Current Turnover Rate (%)", 5, 30, 15)
    
    with col2:
        program_investment = st.number_input("Program Investment (€)", 10000, 500000, 150000)
        target_improvement = st.slider("Target Retention Improvement (%)", 5, 40, 25)
        implementation_months = st.slider("Implementation Timeline (months)", 3, 24, 12)
    
    # Calculs ROI
    annual_turnover_cost = company_size * (current_turnover / 100) * (avg_salary * 1.5)  # Coût remplacement = 1.5x salaire
    retention_improvement = target_improvement / 100
    annual_savings = annual_turnover_cost * retention_improvement
    
    net_roi = annual_savings - program_investment
    roi_percentage = (net_roi / program_investment) * 100 if program_investment > 0 else 0
    
    # Résultats ROI
    st.subheader("📊 ROI Analysis Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Annual Savings",
            f"€{annual_savings:,.0f}",
            f"From {target_improvement}% retention boost"
        )
    
    with col2:
        st.metric(
            "Net ROI (Year 1)",
            f"€{net_roi:,.0f}",
            f"{roi_percentage:.0f}% return"
        )
    
    with col3:
        payback_months = (program_investment / (annual_savings / 12)) if annual_savings > 0 else float('inf')
        st.metric(
            "Payback Period",
            f"{payback_months:.1f} months" if payback_months != float('inf') else "N/A",
            "Break-even timeline"
        )
    
    with col4:
        three_year_roi = (annual_savings * 3) - program_investment
        st.metric(
            "3-Year Total ROI",
            f"€{three_year_roi:,.0f}",
            f"{(three_year_roi / program_investment) * 100:.0f}% return"
        )
    
    # Graphique ROI dans le temps
    months = list(range(1, 37))  # 3 ans
    cumulative_savings = []
    cumulative_investment = []
    
    for month in months:
        monthly_savings = annual_savings / 12
        cum_savings = monthly_savings * month
        cum_investment = program_investment + (program_investment * 0.1 * (month / 12))  # 10% maintenance annuel
        
        cumulative_savings.append(cum_savings)
        cumulative_investment.append(cum_investment)
    
    roi_df = pd.DataFrame({
        'Month': months,
        'Cumulative_Savings': cumulative_savings,
        'Cumulative_Investment': cumulative_investment,
        'Net_ROI': [s - i for s, i in zip(cumulative_savings, cumulative_investment)]
    })
    
    fig_roi = go.Figure()
    
    fig_roi.add_trace(go.Scatter(
        x=roi_df['Month'],
        y=roi_df['Cumulative_Savings'],
        mode='lines',
        name='Cumulative Savings',
        line=dict(color='green', width=3)
    ))
    
    fig_roi.add_trace(go.Scatter(
        x=roi_df['Month'],
        y=roi_df['Cumulative_Investment'],
        mode='lines',
        name='Cumulative Investment',
        line=dict(color='red', width=3)
    ))
    
    fig_roi.add_trace(go.Scatter(
        x=roi_df['Month'],
        y=roi_df['Net_ROI'],
        mode='lines',
        name='Net ROI',
        line=dict(color='blue', width=3),
        fill='tonexty'
    ))
    
    fig_roi.update_layout(
        title="📈 ROI Projection Over Time",
        xaxis_title="Months",
        yaxis_title="Value (€)",
        height=500
    )
    
    st.plotly_chart(fig_roi, use_container_width=True)
    
    # Comparaison programmes
    st.subheader("🔍 Program Comparison")
    
    fig_programs = px.bar(
        df_roi,
        x='Program',
        y='Retention_Improvement_Percent',
        color='Implementation_Cost',
        title="Program Effectiveness vs Investment",
        labels={'Retention_Improvement_Percent': 'Retention Improvement %'}
    )
    fig_programs.update_layout(height=400, xaxis_tickangle=45)
    st.plotly_chart(fig_programs, use_container_width=True)
    
    # Recommandations
    st.subheader("🎯 Strategic Recommendations")
    
    if roi_percentage > 200:
        st.success("🚀 **Excellent ROI** - This program will generate significant value for Ubisoft!")
    elif roi_percentage > 100:
        st.info("💡 **Good ROI** - Solid investment with measurable returns")
    elif roi_percentage > 0:
        st.warning("⚠️ **Moderate ROI** - Consider optimizing program parameters")
    else:
        st.error("❌ **Negative ROI** - Recommend adjusting investment or targets")
    
    recommendations = [
        f"💰 **Budget Optimization**: Focus on neurodiversity programs (highest ROI: {df_roi['Retention_Improvement_Percent'].max():.0f}%)",
        f"⏱️ **Timeline**: Implement in {implementation_months} months for optimal impact",
        f"📊 **Monitoring**: Track retention monthly to validate {target_improvement}% improvement target",
        f"🎯 **Scaling**: Success here enables expansion to other Ubisoft studios globally"
    ]
    
    for rec in recommendations:
        st.info(rec)
s